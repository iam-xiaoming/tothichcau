import stripe

def stripe_create(created, instance):
    try:
        if created:
            # Create Stripe product
            stripe_product = stripe.Product.create(
                name=instance.name,
                description=instance.description,
                images=[instance.image.url]
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
                    description=instance.description,
                    images=[instance.image.url]
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
    
    
def instance_scoring(instance, score, weighted):
    avg_score = instance.average_score
    if avg_score:
            avg_score = (avg_score + weighted * score) / (weighted + 1)
    else:
        avg_score = score
            
    avg_score_percentage = avg_score * 10
    
    if avg_score_percentage <= 19:
        instance.rating = 'overwhelmingly negative'
    elif avg_score_percentage <= 39:
        instance.rating = 'mostly negative' 
    elif avg_score_percentage <= 69:
        instance.rating = 'mixed'
    elif avg_score_percentage <= 79:
        instance.rating = 'mostly positive'
    elif avg_score_percentage <= 94:
        instance.rating = 'very positive'
    else:
        instance.rating = 'overwhelmingly positive'
    
    instance.average_score = avg_score
        
    return instance


def get_game_dlcs(instance):
    if instance:
        return instance.dlc.all()