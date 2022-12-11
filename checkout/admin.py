from django.contrib import admin
from .models import Order, OrderLineItem

# Admin panel for orders control from Boutique Ado project
class OrderLineItemAdminInline(admin.TabularInline):
    # Allows to add and edit line items in the admin panel.
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    #Sets the layout of order preview.
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'order_total',
                       'grand_total',)

    fields = ('order_number', 'date', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'delivery_cost',
              'order_total', 'grand_total',)

    list_display = ('order_number', 'date', 'full_name',
                    'order_total', 'delivery_cost',
                    'grand_total',)

    # Shows orders in reverse chronological order.
    ordering = ('-date',)

admin.site.register(Order, OrderAdmin)