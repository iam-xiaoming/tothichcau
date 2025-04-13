from firebase_admin import auth, credentials
import firebase_admin
from datetime import datetime
from users.models import MyUser
from datetime import datetime

def firebase_config():
    if not firebase_admin._apps:
            try:
                cred = credentials.Certificate(r"firebase_config.json")
                firebase_admin.initialize_app(cred)
                print("Firestore initialized successfully.")
            except   Exception as e:
                print(f"Error initializing Firestore: {e}")


# đồng bộ từ firebase về database của django
def sync_firebase_users():  
    firebase_config()
    for user in auth.iter_users():
        firebase_uid = user.uid
        firebase_username = user.display_name
        firebase_email = user.email
        firebase_role = user.custom_claims.get('role')
        firebase_create_at = datetime.fromtimestamp(user.user_metadata.creation_timestamp / 1000.0).strftime('%Y-%m-%d %H:%M:%S')

        # Tạo mới hoặc cập nhật user
        obj, created = MyUser.objects.update_or_create(
            id =firebase_uid,
            defaults={
                "id": firebase_uid,
                "username": firebase_username,
                "email": firebase_email,
                "role": firebase_role,
                "created_at": firebase_create_at,}
        )   