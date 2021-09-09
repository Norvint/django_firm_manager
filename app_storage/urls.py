from django.urls import path, include

from app_storage.views import ProductCreateView, ProductListView, ProductDetailView, ProductEditView, StoreListView, \
    StoreDetailView, ProductStoreIncomeCreateView, ProductStoreIncomeListView, ProductStoreOutcomeCreateView, \
    ProductStoreOutcomeListView, AddProductToCart, DismissProductFromCart

urlpatterns = [
    path('products/', include([
        path('', ProductListView.as_view(), name='products_list'),
        path('create-product/', ProductCreateView.as_view(), name='product_create'),
        path('<int:pk>/', include([
            path('detail/', ProductDetailView.as_view(), name='product_detail'),
            path('edit/', ProductEditView.as_view(), name='product_edit'),
            path('<int:store_pk>/', include([
                path('add-to-cart/<int:cart_pk>/', AddProductToCart.as_view(), name='add_product_to_cart'),
                path('dismiss-from-cart/<int:cart_pk>/', DismissProductFromCart.as_view(),
                     name='dismiss_product_from_cart'),
            ]))
        ])),
    ])),
    path('stores/', include([
        path('', StoreListView.as_view(), name='stores_list'),
        path('<int:pk>/', include([
            path('', StoreDetailView.as_view(), name='store_detail'),
            path('product-outcome/', include([
                path('create/', ProductStoreOutcomeCreateView.as_view(), name='store_outcome_create'),
                path('list/', ProductStoreOutcomeListView.as_view(), name='store_outcome_list'),
            ])),
            path('product-income/', include([
                path('create/', ProductStoreIncomeCreateView.as_view(), name='store_income_create'),
                path('list/', ProductStoreIncomeListView.as_view(), name='store_income_list'),
            ])),
        ])),
    ])),
]
