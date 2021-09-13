from django.contrib import admin

from app_storage.models import Product, ProductType, PackageOutsideType, PackageInsideType, Store, ProductStore, \
    ProductStoreIncome, ProductStoreOutcome, ProductStoreOutcomeReason, Cart, CartProduct, ProductImage


class ProductStoreInLine(admin.TabularInline):
    model = ProductStore


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['type_of_product', 'number', 'model', 'size', 'version', 'color']
    inlines = [ProductStoreInLine]


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
    inlines = [ProductStoreInLine]


@admin.register(ProductStoreIncome)
class ProductStoreIncomeAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductStoreOutcome)
class ProductStoreOutcomeAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductStoreOutcomeReason)
class ProductStoreOutcomeReasonAdmin(admin.ModelAdmin):
    pass


class CartProductInline(admin.TabularInline):
    model = CartProduct


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_sum']
    inlines = [CartProductInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass