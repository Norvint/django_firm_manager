from django import forms

from app_crm.models import TypeOfContractor, FieldOfActivity, ContractorComment, ContractorContact, Contractor, \
    ContactPersonContactType, ContactPerson, ContractorFile


class ContractorFilterForm(forms.Form):
    country = forms.CharField(widget=forms.TextInput, required=False, label='Страна')
    type_of_contractor = forms.ModelChoiceField(TypeOfContractor.objects.all(), required=False, label='Тип контрагента')
    field_of_activity = forms.ModelChoiceField(FieldOfActivity.objects.all(), required=False,
                                               label='Сфера деятельности')
    tag = forms.CharField(required=False, label='Тэг')


class ContractorCommentForm(forms.ModelForm):
    text = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2, 'cols': 200}),
                           label='Текст комментария')

    class Meta:
        model = ContractorComment
        exclude = ['user', 'created', 'contractor']


class ContractorForm(forms.ModelForm):
    class Meta:
        model = Contractor
        fields = ['title', 'status', 'type_of_contractor', 'field_of_activity', 'position', 'position_en', 'appeal',
                  'appeal_en', 'name', 'second_name', 'last_name', 'country', 'tel', 'legal_address', 'actual_address',
                  'requisites', 'tag']
        widgets = {
            'requisites': forms.Textarea(attrs={'rows': 5, 'cols': 80}),
        }


class ContactPersonForm(forms.ModelForm):
    class Meta:
        model = ContactPerson
        fields = ['name', 'second_name', 'last_name', 'position', 'contractor', 'tag']


class ContactForm(forms.Form):
    type_of_contact = forms.ModelChoiceField(ContactPersonContactType.objects.all(), label='Тип контакта', required=False)
    contact = forms.CharField(max_length=50, label='Контактные данные', required=False)


class ContractorFileForm(forms.ModelForm):
    class Meta:
        model = ContractorFile
        fields = ['title', 'contractor', 'file', 'description', 'category']
