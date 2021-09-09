import factory

from app_organizations.models import Organization, Worker


class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Organization

    title = factory.Sequence(lambda n: f'Организация #{n}')
    title_en = factory.Sequence(lambda n: f'Organization #{n}')
    position = factory.Sequence(lambda n: 'Должность')
    position_en = factory.Sequence(lambda n: 'Position')
    appeal = factory.Sequence(lambda n: 'Г-н')
    appeal_en = factory.Sequence(lambda n: 'Mr')
    name = factory.Sequence(lambda n: f'Имя {n}')
    second_name = factory.Sequence(lambda n: f'Отчество {n}')
    last_name = factory.Sequence(lambda n: f'Фамилия {n}')
    name_en = factory.Sequence(lambda n: f'Name {n}')
    second_name_en = factory.Sequence(lambda n: f'Second name {n}')
    last_name_en = factory.Sequence(lambda n: f'Last name {n}')
    legal_address = factory.Sequence(lambda n: f'Юр. адрес {n}')
    legal_address_en = factory.Sequence(lambda n: f'Legal address {n}')
    actual_address = factory.Sequence(lambda n: f'Фактический адрес {n}')
    tin = factory.Sequence(lambda n: f'24123{n}')
    kpp = factory.Sequence(lambda n: f'52344{n}')
    pprnie = factory.Sequence(lambda n: f'46542345{n}')
    registration = factory.Sequence(lambda n: f'Документ №{n}')
    registration_en = factory.Sequence(lambda n: f'Document #{n}')
    requisites = factory.Sequence(lambda n: f'Реквизиты №{n}')
    requisites_en = factory.Sequence(lambda n: f'Requisites #{n}')


class WorkerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Worker

    name = 'Иван'
    second_name = 'Иванович'
    last_name = 'Иванов'
    position = 'Тестировщик'
    organization = factory.SubFactory(OrganizationFactory)
