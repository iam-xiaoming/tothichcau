from django.apps import AppConfig


class AdminManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_manager'
    
    def ready(self):
        import admin_manager.signals
