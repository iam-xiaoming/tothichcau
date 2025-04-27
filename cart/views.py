from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
import stripe
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order
from games.models import Game
from keys.models import Key
from users.models import UserGame
from game_features.models import Category
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
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.response import Response


stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request, pk, game_pk):
    try:
        user = MyUser.objects.get(pk=pk)
        game = Game.objects.get(id=game_pk)
    except MyUser.DoesNotExist:
        return Response({'error': 'User not found.'}, status=404)
    except Game.DoesNotExist:
        return Response({'error': 'Game not found.'}, status=404)
    
    available_key = Key.objects.filter(status='available').first()
    
    if not available_key:
        return Response({'stockout': 'Stockout'}, status=400)
    
    try:
        order = Order.objects.create(user=user, game=game, key=available_key)
        # update key status
        available_key.status = 'pending'
        available_key.save()
        # get total order count of specific user
        order_count = user.orders.count()
    except Exception as e:
        return Response({'error': str(e)}, status=400)
    else:
        return Response({'success': True, 'order_count': order_count, 'message': 'Game added to cart!'})
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart_count(request, pk):
    try:
        order_count =  Order.objects.filter(user__pk=pk).count()
    except MyUser.DoesNotExist:
        return Response({'error': 'User not found.'}, status=404)
    
    return Response({'message': 'success', 'order_count': order_count}, status=200)


class CartView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'cart/cart.html'
    context_object_name = 'orders'
    login_url = '/login/'

    def get_queryset(self):        
        # Return only the orders of the logged-in user
        return self.request.user.orders.all()
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = context['orders']

        total_price = sum(order.game.price for order in orders)
        total_discounted_price = sum(order.game.discounted_price for order in orders)
        
        context['total_price'] = total_price
        context['total_discounted_price'] = total_discounted_price
        context['discount'] = total_price - total_discounted_price
        context['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLISHABLE_KEY
        context['categories'] = Category.objects.all()
        return context
    

class CartDeleteView(LoginRequiredMixin, View):
    login_url = '/login/'
    
    def post(self, request, pk, *args, **kwargs):
        order = get_object_or_404(Order, pk=pk, user=request.user)
        # update key status
        if order.key:
            order.key.status = 'available'
            order.key.save()
            
        # delete order
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
                'price': order.game.stripe_price_id,
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
    return render(request, "cart/cancel.html")


@csrf_exempt
def webhook_view(request):
    logger = logging.getLogger(__name__)
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        logger.warning(f"[Webhook] Invalid signature or payload: {e}")
        return HttpResponse(status=400)

    if event['type'] not in ['checkout.session.completed', 'checkout.session.async_payment_succeeded']:
        return HttpResponse(status=200)

    session = event['data']['object']
    session_id = session.get('id')
    customer_email = session.get('customer_details', {}).get('email')
    phone = session.get('customer_details', {}).get('phone')
    user_id = session.get('metadata', {}).get('user_id')

    if Transaction.objects.filter(session_id=session_id).exists():
        logger.info(f"[Webhook] Session {session_id} already processed.")
        return HttpResponse(status=200)

    status = 'failed'
    brand = last4 = exp_month = exp_year = None

    payment_intent_id = session.get('payment_intent')
    if payment_intent_id:
        try:
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            payment_method_id = payment_intent.payment_method
            payment_method = stripe.PaymentMethod.retrieve(payment_method_id)
            card_info = payment_method.get('card', {})

            brand = card_info.get('brand')
            last4 = card_info.get('last4')
            exp_month = card_info.get('exp_month')
            exp_year = card_info.get('exp_year')

            if not phone:
                phone = payment_method.get('billing_details', {}).get('phone')

            status = 'completed'
        except Exception as e:
            logger.warning(f"[Webhook] Failed to retrieve payment method: {e}")

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

    for item in line_items['data']:
        product_id = item['price']['product']
        total_amount = item['amount_total'] / 100

        try:
            game = Game.objects.get(stripe_product_id=product_id)
        except Game.DoesNotExist:
            logger.warning(f"[Webhook] Game with product ID {product_id} not found.")
            continue

        # Start database atomic block
        for order in Order.objects.all():
            try:
                with transaction.atomic():
                    # transaction
                    trx = Transaction.objects.create(
                        user=user,
                        game=game,
                        status=status,
                        session_id=session_id,
                        total_amount=total_amount,
                        customer_email=customer_email,
                        brand=brand,
                        last4=last4,
                        phone=phone,
                        exp_month=exp_month,
                        exp_year=exp_year,
                        key=order.key
                    )
                    # user game
                    UserGame.objects.create(
                        user=user,
                        game=game,
                        key=order.key,
                        transaction=trx
                    )
                    # update
                    order.key.status = 'sold'
                    order.key.save()
                    
                    order.delete()

            except Exception as e:
                logger.error(f"[Webhook] Failed processing game {game.name}: {e}")
                return JsonResponse({'error': str(e)}, status=500)

    return HttpResponse(status=200)