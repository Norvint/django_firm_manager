from django.urls import path, include

from app_documents.views import DeliveryConditionsDetailView, DeliveryConditionsListView, ContractCreateView, \
    ContractDetailView, ContractListView, ContractTypeDetailView, ContractTypeListView, CurrencyDetailView, \
    CurrencyListView, OrderCreateView, OrderDetailView, OrderListView, \
    PaymentConditionsListView, OrderBookingDeleteView, OrderBookingEditView, \
    ContractToDeleteView, OrderToDeleteView, CurrencyUpdate, ContractEditView, OrderWCListView, \
    OrderWCCreateView, OrderWCDetailView, OrderWCToDeleteView, \
    OrderWCBookingDeleteView, OrderWCBookingEditView, \
    OrderEditView, OrderWCEditView

urlpatterns = [
    path('contracts/', include([
        path('list/', ContractListView.as_view(), name='contracts_list'),
        path('create-contract/<int:contractor_pk>/', ContractCreateView.as_view(), name='contract_create'),
        path('<int:pk>/', include([
            path('detail/', ContractDetailView.as_view(), name='contract_detail'),
            path('edit/', ContractEditView.as_view(), name='contract_edit'),
            path('download-contract/', ContractDetailView.download_contract, name='download_contract'),
            path('to-delete/', ContractToDeleteView.as_view(), name='contract_to_delete'),
        ])),
        path('contract-types/', include([
            path('list/', ContractTypeListView.as_view(), name='contract_types_list'),
            path('<int:pk>/', ContractTypeDetailView.as_view(), name='contract_type_detail'),
        ])),
        path('currencies/', include([
            path('list/', CurrencyListView.as_view(), name='currencies_list'),
            path('update/', CurrencyUpdate.as_view(), name='currencies_update'),
            path('<int:pk>/', CurrencyDetailView.as_view(), name='currency_detail'),
        ]))
    ])),
    path('orders/', include([
        path('list/', OrderListView.as_view(), name='orders_list'),
        path('create-order/<int:contract_pk>/contractor/<int:contractor_pk>', OrderCreateView.as_view(),
             name='order_create'),
        path('<int:pk>/', include([
            path('detail/', OrderDetailView.as_view(), name='order_detail'),
            path('edit/', OrderEditView.as_view(), name='order_edit'),
            path('to-delete/', OrderToDeleteView.as_view(), name='order_to_delete'),
            path('download-specification/', OrderDetailView.download_specification, name='download_specification'),
            path('download-invoice/', OrderDetailView.download_invoice, name='download_invoice'),
            path('download-goods-acceptance/', OrderDetailView.download_goods_acceptance,
                 name='download_goods_acceptance'),
            path('download-upd/', OrderDetailView.download_upd, name='download_upd'),
        ])),
        path('bookings/<int:booking_pk>/', include([
                path('delete/', OrderBookingDeleteView.as_view(), name='order_booking_delete'),
                path('edit/', OrderBookingEditView.as_view(), name='order_booking_edit'),
        ])),
        path('delivery_conditions/', include([
            path('list/', DeliveryConditionsListView.as_view(), name='delivery_conditions_list'),
            path('<int:pk>/', DeliveryConditionsDetailView.as_view(), name='delivery_condition_detail'),
        ])),
        path('payment-conditions/', PaymentConditionsListView.as_view(), name='payment_conditions_list'),
    ])),
    path('orders-wc/', include([
        path('list/', OrderWCListView.as_view(), name='orders_without_contract_list'),
        path('create/<int:contractor_pk>', OrderWCCreateView.as_view(), name='order_without_contract_create'),
        path('<int:pk>/', include([
            path('edit/', OrderWCEditView.as_view(), name='order_without_contract_edit'),
            path('detail/', OrderWCDetailView.as_view(), name='order_without_contract_detail'),
            path('to-delete/', OrderWCToDeleteView.as_view(), name='order_without_contract_to_delete'),
            path('download-upd/', OrderWCDetailView.download_upd, name='download_upd_wc'),
            path('download-invoice/', OrderWCDetailView.download_invoice, name='download_invoice_wc'),
        ])),
        path('bookings/<int:booking_pk>/', include([
            path('delete/', OrderWCBookingDeleteView.as_view(), name='order_without_contract_booking_delete'),
            path('edit/', OrderWCBookingEditView.as_view(), name='order_without_contract_booking_edit'),
        ]))
    ]))
]
