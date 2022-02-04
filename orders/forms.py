from orders.models import Order
from django import forms

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'email', 'telephone',
            'address1', 'address2', 'postal_code', 'city', 'country', 'note',
            'transport'
        ]