from django.urls import path

from app_crm.views import ContractorCreateView, ContractorListView, ContractorDetailView, ContractorEditView, \
    ContractorContractListView, ContractorOrderListView, ContractorToDeleteView, \
    ContactPersonCreateView, ContactPersonDetailView, ContactPersonToDeleteView, ContractorFileList, \
    ContractorFileCreate, ContractorCommentEditView, ContractorCommentDeleteView, ContactPersonEditView

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
    path('contractors/<int:contractor_id>/contact-persons/create/', ContactPersonCreateView.as_view(),
         name='contact_person_create'),
    path('contractors/<int:contractor_id>/contact-persons/<int:pk>', ContactPersonDetailView.as_view(),
         name='contact_person_detail'),
    path('contractors/<int:contractor_id>/contact-persons/<int:pk>/edit', ContactPersonEditView.as_view(),
         name='contact_person_edit'),
    path('contactors/<int:contractor_id>/contact-persons/<int:pk>', ContactPersonToDeleteView.as_view(),
         name='contact_person_to_delete'),
]
