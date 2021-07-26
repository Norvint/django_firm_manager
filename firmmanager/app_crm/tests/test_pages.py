from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from app_crm.models import TypeOfContractor, FieldOfActivity, Contractor, ContractorStatus, ContractorComment, \
    ContractorContactPerson, ContractorRequisites, Lead, LeadStatus, LeadContactPerson, LeadComment


class CRMPagesTests(TestCase):
    def setUp(self) -> None:
        user = User.objects.create_superuser(username='testuser')
        self.client.force_login(user)
        contractor_status = ContractorStatus(title='Новый')
        contractor_status.save()
        type_of_contractor = TypeOfContractor(title='Клиент')
        type_of_contractor.save()
        field_of_activity = FieldOfActivity(title='Ретейлер')
        field_of_activity.save()
        contractor = Contractor(
            pk=1, title='Юр. наименование контрагента', status=contractor_status, type_of_contractor=type_of_contractor,
            field_of_activity=field_of_activity, position='Директор', name='Иван', last_name='Иванов', country='Россия',
            tel='88888888888', legal_address='г. Санкт-Петербург, ул. Строителей, д. 5', responsible=user)
        contractor.save()
        contractor_comment = ContractorComment(pk=1, user=user, text='Текст комментария', contractor=contractor)
        contractor_comment.save()
        contact_person = ContractorContactPerson(pk=1, name='Иван', contractor=contractor)
        contact_person.save()
        requisites = ContractorRequisites(pk=1, contractor=contractor, short_title='Сокр. имя',
                                          mailing_address='346428, г. Санкт-Петербург, ул. Строителей, д. 5',
                                          tin='1234567890', kpp='2109876541', pprnie='123456712345',
                                          checking_account='12345678901234567890123',
                                          correspondent_account='1234567890123456901234',
                                          bank_bik='123456789', bank_title='Наименование банка')
        requisites.save()
        lead_status = LeadStatus(title='Новый')
        lead_status.save()
        lead = Lead(pk=1, title='Наименование лида', status=lead_status, field_of_activity=field_of_activity,
                    purpose='Продажа продукции', responsible=user, country='Россия')
        lead.save()
        lead_contact_person = LeadContactPerson(pk=1, name='Иван', lead=lead)
        lead_contact_person.save()
        lead_comment = LeadComment(pk=1, user=user, text='Текст комментария', lead=lead)
        lead_comment.save()

    def test_contractor_list_page(self):
        url = reverse('contractors_list')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'app_crm/contractors/contractors_list.html')
        self.assertEqual(response.status_code, 200)

    def test_contractor_create_page(self):
        url = reverse('contractor_create')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'app_crm/contractors/contractor_create.html')
        self.assertEqual(response.status_code, 200)

    def test_contractor_detail_page(self):
        url = reverse('contractor_detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'app_crm/contractors/contractor_detail.html')
        self.assertEqual(response.status_code, 200)

    def test_contractor_edit_page(self):
        url = reverse('contractor_edit', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'app_crm/contractors/contractor_edit.html')
        self.assertEqual(response.status_code, 200)

    def test_contractor_contracts_page(self):
        url = reverse('contractor_contracts_list', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'app_crm/contractors/contractor_contracts_list.html')
        self.assertEqual(response.status_code, 200)

    def test_contractor_orders_page(self):
        url = reverse('contractor_orders_list', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'app_crm/contractors/contractor_orders_list.html')
        self.assertEqual(response.status_code, 200)

    def test_contractor_file_page(self):
        url = reverse('contractor_files_list', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'app_crm/contractors/contractor_files_list.html')
        self.assertEqual(response.status_code, 200)

    def test_contractor_file_create_page(self):
        url = reverse('contractor_file_create', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'app_crm/contractors/contractor_file_create.html')
        self.assertEqual(response.status_code, 200)

    def test_contractor_comment_edit_page(self):
        url = reverse('contractor_comment_edit', kwargs={'pk': 1, 'comment_pk': 1})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'app_crm/comment_edit.html')
        self.assertEqual(response.status_code, 200)

    def test_contractor_contact_person_create_page(self):
        url = reverse('contractor_contact_person_create', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'app_crm/contractors/contact_person_create.html')
        self.assertEqual(response.status_code, 200)

    def test_contractor_contact_person_detail_page(self):
        url = reverse('contractor_contact_person_detail', kwargs={'pk': 1, 'contact_person_pk': 1})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'app_crm/contractors/contact_person_detail.html')
        self.assertEqual(response.status_code, 200)

    def test_contractor_contact_person_edit_page(self):
        url = reverse('contractor_contact_person_edit', kwargs={'pk': 1, 'contact_person_pk': 1})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'app_crm/contractors/contact_person_edit.html')
        self.assertEqual(response.status_code, 200)

    def test_contractor_requisites_create_page(self):
        url = reverse('contractor_requisites_create', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'app_crm/contractors/contractor_requisites_create.html')
        self.assertEqual(response.status_code, 200)

    def test_contractor_requisites_edit_page(self):
        url = reverse('contractor_requisites_edit', kwargs={'pk': 1, 'requisites_pk': 1})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'app_crm/contractors/contractor_requisites_edit.html')
        self.assertEqual(response.status_code, 200)

    def test_leads_list_page(self):
        url = reverse('leads_list')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'app_crm/leads/leads_list.html')
        self.assertEqual(response.status_code, 200)

    def test_lead_create_page(self):
        url = reverse('lead_create')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'app_crm/leads/lead_create.html')
        self.assertEqual(response.status_code, 200)

    def test_lead_detail_page(self):
        url = reverse('lead_detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'app_crm/leads/lead_detail.html')
        self.assertEqual(response.status_code, 200)

    def test_lead_edit_page(self):
        url = reverse('lead_edit', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'app_crm/leads/lead_edit.html')
        self.assertEqual(response.status_code, 200)

    def test_lead_contact_person_create_page(self):
        url = reverse('lead_contact_person_create', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'app_crm/leads/contact_person_create.html')
        self.assertEqual(response.status_code, 200)

    def test_lead_contact_person_detail_page(self):
        url = reverse('lead_contact_person_detail', kwargs={'pk': 1, 'contact_person_pk': 1})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'app_crm/leads/contact_person_detail.html')
        self.assertEqual(response.status_code, 200)

    def test_lead_contact_person_edit_page(self):
        url = reverse('lead_contact_person_edit', kwargs={'pk': 1, 'contact_person_pk': 1})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'app_crm/leads/contact_person_edit.html')
        self.assertEqual(response.status_code, 200)

    def test_lead_comment_edit_page(self):
        url = reverse('lead_comment_edit', kwargs={'pk': 1, 'comment_pk': 1})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'app_crm/comment_edit.html')
        self.assertEqual(response.status_code, 200)






