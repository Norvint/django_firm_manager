from datetime import datetime

from django import forms

from app_crm.models import Contractor
from app_documents.models import Order, Contract
from app_storage.models import ProductStoreOrderBooking


class BookingForm(forms.ModelForm):
    class Meta:
        model = ProductStoreOrderBooking
        fields = ['order', 'product', 'store', 'quantity', 'sum']

    def save(self, commit=True):
        data = self.cleaned_data
        product = data['product']
        product_sum = product.cost * int(data['quantity'])
        spec_booking = ProductStoreOrderBooking(order=data['order'], product=data['product'],
                                                store=data['store'], quantity=data['quantity'], sum=product_sum)
        spec_booking.save()


class OrderBookingForm(forms.ModelForm):
    class Meta:
        model = ProductStoreOrderBooking
        fields = ['product', 'store', 'quantity', 'sum']


class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['number', 'type', 'contractor', 'organization', 'currency', 'created']


class OrderForm(forms.ModelForm):

    def save(self, commit=True):
        data = self.cleaned_data
        current_year = datetime.now().year
        order_id = len(Order.objects.all().filter(contract=data['contract'])) + 1
        if order_id < 10:
            number = f'{current_year}-00{order_id}'
        elif 10 <= order_id < 100:
            number = f'{current_year}-0{order_id}'
        else:
            number = f'{current_year}-{order_id}'
        order = Order(number=number, contract=data['contract'],
                      delivery_conditions=data['delivery_conditions'],
                      delivery_time=data['delivery_time'],
                      delivery_address=data['delivery_address'],
                      payment_conditions=data['payment_conditions'],
                      shipment_mark=data['shipment_mark'], )
        if commit:
            order.save()
        else:
            return order

    class Meta:
        model = Order
        fields = ['number', 'contract', 'delivery_conditions', 'delivery_time', 'delivery_address',
                  'payment_conditions', 'shipment_mark']


class ContractFilterForm(forms.Form):
    created_before = forms.DateField(widget=forms.DateInput, required=False, label='До')
    created_after = forms.DateField(widget=forms.DateInput, required=False, label='От')
    contractor = forms.ModelChoiceField(Contractor.objects.all(), required=False, label='Контрагент')


class OrderFilterForm(forms.Form):
    contractor = forms.ModelChoiceField(Contractor.objects.all(), required=False, label='Контрагент')
    created_after = forms.DateField(widget=forms.DateInput, required=False, label='От')
    created_before = forms.DateField(widget=forms.DateInput, required=False, label='До')
