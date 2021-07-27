from django.urls import path, include

from app_crm.views import ContractorCreateView, ContractorListView, ContractorDetailView, ContractorEditView, \
    ContractorContractListView, ContractorOrderListView, ContractorToDeleteView, ContractorContactPersonCreateView,\
    ContractorContactPersonDetailView, ContactPersonToDeleteView, ContractorFileList, ContractorFileCreate,\
    ContractorCommentEditView, ContractorCommentDeleteView, ContractorContactPersonEditView, LeadListView, \
    LeadDetailView, LeadCreateView, LeadContactPersonCreateView, LeadContactPersonEditView, LeadContactPersonDetailView,\
    LeadContactPersonToDeleteView, LeadEditView, LeadCommentEditView, LeadCommentDeleteView, LeadContractorCreateView, \
    ContractorRequisitesCreateView, ContractorRequisitesEditView, LeadStatusSubstandard, LeadStatusDeferred

urlpatterns = [
    path('contractors/', include([
        path('list/', ContractorListView.as_view(), name='contractors_list'),
        path('create/', ContractorCreateView.as_view(), name='contractor_create'),
        path('<int:pk>/', include([
            path('detail/', ContractorDetailView.as_view(), name='contractor_detail'),
            path('edit/', ContractorEditView.as_view(), name='contractor_edit'),
            path('contracts/', ContractorContractListView.as_view(), name='contractor_contracts_list'),
            path('orders/', ContractorOrderListView.as_view(), name='contractor_orders_list'),
            path('to-delete/', ContractorToDeleteView.as_view(), name='contractor_to_delete'),
            path('files/', include([
                path('list/', ContractorFileList.as_view(), name='contractor_files_list'),
                path('<int:file_pk>/', ContractorFileList.download, name='contractor_file_download'),
                path('create/', ContractorFileCreate.as_view(), name='contractor_file_create'),
            ])),
            path('comments/<int:comment_pk>/', include([
                path('edit/', ContractorCommentEditView.as_view(), name='contractor_comment_edit'),
                path('delete/', ContractorCommentDeleteView.as_view(), name='contractor_comment_delete'),
            ])),
            path('contact-persons/', include([
                path('create/', ContractorContactPersonCreateView.as_view(), name='contractor_contact_person_create'),
                path('<int:contact_person_pk>/', include([
                    path('detail/', ContractorContactPersonDetailView.as_view(), name='contractor_contact_person_detail'),
                    path('edit/', ContractorContactPersonEditView.as_view(), name='contractor_contact_person_edit'),
                    path('to_delete/', ContactPersonToDeleteView.as_view(), name='contractor_contact_person_to_delete'),
                ]))
            ])),
            path('requisites', include([
                path('create/', ContractorRequisitesCreateView.as_view(), name='contractor_requisites_create'),
                path('<int:requisites_pk>/edit', ContractorRequisitesEditView.as_view(),
                     name='contractor_requisites_edit'),
            ]))
        ]))
    ])),
    path('leads/', include([
        path('list/', LeadListView.as_view(), name='leads_list'),
        path('create/', LeadCreateView.as_view(), name='lead_create'),
        path('<int:pk>/', include([
            path('detail', LeadDetailView.as_view(), name='lead_detail'),
            path('edit/', LeadEditView.as_view(), name='lead_edit'),
            path('contact-persons/', include([
                path('create/', LeadContactPersonCreateView.as_view(), name='lead_contact_person_create'),
                path('<int:contact_person_pk>/', include([
                    path('detail/', LeadContactPersonDetailView.as_view(), name='lead_contact_person_detail'),
                    path('edit/', LeadContactPersonEditView.as_view(), name='lead_contact_person_edit'),
                    path('to_delete/', LeadContactPersonToDeleteView.as_view(), name='lead_contact_person_to_delete'),
                ]))
            ])),
            path('comments/<int:comment_pk>/', include([
                path('edit/', LeadCommentEditView.as_view(), name='lead_comment_edit'),
                path('delete/', LeadCommentDeleteView.as_view(), name='lead_comment_delete'),
            ])),
            path('create-contractor/', LeadContractorCreateView.as_view(), name='lead_contractor_create'),
            path('change-status/', include([
                path('substandard/', LeadStatusSubstandard.as_view(), name='lead_status_substandard'),
                path('deferred/', LeadStatusDeferred.as_view(), name='lead_status_deferred'),
            ]))
        ]))
    ]))
]