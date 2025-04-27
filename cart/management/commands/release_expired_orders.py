from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from cart.models import Order

class Command(BaseCommand):
    help = 'Release reserved keys for orders not paid after timeout'

    def handle(self, *args, **kwargs):
        timeout_minutes = 2
        timeout_threshold = timezone.now() - timedelta(minutes=timeout_minutes)

        expired_orders = Order.objects.filter(
            created_at__lt=timeout_threshold,
            key__status='reserved'
        )

        for order in expired_orders:
            self.stdout.write(f"Releasing order {order.pk}...")

            if order.key:
                order.key.status = 'available'
                order.key.save()

            order.delete()

        self.stdout.write(self.style.SUCCESS('Successfully released expired orders!'))
