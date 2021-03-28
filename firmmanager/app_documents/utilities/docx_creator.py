import os
from decimal import Decimal
from pathlib import Path

from docxtpl import DocxTemplate

from app_storage.models import ProductStoreBooking


class ContractCreator:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    def __init__(self, context):
        self.template = os.path.join(self.BASE_DIR, 'static', 'app_documents', 'layouts', 'contract_template.docx')
        self.output_file_path = os.path.join(self.BASE_DIR, 'static', 'app_documents', 'layouts', 'contract.docx')
        self.contract = context

    def create_contract(self):
        doc = DocxTemplate(self.template)
        context = {
            'number': self.contract.pk,
            'created': self.contract.created,
            'client': {
                'title': self.contract.contractor.title,
                'position': self.contract.contractor.position,
                'name': self.contract.contractor.name,
                'last_name': self.contract.contractor.last_name,
                'address': self.contract.contractor.country,
            },
            'organization': {
                'title': self.contract.organization.title,
                'registration': self.contract.organization.registration,
                'address': self.contract.organization.address,
                'tin': self.contract.organization.tin,
                'pprnie': self.contract.organization.pprnie,
                'banks': []
            }
        }
        doc.render(context)
        doc.save(self.output_file_path)


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
                    'time_of_delivery': self.order.delivery_conditions.delivery_time
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
                    'address': self.order.contract.organization.address,
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
        for booked_product in ProductStoreBooking.objects.all().filter(order=self.order):
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
                    'time_of_delivery': self.order.delivery_conditions.delivery_time,
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
                    'address': self.order.contract.organization.address,
                    'tin': self.order.contract.organization.tin,
                    'pprnie': self.order.contract.organization.pprnie,
                },
                'currency': {
                    'title': self.order.contract.currency.title,
                }

            },
            'shipment_mark': self.order.shipment_mark,
            'loading_place': self.order.loading_place,
            'booked_products': []
        }
        total_sum = Decimal(0)
        for i, booked_product in enumerate(ProductStoreBooking.objects.all().filter(order=self.order)):
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
