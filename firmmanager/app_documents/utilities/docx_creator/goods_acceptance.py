import io
import os
from datetime import datetime
from pathlib import Path

import pymorphy2
from docxtpl import DocxTemplate

from app_storage.models import ProductStoreOrderBooking


class GoodsAcceptanceCreator:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

    def __init__(self, context):
        template_path = os.path.join('foreign', 'goods_acceptance_template.docx')
        self.template = os.path.join(self.BASE_DIR, 'static', 'app_documents', 'layouts', template_path)
        self.output_file_path = os.path.join(self.BASE_DIR, 'static', 'app_documents', 'tmp',
                                             'goods_acceptance.docx')
        self.order = context

    def create_goods_acceptance(self):
        doc = DocxTemplate(self.template)
        context = {
            'number': self.order.number,
            'current_date': datetime.now().strftime('%d-%m-%Y'),
            'contract': {
                'number': self.order.contract.number,
                'created': self.order.contract.created.strftime('%d-%m-%Y'),
                'client': {
                    'title': self.order.contract.contractor.title,
                    'appeal_en': self.order.contract.contractor.appeal_en,
                    'position': self.get_contractor_position(),
                    'position_en': self.order.contract.contractor.position_en,
                    'name': self.order.contract.contractor.name,
                    'second_name': self.order.contract.contractor.second_name,
                    'last_name': self.order.contract.contractor.last_name,
                    'legal_address': self.order.contract.contractor.legal_address,
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
                    'position': self.get_organization_position(),
                    'position_en': self.order.contract.organization.position_en,
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
                'tr_number': str(i + 1),
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