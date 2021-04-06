from django.contrib.auth.models import User
from django.db import models


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
    title = models.CharField('Наименование', max_length=50, unique=True)
    status = models.ForeignKey(ContractorStatus, on_delete=models.SET_NULL, null=True, verbose_name='Статус')
    type_of_contractor = models.ForeignKey(TypeOfContractor, on_delete=models.SET_NULL, null=True,
                                           verbose_name='Тип контрагента')
    field_of_activity = models.ForeignKey(FieldOfActivity, on_delete=models.SET_NULL, null=True,
                                          verbose_name='Сфера деятельности')
    position = models.CharField('Должность', max_length=30)
    position_en = models.CharField('Должность(англ)', max_length=30, blank=True)
    appeal = models.CharField('Обращение', max_length=30, default='г-н')
    appeal_en = models.CharField('Обращение(англ)', max_length=30, default='Mr.')
    name = models.CharField('Имя', max_length=30)
    second_name = models.CharField('Отчество', max_length=30, blank=True)
    last_name = models.CharField('Фамилия', max_length=30)
    country = models.CharField('Страна', max_length=30)
    legal_address = models.CharField('Юр. адрес', max_length=200)
    actual_address = models.CharField('Фактический адрес', max_length=200, blank=True)
    requisites = models.TextField('Реквизиты', max_length=500)
    to_delete = models.BooleanField('К удалению', default=False)
    responsible = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name = 'Контрагент'
        verbose_name_plural = 'Контрагент'

    def __str__(self):
        return f'{self.title} - {self.country}'


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


class ContactType(models.Model):
    title = models.CharField('Название', max_length=100)

    class Meta:
        verbose_name = 'Тип контакта'
        verbose_name_plural = 'Типы контактов'

    def __str__(self):
        return self.title


class ContactPerson(models.Model):
    name = models.CharField('Имя', max_length=30)
    second_name = models.CharField('Отчество', max_length=30, blank=True)
    last_name = models.CharField('Фамилия', max_length=30)
    position = models.CharField('Должность', max_length=30)
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE, blank=True, null=True,
                                   verbose_name='Контрагент')
    to_delete = models.BooleanField('К удалению', default=False)

    class Meta:
        verbose_name = 'Контактное лицо'
        verbose_name_plural = 'Контактные лица'


class Contact(models.Model):
    contact_person = models.ForeignKey(ContactPerson, on_delete=models.CASCADE, blank=True, null=True,
                                       verbose_name='Контактое лицо')
    type_of_contact = models.ForeignKey(ContactType, on_delete=models.CASCADE, verbose_name='Вид контакта')
    contact = models.CharField('Контактные данные', max_length=50)

    class Meta:
        verbose_name = 'Контакт контактного лица'
        verbose_name_plural = 'Контакты контактных лиц'

    def __str__(self):
        return f'{self.type_of_contact} {self.contact}'
