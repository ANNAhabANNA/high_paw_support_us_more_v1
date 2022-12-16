from django.apps import AppConfig

class CheckoutConfig(AppConfig):
    #default_auto_field = 'django.db.models.BigAutoField'
    name = 'checkout'

    #Overrides the ready method and importing the signals module.
    def ready(self):
        import checkout.signals
