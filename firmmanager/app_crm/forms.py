from django import forms
from django.contrib.auth.models import User

from app_crm.models import TypeOfContractor, FieldOfActivity, ContractorComment, ContractorContact, Contractor


class ContractorFilterForm(forms.Form):
    country = forms.CharField(widget=forms.TextInput, required=False, label='Страна')
    type_of_contractor = forms.ModelChoiceField(TypeOfContractor.objects.all(), required=False, label='Тип контрагента')
    field_of_activity = forms.ModelChoiceField(FieldOfActivity.objects.all(), required=False, label='Сфера деятельности')


class ContractorCommentForm(forms.ModelForm):
    text = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 5, 'cols': 35}))

    class Meta:
        model = ContractorComment
        exclude = ['user', 'created', 'contractor']


class ContractorForm(forms.ModelForm):
    class Meta:
        model = Contractor
        fields = ['title', 'status', 'type_of_contractor', 'field_of_activity', 'position', 'appeal', 'name',
                  'second_name', 'last_name', 'country', 'requisites']


class ContractorContactForm(forms.ModelForm):
    class Meta:
        model = ContractorContact
        fields = ['contractor', 'type_of_contact', 'contact', 'contact_name']
