from django import forms

from app_crm.models import Contractor
from app_documents.models import Invoice, Specification, Contract
from app_storage.models import ProductStoreBooking


class SpecificationBookingForm(forms.ModelForm):
    class Meta:
        model = ProductStoreBooking
        fields = ['specification', 'product', 'store', 'quantity', 'sum']

    def save(self, commit=True):
        data = self.cleaned_data
        product = data['product']
        product_sum = product.cost * int(data['quantity'])
        spec_booking = ProductStoreBooking(specification=data['specification'], product=data['product'],
                                           store=data['store'], quantity=data['quantity'], sum=product_sum)
        spec_booking.save()


class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['number', 'type', 'contractor', 'organization', 'delivery_address', 'currency']


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['number', 'specification', 'shipment_mark']


class SpecificationForm(forms.ModelForm):
    class Meta:
        model = Specification
        fields = ['number', 'contract', 'delivery_conditions', 'loading_place', 'payment_conditions']


class ContractFilterForm(forms.Form):
    created_before = forms.DateField(widget=forms.DateInput, required=False, label='До')
    created_after = forms.DateField(widget=forms.DateInput, required=False, label='От')
    contractor = forms.ModelChoiceField(Contractor.objects.all(), required=False, label='Контрагент')


class SpecificationFilterForm(forms.Form):
    contractor = forms.ModelChoiceField(Contractor.objects.all(), required=False, label='Контрагент')
    created_after = forms.DateField(widget=forms.DateInput, required=False, label='От')
    created_before = forms.DateField(widget=forms.DateInput, required=False, label='До')


class InvoiceFilterForm(forms.Form):
    contractor = forms.ModelChoiceField(Contractor.objects.all(), required=False, label='Контрагент')
    created_after = forms.DateField(widget=forms.DateInput, required=False, label='От')
    created_before = forms.DateField(widget=forms.DateInput, required=False, label='До')
