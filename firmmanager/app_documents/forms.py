from django import forms

from app_crm.models import Contractor
from app_documents.models import Order, Contract
from app_storage.models import ProductStoreBooking


class OrderBookingForm(forms.ModelForm):
    class Meta:
        model = ProductStoreBooking
        fields = ['order', 'product', 'store', 'quantity', 'sum']

    def save(self, commit=True):
        data = self.cleaned_data
        product = data['product']
        product_sum = product.cost * int(data['quantity'])
        spec_booking = ProductStoreBooking(order=data['order'], product=data['product'],
                                           store=data['store'], quantity=data['quantity'], sum=product_sum)
        spec_booking.save()


class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['number', 'type', 'contractor', 'organization', 'currency', 'created']


class OrderForm(forms.ModelForm):

    def save(self, commit=True):
        data = self.cleaned_data
        number = len(Order.objects.all().filter(contract=data['contract'])) + 1
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
