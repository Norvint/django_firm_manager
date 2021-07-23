import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView, TemplateView

from app_storage.forms import ProductStoreForm, ProductForm, ProductFilterForm, ProductStoreOutcomeForm, \
    ProductStoreOutcomeAdditionForm
from app_storage.models import Product, ProductStore, Store, ProductStoreIncome, ProductStoreOutcome, \
    ProductStoreOrderBooking, ProductStoreOrderWCBooking


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
        ProductFormSet = formset_factory(ProductForm)
        formset = ProductFormSet
        context['formset'] = formset
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        super(ProductCreateView, self).post(request, *args, **kwargs)
        context = self.get_context_data()
        ProductFormSet = formset_factory(ProductForm)
        formset = ProductFormSet(request.POST)
        if formset.is_valid():
            for i, form in enumerate(formset):
                data = formset.cleaned_data[i]
                if form.is_valid() and data:
                    context['answer'] += f'{data["number"]}, '
                    form.save()
                else:
                    context['formset'] = formset
                    context['errors'] = formset.errors
                    return self.render_to_response(context)
            return redirect('products_list')
        else:
            context['formset'] = formset
            context['errors'] = formset.errors
        return self.render_to_response(context)


class ProductEditView(LoginRequiredMixin, UpdateView):
    template_name = 'app_storage/product_edit.html'
    model = Product
    fields = ['number', 'type_of_product', 'model', 'size', 'version', 'materials', 'color',
              'packing_inside', 'packing_outside', 'country', 'cost']
    success_url = '/storage/products'


class ProductStoreIncomeCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'app_storage/product_store_income_create.html'

    def get_context_data(self, **kwargs):
        context = super(ProductStoreIncomeCreateView, self).get_context_data(**kwargs)
        store_income_formset = formset_factory(ProductStoreForm, extra=0)
        formset = store_income_formset(initial=[{'store': kwargs.get('store_id')}])
        context['formset'] = formset
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        store_income_formset = formset_factory(ProductStoreForm)
        formset = store_income_formset(request.POST)
        if formset.is_valid():
            for i, form in enumerate(formset):
                form_data = formset.cleaned_data[i]
                if form.is_valid():
                    product_store_income = ProductStoreIncome(store=form_data['store'], product=form_data['product'],
                                                              quantity=form_data['quantity'], responsible=request.user)
                    product_store_income.save()
                    try:
                        product = ProductStore.objects.all().get(store=form_data['store'], product=form_data['product'])
                        product.quantity += form_data['quantity']
                        product.save()
                    except ProductStore.DoesNotExist:
                        product_on_store = ProductStore(store=form_data['store'], product=form_data['product'],
                                                        quantity=form_data['quantity'], booked=0)
                        product_on_store.save()
            return redirect('store_detail', pk=form_data['store'].id)
        else:
            context['formset'] = formset
        return self.render_to_response(context)


class ProductStoreOutcomeCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'app_storage/product_store_outcome_create.html'

    def get_context_data(self, **kwargs):
        context = super(ProductStoreOutcomeCreateView, self).get_context_data(**kwargs)
        product_outcome_formset = formset_factory(ProductStoreOutcomeForm, extra=0)
        formset = product_outcome_formset(initial=[{'store': kwargs.get('store_id')}])
        context['formset'] = formset
        form = ProductStoreOutcomeAdditionForm()
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        product_outcome_formset = formset_factory(ProductStoreOutcomeForm)
        formset = product_outcome_formset(request.POST)
        form = ProductStoreOutcomeAdditionForm(request.POST)
        if formset.is_valid() and form.is_valid():
            for i, outcome_form in enumerate(formset):
                form_data = formset.cleaned_data[i]
                try:
                    product_on_store = ProductStore.objects.all().get(store=form_data['store'],
                                                                      product=form_data['product'])
                    if outcome_form.is_valid():
                        if form_data['quantity'] <= product_on_store.quantity:
                            product_store_outcome = ProductStoreOutcome(**form_data, responsible=request.user,
                                                                        comment=form.cleaned_data['comment'])
                            product_store_outcome.save()
                            product_on_store.quantity -= form_data['quantity']
                            product_on_store.save()
                        else:
                            context['product_on_store_error'] = f'На {form_data["store"]} недостаточно продукции' \
                                                                f' {form_data["product"]} ' \
                                                                f'(На складе {product_on_store.quantity} шт.)'
                            context['formset'] = formset
                            return self.render_to_response(context)
                except ProductStore.DoesNotExist:
                    context['product_on_store_error'] = f'На {form_data["store"]} нет продукции {form_data["product"]}'
                    context['formset'] = formset
                    return self.render_to_response(context)
            return redirect('store_outcome_list', store_id=form_data['store'].id)
        else:
            context['formset'] = formset
        return self.render_to_response(context)


class ProductStoreOutcomeListView(LoginRequiredMixin, TemplateView):
    template_name = 'app_storage/product_store_outcome_list.html'

    def get_context_data(self, **kwargs):
        context = super(ProductStoreOutcomeListView, self).get_context_data(**kwargs)
        store = kwargs.get('store_id')
        if store != 0:
            product_store_outcome_list = ProductStoreOutcome.objects.all().filter(store=store)
            product_store_orders_outcome_list = ProductStoreOrderBooking.objects.all().filter(store=store)
            product_store_orderswc_outcome_list = ProductStoreOrderWCBooking.objects.all().filter(
                store=store)
        else:
            product_store_outcome_list = ProductStoreOutcome.objects.all()
            product_store_orders_outcome_list = ProductStoreOrderBooking.objects.all()
            product_store_orderswc_outcome_list = ProductStoreOrderWCBooking.objects.all()
        context['product_store_outcome_list'] = product_store_outcome_list
        context['product_store_orders_outcome_list'] = product_store_orders_outcome_list
        context['product_store_orderswc_outcome_list'] = product_store_orderswc_outcome_list
        return context


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
    template_name = 'app_storage/product_store_income_list.html'

    def get_context_data(self, **kwargs):
        context = super(ProductStoreIncomeListView, self).get_context_data(**kwargs)
        store = kwargs.get('store_id')
        if store != 0:
            product_store_income_list = ProductStoreIncome.objects.all().filter(store=store)
        else:
            product_store_income_list = ProductStoreIncome.objects.all()
        context['product_store_income_list'] = product_store_income_list
        return context
