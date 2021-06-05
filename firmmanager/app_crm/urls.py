from django.urls import path

from app_crm.views import ContractorCreateView, ContractorListView, ContractorDetailView, ContractorEditView, \
    ContractorContractListView, ContractorOrderListView, ContractorToDeleteView, \
    ContractorContactPersonCreateView, ContractorContactPersonDetailView, ContactPersonToDeleteView, ContractorFileList, \
    ContractorFileCreate, ContractorCommentEditView, ContractorCommentDeleteView, ContractorContactPersonEditView, \
    LeadListView, \
    LeadDetailView, LeadCreateView, LeadContactPersonCreateView, LeadContactPersonEditView, LeadContactPersonDetailView, \
    LeadContactPersonToDeleteView, LeadEditView, LeadCommentEditView, LeadCommentDeleteView, LeadContractorCreateView, \
    ContractorRequisitesCreateView, ContractorRequisitesEditView

# contractors
urlpatterns = [
    path('contractors', ContractorListView.as_view(), name='contractors_list'),
    path('contractors/create-contractor/', ContractorCreateView.as_view(), name='contractor_create'),
    path('contractors/<int:pk>', ContractorDetailView.as_view(), name='contractor_detail'),
    path('contractors/<int:contractor_id>/edit/', ContractorEditView.as_view(), name='contractor_edit'),
    path('contractors/<int:contractor_id>/files/<str:category_slug>', ContractorFileList.as_view(),
         name='contractor_files_list'),
    path('contractors/<int:contractor_id>/files/all/<int:file_id>', ContractorFileList.download,
         name='contractor_file_download'),
    path('contractors/<int:contractor_id>/files/all/create', ContractorFileCreate.as_view(),
         name='contractor_file_create'),
    path('contractors/<int:contractor_id>/contracts', ContractorContractListView.as_view(),
         name='contractor_contracts_list'),
    path('contractors/<int:contractor_id>/comments/<int:comment_id>/edit', ContractorCommentEditView.as_view(),
         name='contractor_comment_edit'),
    path('contractors/<int:contractor_id>/comments/<int:comment_id>/delete', ContractorCommentDeleteView.as_view(),
         name='contractor_comment_delete'),
    path('contractors/<int:contractor_id>/orders', ContractorOrderListView.as_view(),
         name='contractor_orders_list'),
    path('contractors/<int:pk>/to-delete/', ContractorToDeleteView.as_view(), name='contractor_to_delete'),
    path('contractors/<int:contractor_id>/contact-persons/create/', ContractorContactPersonCreateView.as_view(),
         name='contractor_contact_person_create'),
    path('contractors/<int:contractor_id>/contact-persons/<int:pk>', ContractorContactPersonDetailView.as_view(),
         name='contractor_contact_person_detail'),
    path('contractors/<int:contractor_id>/contact-persons/<int:pk>/edit', ContractorContactPersonEditView.as_view(),
         name='contractor_contact_person_edit'),
    path('contactors/<int:contractor_id>/contact-persons/<int:pk>/to_delete', ContactPersonToDeleteView.as_view(),
         name='contractor_contact_person_to_delete'),
    path('contractors/<int:contractor_id>/requisites/create/', ContractorRequisitesCreateView.as_view(),
         name='contractor_requisites_create'),
    path('contractors/<int:contractor_id>/requisites/<int:contractor_requisites_id>/edit',
         ContractorRequisitesEditView.as_view(),
         name='contractor_requisites_edit'),
]

# leads
urlpatterns += [
    path('leads', LeadListView.as_view(), name='leads_list'),
    path('leads/<int:pk>', LeadDetailView.as_view(), name='lead_detail'),
    path('leads/create-lead/', LeadCreateView.as_view(), name='lead_create'),
    path('leads/<int:pk>/edit/', LeadEditView.as_view(), name='lead_edit'),
    path('leads/<int:pk>/contact-persons/create/', LeadContactPersonCreateView.as_view(),
         name='lead_contact_person_create'),
    path('leads/<int:lead_id>/contact-persons/<int:pk>', LeadContactPersonDetailView.as_view(),
         name='lead_contact_person_detail'),
    path('leads/<int:lead_id>/contact-persons/<int:pk>/edit', LeadContactPersonEditView.as_view(),
         name='lead_contact_person_edit'),
    path('leads/<int:lead_id>/contact-persons/<int:pk>/to_delete', LeadContactPersonToDeleteView.as_view(),
         name='lead_contact_person_to_delete'),
    path('leads/<int:lead_id>/comments/<int:comment_id>/edit', LeadCommentEditView.as_view(),
         name='lead_comment_edit'),
    path('leads/<int:lead_id>/comments/<int:comment_id>/delete', LeadCommentDeleteView.as_view(),
         name='lead_comment_delete'),
    path('leads/<int:lead_id>/create-contractor-from-lead/', LeadContractorCreateView.as_view(),
         name='lead_contractor_create'),
]
