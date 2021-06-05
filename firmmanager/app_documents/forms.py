from datetime import datetime

from django import forms

from app_crm.models import Contractor
from app_documents.models import Order, Contract, OrderWithoutContract
from app_storage.models import ProductStoreOrderBooking, ProductStoreOrderWithoutContractBooking


class BookingCreateForm(forms.ModelForm):
    class Meta:
        model = ProductStoreOrderBooking
        fields = ['order', 'product', 'store', 'quantity', 'counted_sum']

    def save(self, commit=True):
        data = self.cleaned_data
        product = data['product']
        counted_sum = product.cost * int(data['quantity'])
        spec_booking = ProductStoreOrderBooking(order=data['order'], product=data['product'], price=product.cost,
                                                store=data['store'], quantity=data['quantity'], counted_sum=counted_sum,
                                                total_sum=counted_sum)
        spec_booking.save()


class OrderWithoutContractBookingCreateForm(forms.ModelForm):
    class Meta:
        model = ProductStoreOrderWithoutContractBooking
        fields = ['order', 'product', 'store', 'quantity', 'counted_sum']

    def save(self, commit=True):
        data = self.cleaned_data
        product = data['product']
        counted_sum = product.cost * int(data['quantity'])
        spec_booking = ProductStoreOrderWithoutContractBooking(order=data['order'], product=data['product'],
                                                               price=product.cost, store=data['store'],
                                                               quantity=data['quantity'], counted_sum=counted_sum,
                                                               total_sum=counted_sum)
        spec_booking.save()


class BookingEditForm(forms.ModelForm):
    class Meta:
        model = ProductStoreOrderBooking
        fields = ['order', 'product', 'store', 'quantity', 'total_price']


class OrderWithoutContractBookingEditForm(forms.ModelForm):
    class Meta:
        model = ProductStoreOrderWithoutContractBooking
        fields = ['order', 'product', 'store', 'quantity', 'total_price']


class OrderBookingForm(forms.ModelForm):
    class Meta:
        model = ProductStoreOrderBooking
        fields = ['product', 'store', 'quantity']


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
            number = f'00{order_id}-{current_year}'
        elif 10 <= order_id < 100:
            number = f'0{order_id}-{current_year}'
        else:
            number = f'{order_id}-{current_year}'
        order = Order(number=number, contract=data['contract'],
                      delivery_conditions=data['delivery_conditions'],
                      delivery_time=data['delivery_time'],
                      delivery_address=data['delivery_address'],
                      payment_conditions=data['payment_conditions'],)
        if commit:
            order.save()
        else:
            return order

    class Meta:
        model = Order
        fields = ['number', 'contract', 'delivery_conditions', 'delivery_time', 'delivery_address',
                  'payment_conditions']


class OrderWithoutContractForm(forms.ModelForm):
    def save(self, commit=True):
        data = self.cleaned_data
        current_year = datetime.now().year
        order_id = len(OrderWithoutContract.objects.all().filter(contractor=data['contractor'])) + 1
        if order_id < 10:
            number = f'00{order_id}-{current_year}'
        elif 10 <= order_id < 100:
            number = f'0{order_id}-{current_year}'
        else:
            number = f'{order_id}-{current_year}'
        order = OrderWithoutContract(number=number, contractor=data['contractor'], organization=data['organization'],
                                     currency=data['currency'],delivery_conditions=data['delivery_conditions'],
                                     delivery_time=data['delivery_time'], delivery_address=data['delivery_address'],
                                     payment_conditions=data['payment_conditions'],)
        if commit:
            order.save()
        else:
            return order

    class Meta:
        model = OrderWithoutContract
        exclude = ['created', 'shipment_mark', 'counted_sum', 'total_sum', 'to_delete', 'responsible']


class ContractFilterForm(forms.Form):
    created_before = forms.DateField(widget=forms.DateInput, required=False, label='До')
    created_after = forms.DateField(widget=forms.DateInput, required=False, label='От')
    contractor = forms.ModelChoiceField(Contractor.objects.all(), required=False, label='Контрагент')


class OrderFilterForm(forms.Form):
    contractor = forms.ModelChoiceField(Contractor.objects.all(), required=False, label='Контрагент')
    created_after = forms.DateField(widget=forms.DateInput, required=False, label='От')
    created_before = forms.DateField(widget=forms.DateInput, required=False, label='До')


class OrderWithoutContractFilterForm(forms.Form):
    contractor = forms.ModelChoiceField(Contractor.objects.all(), required=False, label='Контрагент')
    created_after = forms.DateField(widget=forms.DateInput, required=False, label='От')
    created_before = forms.DateField(widget=forms.DateInput, required=False, label='До')
