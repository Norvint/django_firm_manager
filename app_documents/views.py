import mimetypes
import os
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory, model_to_dict
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView, DeleteView, UpdateView

from app_crm.models import ContractorRequisites
from app_documents.forms import OrderForm, ContractFilterForm, ContractForm, OrderFilterForm, OrderBookingForm, \
    BookingEditForm, OrderWithoutContractFilterForm, OrderWithoutContractForm, OrderWithoutContractBookingEditForm, \
    OrderWCBookingForm
from app_documents.models import Contract, ContractType, Currency, DeliveryConditions, PaymentConditions, Order, \
    OrderWithoutContract
from app_documents.utilities.currencies_parser import CurrenciesUpdater
from app_documents.utilities.docx_creator.goods_acceptance import GoodsAcceptanceCreator
from app_documents.utilities.docx_creator.invoice import InvoiceCreator, RussianInvoiceWCCreator
from app_documents.utilities.docx_creator.specification import SpecificationCreator
from app_documents.utilities.docx_creator.contract import ContractCreator
from app_documents.utilities.docx_creator.upd import UpdCreator, UpdWithoutContractCreator
from app_storage.models import ProductStore, ProductStoreOrderBooking, ProductStoreOrderWCBooking, CartProduct
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
        contract_form = ContractForm(initial={'number': number, 'contractor': kwargs.get('contractor_pk')})
        context['form'] = contract_form
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        contract_form = ContractForm(request.POST)
        if contract_form.is_valid():
            contract = contract_form.save(commit=False)
            contract.responsible = request.user
            contract.save()
            return redirect('contracts_list')
        else:
            context['form'] = contract_form
            context['errors'] = contract_form.errors
        return self.render_to_response(context)


class ContractDetailView(LoginRequiredMixin, DetailView):
    template_name = 'app_documents/contracts/contract_detail.html'
    model = Contract

    async def download_contract(request, **kwargs):
        contract = Contract.objects.get(pk=kwargs.get('pk'))
        contract_creator = ContractCreator(contract)
        contract_creator.create_contract()
        fl_path = os.path.join(BASE_DIR, 'static', 'app_documents', 'tmp', 'contract.docx')
        filename = 'contract.docx'
        fl = open(fl_path, 'rb')
        mime_type, _ = mimetypes.guess_type(fl_path)
        response = HttpResponse(fl, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response


class ContractEditView(LoginRequiredMixin, UpdateView):
    template_name = 'app_documents/contracts/contract_edit.html'
    model = Contract
    fields = ['number', 'type', 'contractor', 'organization', 'currency']
    success_url = f'/documents/contracts/'

    def get_success_url(self):
        url = super(ContractEditView, self).get_success_url() + str(self.object.id)
        return url


class ContractToDeleteView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        obj = Contract.objects.get(pk=kwargs.get('pk'))
        if obj:
            if obj.to_delete:
                obj.to_delete = False
            else:
                obj.to_delete = True
            obj.save()
            return redirect('contract_detail', pk=kwargs.get('pk'))


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


class CurrencyUpdate(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
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
        contract = kwargs.get('contract_pk')
        contractor = kwargs.get('contractor_pk')
        if contract:
            order_form = OrderForm(initial={'contract': contract})
        elif contractor and not contract:
            order_form = OrderForm()
            order_form.fields['contract'].queryset = Contract.objects.all().filter(contractor=contractor)
        else:
            order_form = OrderForm()
        context['form'] = order_form
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.responsible = request.user
            order.save()
            for product_in_cart in CartProduct.objects.filter(cart=self.request.user.cart):
                product_in_cart: CartProduct
                product_booking = ProductStoreOrderBooking(
                    order=order, store=product_in_cart.store, quantity=product_in_cart.quantity,
                    product=product_in_cart.product)
                product_booking.save()
                product_in_cart.delete()
            order.save()
            return redirect('order_detail', order.id)
        else:
            context['form'] = order_form
        return self.render_to_response(context)


class OrderDetailView(LoginRequiredMixin, DetailView):
    template_name = 'app_documents/orders/order_detail.html'
    model = Order

    def download_specification(request, **kwargs):
        order = Order.objects.get(pk=kwargs.get('pk'))
        specification_creator = SpecificationCreator(order)
        specification_creator.create_specification()
        fl_path = os.path.join(BASE_DIR, 'static', 'app_documents', 'tmp', 'specification.docx')
        filename = 'specification.docx'
        fl = open(fl_path, 'rb')
        mime_type, _ = mimetypes.guess_type(fl_path)
        response = HttpResponse(fl, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response

    def download_invoice(request, **kwargs):
        order = Order.objects.get(pk=kwargs.get('pk'))
        invoice_creator = InvoiceCreator(order)
        invoice_creator.create_invoice()
        fl_path = os.path.join(BASE_DIR, 'static', 'app_documents', 'tmp', 'invoice.docx')
        filename = 'invoice.docx'
        fl = open(fl_path, 'rb')
        mime_type, _ = mimetypes.guess_type(fl_path)
        response = HttpResponse(fl, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response

    def download_goods_acceptance(request, **kwargs):
        order = Order.objects.get(pk=kwargs.get('pk'))
        goods_acceptance_creator = GoodsAcceptanceCreator(order)
        goods_acceptance_creator.create_goods_acceptance()
        fl_path = os.path.join(BASE_DIR, 'static', 'app_documents', 'tmp', 'goods_acceptance.docx')
        filename = 'goods_acceptance.docx'
        fl = open(fl_path, 'rb')
        mime_type, _ = mimetypes.guess_type(fl_path)
        response = HttpResponse(fl, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response

    def download_upd(request, **kwargs):
        order = Order.objects.get(pk=kwargs.get('pk'))
        upd_creator = UpdCreator(order)
        upd_creator.create_upd()
        fl_path = os.path.join(BASE_DIR, 'static', 'app_documents', 'tmp', 'upd.docx')
        filename = 'upd.docx'
        fl = open(fl_path, 'rb')
        mime_type, _ = mimetypes.guess_type(fl_path)
        response = HttpResponse(fl, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response


class OrderEditView(LoginRequiredMixin, TemplateView):
    template_name = 'app_documents/orders/order_edit.html'

    def get_context_data(self, **kwargs):
        context = super(OrderEditView, self).get_context_data(**kwargs)
        order = Order.objects.get(pk=kwargs.get('pk'))
        product_booking_data = [{**model_to_dict(product_booking)} for product_booking in order.bookings.all()]
        product_store_book_formset = formset_factory(OrderBookingForm)
        context['formset'] = product_store_book_formset(initial=product_booking_data)
        context['form'] = OrderForm(initial={**model_to_dict(order)})
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        order_form = OrderForm(request.POST)
        product_store_book_formset = formset_factory(OrderBookingForm)
        formset = product_store_book_formset(request.POST)
        if order_form.is_valid() and formset.is_valid():
            order = Order.objects.get(pk=kwargs.get('pk'))
            for i, form in enumerate(formset):
                data = formset.cleaned_data[i]
                if form.is_valid() and data != {}:
                    try:
                        product_on_store = ProductStore.objects.get(product=data['product'], store=data['store'])
                    except ProductStore.DoesNotExist:
                        context['formset'] = formset
                        context['form'] = order_form
                        context['products_on_store_error'] = f'На складе {data["store"]} нет продукции {data["product"]}'
                        return self.render_to_response(context)
                    try:
                        product_booking = ProductStoreOrderBooking.objects.get(order=order, product=data['product'])
                        product_booking.quantity = data['quantity']
                        if product_on_store.quantity >= data['quantity']:
                            product_on_store.cancel_book_product(product_booking.quantity)
                            product_on_store.book_product(quantity=data['quantity'])
                            product_on_store.save()
                            product_booking.save()
                        else:
                            context['formset'] = formset
                            context['form'] = order_form
                            context['products_on_store_error'] = product_on_store.less_then_needed_error(
                                product_booking.quantity)
                            return self.render_to_response(context)
                    except ProductStoreOrderBooking.DoesNotExist:
                        product_booking = ProductStoreOrderBooking(order=order, product=data['product'],
                                                                   store=data['store'], quantity=data['quantity'])
                        if product_on_store.quantity >= data['quantity']:
                            product_on_store.book_product(quantity=data['quantity'])
                            product_on_store.save()
                            product_booking.save()
                        else:
                            context['formset'] = formset
                            context['form'] = order_form
                            context['products_on_store_error'] = product_on_store.less_then_needed_error(
                                product_booking.quantity)
                            return self.render_to_response(context)
            order.update_order(form_data=order_form.cleaned_data)
            order.save()
            return redirect('order_detail', order.id)
        else:
            context['formset'] = formset
            context['form'] = order_form
        return self.render_to_response(context)


class OrderToDeleteView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        obj = Order.objects.get(pk=kwargs.get('pk'))
        if obj:
            if obj.to_delete:
                obj.to_delete = False
            else:
                obj.to_delete = True
            obj.save()
            return redirect('order_detail', pk=kwargs.get('pk'))


class OrderBookingDeleteView(LoginRequiredMixin, DeleteView):

    def post(self, request, *args, **kwargs):
        obj = ProductStoreOrderBooking.objects.get(pk=kwargs.get('booking_pk'))
        order = obj.order
        if obj:
            product_on_store = ProductStore.objects.get(product=obj.product, store=obj.store)
            product_on_store.cancel_book_product(quantity=obj.quantity)
            product_on_store.save()
            obj.delete()
            order.save()
            return redirect('order_detail', pk=order.pk)


class OrderBookingEditView(LoginRequiredMixin, TemplateView):
    template_name = 'app_documents/orders/order_booking_edit.html'

    def get_context_data(self, **kwargs):
        context = super(OrderBookingEditView, self).get_context_data(**kwargs)
        object = ProductStoreOrderBooking.objects.get(pk=kwargs.get('booking_pk'))
        context['order_booking'] = object
        context['form'] = BookingEditForm(initial={**model_to_dict(object)})
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = BookingEditForm(request.POST)
        booking = ProductStoreOrderBooking.objects.get(pk=kwargs.get('booking_pk'))
        if form.is_valid():
            product_on_store = ProductStore.objects.get(product=booking.product, store=booking.store)
            product_on_store.quantity = product_on_store.quantity + booking.quantity
            product_on_store.booked = product_on_store.booked - booking.quantity
            if product_on_store.quantity >= form.cleaned_data['quantity']:
                product_on_store.book_product(quantity=form.cleaned_data['quantity'])
                product_on_store.save()
                booking.quantity = form.cleaned_data['quantity']
                booking.total_price = form.cleaned_data['total_price']
                booking.save()
                booking.order.save()
                return redirect('order_detail', pk=booking.order.pk)
            else:
                context['form'] = form
                context['products_on_store_error'] = product_on_store.less_then_needed_error(
                    quantity=form.cleaned_data['quantity'])
        else:
            context['form'] = form
        return self.render_to_response(context)


class OrderWCListView(LoginRequiredMixin, ListView):
    template_name = 'app_documents/orders_without_contract/orders_list.html'
    queryset = OrderWithoutContract.objects.all()
    context_object_name = 'orders'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OrderWCListView, self).get_context_data(**kwargs)
        filter_data = OrderWithoutContractFilterForm()
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
                self.object_list = self.object_list.filter(contractor=contractor)
            if created_after:
                self.object_list = self.object_list.filter(created__gt=created_after)
            if created_before:
                self.object_list = self.object_list.filter(created__lt=created_before)
        context = self.get_context_data()
        context['filter'] = filter_data
        return self.render_to_response(context)


class OrderWCCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'app_documents/orders_without_contract/order_create.html'

    def get_context_data(self, **kwargs):
        context = super(OrderWCCreateView, self).get_context_data(**kwargs)
        contractor = kwargs.get('contractor_pk')
        order_form = OrderWithoutContractForm()
        if contractor:
            order_form.initial['contractor'] = contractor
        context['form'] = order_form
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        order_form = OrderWithoutContractForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.responsible = request.user
            order.save()
            for product_in_cart in CartProduct.objects.filter(cart=self.request.user.cart):
                product_booking = ProductStoreOrderWCBooking(
                    order=order, product=product_in_cart.product, store=product_in_cart.store,
                    quantity=product_in_cart.quantity)
                product_booking.save()
                product_in_cart.delete()
            order.save()
            return redirect('order_without_contract_detail', order.id)
        else:
            context['form'] = order_form
        return self.render_to_response(context)


class OrderWCEditView(LoginRequiredMixin, TemplateView):
    template_name = 'app_documents/orders_without_contract/order_edit.html'

    def get_context_data(self, **kwargs):
        context = super(OrderWCEditView, self).get_context_data(**kwargs)
        order = OrderWithoutContract.objects.get(pk=kwargs.get('pk'))
        product_booking_data = [{**model_to_dict(product_booking)} for product_booking in order.bookings.all()]
        product_store_book_formset = formset_factory(OrderWCBookingForm)
        context['formset'] = product_store_book_formset(initial=product_booking_data)
        context['form'] = OrderWithoutContractForm(initial={**model_to_dict(order)})
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        order_form = OrderWithoutContractForm(request.POST)
        product_store_book_formset = formset_factory(OrderWCBookingForm)
        formset = product_store_book_formset(request.POST)
        if order_form.is_valid() and formset.is_valid():
            order = OrderWithoutContract.objects.get(pk=kwargs.get('pk'))
            for i, form in enumerate(formset):
                data = formset.cleaned_data[i]
                if form.is_valid() and data != {}:
                    try:
                        product_on_store = ProductStore.objects.get(product=data['product'], store=data['store'])
                    except ProductStore.DoesNotExist:
                        context['formset'] = formset
                        context['form'] = order_form
                        context[
                            'products_on_store_error'] = f'На складе {data["store"]} нет продукции {data["product"]}'
                        return self.render_to_response(context)
                    try:
                        product_booking = ProductStoreOrderWCBooking.objects.get(order=order, product=data['product'])
                        product_booking.quantity = data['quantity']
                        if product_on_store.quantity >= data['quantity']:
                            product_on_store.cancel_book_product(product_booking.quantity)
                            product_on_store.book_product(quantity=data['quantity'])
                            product_on_store.save()
                            product_booking.save()
                        else:
                            context['formset'] = formset
                            context['form'] = order_form
                            context['products_on_store_error'] = product_on_store.less_then_needed_error(
                                product_booking.quantity)
                            return self.render_to_response(context)
                    except ProductStoreOrderWCBooking.DoesNotExist:
                        product_booking = ProductStoreOrderWCBooking(order=order, product=data['product'],
                                                                   store=data['store'], quantity=data['quantity'])
                        if product_on_store.quantity >= data['quantity']:
                            product_on_store.book_product(quantity=data['quantity'])
                            product_on_store.save()
                            product_booking.save()
                        else:
                            context['formset'] = formset
                            context['form'] = order_form
                            context['products_on_store_error'] = product_on_store.less_then_needed_error(
                                product_booking.quantity)
                            return self.render_to_response(context)
            order.update_order(form_data=order_form.cleaned_data)
            order.save()
            return redirect('order_detail', order.id)
        else:
            context['formset'] = formset
            context['form'] = order_form
        return self.render_to_response(context)


class OrderWCDetailView(LoginRequiredMixin, DetailView):
    template_name = 'app_documents/orders_without_contract/order_detail.html'
    model = OrderWithoutContract

    def get_context_data(self, **kwargs):
        context = super(OrderWCDetailView, self).get_context_data(**kwargs)
        order = self.get_object()
        order_bookings = ProductStoreOrderWCBooking.objects.filter(order=order)
        try:
            context['contractor_requisites'] = ContractorRequisites.objects.get(contractor=order.contractor)
        except ContractorRequisites.DoesNotExist:
            context['contractor_requisites'] = None
        context['order_booking'] = order_bookings
        currency_total_sum = round(order.total_sum * (order.currency.nominal / order.currency.cost))
        currency_counted_sum = round(
            order.counted_sum * (order.currency.nominal / order.currency.cost))
        context['currency_total_sum'] = currency_total_sum
        if currency_total_sum != order.counted_sum:
            context['currency_counted_sum'] = currency_counted_sum
        return context

    def download_upd(request, **kwargs):
        order = OrderWithoutContract.objects.get(pk=kwargs.get('pk'))
        if order.created.year == 2021 and order.created.month < 7:
            template_path = os.path.join('russian', 'upd_template.docx')
        else:
            template_path = os.path.join('russian', 'upd_template_2021.docx')
        upd_creator = UpdWithoutContractCreator(order, template_path)
        upd_creator.create_upd()
        fl_path = os.path.join(BASE_DIR, 'static', 'app_documents', 'tmp', 'upd.docx')
        filename = 'upd.docx'
        fl = open(fl_path, 'rb')
        mime_type, _ = mimetypes.guess_type(fl_path)
        response = HttpResponse(fl, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response

    def download_invoice(request, **kwargs):
        order = OrderWithoutContract.objects.get(pk=kwargs.get('pk'))
        if 'Геркен П.В.' in order.organization.title:
            template_path = os.path.join('russian', 'invoice_gerkenpv_template.docx')
        else:
            template_path = os.path.join('russian', 'invoice_gerkenea_template.docx')
        invoice_creator = RussianInvoiceWCCreator(order, template_path)
        invoice_creator.create_invoice()
        fl_path = os.path.join(BASE_DIR, 'static', 'app_documents', 'tmp', 'invoice.docx')
        filename = 'invoice.docx'
        fl = open(fl_path, 'rb')
        mime_type, _ = mimetypes.guess_type(fl_path)
        response = HttpResponse(fl, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response


class OrderWCToDeleteView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        obj = OrderWithoutContract.objects.get(pk=kwargs.get('pk'))
        if obj:
            if obj.to_delete:
                obj.to_delete = False
            else:
                obj.to_delete = True
            obj.save()
            return redirect('order_without_contract_detail', pk=kwargs.get('pk'))


class OrderWCBookingDeleteView(LoginRequiredMixin, DeleteView):

    def post(self, request, *args, **kwargs):
        obj = ProductStoreOrderWCBooking.objects.get(pk=kwargs.get('booking_pk'))
        order = obj.order
        if obj:
            product_on_store = ProductStore.objects.get(product=obj.product, store=obj.store)
            product_on_store.cancel_book_product(quantity=obj.quantity)
            product_on_store.save()
            order.save()
            obj.delete()
            return redirect('order_without_contract_detail', pk=obj.order.pk)


class OrderWCBookingEditView(LoginRequiredMixin, TemplateView):
    template_name = 'app_documents/orders_without_contract/order_booking_edit.html'

    def get_context_data(self, **kwargs):
        context = super(OrderWCBookingEditView, self).get_context_data(**kwargs)
        object = ProductStoreOrderWCBooking.objects.get(pk=kwargs.get('booking_pk'))
        context['order_booking'] = object
        context['form'] = OrderWithoutContractBookingEditForm(initial={**model_to_dict(object)})
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = OrderWithoutContractBookingEditForm(request.POST)
        booking = ProductStoreOrderWCBooking.objects.get(pk=kwargs.get('booking_pk'))
        order = booking.order
        if form.is_valid():
            product_on_store = ProductStore.objects.get(product=booking.product, store=booking.store)
            product_on_store.cancel_book_product(quantity=booking.quantity)
            if product_on_store.quantity > form.cleaned_data['quantity']:
                product_on_store.book_product(form.cleaned_data['quantity'])
                product_on_store.save()
                booking.update_booking(form.cleaned_data)
                booking.save()
                order.save()
                return redirect('order_without_contract_detail', pk=booking.order.pk)
            else:
                context['form'] = form
                context['products_on_store_error'] = product_on_store.less_then_needed_error(
                    quantity=form.cleaned_data['quantity'])
        else:
            context['form'] = form
        return self.render_to_response(context)
