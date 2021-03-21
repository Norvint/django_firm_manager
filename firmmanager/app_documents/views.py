import mimetypes
import os
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView, DeleteView

from app_documents.forms import OrderBookingForm, OrderForm, ContractFilterForm, \
    ContractForm, OrderFilterForm
from app_documents.models import Contract, ContractType, Currency, DeliveryConditions, PaymentConditions, Order
from app_documents.utilities.currencies_parser import CurrenciesUpdater
from app_documents.utilities.docx_creator import ContractCreator, SpecificationCreator, InvoiceCreator
from app_storage.models import ProductStore, ProductStoreBooking
from firmmanager.settings import BASE_DIR


class ContractListView(LoginRequiredMixin, ListView):
    template_name = 'app_documents/contracts/contracts_list.html'
    queryset = Contract.objects.all()
    context_object_name = 'contracts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ContractListView, self).get_context_data()
        filter_data = ContractFilterForm()
        context['filter'] = filter_data
        return context

    def post(self, request, *args, **kwargs):
        filter_data = ContractFilterForm(request.POST)
        self.object_list = self.get_queryset()
        if filter_data.is_valid():
            contractor = filter_data.cleaned_data['contractor']
            created_before = filter_data.cleaned_data['created_before']
            created_after = filter_data.cleaned_data['created_after']
            if contractor:
                self.object_list = self.object_list.filter(contractor=contractor)
            if created_after:
                self.object_list = self.object_list.filter(created__gt=created_after)
            if created_before:
                self.object_list = self.object_list.filter(created__lt=created_before)
        context = self.get_context_data()
        context['filter'] = filter_data
        return self.render_to_response(context)


class ContractCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'app_documents/contracts/contract_create.html'

    def get_context_data(self, **kwargs):
        context = super(ContractCreateView, self).get_context_data(**kwargs)
        current_year = datetime.now().year
        contract_id = len(Contract.objects.all()) + 1
        if contract_id < 10:
            number = f'{current_year}-00{contract_id}'
        elif 10 <= contract_id < 100:
            number = f'{current_year}-0{contract_id}'
        else:
            number = f'{current_year}-{contract_id}'
        contract_form = ContractForm(initial={'number': number})
        context['form'] = contract_form
        context['answer'] = kwargs
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        contract_form = ContractForm(request.POST)
        if contract_form.is_valid():
            contract_form.save()
            return redirect('contracts_list')
        else:
            context['form'] = contract_form
            context['errors'] = contract_form.errors
        return self.render_to_response(context)


class ContractDetailView(LoginRequiredMixin, DetailView):
    template_name = 'app_documents/contracts/contract_detail.html'
    model = Contract

    def get_context_data(self, **kwargs):
        context = super(ContractDetailView, self).get_context_data(**kwargs)
        contract = self.get_object()
        orders = Order.objects.filter(contract=contract)
        context['orders'] = orders
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        contract = Contract.objects.get(pk=kwargs.get('pk'))
        contract_creator = ContractCreator(contract)
        contract_creator.create_contract()
        context['file'] = True
        return self.render_to_response(context)


class ContractToDeleteView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        obj = Contract.objects.get(pk=kwargs.get('pk'))
        if obj:
            if obj.to_delete:
                obj.to_delete = False
            else:
                obj.to_delete = True
            obj.save()
            return redirect('contract_detail', pk=kwargs.get('pk'))


def download_contract(request):
    fl_path = os.path.join(BASE_DIR, 'static', 'app_documents', 'layouts', 'contract.docx')
    filename = 'contract.docx'
    fl = open(fl_path, 'rb')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


class ContractTypeListView(LoginRequiredMixin, ListView):
    template_name = 'app_documents/contracts/contract_types_list.html'
    queryset = ContractType.objects.all()
    context_object_name = 'contract_types'


class ContractTypeDetailView(LoginRequiredMixin, DetailView):
    template_name = 'app_documents/contracts/contract_type_detail.html'
    model = ContractType


class DeliveryConditionsListView(LoginRequiredMixin, ListView):
    template_name = 'app_documents/orders/delivery_conditions_list.html'
    queryset = DeliveryConditions.objects.all()
    context_object_name = 'delivery_conditions'


class DeliveryConditionsDetailView(LoginRequiredMixin, DetailView):
    template_name = 'app_documents/orders/delivery_condition_detail.html'
    model = DeliveryConditions


class CurrencyListView(LoginRequiredMixin, ListView):
    template_name = 'app_documents/contracts/currencies_list.html'
    queryset = Currency.objects.all()
    context_object_name = 'currencies'


class CurrencyDetailView(LoginRequiredMixin, DetailView):
    template_name = 'app_documents/contracts/currency_detail.html'
    model = Currency


class CurrencyUpdate(LoginRequiredMixin, TemplateView):
    template_name = ''

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        currencies_updater = CurrenciesUpdater()
        currencies_updater.get_currencies()
        currencies_updater.update_currencies()
        return redirect('currencies_list')


class PaymentConditionsListView(LoginRequiredMixin, ListView):
    template_name = 'app_documents/orders/payment_conditions_list.html'
    queryset = PaymentConditions.objects.all()
    context_object_name = 'payment_conditions'


class OrderListView(LoginRequiredMixin, ListView):
    template_name = 'app_documents/orders/orders_list.html'
    queryset = Order.objects.all()
    context_object_name = 'orders'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OrderListView, self).get_context_data()
        filter_data = OrderFilterForm()
        context['filter'] = filter_data
        return context

    def post(self, request, *args, **kwargs):
        filter_data = OrderFilterForm(request.POST)
        self.object_list = self.get_queryset()
        if filter_data.is_valid():
            contractor = filter_data.cleaned_data['contractor']
            created_before = filter_data.cleaned_data['created_before']
            created_after = filter_data.cleaned_data['created_after']
            if contractor:
                self.object_list = self.object_list.filter(contract__contractor=contractor)
            if created_after:
                self.object_list = self.object_list.filter(created__gt=created_after)
            if created_before:
                self.object_list = self.object_list.filter(created__lt=created_before)
        context = self.get_context_data()
        context['filter'] = filter_data
        return self.render_to_response(context)


class OrderCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'app_documents/orders/order_create.html'

    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        number = len(Order.objects.filter(contract=kwargs.get('contract_id'))) + 1
        order_form = OrderForm(initial={'number': number, 'contract': kwargs.get('contract_id')})
        context['form'] = order_form
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order_form.save()
            return redirect('orders_list')
        else:
            context['form'] = order_form
            context['errors'] = order_form.errors
        return self.render_to_response(context)


class OrderDetailView(LoginRequiredMixin, DetailView):
    template_name = 'app_documents/orders/order_detail.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        order = self.get_object()
        order_booking = ProductStoreBooking.objects.filter(order=order)
        context['order_booking'] = order_booking
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        specification_creator = SpecificationCreator(self.object)
        specification_creator.create_specification()
        invoice_creator = InvoiceCreator(self.object)
        invoice_creator.create_invoice()
        context['file'] = True
        return self.render_to_response(context)


class OrderToDeleteView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        obj = Order.objects.get(pk=kwargs.get('pk'))
        if obj:
            if obj.to_delete:
                obj.to_delete = False
            else:
                obj.to_delete = True
            obj.save()
            return redirect('order_detail', pk=kwargs.get('pk'))


def download_specification(request):
    fl_path = os.path.join(BASE_DIR, 'static', 'app_documents', 'layouts', 'specification.docx')
    filename = 'specification.docx'
    fl = open(fl_path, 'rb')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


class OrderBookingCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'app_documents/orders/order_booking.html'

    def get_context_data(self, **kwargs):
        context = super(OrderBookingCreateView, self).get_context_data(**kwargs)
        product_store_book_form_set = formset_factory(OrderBookingForm, extra=0)
        formset = product_store_book_form_set(initial=[{
            'order': kwargs.get('order_id')
        }])
        context['formset'] = formset
        context['answer'] = kwargs
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        product_store_book_form_set = formset_factory(OrderBookingForm)
        formset = product_store_book_form_set(request.POST)
        if formset.is_valid():
            for i, form in enumerate(formset):
                data = formset.cleaned_data[i]
                if form.is_valid() and data:
                    product = data['product']
                    products_on_store = ProductStore.objects.filter(product=data['product'], store=data['store'])
                    order = Order.objects.get(pk=kwargs.get('order_id'))
                    for product_on_store in products_on_store:
                        product_on_store.quantity -= data['quantity']
                        product_on_store.booked += data['quantity']
                        order.total_sum += int(data['quantity']) * product.cost
                        order.save()
                        product_on_store.save()
                    form.save()
            return redirect('order_detail', pk=kwargs.get('order_id'))
        else:
            context['formset'] = formset
            context['errors'] = formset.errors
        return self.render_to_response(context)


class OrderBookingDeleteView(LoginRequiredMixin, DeleteView):

    def get(self, request, *args, **kwargs):
        obj = ProductStoreBooking.objects.get(pk=kwargs.get('order_booking_id'))
        order = obj.order
        if obj:
            product_on_store = ProductStore.objects.get(product=obj.product, store=obj.store)
            product_on_store.booked -= obj.quantity
            product_on_store.quantity += obj.quantity
            product_on_store.save()
            order.total_sum -= int(obj.quantity) * obj.product.cost
            order.save()
            obj.delete()
            return redirect('order_detail', pk=obj.order.pk)


class OrderBookingEditView(LoginRequiredMixin, TemplateView):
    template_name = 'app_documents/orders/order_booking_edit.html'

    def get_context_data(self, **kwargs):
        context = super(OrderBookingEditView, self).get_context_data(**kwargs)
        object = ProductStoreBooking.objects.get(pk=kwargs.get('order_booking_id'))
        form = OrderBookingForm(initial={'order': object.order,
                                         'product': object.product,
                                         'store': object.store,
                                         'quantity': object.quantity,
                                         'sum': object.sum}
                                )
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = OrderBookingForm(request.POST)
        product_booking = ProductStoreBooking.objects.get(pk=kwargs.get('order_booking_id'))
        order = product_booking.order
        if form.is_valid():
            data = form.cleaned_data
            product_on_store = ProductStore.objects.get(product=product_booking.product, store=product_booking.store)
            product_on_store.booked -= product_booking.quantity
            product_on_store.quantity += product_booking.quantity
            order.total_sum -= int(product_booking.quantity) * product_booking.product.cost
            order.save()
            product_on_store.quantity -= data['quantity']
            product_on_store.booked += data['quantity']
            order.total_sum += int(data['quantity']) * product_booking.product.cost
            order.save()
            product_on_store.save()
            product_booking.product = data['product']
            product_booking.order = data['order']
            product_booking.store = data['store']
            product_booking.quantity = data['quantity']
            product_booking.sum = product_booking.product.cost * product_booking.quantity
            product_booking.save()
            return redirect('order_detail', pk=product_booking.order.pk)
        else:
            context['errors'] = form.errors
        return self.render_to_response(context)


def download_invoice(request):
    fl_path = os.path.join(BASE_DIR, 'static', 'app_documents', 'layouts', 'invoice.docx')
    filename = 'invoice.docx'
    fl = open(fl_path, 'rb')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response
