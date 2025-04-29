from .models import Transaction
from users.models import UserGame
from track.models import UserInteraction



def create_user_interaction(user_id, item_id, timestamp, event_type='buy'):
    
    UserInteraction.objects.create(
        user_id=user_id,
        item_id=item_id,
        event_type=event_type,
        timestamp=timestamp
    ) 
   

def create_user_game(user, key, transaction, game, dlc):
    if not (game or dlc):
        raise ValueError("Either 'game' or 'dlc' must be provided.")
    
    if game:
        UserGame.objects.create(user=user, key=key, transaction=transaction, game=game)
    else:
        UserGame.objects.create(user=user, key=key, transaction=transaction, dlc=dlc)
        
        

def create_transaction(user, status, session_id, total_amount, customer_email, brand, last4, phone, exp_month, exp_year, key, game=None, dlc=None):
    if not (game or dlc):
        raise ValueError("Either 'game' or 'dlc' must be provided.")

    if game:
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
            key=key
        )
    else:
        trx = Transaction.objects.create(
            user=user,
            dlc=dlc,
            status=status,
            session_id=session_id,
            total_amount=total_amount,
            customer_email=customer_email,
            brand=brand,
            last4=last4,
            phone=phone,
            exp_month=exp_month,
            exp_year=exp_year,
            key=key
        )

    return trx
