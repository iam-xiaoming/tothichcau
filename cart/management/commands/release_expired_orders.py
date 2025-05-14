from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from cart.models import Order

class Command(BaseCommand):
    help = 'Release expired orders after 1 hour of inactivity'

    def handle(self, *args, **kwargs):
        expired_time = timezone.now() - timedelta(hours=1)
        expired_orders = Order.objects.filter(
            key__isnull=False,
            created_at__lt=expired_time
        )

        count = 0
        for order in expired_orders:
            key = order.key
            if key:
                key.status = 'available'
                key.save()
                order.key = None
                order.save()
                count += 1

        self.stdout.write(f"Released {count} expired order(s)")
