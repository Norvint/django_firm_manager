from django import forms
from django.contrib.auth.models import User

from app_crm.models import TypeOfContractor, FieldOfActivity, ContractorComment, Contractor, ContactPersonContactType, \
    ContractorContactPerson, ContractorFile, LeadStatus, LeadComment, Lead, LeadContactPerson, ContractorRequisites, \
    LeadContact


class ContractorFilterForm(forms.Form):
    country = forms.CharField(widget=forms.TextInput, required=False, label='Страна')
    type_of_contractor = forms.ModelChoiceField(TypeOfContractor.objects.all(), required=False, label='Тип контрагента')
    field_of_activity = forms.ModelChoiceField(FieldOfActivity.objects.all(), required=False,
                                               label='Сфера деятельности')
    tag = forms.CharField(required=False, label='Тэг')


class LeadFilterForm(forms.Form):
    status = forms.ModelChoiceField(LeadStatus.objects.all(), required=False, label='Статус')
    responsible = forms.ModelChoiceField(User.objects.all(), required=False, label='Ответственный')
    field_of_activity = forms.ModelChoiceField(FieldOfActivity.objects.all(), required=False,
                                               label='Сфера деятельности')
    tag = forms.CharField(required=False, label='Тэг')


class ContractorCommentForm(forms.ModelForm):
    text = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2, 'cols': 200}),
                           label='Текст комментария')

    class Meta:
        model = ContractorComment
        exclude = ['user', 'created', 'contractor']


class LeadCommentForm(forms.ModelForm):
    text = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2, 'cols': 200}),
                           label='Текст комментария')

    class Meta:
        model = LeadComment
        exclude = ['user', 'created', 'lead']


class ContractorForm(forms.ModelForm):
    class Meta:
        model = Contractor
        widgets = {
            'requisites': forms.Textarea(attrs={'rows': 5, 'cols': 80}),
        }
        exclude = ['to_delete', 'responsible']


class ContractorRequisitesForm(forms.ModelForm):
    class Meta:
        model = ContractorRequisites
        exclude = ['contractor']


class ContractorContactPersonForm(forms.ModelForm):
    class Meta:
        model = ContractorContactPerson
        exclude = ['to_delete']


class ContactForm(forms.Form):
    type_of_contact = forms.ModelChoiceField(ContactPersonContactType.objects.all(), label='Тип контакта', required=False)
    contact = forms.CharField(max_length=50, label='Контактные данные', required=False)


class ContractorFileForm(forms.ModelForm):
    class Meta:
        model = ContractorFile
        fields = ['title', 'contractor', 'file', 'description', 'category']


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        exclude = ['responsible']


class LeadContactPersonForm(forms.ModelForm):
    class Meta:
        model = LeadContactPerson
        exclude = ['to_delete']


class LeadContactForm(forms.ModelForm):
    class Meta:
        model = LeadContact
        exclude = ['lead']

