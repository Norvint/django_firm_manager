from django import forms

from app_crm.models import TypeOfContractor, FieldOfActivity, ContractorComment, Contact, Contractor, \
    ContactType, ContactPerson


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
                  'second_name', 'last_name', 'country', 'legal_address', 'actual_address', 'requisites']
        widgets = {
            'requisites': forms.Textarea(attrs={'rows': 3, 'cols': 20}),
        }


class ContactPersonForm(forms.ModelForm):
    model = ContactPerson
    fields = ['name', 'second_name', 'last_name', 'position', 'contractor']


class ContactForm(forms.Form):
    type_of_contact = forms.ModelChoiceField(ContactType.objects.all(), label='Тип контакта')
    contact = forms.CharField(max_length=50, label='Контактные данные')
