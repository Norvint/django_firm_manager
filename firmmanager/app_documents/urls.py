from django.urls import path

from app_documents.views import DeliveryConditionsDetailView, DeliveryConditionsListView, ContractCreateView, \
    ContractDetailView, ContractListView, ContractTypeDetailView, ContractTypeListView, CurrencyDetailView, \
    CurrencyListView, OrderCreateView, OrderBookingCreateView, OrderDetailView, OrderListView, \
    PaymentConditionsListView, OrderBookingDeleteView, OrderBookingEditView, \
    ContractToDeleteView, OrderToDeleteView, CurrencyUpdate, ContractEditView, OrderWithoutContractListView, \
    OrderWithoutContractCreateView, OrderWithoutContractDetailView, OrderWithoutContractToDeleteView, \
    OrderWithoutContractBookingDeleteView, OrderWithoutContractBookingEditView, OrderWithoutContractBookingCreateView

# contracts
urlpatterns = [
    path('contracts/', ContractListView.as_view(), name='contracts_list'),
    path('contracts/create-contract/<int:contractor_id>/', ContractCreateView.as_view(), name='contract_create'),
    path('contracts/<int:pk>', ContractDetailView.as_view(), name='contract_detail'),
    path('contracts/<int:pk>/edit', ContractEditView.as_view(), name='contract_edit'),
    path('contracts/<int:pk>/download-contract/', ContractDetailView.download_contract, name='download_contract'),
    path('contracts/contract-types/', ContractTypeListView.as_view(), name='contract_types_list'),
    path('contracts/contract-types/<int:pk>', ContractTypeDetailView.as_view(), name='contract_type_detail'),
    path('contracts/currencies/', CurrencyListView.as_view(), name='currencies_list'),
    path('contracts/currencies/update', CurrencyUpdate.as_view(), name='currencies_update'),
    path('contracts/currencies/<int:pk>', CurrencyDetailView.as_view(),
         name='currency_detail'),
    path('contracts/<int:pk>/to-delete/', ContractToDeleteView.as_view(), name='contract_to_delete'),
]

# orders
urlpatterns += [
    path('orders/', OrderListView.as_view(), name='orders_list'),
    path('orders/create-order/<int:contract_id>/contractor/<int:contractor_id>', OrderCreateView.as_view(),
         name='order_create'),
    path('orders/<int:pk>', OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:pk>/download-specification/', OrderDetailView.download_specification,
         name='download_specification'),
    path('orders/delivery-conditions', DeliveryConditionsListView.as_view(), name='delivery_conditions_list'),
    path('orders/delivery-conditions/<int:pk>', DeliveryConditionsDetailView.as_view(),
         name='delivery_condition_detail'),
    path('orders/payment-conditions', PaymentConditionsListView.as_view(), name='payment_conditions_list'),
    path('orders/bookings/<int:order_id>/create', OrderBookingCreateView.as_view(),
         name='order_booking'),
    path('orders/bookings/<int:order_booking_id>/delete', OrderBookingDeleteView.as_view(),
         name='order_booking_delete'),
    path('orders/bookings/<int:order_booking_id>/edit', OrderBookingEditView.as_view(),
         name='order_booking_edit'),
    path('orders/<int:pk>/to-delete/', OrderToDeleteView.as_view(), name='order_to_delete'),
    path('orders/<int:pk>/download-invoice/', OrderDetailView.download_invoice, name='download_invoice'),
    path('orders/<int:pk>/download-goods-acceptance/', OrderDetailView.download_goods_acceptance,
         name='download_goods_acceptance'),
    path('orders/<int:pk>/download-upd/', OrderDetailView.download_upd,
         name='download_upd'),
]

# orders without contract
urlpatterns += [
    path('orders-without-contract/', OrderWithoutContractListView.as_view(), name='orders_without_contract_list'),
    path('orders-without-contract/create-order/<int:contractor_id>',
         OrderWithoutContractCreateView.as_view(),
         name='order_without_contract_create'),
    path('orders-without-contract/<int:pk>', OrderWithoutContractDetailView.as_view(),
         name='order_without_contract_detail'),
    path('orders-without-contract/bookings/<int:order_without_contract_id>/create',
         OrderWithoutContractBookingCreateView.as_view(),
         name='order_without_contract_booking'),
    path('orders-without-contract/bookings/<int:order_without_contract_booking_id>/delete',
         OrderWithoutContractBookingDeleteView.as_view(),
         name='order_without_contract_booking_delete'),
    path('orders-without-contract/bookings/<int:order_without_contract_booking_id>/edit',
         OrderWithoutContractBookingEditView.as_view(),
         name='order_without_contract_booking_edit'),
    path('orders-without-contract/<int:pk>/to-delete/', OrderWithoutContractToDeleteView.as_view(),
         name='order_without_contract_to_delete'),
    path('orders-without-contract/<int:pk>/download-upd/', OrderWithoutContractDetailView.download_upd,
         name='download_upd_wc'),
]
