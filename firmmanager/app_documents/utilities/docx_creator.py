import os
from datetime import datetime
from decimal import Decimal
from pathlib import Path

import pymorphy2
from docxtpl import DocxTemplate

from app_storage.models import ProductStoreOrderBooking


class ContractCreator:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    def __init__(self, context):
        self.template = os.path.join(self.BASE_DIR, 'static', 'app_documents', 'layouts', 'contract_template.docx')
        self.output_file_path = os.path.join(self.BASE_DIR, 'static', 'app_documents', 'layouts', 'contract.docx')
        self.contract = context

    def create_contract(self):
        doc = DocxTemplate(self.template)
        context = {
            'number': self.contract.number,
            'created': self.contract.created,
            'created_year': self.get_created_year(),
            'client': {
                'title': self.contract.contractor.title,
                'position': self.contract.contractor.position,
                'position_en': self.contract.contractor.position_en,
                'name': self.contract.contractor.name,
                'second_name': self.contract.contractor.second_name,
                'last_name': self.contract.contractor.last_name,
                'legal_address': self.contract.contractor.legal_address,
                'requisites': self.contract.contractor.requisites,
                'initials': self.get_contractor_initials(),
            },
            'organization': {
                'title': self.contract.organization.title,
                'title_en': self.contract.organization.title_en,
                'appeal': self.contract.organization.appeal,
                'appeal_en': self.contract.organization.appeal_en,
                'name': self.contract.organization.name,
                'name_en': self.contract.organization.name_en,
                'second_name': self.contract.organization.second_name,
                'second_name_en': self.contract.organization.second_name_en,
                'last_name': self.contract.organization.last_name,
                'last_name_en': self.contract.organization.last_name_en,
                'word_ending': self.get_word_ending(),
                'registration': self.contract.organization.registration,
                'registration_en': self.contract.organization.registration_en,
                'legal_address': self.contract.organization.legal_address,
                'legal_address_en': self.contract.organization.legal_address_en,
                'tin': self.contract.organization.tin,
                'pprnie': self.contract.organization.pprnie,
                'requisites': self.contract.organization.requisites,
                'requisites_en': self.contract.organization.requisites_en,
                'position': self.get_position(),
                'position_en': self.contract.organization.position_en,
            },
            'currency': {
                'title': self.contract.currency.title,
                'char_code': self.contract.currency.char_code,
            }
        }
        doc.render(context)
        doc.save(self.output_file_path)

    def get_word_ending(self):
        if self.contract.organization.appeal[:-1] != 'а':
            return 'его'
        else:
            return 'ую'

    def get_contractor_initials(self):
        return f'{self.contract.contractor.name[:1]}. {self.contract.contractor.second_name[:1]}.'

    def get_created_year(self):
        created_year = self.contract.created.strftime('%Y')
        return created_year

    def get_position(self):
        morph = pymorphy2.MorphAnalyzer()
        position_raw = morph.parse(self.contract.organization.position)[0]
        position = position_raw.inflect({'gent'})
        print(position.word)
        return position.word


class SpecificationCreator:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    def __init__(self, context):
        self.template = os.path.join(self.BASE_DIR, 'static', 'app_documents', 'layouts', 'specification_template.docx')
        self.output_file_path = os.path.join(self.BASE_DIR, 'static', 'app_documents', 'layouts', 'specification.docx')
        self.order = context

    def create_specification(self):
        doc = DocxTemplate(self.template)
        context = {
            'number': self.order.number,
            'payment_conditions': {
                'description': self.order.payment_conditions.description,
                'description_en': self.order.payment_conditions.description_en
            },
            'current_date': self.order.created,
            'delivery_conditions':
                {
                    'title': self.order.delivery_conditions.title,
                },
            'delivery_time': self.order.delivery_time,
            'contract': {
                'number': self.order.contract.number,
                'created': self.order.contract.created,
                'created_year': self.get_created_year(),
                'client': {
                    'title': self.order.contract.contractor.title,
                    'appeal_en': self.order.contract.contractor.appeal_en,
                    'position': self.order.contract.contractor.position,
                    'position_en': self.order.contract.contractor.position_en,
                    'name': self.order.contract.contractor.name,
                    'second_name': self.order.contract.contractor.second_name,
                    'last_name': self.order.contract.contractor.last_name,
                    'legal_address': self.order.contract.contractor.legal_address,
                    'requisites': self.order.contract.contractor.requisites,
                    'initials': self.get_contractor_initials(),
                },
                'organization': {
                    'title': self.order.contract.organization.title,
                    'title_en': self.order.contract.organization.title_en,
                    'appeal': self.order.contract.organization.appeal,
                    'appeal_en': self.order.contract.organization.appeal_en,
                    'name': self.order.contract.organization.name,
                    'name_en': self.order.contract.organization.name_en,
                    'second_name': self.order.contract.organization.second_name,
                    'second_name_en': self.order.contract.organization.second_name_en,
                    'last_name': self.order.contract.organization.last_name,
                    'last_name_en': self.order.contract.organization.last_name_en,
                    'registration': self.order.contract.organization.registration,
                    'registration_en': self.order.contract.organization.registration_en,
                    'legal_address': self.order.contract.organization.legal_address,
                    'legal_address_en': self.order.contract.organization.legal_address_en,
                    'tin': self.order.contract.organization.tin,
                    'pprnie': self.order.contract.organization.pprnie,
                    'requisites': self.order.contract.organization.requisites,
                    'requisites_en': self.order.contract.organization.requisites_en,
                    'position': self.get_position(),
                    'position_en': self.order.contract.organization.position_en,
                    'initials': self.get_organization_initials(),
                    'initials_en': self.get_organization_english_initials(),
                },
                'currency': {
                    'title': self.order.contract.currency.title,
                    'char_code': self.order.contract.currency.char_code,
                }
            },
            'currency_total_sum': round(self.order.total_sum * (
                    self.order.contract.currency.nominal / self.order.contract.currency.cost), 1),
            'booked_products': []
        }
        for booked_product in ProductStoreOrderBooking.objects.all().filter(order=self.order):
            context['booked_products'].append({
                'product': {
                    'article': booked_product.product.number,
                    'description': booked_product.product.description,
                    'description_en': booked_product.product.description_en,
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

    def get_organization_english_initials(self):
        return f'{self.order.contract.organization.name_en[:1]}. {self.order.contract.organization.second_name_en[:1]}.'

    def get_created_year(self):
        created_year = self.order.contract.created.strftime('%Y')
        return created_year

    def get_position(self):
        morph = pymorphy2.MorphAnalyzer()
        position_raw = morph.parse(self.order.contract.organization.position)[0]
        position = position_raw.inflect({'gent'})
        print(position.word)
        return position.word


class InvoiceCreator:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    def __init__(self, context):
        self.template = os.path.join(self.BASE_DIR, 'static', 'app_documents', 'layouts', 'invoice_template.docx')
        self.output_file_path = os.path.join(self.BASE_DIR, 'static', 'app_documents', 'layouts', 'invoice.docx')
        self.order = context

    def create_invoice(self):
        doc = DocxTemplate(self.template)
        context = {
            'number': self.order.number,
            'payment_conditions': {
                'description': self.order.payment_conditions.description,
                'description_en': self.order.payment_conditions.description_en
            },
            'current_date': datetime.now().date(),
            'delivery_conditions':
                {
                    'title': self.order.delivery_conditions.title,
                },
            'delivery_time': self.order.delivery_time,
            'contract': {
                'number': self.order.contract.number,
                'created': self.order.contract.created,
                'created_year': self.get_created_year(),
                'client': {
                    'title': self.order.contract.contractor.title,
                    'appeal_en': self.order.contract.contractor.appeal_en,
                    'position': self.order.contract.contractor.position,
                    'position_en': self.order.contract.contractor.position_en,
                    'name': self.order.contract.contractor.name,
                    'second_name': self.order.contract.contractor.second_name,
                    'last_name': self.order.contract.contractor.last_name,
                    'tel': self.order.contract.contractor.tel,
                    'legal_address': self.order.contract.contractor.legal_address,
                    'requisites': self.order.contract.contractor.requisites,
                    'initials': self.get_contractor_initials(),
                },
                'organization': {
                    'title': self.order.contract.organization.title,
                    'title_en': self.order.contract.organization.title_en,
                    'appeal': self.order.contract.organization.appeal,
                    'appeal_en': self.order.contract.organization.appeal_en,
                    'name': self.order.contract.organization.name,
                    'name_en': self.order.contract.organization.name_en,
                    'second_name': self.order.contract.organization.second_name,
                    'second_name_en': self.order.contract.organization.second_name_en,
                    'last_name': self.order.contract.organization.last_name,
                    'last_name_en': self.order.contract.organization.last_name_en,
                    'registration': self.order.contract.organization.registration,
                    'registration_en': self.order.contract.organization.registration_en,
                    'legal_address': self.order.contract.organization.legal_address,
                    'legal_address_en': self.order.contract.organization.legal_address_en,
                    'tin': self.order.contract.organization.tin,
                    'pprnie': self.order.contract.organization.pprnie,
                    'requisites': self.order.contract.organization.requisites,
                    'requisites_en': self.order.contract.organization.requisites_en,
                    'position': self.get_position(),
                    'position_en': self.order.contract.organization.position_en,
                    'initials': self.get_organization_initials(),
                    'initials_en': self.get_organization_english_initials(),
                },
                'currency': {
                    'title': self.order.contract.currency.title,
                    'char_code': self.order.contract.currency.char_code,
                }
            },
            'currency_total_sum': round(self.order.total_sum * (
                    self.order.contract.currency.nominal / self.order.contract.currency.cost), 1),
            'booked_products': []
        }
        for i, booked_product in enumerate(ProductStoreOrderBooking.objects.all().filter(order=self.order)):
            context['booked_products'].append({
                'tr_number': i,
                'product': {
                    'article': booked_product.product.number,
                    'description': booked_product.product.description,
                    'description_en': booked_product.product.description_en,
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

    def get_organization_english_initials(self):
        return f'{self.order.contract.organization.name_en[:1]}. {self.order.contract.organization.second_name_en[:1]}.'

    def get_created_year(self):
        created_year = self.order.contract.created.strftime('%Y')
        return created_year

    def get_position(self):
        morph = pymorphy2.MorphAnalyzer()
        position_raw = morph.parse(self.order.contract.organization.position)[0]
        position = position_raw.inflect({'gent'})
        print(position.word)
        return position.word

