import os
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

from app_organizations.models import UploadToPathAndRename
from firmmanager.settings import MEDIA_ROOT


class TypeOfContractor(models.Model):
    title = models.CharField('Наименование', max_length=40, unique=True)

    class Meta:
        verbose_name = 'Тип контрагентов'
        verbose_name_plural = 'Типы контрагентов'

    def __str__(self):
        return self.title


class FieldOfActivity(models.Model):
    title = models.CharField('Наименование', max_length=60, unique=True)

    class Meta:
        verbose_name = 'Сфера деятельности'
        verbose_name_plural = 'Сферы деятельности'

    def __str__(self):
        return self.title


class ContractorStatus(models.Model):
    title = models.CharField('Название', max_length=50, unique=True)
    description = models.CharField('Описание', max_length=150, blank=True, null=True)

    class Meta:
        verbose_name = 'Статус контрагентов'
        verbose_name_plural = 'Статусы контрагентов'

    def __str__(self):
        return self.title


class Contractor(models.Model):
    title = models.CharField('Наименование', max_length=150)
    status = models.ForeignKey(ContractorStatus, on_delete=models.SET_NULL, null=True, verbose_name='Статус')
    type_of_contractor = models.ForeignKey(TypeOfContractor, on_delete=models.SET_NULL, null=True,
                                           verbose_name='Тип контрагента')
    field_of_activity = models.ForeignKey(FieldOfActivity, on_delete=models.SET_NULL, null=True,
                                          verbose_name='Сфера деятельности')
    position = models.CharField('Должность', max_length=30)
    position_en = models.CharField('Должность(англ)', max_length=30, blank=True)
    appeal = models.CharField('Обращение', max_length=30, default='г-н')
    appeal_en = models.CharField('Обращение(англ)', max_length=30, default='Mr.', blank=True)
    name = models.CharField('Имя', max_length=30)
    second_name = models.CharField('Отчество', max_length=30, blank=True)
    last_name = models.CharField('Фамилия', max_length=30)
    country = models.CharField('Страна', max_length=30)
    tel = models.CharField('Основной номер телефона', max_length=20)
    legal_address = models.CharField('Юр. адрес', max_length=200)
    actual_address = models.CharField('Фактический адрес', max_length=200, blank=True)
    requisites = models.TextField('Реквизиты', max_length=1000, blank=True, null=True)
    to_delete = models.BooleanField('К удалению', default=False)
    tag = models.CharField('Теги', max_length=1000, blank=True, null=True)
    responsible = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name = 'Контрагент'
        verbose_name_plural = 'Контрагент'

    def __str__(self):
        return f'{self.title} - {self.country}'


class ContractorRequisites(models.Model):
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE, verbose_name='Контрагент')
    short_title = models.CharField('Сокр. наименование', max_length=50)
    mailing_address = models.CharField('Почтовый адрес', max_length=200)
    tin = models.CharField('ИНН(TIN)', max_length=12)
    kpp = models.CharField('КПП', max_length=12)
    pprnie = models.CharField('ОГРН(ИП)', max_length=15)
    checking_account = models.CharField('Расчетный счет', max_length=24)
    correspondent_account = models.CharField('Корреспондентский счет', max_length=24)
    bank_bik = models.CharField('БИК Банка', max_length=9)
    bank_title = models.CharField('Банк', max_length=200)

    class Meta:
        verbose_name = 'Реквизиты контрагента'
        verbose_name_plural = 'Реквизиты контрагентов'

    def __str__(self):
        return f'{self.contractor} {self.tin}/{self.pprnie}'


class ContractorComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField('Текст комментария', max_length=500)
    created = models.DateTimeField('Дата создания', auto_now=True)
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE, verbose_name='Контрагент')

    class Meta:
        verbose_name = 'Комментарий к контрагенту'
        verbose_name_plural = 'Комментарии к контрагенту'

    def __str__(self):
        return f'{self.user} - {self.text}'


class ContactPersonContactType(models.Model):
    title = models.CharField('Название', max_length=100)

    class Meta:
        verbose_name = 'Тип контакта'
        verbose_name_plural = 'Типы контактов'

    def __str__(self):
        return self.title


class ContractorContactPerson(models.Model):
    name = models.CharField('Имя', max_length=30)
    second_name = models.CharField('Отчество', max_length=30, blank=True)
    last_name = models.CharField('Фамилия', max_length=30)
    position = models.CharField('Должность', max_length=30)
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE, blank=True, null=True,
                                   verbose_name='Контрагент')
    tag = models.CharField('Теги', max_length=1000, blank=True, null=True)
    serial_number = models.CharField('Серия', max_length=4, blank=True, null=True)
    number = models.CharField('Номер', max_length=6, blank=True, null=True)
    issued_by = models.CharField('Кем выдан', max_length=100, blank=True, null=True)
    date = models.DateField('Дата выдачи', default=datetime(year=1970, month=1, day=1), blank=True, null=True)
    date_of_birth = models.DateField('Дата рождения', default=datetime(year=1970, month=1, day=1), blank=True,
                                     null=True)
    department_code = models.CharField('Код подразделения', max_length=20, blank=True, null=True)
    to_delete = models.BooleanField('К удалению', default=False)

    class Meta:
        verbose_name = 'Контактное лицо'
        verbose_name_plural = 'Контактные лица'

    def __str__(self):
        return f'{self.name} {self.second_name} {self.last_name} - {self.contractor}'


class ContractorContactPersonContact(models.Model):
    contact_person = models.ForeignKey(ContractorContactPerson, on_delete=models.CASCADE, blank=True, null=True,
                                       verbose_name='Контактое лицо')
    type_of_contact = models.ForeignKey(ContactPersonContactType, on_delete=models.CASCADE, verbose_name='Вид контакта')
    contact = models.CharField('Контактные данные', max_length=50)

    class Meta:
        verbose_name = 'Контакт контактного лица контрагента'
        verbose_name_plural = 'Контакты контактных лиц контрагентов'

    def __str__(self):
        return f'{self.type_of_contact} {self.contact}'


class ContractorFileCategory(models.Model):
    title = models.CharField('Название', max_length=100)
    slug = models.CharField('Наимнование для образования ссылки(англ)', max_length=100)

    class Meta:
        verbose_name = 'Категория файлов контрагента'
        verbose_name_plural = 'Категории файлов контрагентов'

    def __str__(self):
        return self.title


class ContractorFile(models.Model):
    title = models.CharField('Название', max_length=100)
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE, verbose_name='Организация')
    file = models.FileField('Файл', upload_to=UploadToPathAndRename(
        os.path.join(MEDIA_ROOT, 'app_organizations', 'organization_files')), max_length=500)
    description = models.TextField('Описание', blank=True)
    category = models.ForeignKey(ContractorFileCategory, on_delete=models.CASCADE, verbose_name='Категория')
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        verbose_name = 'Файл контрагента'
        verbose_name_plural = 'Файлы контрагентов'

    def __str__(self):
        return self.title


class LeadStatus(models.Model):
    title = models.CharField('Название', max_length=50, unique=True)
    description = models.CharField('Описание', max_length=150, blank=True, null=True)

    class Meta:
        verbose_name = 'Статус лида'
        verbose_name_plural = 'Статусы лидов'

    def __str__(self):
        return self.title


class Lead(models.Model):
    title = models.CharField('Наименование', max_length=500)
    status = models.ForeignKey(LeadStatus, on_delete=models.SET_NULL, null=True, verbose_name='Статус')
    field_of_activity = models.ForeignKey(FieldOfActivity, on_delete=models.SET_NULL, null=True,
                                          verbose_name='Сфера деятельности')
    name = models.CharField('Имя', max_length=30)
    second_name = models.CharField('Отчество', max_length=30, blank=True, null=True)
    last_name = models.CharField('Фамилия', max_length=30, blank=True, null=True)
    position = models.CharField('Должность', max_length=30)
    purpose = models.CharField('Цель сотрудничества', max_length=1000)
    tag = models.CharField('Теги', max_length=1000, blank=True, null=True)
    responsible = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    country = models.CharField('Страна', max_length=100)

    class Meta:
        verbose_name = 'Лид'
        verbose_name_plural = 'Лиды'

    def __str__(self):
        return self.title


class LeadComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField('Текст комментария', max_length=500)
    created = models.DateTimeField('Дата создания', auto_now=True)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, verbose_name='Лид')

    class Meta:
        verbose_name = 'Комментарий к лиду'
        verbose_name_plural = 'Комментарии к лидам'

    def __str__(self):
        return f'{self.user} - {self.text}'


class LeadContactPerson(models.Model):
    name = models.CharField('Имя', max_length=30)
    second_name = models.CharField('Отчество', max_length=30, blank=True, null=True)
    last_name = models.CharField('Фамилия', max_length=30)
    position = models.CharField('Должность', max_length=30)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Лид')
    tag = models.CharField('Теги', max_length=1000, blank=True, null=True)
    to_delete = models.BooleanField('К удалению', default=False)

    class Meta:
        verbose_name = 'Контактное лицо лида'
        verbose_name_plural = 'Контактные лица лидов'

    def __str__(self):
        return f'{self.name} {self.second_name} {self.last_name} - {self.lead}'


class LeadContactPersonContact(models.Model):
    contact_person = models.ForeignKey(LeadContactPerson, on_delete=models.CASCADE, blank=True, null=True,
                                       verbose_name='Контактое лицо')
    type_of_contact = models.ForeignKey(ContactPersonContactType, on_delete=models.CASCADE, verbose_name='Вид контакта')
    contact = models.CharField('Контактные данные', max_length=50)

    class Meta:
        verbose_name = 'Контакт контактного лица лида'
        verbose_name_plural = 'Контакты контактных лиц лидов'

    def __str__(self):
        return f'{self.type_of_contact} {self.contact}'
