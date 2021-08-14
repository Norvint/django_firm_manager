import os
from pathlib import Path

import pymorphy2
from docxtpl import DocxTemplate

from app_documents.models import Contract


class ContractCreator:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

    def __init__(self, context: Contract):
        if context.type.title == 'Экскл. Дистриб-во (Экспорт)':
            template_path = os.path.join('foreign', 'contract_template_distr_export.docx')
        elif context.type.title == 'Поставка (Косвенный Реэкспорт)':
            template_path = os.path.join('foreign', 'contract_template.docx')
        elif context.type.title == 'Экскл. Дистриб-во (Косв. Реэкспорт)':
            template_path = os.path.join('foreign', 'contract_template_distr_reexport.docx')
        elif context.type.title == 'Поставка (Экспорт)':
            template_path = os.path.join('foreign', 'contract_template_export.docx')
        self.template = os.path.join(self.BASE_DIR, 'static', 'app_documents', 'layouts', template_path)
        self.output_file_path = os.path.join(self.BASE_DIR, 'static', 'app_documents', 'tmp', 'contract.docx')
        self.contract = context

    def create_contract(self):
        doc = DocxTemplate(self.template)
        context = {
            'number': self.contract.number,
            'created': self.contract.created.strftime('%d-%m-%Y'),
            'created_year': self.get_created_year(),
            'client': {
                'title': self.contract.contractor.title,
                'appeal_en': self.contract.contractor.appeal_en,
                'position': self.contract.contractor.position,
                'position_en': self.contract.contractor.position_en,
                'name': self.contract.contractor.name,
                'second_name': self.contract.contractor.second_name,
                'last_name': self.contract.contractor.last_name,
                'legal_address': self.contract.contractor.legal_address,
                'requisites': self.contract.contractor.requisites,
                'initials': self.get_contractor_initials(),
                'country': self.contract.contractor.country,
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
                'initials': self.get_organization_initials(),
            },
            'currency': {
                'title': self.contract.currency.title,
                'char_code': self.contract.currency.char_code,
            },
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

    def get_organization_initials(self):
        return f'{self.contract.organization.name[:1]}. {self.contract.organization.second_name[:1]}.'

    def get_created_year(self):
        created_year = self.contract.created.strftime('%Y')
        return created_year

    def get_position(self):
        morph = pymorphy2.MorphAnalyzer()
        position_raw = morph.parse(self.contract.organization.position)[0]
        position = position_raw.inflect({'gent'})
        print(position.word)
        return position.word