from django.http import HttpResponse

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
            content=f'Webhook received: {event["type"]}',
            status=200)