from django import forms

from app_storage.models import ProductStore, Product, ProductType


class ProductStoreForm(forms.ModelForm):
    class Meta:
        model = ProductStore
        fields = ['store', 'product', 'quantity']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['number', 'type_of_product', 'model', 'size', 'version', 'materials', 'color', 'packing_inside',
                  'packing_outside', 'country', 'cost']


class ProductFilterForm(forms.Form):
    type_of_product = forms.ModelChoiceField(ProductType.objects.all(), required=False, label='Тип продукта')
    model = forms.CharField(max_length=30, required=False, label='Модель')
    version = forms.CharField(max_length=30, required=False, label='Версия')
    size = forms.CharField(max_length=30, required=False, label='Размер')
    color = forms.CharField(max_length=30, required=False, label='Цвет')
