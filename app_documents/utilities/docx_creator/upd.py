import os
from datetime import datetime
from pathlib import Path

import pymorphy2
from docxtpl import DocxTemplate

from app_crm.models import ContractorRequisites
from app_documents.models import Order
from app_storage.models import ProductStoreOrderBooking, ProductStoreOrderWCBooking


class UpdCreator:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

    def __init__(self, context: Order):
        if context.created.year == 2021 and context.created.month < 7:
            template_path = os.path.join('russian', 'upd_template.docx')
        else:
            template_path = os.path.join('russian', 'upd_template_2021.docx')
        self.template = os.path.join(self.BASE_DIR, 'static', 'app_documents', 'layouts', template_path)
        self.output_file_path = os.path.join(self.BASE_DIR, 'static', 'app_documents', 'tmp', 'upd.docx')
        self.order = context

    def create_upd(self):
        doc = DocxTemplate(self.template)
        context = {
            'order_id': self.order.id,
            'current_date': datetime.now().strftime('%d.%m.%Y'),
            'organization': {
                'title': self.order.contract.organization.title,
                'appeal': self.order.contract.organization.appeal,
                'name': self.order.contract.organization.name,
                'second_name': self.order.contract.organization.second_name,
                'last_name': self.order.contract.organization.last_name,
                'registration': self.order.contract.organization.registration,
                'legal_address': self.order.contract.organization.legal_address,
                'tin': self.order.contract.organization.tin,
                'tin_and_kpp': f'{self.order.contract.organization.tin}/{self.order.contract.organization.kpp}',
                'pprnie': self.order.contract.organization.pprnie,
                'position': self.get_organization_position(),
                'initials': self.get_organization_initials(),
            },
            'contractor': {
                'title': self.order.contract.contractor.title,
                'position': self.get_contractor_position(),
                'name': self.order.contract.contractor.name,
                'last_name': self.order.contract.contractor.last_name,
                'legal_address': self.order.contract.contractor.legal_address,
                'requisites': self.order.contract.contractor.requisites,
                'initials': self.get_contractor_initials(),
                'tin_and_kpp': self.get_contractor_tin_and_kpp(),
            },
            'currency_total_sum': round(self.order.total_sum * (
                    self.order.contract.currency.nominal / self.order.contract.currency.cost), 1),
            'booked_products': [],
            'date': {
                'day': datetime.now().day,
                'month': self.get_russian_month(datetime.now().month),
                'year': datetime.now().year,
            },
            'shipping_document': self.get_shipping_document(),
        }
        for i, booked_product in enumerate(ProductStoreOrderBooking.objects.all().filter(order=self.order)):
            context['booked_products'].append({
                'tr_number': str(i + 1),
                'product': {
                    'article': booked_product.product.number,
                    'description': booked_product.product.description,
                },
                'total_sum': round(booked_product.total_sum * (
                        self.order.contract.currency.nominal / self.order.contract.currency.cost), 1),
                'total_price': round(booked_product.total_price * (
                        self.order.contract.currency.nominal / self.order.contract.currency.cost), 1),
                'quantity': booked_product.quantity,
            })
        doc.render(context)
        doc.save(self.output_file_path)

    def get_contractor_initials(self):
        return f'{self.order.contract.contractor.name[:1]}. {self.order.contract.contractor.second_name[:1]}.'

    def get_organization_initials(self):
        return f'{self.order.contract.organization.name[:1]}. {self.order.contract.organization.second_name[:1]}.'

    def get_organization_position(self):
        morph = pymorphy2.MorphAnalyzer()
        position = ''
        for raw_word in self.order.contract.organization.position.split(' '):
            new_word = morph.parse(raw_word)[0]
            position += new_word.inflect({'gent'}).word + ' '
        return position

    def get_contractor_position(self):
        morph = pymorphy2.MorphAnalyzer()
        position = ''
        for raw_word in self.order.contract.contractor.position.split(' '):
            new_word = morph.parse(raw_word)[0]
            position += new_word.inflect({'gent'}).word + ' '
        return position

    def get_russian_month(self, month):
        russian_months = {1: 'Января', 2: 'Ферваля', 3: 'Марта', 4: 'Апреля', 5: 'Мая', 6: 'Июня',
                          7: 'Июля', 8: 'Августа', 9: 'Сентября', 10: 'Октрября', 11: 'Ноября', 12: 'Декабря'}
        return russian_months[month]

    def get_contractor_tin_and_kpp(self):
        requisites = ContractorRequisites.objects.get(contractor=self.order.contract.contractor)
        return f'{requisites.tin}/{requisites.kpp}'

    def get_shipping_document(self):
        products = len(ProductStoreOrderBooking.objects.all().filter(order=self.order))
        if products == 1:
            return f'№ п/п 1 № {self.order.id} от {self.order.created}'
        else:
            return f'№ п/п 1-{products} № {self.order.id} от {self.order.created}'


class UpdWithoutContractCreator:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

    def __init__(self, context, template):
        self.template = os.path.join(self.BASE_DIR, 'static', 'app_documents', 'layouts', template)
        self.output_file_path = os.path.join(self.BASE_DIR, 'static', 'app_documents', 'tmp', 'upd.docx')
        self.order = context

    def create_upd(self):
        print(os.path.isfile(self.template))
        doc = DocxTemplate(self.template)
        context = {
            'order_id': self.order.id,
            'current_date': datetime.now().strftime('%d.%m.%Y'),
            'organization': {
                'title': self.order.organization.title,
                'appeal': self.order.organization.appeal,
                'name': self.order.organization.name,
                'second_name': self.order.organization.second_name,
                'last_name': self.order.organization.last_name,
                'registration': self.order.organization.registration,
                'legal_address': self.order.organization.legal_address,
                'tin': self.order.organization.tin,
                'tin_and_kpp': f'{self.order.organization.tin}/{self.order.organization.kpp}',
                'pprnie': self.order.organization.pprnie,
                'position': self.get_organization_position(),
                'initials': self.get_organization_initials(),
            },
            'contractor': {
                'title': self.order.contractor.title,
                'position': self.get_contractor_position(),
                'name': self.order.contractor.name,
                'last_name': self.order.contractor.last_name,
                'legal_address': self.order.contractor.legal_address,
                'requisites': self.order.contractor.requisites,
                'initials': self.get_contractor_initials(),
                'tin_and_kpp': self.get_contractor_tin_and_kpp(),
            },
            'currency_total_sum': round(self.order.total_sum * (
                    self.order.currency.nominal / self.order.currency.cost), 1),
            'booked_products': [],
            'date': {
                'day': datetime.now().day,
                'month': self.get_russian_month(datetime.now().month),
                'year': datetime.now().year,
            },
            'shipping_document': self.get_shipping_document(),
        }
        for i, booked_product in enumerate(ProductStoreOrderWCBooking.objects.all().filter(
                order=self.order)):
            context['booked_products'].append({
                'tr_number': str(i + 1),
                'product': {
                    'article': booked_product.product.number,
                    'description': booked_product.product.description,
                },
                'total_sum': round(booked_product.total_sum * (
                        self.order.currency.nominal / self.order.currency.cost), 1),
                'total_price': round(booked_product.total_price * (
                        self.order.currency.nominal / self.order.currency.cost), 1),
                'quantity': booked_product.quantity,
            })
        doc.render(context)
        doc.save(self.output_file_path)

    def get_contractor_initials(self):
        return f'{self.order.contractor.name[:1]}. {self.order.contractor.second_name[:1]}.'

    def get_organization_initials(self):
        return f'{self.order.organization.name[:1]}. {self.order.organization.second_name[:1]}.'

    def get_organization_position(self):
        morph = pymorphy2.MorphAnalyzer()
        position = ''
        for raw_word in self.order.organization.position.split(' '):
            new_word = morph.parse(raw_word)[0]
            position += new_word.inflect({'gent'}).word + ' '
        return position

    def get_contractor_position(self):
        morph = pymorphy2.MorphAnalyzer()
        position = ''
        for raw_word in self.order.contractor.position.split(' '):
            new_word = morph.parse(raw_word)[0]
            position += new_word.inflect({'gent'}).word + ' '
        return position

    def get_russian_month(self, month):
        russian_months = {1: 'Января', 2: 'Ферваля', 3: 'Марта', 4: 'Апреля', 5: 'Мая', 6: 'Июня',
                          7: 'Июля', 8: 'Августа', 9: 'Сентября', 10: 'Октрября', 11: 'Ноября', 12: 'Декабря'}
        return russian_months[month]

    def get_contractor_tin_and_kpp(self):
        requisites = ContractorRequisites.objects.get(contractor=self.order.contractor)
        return f'{requisites.tin}/{requisites.kpp}'

    def get_shipping_document(self):
        products = len(ProductStoreOrderWCBooking.objects.all().filter(order=self.order))
        if products == 1:
            return f'№ п/п 1 № {self.order.id} от {self.order.created}'
        else:
            return f'№ п/п 1-{products} № {self.order.id} от {self.order.created}'
