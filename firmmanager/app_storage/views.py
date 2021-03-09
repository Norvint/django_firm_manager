import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView, TemplateView

from app_storage.forms import ProductStoreForm, ProductForm, ProductFilterForm
from app_storage.models import Product, ProductStore, Store


class ProductListView(LoginRequiredMixin, ListView):
    template_name = 'app_storage/products_list.html'
    context_object_name = 'products_list'
    queryset = Product.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data()
        filter_data = ProductFilterForm()
        context['filter'] = filter_data
        return context

    def post(self, request, *args, **kwargs):
        filter_data = ProductFilterForm(request.POST)
        self.object_list = self.get_queryset()
        if filter_data.is_valid():
            type_of_product = filter_data.cleaned_data['type_of_product']
            model = filter_data.cleaned_data['model']
            version = filter_data.cleaned_data['version']
            size = filter_data.cleaned_data['size']
            color = filter_data.cleaned_data['color']
            if type_of_product:
                self.object_list = self.object_list.filter(type_of_product=type_of_product)
            if model:
                self.object_list = self.object_list.filter(model__icontains=model)
            if version:
                self.object_list = self.object_list.filter(version__icontains=version)
            if size:
                self.object_list = self.object_list.filter(size__icontains=size)
            if color:
                self.object_list = self.object_list.filter(color__icontains=color)
        context = self.get_context_data()
        context['filter'] = filter_data
        return self.render_to_response(context)


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'app_storage/product_detail.html'

    def get(self, request, *args, **kwargs):
        super(ProductDetailView, self).get(request, *args, **kwargs)
        context = self.get_context_data()
        stores_with_product = ProductStore.objects.all().filter(product=self.object)
        context['stores_with_product'] = stores_with_product
        return self.render_to_response(context)


class ProductCreateView(LoginRequiredMixin, CreateView):
    template_name = 'app_storage/product_create.html'
    model = Product
    fields = ['number', 'type_of_product', 'model', 'size', 'version', 'materials', 'color',
              'packing_inside', 'packing_outside', 'country']

    def get(self, request, *args, **kwargs):
        super(ProductCreateView, self).get(request, *args, **kwargs)
        context = self.get_context_data()
        ProductFormSet = formset_factory(ProductForm, extra=kwargs.get('forms'))
        formset = ProductFormSet
        context['formset'] = formset
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        super(ProductCreateView, self).post(request, *args, **kwargs)
        context = self.get_context_data()
        ProductFormSet = formset_factory(ProductForm, extra=kwargs.get('forms'))
        formset = ProductFormSet(request.POST)
        context['answer'] = ''
        if formset.is_valid():
            for i, form in enumerate(formset):
                data = formset.cleaned_data[i]
                if form.is_valid() and data:
                    context['answer'] += f'{data["number"]}, '
                    form.save()
            formset = ProductFormSet
            context['formset'] = formset
        else:
            context['formset'] = formset
            context['errors'] = formset.errors
        return self.render_to_response(context)


class ProductEditView(LoginRequiredMixin, UpdateView):
    template_name = 'app_storage/product_edit.html'
    model = Product
    fields = ['number', 'type_of_product', 'model', 'size', 'version', 'materials', 'color',
              'packing_inside', 'packing_outside', 'country']
    success_url = '/storage/products'


class ProductStoreIncomeView(LoginRequiredMixin, FormView):
    template_name = 'app_storage/product_store_income.html'
    form_class = ProductStoreForm
    success_url = f'/storage/stores'

    def form_valid(self, form):
        form_data = form.cleaned_data
        print(self.form_class.changed_data)
        products = ProductStore.objects.all().filter(store=form_data['store'], product=form_data['product'])
        if products:
            for product in products:
                product.quantity += form_data['quantity']
                product.save()
        else:
            product_income = ProductStore(store=form_data['store'], product=form_data['product'],
                                          quantity=form_data['quantity'], booked=0)
            product_income.save()
        return super().form_valid(form)


class StoreListView(LoginRequiredMixin, ListView):
    template_name = 'app_storage/stores_list.html'
    context_object_name = 'stores_list'
    queryset = Store.objects.all()


class StoreDetailView(LoginRequiredMixin, DetailView):
    model = Store
    template_name = 'app_storage/store_detail.html'

    def get(self, request, *args, **kwargs):
        super(StoreDetailView, self).get(request, *args, **kwargs)
        context = self.get_context_data()
        products_in_store = ProductStore.objects.all().filter(store=self.object)
        context['products_in_store'] = products_in_store
        return self.render_to_response(context)


class ProductStoreIncomeListView(LoginRequiredMixin, TemplateView):
    template_name = ''
