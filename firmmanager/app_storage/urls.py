from django.urls import path

from app_storage.views import ProductCreateView, ProductListView, ProductDetailView, ProductEditView, StoreListView,\
    StoreDetailView, ProductStoreIncomeView


urlpatterns = [
    path('products/', ProductListView.as_view(), name='products_list'),
    path('products/create-product/<int:forms>', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:pk>/edit/', ProductEditView.as_view(), name='product_edit'),
    path('stores/', StoreListView.as_view(), name='stores_list'),
    path('stores/<int:pk>', StoreDetailView.as_view(), name='store_detail'),
    path('stores/product-income', ProductStoreIncomeView.as_view(), name='product_store_income'),
]