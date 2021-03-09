from django import forms
from django.contrib.auth.models import User

from app_crm.models import TypeOfContractor, FieldOfActivity, ContractorComment


class ContractorFilterForm(forms.Form):
    country = forms.CharField(widget=forms.TextInput, required=False, label='Страна')
    type_of_contractor = forms.ModelChoiceField(TypeOfContractor.objects.all(), required=False, label='Тип контрагента')
    field_of_activity = forms.ModelChoiceField(FieldOfActivity.objects.all(), required=False, label='Сфера деятельности')


class ContractorCommentForm(forms.ModelForm):
    text = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 5, 'cols': 35}))

    class Meta:
        model = ContractorComment
        exclude = ['user', 'created', 'contractor']
