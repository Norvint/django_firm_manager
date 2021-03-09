from django.urls import path

from app_documents.views import DeliveryConditionsDetailView, DeliveryConditionsListView, \
    ContractCreateView, ContractDetailView, ContractListView, \
    ContractTypeDetailView, ContractTypeListView, CurrencyDetailView, CurrencyListView, download_contract, \
    SpecificationCreateView, SpecificationBookingCreateView, SpecificationDetailView, SpecificationListView, \
    PaymentConditionsListView, download_specification, InvoiceCreateView, InvoiceDetailView, InvoiceListView, \
    download_invoice, SpecificationBookingDeleteView, SpecificationBookingEditView

# contracts
urlpatterns = [
    path('contracts/', ContractListView.as_view(), name='contracts_list'),
    path('contracts/create-contract/', ContractCreateView.as_view(), name='contract_create'),
    path('contracts/<int:pk>', ContractDetailView.as_view(), name='contract_detail'),
    path('contracts/download-contract/', download_contract, name='download_contract'),
    path('contracts/contract-types/', ContractTypeListView.as_view(), name='contract_types_list'),
    path('contracts/contract-types/<int:pk>', ContractTypeDetailView.as_view(), name='contract_type_detail'),
    path('contracts/currencies/', CurrencyListView.as_view(), name='currencies_list'),
    path('contracts/currencies/<int:pk>', CurrencyDetailView.as_view(),
         name='currency_detail'),
]

# specification
urlpatterns += [
    path('specifications/', SpecificationListView.as_view(), name='specifications_list'),
    path('specifications/create-specification/<int:contract_id>', SpecificationCreateView.as_view(),
         name='specification_create'),
    path('specifications/<int:pk>', SpecificationDetailView.as_view(), name='specification_detail'),
    path('specifications/download-specification/', download_specification, name='download_specification'),
    path('specifications/delivery-conditions', DeliveryConditionsListView.as_view(), name='delivery_conditions_list'),
    path('specifications/delivery-conditions/<int:pk>', DeliveryConditionsDetailView.as_view(),
         name='delivery_condition_detail'),
    path('specifications/payment-conditions', PaymentConditionsListView.as_view(), name='payment_conditions_list'),
    path('specifications/<int:specification_id>/create-booking', SpecificationBookingCreateView.as_view(),
         name='specification_booking'),
    path('specifications/delete_booking/<int:specification_booking_id>', SpecificationBookingDeleteView.as_view(),
         name='specification_booking_delete'),
path('specifications/edit_booking/<int:specification_booking_id>', SpecificationBookingEditView.as_view(),
         name='specification_booking_edit')
]

# invoices
urlpatterns += [
    path('invoices/', InvoiceListView.as_view(), name='invoices_list'),
    path('invoices/create-invoice/<int:specification_id>', InvoiceCreateView.as_view(), name='invoice_create'),
    path('invoices/<int:pk>', InvoiceDetailView.as_view(), name='invoice_detail'),
    path('invoices/download-invoice/', download_invoice, name='download_invoice'),
]
