from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from .models import Game
import stripe


@receiver(post_delete, sender=Game)
def delete_game(sender, instance, **kwargs):
    if instance:
        instance.image.delete(save=False)
        

@receiver(pre_save, sender=Game)
def pre_save_game(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Game.objects.get(pk=instance.pk)
        
        if old_instance.image != instance.image:
            if old_instance.image:
                old_instance.image.delete(save=False)
                
                
@receiver(post_save, sender=Game)
def post_save_game(sender, instance, created, **kwargs):
    try:
        if created:
            # Create Stripe product
            stripe_product = stripe.Product.create(
                name=instance.name,
                description=instance.description
            )
            stripe_price = stripe.Price.create(
                product=stripe_product.id,
                unit_amount=int(instance.discounted_price * 100),
                currency='usd',
            )

            instance.stripe_product_id = stripe_product.id
            instance.stripe_price_id = stripe_price.id
            instance.save(update_fields=["stripe_product_id", "stripe_price_id"])

        else:
            # Update existing Stripe product
            if instance.stripe_product_id:
                stripe.Product.modify(
                    instance.stripe_product_id,
                    name=instance.name,
                    description=instance.description
                )

            # Stripe prices are immutable (can’t update amount),
            # so we create a new price if the price has changed
            if instance.stripe_price_id:
                old_price = stripe.Price.retrieve(instance.stripe_price_id)
                new_price_amount = int(instance.discounted_price * 100)

                if old_price.unit_amount != new_price_amount:
                    new_price = stripe.Price.create(
                        product=instance.stripe_product_id,
                        unit_amount=new_price_amount,
                        currency='usd',
                    )
                    instance.stripe_price_id = new_price.id
                    instance.save(update_fields=["stripe_price_id"])

    except Exception as e:
        print(f"Stripe sync error: {e}")
        raise
