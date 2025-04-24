from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
import stripe
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order
from games.models import Game, Key, UserGame, Category
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from users.models import MyUser
from .models import Transaction
import logging
from django.views.decorators.http import require_GET
from django.db import transaction
from django.urls import reverse


stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
@require_GET
def is_game_in_cart(request):
    if not request.user.is_authenticated:
        return JsonResponse({'in_cart': False})

    game_id = request.GET.get('game_id')
    if not game_id:
        return JsonResponse({'error': 'Missing game_id'}, status=400)


    in_cart = Order.objects.filter(user=request.user, game_id=game_id).exists()
    if in_cart:
        return JsonResponse({'in_cart': in_cart})
    in_library = UserGame.objects.filter(user=request.user,
                                    game=Game.objects.get(id=game_id)).exists()
    if in_library:
        return JsonResponse({'in_library': in_library})
        
    return JsonResponse({'add_to_cart': True})


@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST' and request.user.is_authenticated:
        user = request.user
        game_id = request.POST.get('game_id')

        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Game not found.'})

        # Check if already in cart
        if Order.objects.filter(user=user, game=game).exists():
            return JsonResponse({
                'success': False,
                'already_in_cart': True,
                'message': 'Already in cart.'
            })

        # Add to cart
        Order.objects.create(user=user, game=game)
        return JsonResponse({'success': True, 'message': 'Game added to cart!'})

    return JsonResponse({'success': False, 'message': 'Invalid request or not authenticated.'})


def get_cart_count(request):
    user = request.user
    if user.is_authenticated:
        order_count = user.orders.count()  # Correct way to access related orders
    else:
        order_count = 0  # If not authenticated, set count to 0
    return JsonResponse({'order_count': order_count})


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
        
        try:
            with transaction.atomic():
                key = Key.objects.select_for_update().filter(game=game, status='available').first()
                if not key:
                    return JsonResponse({'error': 'Out of stock. No available key for this game.'}, status=400)
            
            key.status = 'sold'
            key.save()
            
            trx = Transaction.objects.create(
                user=user,
                game=game,
                key=key,
                status=status,
                session_id=session_id,
                total_amount=total_amount,
                customer_email=customer_email,
                brand=brand,
                last4=last4,
                phone=phone,
                exp_month=exp_month,
                exp_year=exp_year
            )
            UserGame.objects.create(user=user, game=game, key=key, transaction=trx)
            Order.objects.filter(user=user, game=game).delete()
            
        except Exception as e:
            raise JsonResponse({'error': str(e)}, status=500)

    return HttpResponse(status=200)