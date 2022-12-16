from django.http import HttpResponse

# The webhook handler from Boutique Ado
class StripeWH_Handler:
    """
    Handle Stripe webhooks
    """

    # Called every time an instance of the class is created.
    # Assigned request as an attribute provides an access  to any attributes of the request coming from Stripe.
    def __init__(self, request):
        self.request = request

    # Takes the event stripe is sending and returns an HTTP response indicating it was received.
    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    # Sent each time a user completes the payment process.    
    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)