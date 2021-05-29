from datetime import datetime

from django import forms
from django.contrib.auth.models import User

from app_organizations.models import Organization, OrganizationFile, WorkerContactType, Worker


class WorkerForm(forms.Form):
    user = forms.ModelChoiceField(User.objects.all(), required=False, blank=True, label='Пользователь')
    name = forms.CharField(max_length=30, label='Имя')
    second_name = forms.CharField(max_length=30, label='Отчество')
    last_name = forms.CharField(max_length=30, label='Фамилия')
    position = forms.CharField(max_length=30, label='Должность')
    organization = forms.ModelChoiceField(Organization.objects.all(), required=False, label='Организация')
    serial_number = forms.CharField(max_length=4, required=False, label='Серия')
    number = forms.CharField(max_length=6, required=False, label='Номер')
    issued_by = forms.CharField(max_length=100, required=False, label='Кем выдан')
    date = forms.DateField(widget=forms.SelectDateWidget(years=(range(datetime.now().year, 1930, -1))), required=False,
                           label='Дата выдачи')
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=(range(datetime.now().year, 1930, -1))),
                                    required=False, label='Дата рождения')
    department_code = forms.CharField(max_length=20, required=False, label='Код подразделения')


class ContactForm(forms.Form):
    type_of_contact = forms.ModelChoiceField(WorkerContactType.objects.all(), label='Тип контакта')
    contact = forms.CharField(max_length=50, label='Контактные данные')


class OrganizationFileForm(forms.ModelForm):
    class Meta:
        model = OrganizationFile
        fields = ['title', 'organization', 'file', 'description']