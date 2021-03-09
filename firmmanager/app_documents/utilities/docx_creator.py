import os
from decimal import Decimal
from pathlib import Path

from docxtpl import DocxTemplate

from app_storage.models import ProductStoreBooking
from app_organizations.models import Bank


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
        for bank in Bank.objects.all().filter(recipient=self.contract.organization):
            context['organization']['banks'].append({
                'title': bank.title,
                'short_code': bank.short_code,
                'payment_account': bank.payment_account,
                'correspondent_account': bank.correspondent_account,
                'address': bank.address,
                'recipient': bank.recipient
            })
        doc.render(context)
        doc.save(self.output_file_path)


class SpecificationCreator:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    def __init__(self, context):
        self.template = os.path.join(self.BASE_DIR, 'static', 'app_documents', 'layouts', 'specification_template.docx')
        self.output_file_path = os.path.join(self.BASE_DIR, 'static', 'app_documents', 'layouts', 'specification.docx')
        self.specification = context

    def create_specification(self):
        doc = DocxTemplate(self.template)
        context = {
            'number': self.specification.number,
            'payment_conditions': {
                'description': self.specification.payment_conditions.description
            },
            'delivery_conditions':
                {
                    'title': self.specification.delivery_conditions.title,
                    'time_of_delivery': self.specification.delivery_conditions.delivery_time
                },
            'contract': {
                'number': self.specification.contract.number,
                'client': {
                    'title': self.specification.contract.contractor.title,
                    'position': self.specification.contract.contractor.position,
                    'name': self.specification.contract.contractor.name,
                    'last_name': self.specification.contract.contractor.last_name,
                    'address': self.specification.contract.contractor.country,
                },
                'organization': {
                    'title': self.specification.contract.organization.title,
                    'registration': self.specification.contract.organization.registration,
                    'address': self.specification.contract.organization.address,
                    'tin': self.specification.contract.organization.tin,
                    'pprnie': self.specification.contract.organization.pprnie,
                },
                'currency': {
                    'title': self.specification.contract.currency.title,
                }
            },
            'booked_products': []
        }
        total_sum = Decimal(0)
        for booked_product in ProductStoreBooking.objects.all().filter(specification=self.specification):
            context['booked_products'].append({
                'product': {
                    'title': booked_product.product.type_of_product,
                    'color': booked_product.product.color,
                    'model': booked_product.product.model,
                    'cost': booked_product.product.cost,
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
        self.invoice = context

    def create_invoice(self):
        doc = DocxTemplate(self.template)
        context = {
            'number': self.invoice.number,
            'specification': {
                'payment_conditions': {
                    'description': self.invoice.specification.payment_conditions.description
                },
                'delivery_conditions':
                    {
                        'title': self.invoice.specification.delivery_conditions.title,
                        'time_of_delivery': self.invoice.specification.delivery_conditions.delivery_time,
                        'description': self.invoice.specification.delivery_conditions.description
                    },
                'contract': {
                    'created': self.invoice.specification.contract.created,
                    'number': self.invoice.specification.contract.number,
                    'client': {
                        'title': self.invoice.specification.contract.contractor.title,
                        'position': self.invoice.specification.contract.contractor.position,
                        'name': self.invoice.specification.contract.contractor.name,
                        'last_name': self.invoice.specification.contract.contractor.last_name,
                        'address': self.invoice.specification.contract.contractor.country,
                        'phone': self.invoice.specification.contract.contractor.phone
                    },
                    'organization': {
                        'title': self.invoice.specification.contract.organization.title,
                        'registration': self.invoice.specification.contract.organization.registration,
                        'address': self.invoice.specification.contract.organization.address,
                        'tin': self.invoice.specification.contract.organization.tin,
                        'pprnie': self.invoice.specification.contract.organization.pprnie,
                    },
                    'currency': {
                        'title': self.invoice.specification.contract.currency.title,
                    }
                },
            },
            'shipment_mark': self.invoice.shipment_mark,
            'loading_place': self.invoice.specification.loading_place,
            'booked_products': []
        }
        total_sum = Decimal(0)
        for i, booked_product in enumerate(ProductStoreBooking.objects.all().filter(specification=self.invoice.specification)):
            context['booked_products'].append({
                'number': i + 1,
                'product': {
                    'title': booked_product.product.type_of_product,
                    'color': booked_product.product.color,
                    'model': booked_product.product.model,
                    'cost': booked_product.product.cost,
                },
                'total_sum': booked_product.sum,
                'quantity': booked_product.quantity,
            })
            total_sum += Decimal(booked_product.sum)
        context['total_sum'] = total_sum
        doc.render(context)
        doc.save(self.output_file_path)
