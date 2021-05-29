from django.contrib import admin

from app_storage.models import Product, ProductType, PackageOutsideType, PackageInsideType, Store, ProductStore, \
    ProductStoreIncome, ProductStoreOutcome, ProductStoreOutcomeReason


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['type_of_product', 'number', 'model', 'size', 'version', 'color']


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ['title',]


@admin.register(PackageInsideType)
class PackageInsideTypeAdmin(admin.ModelAdmin):
    list_display = ['title',]


@admin.register(PackageOutsideType)
class PackageOutsideTypeAdmin(admin.ModelAdmin):
    list_display = ['title',]


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['title', 'address']


@admin.register(ProductStore)
class ProductStoreAdmin(admin.ModelAdmin):
    list_display = ['store', 'product', 'quantity']


@admin.register(ProductStoreIncome)
class ProductStoreIncomeAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductStoreOutcome)
class ProductStoreOutcomeAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductStoreOutcomeReason)
class ProductStoreOutcomeReasonAdmin(admin.ModelAdmin):
    pass
