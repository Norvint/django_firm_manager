from django import forms
from django.core.validators import FileExtensionValidator

from app_storage.models import Product, ProductType, ProductStoreIncome, ProductStoreOutcome


class ProductStoreIncomeForm(forms.ModelForm):
    class Meta:
        model = ProductStoreIncome
        fields = ['store', 'product', 'quantity']


class ProductStoreOutcomeForm(forms.ModelForm):
    class Meta:
        model = ProductStoreOutcome
        fields = ['store', 'product', 'quantity', 'reason']


class ProductStoreOutcomeAdditionForm(forms.ModelForm):
    class Meta:
        model = ProductStoreOutcome
        fields = ['comment']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class ProductImageForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),
                           validators=[FileExtensionValidator(allowed_extensions=['png, jpeg', 'jpg', 'svg',
                                                                                        'jpeg'])],
                           label='Изображения товара', required=False)


class ProductFilterForm(forms.Form):
    type_of_product = forms.ModelChoiceField(ProductType.objects.all(), required=False, label='Тип продукта')
    model = forms.CharField(max_length=30, required=False, label='Модель')
    version = forms.CharField(max_length=30, required=False, label='Версия')
    size = forms.CharField(max_length=30, required=False, label='Размер')
    color = forms.CharField(max_length=30, required=False, label='Цвет')
