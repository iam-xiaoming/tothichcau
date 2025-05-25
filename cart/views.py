from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
import stripe
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order
from games.models import Game, DLC
from keys.models import Key
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from users.models import MyUser
from .models import Transaction
import logging
from django.db import transaction
from django.urls import reverse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
import numpy as np
from .utils import create_transaction, create_user_game, create_user_interaction
from .mailjet import send_mailjet_email_purchase_success

stripe.api_key = settings.STRIPE_SECRET_KEY


def reserve_key(item_model, item_id, order_id, out_of_stock):
    try:
        item = item_model.objects.get(pk=item_id)
        if not item.keys.filter(status='available').exists():
            out_of_stock.append({'orderId': order_id, 'name': item.name})
        else:
            with transaction.atomic():
                order = Order.objects.get(pk=order_id)
                key = item.keys.select_for_update().filter(status='available').first()
                if key:
                    order.key = key
                    key.status = 'reserved'
                    key.save()
                    order.save()
                else:
                    out_of_stock.append({'orderId': order_id, 'name': item.name})
    except item_model.DoesNotExist:
        pass


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_stock(request):
    try:
        items = request.data.get('items', [])
        out_of_stock = []
        
        if not isinstance(items, list):
            return Response({'error': 'Invalid format for items.'}, status=400)

        for item in items:
            item_id = item.get('item_id')
            order_id = item.get('orderId')
            data_type = item.get('dataType')

            if not (item_id and order_id and data_type):
                continue
            
            if data_type == 'base':
                reserve_key(Game, item_id, order_id, out_of_stock)
            else:
                reserve_key(DLC, item_id, order_id, out_of_stock)
            
        return Response({
            'out_of_stock': out_of_stock,
            'reserved': len(items) - len(out_of_stock)
        })
    except Exception as e:
        return Response({'error': f'An error occurred while checking stock - {e}.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_game_to_cart(request, pk, game_pk):
    try:
        user = MyUser.objects.get(pk=pk)
        game = Game.objects.get(id=game_pk)
    except MyUser.DoesNotExist:
        return Response({'error': 'User not found.'}, status=404)
    except Game.DoesNotExist:
        return Response({'error': 'Game not found.'}, status=404)
    
    try:
        Order.objects.create(user=user, game=game)
        
        # get total order count of specific user
        order_count = user.orders.count()
        
        # get number of available key remaining
        key_remain = Key.objects.filter(status='available').count()
        
    except Exception as e:
        print(e)
        return Response({'error': str(e)}, status=400)
    else:
        return Response({
            'success': True,
            'order_count': order_count,
            'key_remain': key_remain,
            'message':'Game added to cart!'})
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_dlc_to_cart(request, pk, game_pk):
    try:
        user = MyUser.objects.get(pk=pk)
        dlc = DLC.objects.get(id=game_pk)
    except MyUser.DoesNotExist:
        return Response({'error': 'User not found.'}, status=404)
    except DLC.DoesNotExist:
        return Response({'error': 'DLC not found.'}, status=404)
    
    try:
        Order.objects.create(user=user, dlc=dlc)
        
        # get total order count of specific user
        order_count = user.orders.count()
        
        # get number of available key remaining
        key_remain = Key.objects.filter(status='available').count()
        
    except Exception as e:
        print(e)
        return Response({'error': str(e)}, status=400)
    else:
        return Response({
            'success': True,
            'order_count': order_count,
            'key_remain': key_remain,
            'message':'Game added to cart!'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart_count(request, pk):
    try:
        order_count = Order.objects.filter(user__pk=pk).count()
    except MyUser.DoesNotExist:
        return Response({'error': 'User not found.'}, status=404)
    
    return Response({'message': 'success', 'order_count': order_count}, status=200)


class CartView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'cart/cart.html'
    login_url = '/login/'
    context_object_name = 'orders'

    def get_queryset(self):        
        # Return only the orders of the logged-in user
        return self.request.user.orders.all()
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = context['orders']
        
        games = [order.game for order in orders if order.game]
        dlcs = [order.dlc for order in orders if order.dlc]
                
        total_price = np.sum(game.price for game in games) + np.sum(dlc.price for dlc in dlcs)
        total_discounted_price = np.sum(game.discounted_price for game in games) + np.sum(dlc.discounted_price for dlc in dlcs)
        
        context['orders'] = Order.objects.select_related('game', 'dlc').filter(user=self.request.user)
        context['total_price'] = total_price
        context['total_discounted_price'] = total_discounted_price
        context['discount'] = total_price - total_discounted_price
        context['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLISHABLE_KEY
        return context
    

class CartDeleteView(LoginRequiredMixin, View):
    login_url = '/login/'
    
    def post(self, request, pk, *args, **kwargs):
        order = get_object_or_404(Order, pk=pk, user=request.user)
        with transaction.atomic():
            if order.key:
                key = order.key
                key.status = 'available'
                order.key = None
            order.delete()
        return redirect('cart')
    

class CreateCheckoutSessionView(LoginRequiredMixin, View):
    login_url = '/login/'  # Redirect here if user is not logged in
    
    def post(self, request, *args, **kwargs):
        user = self.request.user
        orders = user.orders.all()
        
        line_items = []
        
        for order in orders:
            line_items.append({
                'price': order.game.stripe_price_id if order.game else order.dlc.stripe_price_id,
                'quantity': 1
            })
            
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=line_items,
                metadata = {
                    "user_id": str(request.user.id),
                    "order_ids": ",".join(str(order.id) for order in orders)
                },
                mode="payment",
                success_url=request.build_absolute_uri(reverse("success")),
                cancel_url=request.build_absolute_uri(reverse("cancel")),
            )
            return JsonResponse({'id': checkout_session.id})
        except stripe.error.StripeError as e:
            return JsonResponse({'error': str(e)}, status=400)
    

@login_required
def success(request):
    return render(request, "cart/success.html")



@login_required
def cancel(request):
    orders = Order.objects.filter(user=request.user)
    with transaction.atomic():
        for order in orders:
            key = order.key
            if key:
                key.status = 'available'
                key.save()
            order.key = None
            order.save()
    return render(request, "cart/cancel.html")


def verify_stripe_event(payload, sig_header, webhook_secret, logger):
    try:
        return stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        logger.warning(f"[Webhook] Invalid signature or payload: {e}")
        return None
    

def get_payment_info(session):
    payment_intent_id = session.get('payment_intent')
    info = {
        "status": "failed",
        "brand": None,
        "last4": None,
        "exp_month": None,
        "exp_year": None,
        "phone": session.get('customer_details', {}).get('phone')
    }

    if not payment_intent_id:
        return info

    try:
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        payment_method_id = payment_intent.payment_method
        payment_method = stripe.PaymentMethod.retrieve(payment_method_id)
        card = payment_method.get('card', {})

        info.update({
            "status": "completed",
            "brand": card.get('brand'),
            "last4": card.get('last4'),
            "exp_month": card.get('exp_month'),
            "exp_year": card.get('exp_year'),
        })

        if not info["phone"]:
            info["phone"] = payment_method.get('billing_details', {}).get('phone')

    except Exception as e:
        logging.warning(f"[Webhook] Failed to retrieve payment method: {e}")

    return info


def process_order(order, user, total_amount, session_id, customer_email, card_info):
    if order.key.status != 'reserved':
        logging.warning(f"[Webhook] Key for order {order.pk} is not reserved.")
        return False

    timestamp = int(datetime.now().timestamp() * 1000)

    if order.game:
        item_id = order.game.id
        trx = create_transaction(user, card_info["status"], session_id, total_amount, customer_email,
                                 card_info["brand"], card_info["last4"], card_info["phone"],
                                 card_info["exp_month"], card_info["exp_year"],
                                 order.key, order.game, None)
        send_mailjet_email_purchase_success(customer_email, order.game.name, order.id, order.key)
        create_user_game(user, order.key, trx, order.game, None)
    else:
        item_id = order.dlc.id
        trx = create_transaction(user, card_info["status"], session_id, total_amount, customer_email,
                                 card_info["brand"], card_info["last4"], card_info["phone"],
                                 card_info["exp_month"], card_info["exp_year"],
                                 order.key, None, order.dlc)
        send_mailjet_email_purchase_success(customer_email, order.dlc.name, order.id, order.key)
        create_user_game(user, order.key, trx, None, order.dlc)

    create_user_interaction(user.id, item_id, timestamp)

    order.key.status = 'sold'
    order.key.save()
    order.delete()

    return True

@csrf_exempt
def webhook_view(request):
    logger = logging.getLogger(__name__)
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    event = verify_stripe_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET, logger)
    if event is None:
        return HttpResponse(status=400)

    if event['type'] not in ['checkout.session.completed', 'checkout.session.async_payment_succeeded']:
        return HttpResponse(status=200)

    session = event['data']['object']
    session_id = session.get('id')
    customer_email = session.get('customer_details', {}).get('email')
    user_id = session.get('metadata', {}).get('user_id')

    if Transaction.objects.filter(session_id=session_id).exists():
        logger.info(f"[Webhook] Session {session_id} already processed.")
        return HttpResponse(status=200)

    try:
        user = MyUser.objects.get(id=user_id)
    except MyUser.DoesNotExist:
        logger.warning(f"[Webhook] User with ID {user_id} not found.")
        return HttpResponse(status=404)

    try:
        line_items = stripe.checkout.Session.list_line_items(session_id)
    except Exception as e:
        logger.error(f"[Webhook] Failed to get line items: {e}")
        return HttpResponse(status=500)

    card_info = get_payment_info(session)

    processed_orders = 0
    
    order_ids_str = session.metadata.get("order_ids", "")
    order_ids = [int(id.strip()) for id in order_ids_str.split(",") if id.strip()]
    
    line_items_data = line_items['data']
    
    if len(line_items_data) != len(order_ids):
        logger.warning(f"[Webhook] Mismatch: {len(line_items_data)} items vs {len(order_ids)} orders.")
        return HttpResponse(status=400)

    for item, order_id in zip(line_items_data, order_ids):
        try:
            order = Order.objects.get(id=order_id, user=user, key__status='reserved')
            total_amount = item['amount_total'] / 100
            with transaction.atomic():
                if process_order(order, user, total_amount, session_id, customer_email, card_info):
                    processed_orders += 1
        except Order.DoesNotExist:
            logger.error(f"[Webhook] Order with ID {order_id} not found or not reserved.")
            continue
        except Exception as e:
            logger.error(f"[Webhook] Failed processing order {order.pk}: {e}")
            continue

    if processed_orders == 0:
        return HttpResponse(status=400)
    return HttpResponse(status=200)
