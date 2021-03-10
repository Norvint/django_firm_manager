from django.urls import path

from app_crm.views import ContractorCreateView, ContractorListView, ContractorDetailView, ContractorEditView, \
    ContractorContractListView, ContractorSpecificationListView, ContractorInvoiceListView, ContractorToDeleteView

urlpatterns = [
    path('contractors', ContractorListView.as_view(), name='contractors_list'),
    path('contractors/create-contractor/', ContractorCreateView.as_view(), name='contractor_create'),
    path('contractors/<int:pk>', ContractorDetailView.as_view(), name='contractor_detail'),
    path('contractors/<int:pk>/edit/', ContractorEditView.as_view(), name='contractor_edit'),
    path('contractors/<int:contractor_id>/contracts', ContractorContractListView.as_view(),
         name='contractor_contracts_list'),
    path('contractors/<int:contractor_id>/specifications', ContractorSpecificationListView.as_view(),
         name='contractor_specifications_list'),
    path('contractors/<int:contractor_id>/invoices', ContractorInvoiceListView.as_view(),
         name='contractor_invoices_list'),
    path('contractors/<int:pk>/to-delete/', ContractorToDeleteView.as_view(), name='contractor_to_delete'),
]
