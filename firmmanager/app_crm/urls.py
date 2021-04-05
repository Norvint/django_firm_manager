from django.urls import path

from app_crm.views import ContractorCreateView, ContractorListView, ContractorDetailView, ContractorEditView, \
    ContractorContractListView, ContractorOrderListView, ContractorToDeleteView, ContactPersonListView, \
    ContactPersonCreateView, ContactPersonDetailView, ContactPersonToDeleteView

urlpatterns = [
    path('contractors', ContractorListView.as_view(), name='contractors_list'),
    path('contractors/create-contractor/', ContractorCreateView.as_view(), name='contractor_create'),
    path('contractors/<int:pk>', ContractorDetailView.as_view(), name='contractor_detail'),
    path('contractors/<int:pk>/edit/', ContractorEditView.as_view(), name='contractor_edit'),
    path('contractors/<int:contractor_id>/contracts', ContractorContractListView.as_view(),
         name='contractor_contracts_list'),
    path('contractors/<int:contractor_id>/orders', ContractorOrderListView.as_view(),
         name='contractor_orders_list'),
    path('contractors/<int:pk>/to-delete/', ContractorToDeleteView.as_view(), name='contractor_to_delete'),
    path('contractors/<int:contractor_id>/contact-persons/', ContactPersonListView.as_view(),
         name='contact_persons_list'),
    path('contractors/<int:contractor_id>/contact-persons/create/', ContactPersonCreateView.as_view(),
         name='contact_person_create'),
    path('contractors/<int:contractor_id>/contact-persons/<int:pk>', ContactPersonDetailView.as_view(),
         name='contact_person_detail'),
    path('contactors/<int:contractor_id>/contact-persons/<int:pk>', ContactPersonToDeleteView.as_view(),
         name='contact_person_to_delete'),
]
