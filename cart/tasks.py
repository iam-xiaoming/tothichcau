# cart/tasks.py
from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from cart.models import Order

@shared_task
def release_expired_orders():
    expired_orders = Order.objects.filter(
        key__isnull=False,
        created_at__lt=timezone.now() - timedelta(hours=1)
    )
    for order in expired_orders:
        key = order.key
        key.status = 'available'
        key.save()
        order.key = None
        order.save()
    return f"{expired_orders.count()} expired orders released."
