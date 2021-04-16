import os
from decimal import Decimal
from pathlib import Path

import pymorphy2
from docxtpl import DocxTemplate

from app_storage.models import ProductStoreSpecificationBooking


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
                'description': self.order.payment_conditions.description
            },
            'delivery_conditions':
                {
                    'title': self.order.delivery_conditions.title,
                    'time_of_delivery': self.order.delivery_time
                },
            'contract': {
                'number': self.order.contract.number,
                'client': {
                    'title': self.order.contract.contractor.title,
                    'position': self.order.contract.contractor.position,
                    'name': self.order.contract.contractor.name,
                    'last_name': self.order.contract.contractor.last_name,
                    'address': self.order.contract.contractor.country,
                },
                'organization': {
                    'title': self.order.contract.organization.title,
                    'registration': self.order.contract.organization.registration,
                    'address': self.order.contract.organization.legal_address,
                    'tin': self.order.contract.organization.tin,
                    'pprnie': self.order.contract.organization.pprnie,
                },
                'currency': {
                    'title': self.order.contract.currency.title,
                }
            },
            'booked_products': []
        }
        total_sum = Decimal(0)
        for booked_product in ProductStoreSpecificationBooking.objects.all().filter(order=self.order):
            context['booked_products'].append({
                'product': {
                    'title': booked_product.product.type_of_product,
                    'color': booked_product.product.color,
                    'model': booked_product.product.model,
                    'cost': booked_product.product.cost,
                    'description': booked_product.product.description,
                },
                'total_sum': booked_product.sum,
                'quantity': booked_product.quantity,
            })
            total_sum += Decimal(booked_product.sum)
        context['total_sum'] = total_sum
        doc.render(context)
        doc.save(self.output_file_path)


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
                'description': self.order.payment_conditions.description
            },
            'delivery_conditions':
                {
                    'title': self.order.delivery_conditions.title,
                    'time_of_delivery': self.order.delivery_time,
                    'description': self.order.delivery_conditions.description
                },
            'contract': {
                'created': self.order.contract.created,
                'number': self.order.contract.number,
                'client': {
                    'title': self.order.contract.contractor.title,
                    'position': self.order.contract.contractor.position,
                    'name': self.order.contract.contractor.name,
                    'last_name': self.order.contract.contractor.last_name,
                    'address': self.order.contract.contractor.country,
                },
                'organization': {
                    'title': self.order.contract.organization.title,
                    'registration': self.order.contract.organization.registration,
                    'address': self.order.contract.organization.legal_address,
                    'tin': self.order.contract.organization.tin,
                    'pprnie': self.order.contract.organization.pprnie,
                },
                'currency': {
                    'title': self.order.contract.currency.title,
                }

            },
            'shipment_mark': self.order.shipment_mark,
            'loading_place': self.order.delivery_address,
            'booked_products': []
        }
        total_sum = Decimal(0)
        for i, booked_product in enumerate(ProductStoreSpecificationBooking.objects.all().filter(order=self.order)):
            context['booked_products'].append({
                'number': i + 1,
                'product': {
                    'title': booked_product.product.type_of_product,
                    'color': booked_product.product.color,
                    'model': booked_product.product.model,
                    'cost': booked_product.product.cost,
                    'description': booked_product.product.description,
                },
                'total_sum': booked_product.sum,
                'quantity': booked_product.quantity,
            })
            total_sum += Decimal(booked_product.sum)
        context['total_sum'] = total_sum
        doc.render(context)
        doc.save(self.output_file_path)
