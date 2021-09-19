from django.contrib.auth.models import User
from django.db import models

from app_crm.models import Contractor, Lead
from app_documents.models import Contract, Order, OrderWithoutContract
from app_organizations.models import Organization, Worker
from app_storage.models import Product, Store


class TaskStatus(models.Model):
    title = models.CharField('Название', max_length=100)

    class Meta:
        verbose_name = 'Статус задачи'
        verbose_name_plural = 'Статусы задач'

    def __str__(self):
        return self.title


class Task(models.Model):
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', max_length=4000)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Постановщик')
    created = models.DateTimeField('Дата и время создания', auto_created=True)
    deadline = models.DateTimeField('Крайний срок', blank=True, null=True)
    status = models.ForeignKey(TaskStatus, on_delete=models.CASCADE, verbose_name='Статус задачи')
    tags = models.CharField('Тэги', max_length=200)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.title


class TaskResponsible(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE, verbose_name='Задача')
    responsible = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Ответственный')

    class Meta:
        verbose_name = 'Исполнитель задачи'
        verbose_name_plural = 'Исполнители задач'

    def __str__(self):
        return self.responsible


class TaskCoexecutor(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name='Задача')
    coexecutor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Соисполнитель')

    class Meta:
        verbose_name = 'Соисполнитель задачи'
        verbose_name_plural = 'Соисполнители задач'

    def __str__(self):
        return self.coexecutor


class TaskRef(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name='Задача', related_name='subjects_references')
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE, verbose_name='Контрагент',
                                   related_name='tasks_references', blank=True, null=True)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, verbose_name='Лид', related_name='tasks_references',
                             blank=True, null=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, verbose_name='Договор',
                                 related_name='tasks_references', blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ', related_name='tasks_references',
                              blank=True, null=True)
    order_wc = models.ForeignKey(OrderWithoutContract, on_delete=models.CASCADE, verbose_name='Заказ без договора',
                                 related_name='tasks_references', blank=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name='Организация',
                                     related_name='tasks_references', blank=True, null=True)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, verbose_name='Сотрудник',
                               related_name='tasks_references', blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукция',
                                related_name='tasks_references', blank=True, null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, verbose_name='Склад', related_name='tasks_references',
                              blank=True, null=True)

    class Meta:
        verbose_name = 'Ссылка задачи'
        verbose_name_plural = 'Ссылки задач'

    def __str__(self):
        if self.contractor:
            return self.contractor
        elif self.lead:
            return self.lead
        elif self.contract:
            return self.contract
        elif self.order:
            return self.order
        elif self.order_wc:
            return self.order_wc
        elif self.organization:
            return self.organization
        elif self.product:
            return self.product
        elif self.worker:
            return self.worker
        elif self.store:
            return self.store
        else:
            return 'Без основания'



