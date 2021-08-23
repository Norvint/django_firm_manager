import os

from django.contrib.auth.models import User
from django.forms import model_to_dict
from django.http import FileResponse
from django.test import TestCase
from django.urls import reverse

from app_crm.models import ContractorStatus, TypeOfContractor, FieldOfActivity, Contractor, ContractorComment, \
    ContractorFileCategory, ContractorFile, ContractorContactPerson, ContractorRequisites, ContactPersonContactType, \
    ContractorContactPersonContact, Lead, LeadStatus, LeadContactPerson, LeadComment, LeadContactType, LeadContact, \
    LeadContactPersonContact
from firmmanager.settings import BASE_DIR


class CRMViewsTests(TestCase):
    def setUp(self) -> None:
        self.client.force_login(User.objects.get(username='testuser'))

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_superuser(username='testuser')
        contractor_status = ContractorStatus(pk=1, title='Новый')
        contractor_status.save()
        type_of_contractor = TypeOfContractor(pk=1, title='Клиент')
        type_of_contractor.save()
        field_of_activity = FieldOfActivity(pk=1, title='Ретейлер')
        field_of_activity.save()
        contractor = Contractor(
            title='Юр. наименование контрагента', status=contractor_status, type_of_contractor=type_of_contractor,
            field_of_activity=field_of_activity, position='Директор', name='Андрей', last_name='Андреев',
            country='Россия', tel='88888888889', legal_address='г. Москва, ул. Строителей, д. 5', responsible=user)
        contractor.save()
        contractor_file_category = ContractorFileCategory(pk=1, title='Документ', slug='doc')
        contractor_file_category.save()
        type_of_contact = ContactPersonContactType(title='Telegram')
        type_of_contact.save()

        contact_person = ContractorContactPerson(name='Иван', contractor=contractor)
        contact_person.save()
        lead_status = LeadStatus(pk=1, title='Новый')
        lead_status.save()
        lead = Lead(title='Наименование лида', status=lead_status, field_of_activity=field_of_activity,
                    purpose='Продажа продукции', responsible=user, country='Россия')
        lead.save()
        lead_type_of_contact = LeadContactType(title='Telegram')
        lead_type_of_contact.save()
        lead_contact_person = LeadContactPerson(name='Иван', lead=lead)
        lead_contact_person.save()
        lead_comment = LeadComment(user=user, text='Текст комментария', lead=lead)
        lead_comment.save()

    def test_contractor_crate_view(self):
        url = reverse('contractor_create')
        response = self.client.post(url, {'title': 'Юр. наименование контрагента', 'status': '1',
                                          'type_of_contractor': '1', 'field_of_activity': '1',
                                          'position': 'Директор', 'name': 'Иван', 'last_name': 'Иванов',
                                          'country': 'Россия', 'tel': '88888888888', 'appeal': 'г-н',
                                          'legal_address': 'г. Санкт-Петербург, ул. Строителей, д. 5'})
        contractor = Contractor.objects.all().last()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Contractor.objects.all()), 2)
        self.assertRedirects(response, reverse('contractor_detail', kwargs={'pk': contractor.pk}))

    def test_contractor_detail_view(self):
        contractor = Contractor.objects.all().first()
        url = reverse('contractor_detail', kwargs={'pk': contractor.pk})
        response = self.client.post(url, {'text': 'Новый комментарий'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(ContractorComment.objects.filter(contractor=contractor.pk)), 1)

    def test_contractor_edit_view(self):
        contractor = Contractor.objects.all().first()
        url = reverse('contractor_edit', kwargs={'pk': contractor.pk})
        response = self.client.post(url, {
            'title': 'Юр. наименование', 'work_title': 'Новое раб. наименование', 'status': '1',
            'type_of_contractor': '1', 'field_of_activity': '1', 'appeal': 'г-н', 'appeal_en': 'Mr.',
            'position': 'Директор', 'position_en': 'Director', 'name': 'Иван', 'second_name': 'Иванович',
            'last_name': 'Иванов', 'tags': '#Близко', 'tel': '88888888888', 'country': 'Россия', 'city': 'Москва',
            'legal_address': 'г. Москва, ул. Строителей, д. 5', 'actual_address': 'г. Москва, ул. Строителей, д. 5'})
        edited_contractor = Contractor.objects.get(pk=contractor.pk)
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(model_to_dict(contractor), model_to_dict(edited_contractor))
        self.assertRedirects(response, reverse('contractor_detail', kwargs={'pk': edited_contractor.pk}))

    def test_contractor_to_delete_view(self):
        contractor = Contractor.objects.all().first()
        url = reverse('contractor_to_delete', kwargs={'pk': contractor.pk})
        response = self.client.get(url)
        contractor = Contractor.objects.get(pk=contractor.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(contractor.to_delete, True)
        self.assertRedirects(response, reverse('contractor_detail', kwargs={'pk': contractor.pk}))

    def test_contractor_comment_edit_view(self):
        contractor = Contractor.objects.all().first()
        url = reverse('contractor_detail', kwargs={'pk': contractor.pk})
        self.client.post(url, {'text': 'Новый комментарий'})
        comment = ContractorComment.objects.all().first()
        url = reverse('contractor_comment_edit', kwargs={'pk': contractor.pk, 'comment_pk': comment.pk})
        response = self.client.post(url, {'text': 'Отредактированный комментарий'})
        edited_comment = ContractorComment.objects.get(pk=comment.pk)
        self.assertEqual(edited_comment.text, 'Отредактированный комментарий')
        self.assertRedirects(response, reverse('contractor_detail', kwargs={'pk': contractor.pk}))

    def test_contractor_comment_delete_view(self):
        contractor = Contractor.objects.all().first()
        url = reverse('contractor_detail', kwargs={'pk': contractor.pk})
        self.client.post(url, {'text': 'Новый комментарий'})
        comment = ContractorComment.objects.all().first()
        url = reverse('contractor_comment_delete', kwargs={'pk': contractor.pk, 'comment_pk': comment.pk})
        response = self.client.get(url)
        edited_comment = ContractorComment.objects.get(pk=comment.pk)
        self.assertEqual(edited_comment.text, '*Комментарий удален*')
        self.assertRedirects(response, reverse('contractor_detail', kwargs={'pk': contractor.pk}))

    def test_contractor_contact_person_create_view(self):
        contractor = Contractor.objects.all().first()
        type_of_contact = ContactPersonContactType.objects.all().first()
        url = reverse('contractor_contact_person_create', kwargs={'pk': contractor.pk})
        response = self.client.post(url, {'name': 'Андрей', 'contractor': f'{contractor.pk}',
                                          'form-0-type_of_contact': f'{type_of_contact.pk}',
                                          'form-0-contact': '@ndsdfs', 'form-TOTAL_FORMS': 1, 'form-INITIAL_FORMS': 0})
        contact_person = ContractorContactPerson.objects.all().last()
        contacts = ContractorContactPersonContact.objects.filter(contact_person=contact_person).first()
        self.assertEqual(model_to_dict(contacts),
                         {'id': 1, 'contact_person': 2, 'type_of_contact': 1, 'contact': '@ndsdfs'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('contractor_contact_person_detail',
                                               kwargs={'pk': contractor.pk, 'contact_person_pk': contact_person.pk}))

    def test_contractor_contact_person_edit_view(self):
        contractor = Contractor.objects.all().first()
        contact_person = ContractorContactPerson.objects.all().first()
        type_of_contact = ContactPersonContactType.objects.all().first()
        url = reverse('contractor_contact_person_edit', kwargs={'pk': contractor.pk,
                                                                'contact_person_pk': contact_person.pk})
        response = self.client.post(url, {'name': 'Андрей', 'contractor': f'{contractor.pk}',
                                          'form-0-type_of_contact': f'{type_of_contact.pk}',
                                          'form-0-contact': '@ndsdfs',
                                          'form-TOTAL_FORMS': 1, 'form-INITIAL_FORMS': 0})
        edited_contact_person = ContractorContactPerson.objects.all().first()
        contacts = ContractorContactPersonContact.objects.filter(contact_person=edited_contact_person).first()
        self.assertNotEqual(contact_person.name, edited_contact_person.name)
        self.assertEqual(model_to_dict(contacts),
                         {'id': 2, 'contact_person': 1, 'type_of_contact': 1, 'contact': '@ndsdfs'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('contractor_contact_person_detail',
                                               kwargs={'pk': contractor.pk,
                                                       'contact_person_pk': edited_contact_person.pk}))

    def test_contractor_contact_person_to_delete_view(self):
        contract_person = ContractorContactPerson.objects.all().first()
        url = reverse('contractor_contact_person_to_delete', kwargs={'pk': contract_person.contractor.pk,
                                                                     'contact_person_pk': contract_person.pk})
        response = self.client.get(url)
        edited_contact_person = ContractorContactPerson.objects.all().first()
        self.assertNotEqual(contract_person.to_delete, edited_contact_person.to_delete)
        self.assertRedirects(response, reverse('contractor_detail', kwargs={'pk': contract_person.contractor.pk}))

    def test_contractor_requisites_create_view(self):
        contractor = Contractor.objects.all().first()
        url = reverse('contractor_requisites_create', kwargs={'pk': contractor.pk})
        response = self.client.post(url, {'short_title': 'Сокр. имя', 'tin': '1234567890', 'kpp': '2109876541',
                                          'mailing_address': '346428, г. Санкт-Петербург, ул. Строителей, д. 5',
                                          'pprnie': '123456712345', 'checking_account': '12345678901234567890123',
                                          'correspondent_account': '1234567890123456901234', 'bank_bik': '123456789',
                                          'bank_title': 'Наименование банка'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('contractor_detail', kwargs={'pk': contractor.pk}))

    def test_contractor_requisites_edit_view(self):
        contractor = Contractor.objects.all().first()
        url = reverse('contractor_requisites_create', kwargs={'pk': contractor.pk})
        self.client.post(url, {'short_title': 'Сокр. имя', 'tin': '1234567890', 'kpp': '2109876541',
                               'mailing_address': '346428, г. Санкт-Петербург, ул. Строителей, д. 5',
                               'pprnie': '123456712345', 'checking_account': '12345678901234567890123',
                               'correspondent_account': '1234567890123456901234', 'bank_bik': '123456789',
                               'bank_title': 'Наименование банка'})
        requisites = ContractorRequisites.objects.get(contractor=contractor)
        url = reverse('contractor_requisites_edit', kwargs={'pk': contractor.pk, 'requisites_pk': requisites.pk})
        response = self.client.post(url, {'short_title': 'Сокр. имя', 'tin': '1234567890', 'kpp': '2109876541',
                                          'mailing_address': '346428, г. Санкт-Петербург, ул. Ломателей, д. 5',
                                          'pprnie': '123456712345', 'checking_account': '12345678901234567890123',
                                          'correspondent_account': '1234567890123456901234', 'bank_bik': '123456789',
                                          'bank_title': 'Наименование банка'})
        edited_requisites = ContractorRequisites.objects.get(contractor=contractor)
        self.assertNotEqual(model_to_dict(requisites), model_to_dict(edited_requisites))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('contractor_detail', kwargs={'pk': contractor.pk}))

    def test_lead_create_view(self):
        url = reverse('lead_create')
        type_of_contact = LeadContactType.objects.all().first()
        response = self.client.post(url, {'title': 'Наименование лида', 'status': '1', 'field_of_activity': '1',
                                          'purpose': 'Продажа продукции', 'country': 'Россия',
                                          'form-0-type_of_contact': f'{type_of_contact.pk}',
                                          'form-0-contact': '@ndsdfs',
                                          'form-TOTAL_FORMS': 1, 'form-INITIAL_FORMS': 0})
        lead = Lead.objects.all().last()
        self.assertTrue(len(Lead.objects.all()) > 1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('lead_detail', kwargs={'pk': lead.pk}))

    def test_lead_detail_view(self):
        lead = Lead.objects.all().first()
        url = reverse('lead_detail', kwargs={'pk': lead.pk})
        response = self.client.post(url, {'text': 'Новый комментарий'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(LeadComment.objects.filter(lead=lead.pk)) > 1)

    def test_lead_edit_view(self):
        type_of_contact = LeadContactType.objects.all().first()
        lead = Lead.objects.all().first()
        url = reverse('lead_edit', kwargs={'pk': lead.pk})
        response = self.client.post(url, {'title': 'Наименование лида', 'status': '1', 'field_of_activity': '1',
                                          'purpose': 'Покупка продукции', 'country': 'Россия',
                                          'form-0-type_of_contact': f'{type_of_contact.pk}',
                                          'form-0-contact': '@norvint',
                                          'form-TOTAL_FORMS': 1, 'form-INITIAL_FORMS': 0})
        edited_lead = Lead.objects.get(pk=lead.pk)
        lead_contact = LeadContact.objects.get(lead=lead, type_of_contact=type_of_contact)
        self.assertEqual(lead_contact.contact, '@norvint')
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(model_to_dict(lead), model_to_dict(edited_lead))
        self.assertRedirects(response, reverse('lead_detail', kwargs={'pk': edited_lead.pk}))

    def test_lead_contact_person_create_view(self):
        lead = Lead.objects.all().first()
        type_of_contact = ContactPersonContactType.objects.all().first()
        url = reverse('lead_contact_person_create', kwargs={'pk': lead.pk})
        response = self.client.post(url, {'name': 'Андрей', 'lead': f'{lead.pk}',
                                          'form-0-type_of_contact': f'{type_of_contact.pk}',
                                          'form-0-contact': '@ndsdfs', 'form-TOTAL_FORMS': 1, 'form-INITIAL_FORMS': 0})
        contact_person = LeadContactPerson.objects.all().last()
        contacts = LeadContactPersonContact.objects.filter(contact_person=contact_person).first()
        self.assertEqual(model_to_dict(contacts),
                         {'id': 1, 'contact_person': 2, 'type_of_contact': 1, 'contact': '@ndsdfs'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('lead_contact_person_detail',
                                               kwargs={'pk': lead.pk, 'contact_person_pk': contact_person.pk}))

    def test_lead_contact_person_edit_view(self):
        lead = Lead.objects.all().first()
        contact_person = LeadContactPerson.objects.all().first()
        type_of_contact = ContactPersonContactType.objects.all().first()
        url = reverse('lead_contact_person_edit', kwargs={'pk': lead.pk,
                                                          'contact_person_pk': contact_person.pk})
        response = self.client.post(url, {'name': 'Андрей', 'lead': f'{lead.pk}',
                                          'form-0-type_of_contact': f'{type_of_contact.pk}',
                                          'form-0-contact': '@norvint',
                                          'form-TOTAL_FORMS': 1, 'form-INITIAL_FORMS': 0})
        edited_contact_person = LeadContactPerson.objects.all().first()
        contacts = LeadContactPersonContact.objects.filter(contact_person=edited_contact_person).first()
        self.assertNotEqual(contact_person.name, edited_contact_person.name)
        self.assertEqual(model_to_dict(contacts),
                         {'id': 2, 'contact_person': 1, 'type_of_contact': 1, 'contact': '@norvint'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('lead_contact_person_detail',
                                               kwargs={'pk': lead.pk, 'contact_person_pk': edited_contact_person.pk}))

    def test_lead_contact_person_to_delete_view(self):
        contract_person = LeadContactPerson.objects.all().first()
        url = reverse('lead_contact_person_to_delete', kwargs={'pk': contract_person.lead.pk,
                                                               'contact_person_pk': contract_person.pk})
        response = self.client.get(url)
        edited_contact_person = LeadContactPerson.objects.all().first()
        self.assertNotEqual(contract_person.to_delete, edited_contact_person.to_delete)
        self.assertRedirects(response, reverse('lead_detail', kwargs={'pk': contract_person.lead.pk}))

    def test_lead_comment_edit_view(self):
        lead = Lead.objects.all().first()
        comment = LeadComment.objects.filter(lead=lead).first()
        url = reverse('lead_comment_edit', kwargs={'pk': lead.pk, 'comment_pk': comment.pk})
        response = self.client.post(url, {'text': 'Отредактированный комментарий'})
        edited_comment = LeadComment.objects.get(pk=comment.pk)
        self.assertEqual(edited_comment.text, 'Отредактированный комментарий')
        self.assertRedirects(response, reverse('lead_detail', kwargs={'pk': lead.pk}))

    def test_lead_comment_delete_view(self):
        lead = Lead.objects.all().first()
        comment = LeadComment.objects.all().first()
        url = reverse('lead_comment_delete', kwargs={'pk': lead.pk, 'comment_pk': comment.pk})
        response = self.client.get(url)
        edited_comment = LeadComment.objects.get(pk=comment.pk)
        self.assertEqual(edited_comment.text, '*Комментарий удален*')
        self.assertRedirects(response, reverse('lead_detail', kwargs={'pk': lead.pk}))

    def test_lead_contractor_create(self):
        lead = Lead.objects.all().first()
        url = reverse('lead_contractor_create', kwargs={'pk': lead.pk})
        response = self.client.post(url, {'title': 'Наименование лида', 'status': '1',
                                          'type_of_contractor': '1', 'field_of_activity': '1',
                                          'position': 'Директор', 'name': 'Иван', 'last_name': 'Иванов',
                                          'country': 'Россия', 'tel': '88888888888', 'appeal': 'г-н',
                                          'legal_address': 'г. Санкт-Петербург, ул. Строителей, д. 5'})
        contractor = Contractor.objects.all().last()
        self.assertEqual(lead.title, contractor.title)
        self.assertEqual(len(LeadContactPerson.objects.filter(lead=lead)),
                         len(ContractorContactPerson.objects.filter(contractor=contractor)))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('contractor_detail', kwargs={'pk': contractor.pk}))
