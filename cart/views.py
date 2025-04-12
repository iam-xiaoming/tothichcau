from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
import stripe
from django.views import View
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order


stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
def cart_view(request):
    orders = Order.objects.all()
    return render(request, 'cart/cart.html', {'orders': orders})

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price": "price_1RCuquE8Jpbq2wr1BXiCUhN9",
                        "quantity": 1,
                    }
                ],
                metadata={
                    "product_id": 'prod_S799Z6Mxal533G'    
                },
                mode="payment",
                success_url=request.build_absolute_uri(reverse("success")),
                cancel_url=request.build_absolute_uri(reverse("cancel")),
            )
            return JsonResponse({'id': checkout_session.id})
        except stripe.error.StripeError as e:
            return JsonResponse({'error': str(e)}, status=400)


class CheckoutView(TemplateView):
    template_name = 'cart/checkout.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY
        })
        return context


def success(request):
    return render(request, "cart/success.html")


def cancel(request):
    return render(request, "cart/cancel.html")


# @csrf_exempt
# def webhook_view(request):
#     payload = request.body
    
#     sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#     event = None
    
#     try:
#         event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
#     except ValueError as e:
#         return HttpResponse(status=400)
#     except stripe.error.SignatureVerificationError as e:
#         return HttpResponse(status=400)
    
#     if event['type'] == 'checkout.session.completed' or event['type'] == 'checkout.session.async_payment_succeeded':
#         session = event['data']['object']
        
#         customer_email = session['customer_details']['email']
#         product_id = session['metadata']['product_id']
        
#         # mailjet.send_mailjet_email_purchase_success(customer_email, product_id, 'Outlast2')
    
#     return HttpResponse(status=200)