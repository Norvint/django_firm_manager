import os
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.deconstruct import deconstructible

from firmmanager.settings import MEDIA_ROOT


class Organization(models.Model):
    title = models.CharField('Наименование', max_length=100)
    title_en = models.CharField('Наименование(англ)', max_length=100, blank=True)
    position = models.CharField('Должность', max_length=30, blank=True)
    position_en = models.CharField('Должность(англ)', max_length=30, blank=True)
    appeal = models.CharField('Обращение', max_length=30, default='г-н', blank=True)
    appeal_en = models.CharField('Обращение(англ)', max_length=30, default='Mr.', blank=True)
    name = models.CharField('Имя', max_length=30, blank=True)
    second_name = models.CharField('Отчество', max_length=30, blank=True)
    last_name = models.CharField('Фамилия', max_length=30, blank=True)
    name_en = models.CharField('Имя(Англ)', max_length=30, blank=True)
    second_name_en = models.CharField('Отчество(Англ)', max_length=30, blank=True)
    last_name_en = models.CharField('Фамилия(Англ)', max_length=30, blank=True)
    legal_address = models.CharField('Юр. адрес', max_length=200)
    legal_address_en = models.CharField('Юр. адрес(англ)', max_length=200, blank=True)
    actual_address = models.CharField('Фактический адрес', max_length=200, blank=True)
    tin = models.CharField('ИНН(TIN)', max_length=12)
    pprnie = models.CharField('ОГРН(ИП)', max_length=15)
    registration = models.CharField('Действующий на основании', max_length=100, blank=True)
    registration_en = models.CharField('Действующий на основании(англ)', max_length=100, blank=True)
    requisites = models.TextField('Банковские реквизиты', max_length=1000)
    requisites_en = models.TextField('Банковские реквизиты(англ)', max_length=1000, blank=True)

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return self.title


class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')
    name = models.CharField('Имя', max_length=30)
    second_name = models.CharField('Отчество', max_length=30)
    last_name = models.CharField('Фамилия', max_length=30)
    position = models.CharField('Должность', max_length=30)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, blank=True, null=True,
                                     verbose_name='Организация')
    serial_number = models.CharField('Серия', max_length=4, blank=True)
    number = models.CharField('Номер', max_length=6, blank=True)
    issued_by = models.CharField('Кем выдан', max_length=100, blank=True)
    date = models.DateField('Дата выдачи', default=datetime(year=1970, month=1, day=1), blank=True, null=True)
    date_of_birth = models.DateField('Дата рождения', default=datetime(year=1970, month=1, day=1), blank=True, null=True)
    department_code = models.CharField('Код подразделения', max_length=20, blank=True)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f'{self.name} {self.second_name} {self.last_name}'


class WorkerContactType(models.Model):
    title = models.CharField('Название', max_length=100)

    class Meta:
        verbose_name = 'Тип контакта'
        verbose_name_plural = 'Типы контактов'

    def __str__(self):
        return self.title


class WorkerContact(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, verbose_name='Сотрудник')
    type_of_contact = models.ForeignKey(WorkerContactType, on_delete=models.CASCADE, verbose_name='Тип контакта')
    contact = models.CharField('Контактные данные', max_length=50)

    class Meta:
        verbose_name = 'Контакт сотрудника'
        verbose_name_plural = 'Контакты сотрудников'

    def __str__(self):
        return f'{self.type_of_contact} {self.contact}'


@deconstructible
class UploadToPathAndRename(object):

    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        filename = f'{datetime.now().strftime("%m%d%Y-%H-%M-%S")}_{filename}'
        return os.path.join(self.sub_path, filename)


class OrganizationFile(models.Model):
    title = models.CharField('Название', max_length=100)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name='Организация')
    file = models.FileField('Файл', upload_to=UploadToPathAndRename(
        os.path.join(MEDIA_ROOT, 'app_organizations', 'organization_files')), max_length=500)
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def __str__(self):
        return self.title
