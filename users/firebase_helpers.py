import pyrebase
from GameArt import settings

def firebase_config():
    config = settings.FIREBASE_CONFIG
    try:
        firebase = pyrebase.initialize_app(config)
        print("Firebase initialized successfully")  # Debug
        return firebase
    except Exception as e:
        print(f"Firebase initialization error: {str(e)}")
        raise ValueError(f"Failed to initialize Firebase: {str(e)}")