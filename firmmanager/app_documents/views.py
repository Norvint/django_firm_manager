import mimetypes
import os
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, TemplateView, DeleteView, UpdateView

from app_documents.forms import SpecificationBookingForm, InvoiceForm, SpecificationForm, ContractFilterForm, \
    ContractForm, SpecificationFilterForm, InvoiceFilterForm
from app_documents.models import Contract, ContractType, Currency, DeliveryConditions, PaymentConditions, Specification, \
    Invoice
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
        specifications = Specification.objects.filter(contract=contract)
        context['specifications'] = specifications
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
    template_name = 'app_documents/specifications/delivery_conditions_list.html'
    queryset = DeliveryConditions.objects.all()
    context_object_name = 'delivery_conditions'


class DeliveryConditionsDetailView(LoginRequiredMixin, DetailView):
    template_name = 'app_documents/specifications/delivery_condition_detail.html'
    model = DeliveryConditions


class CurrencyListView(LoginRequiredMixin, ListView):
    template_name = 'app_documents/contracts/currencies_list.html'
    queryset = Currency.objects.all()
    context_object_name = 'currencies'


class CurrencyDetailView(LoginRequiredMixin, DetailView):
    template_name = 'app_documents/contracts/currency_detail.html'
    model = Currency


class PaymentConditionsListView(LoginRequiredMixin, ListView):
    template_name = 'app_documents/specifications/payment_conditions_list.html'
    queryset = PaymentConditions.objects.all()
    context_object_name = 'payment_conditions'


class SpecificationListView(LoginRequiredMixin, ListView):
    template_name = 'app_documents/specifications/specifications_list.html'
    queryset = Specification.objects.all()
    context_object_name = 'specifications'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SpecificationListView, self).get_context_data()
        filter_data = SpecificationFilterForm()
        context['filter'] = filter_data
        return context

    def post(self, request, *args, **kwargs):
        filter_data = SpecificationFilterForm(request.POST)
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


class SpecificationCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'app_documents/specifications/specification_create.html'

    def get_context_data(self, **kwargs):
        context = super(SpecificationCreateView, self).get_context_data(**kwargs)
        number = len(Specification.objects.filter(contract=kwargs.get('contract_id'))) + 1
        specification_form = SpecificationForm(initial={'number': number, 'contract': kwargs.get('contract_id')})
        context['form'] = specification_form
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        specification_form = SpecificationForm(request.POST)
        if specification_form.is_valid():
            specification_form.save()
            return redirect('specifications_list')
        else:
            context['form'] = specification_form
            context['errors'] = specification_form.errors
        return self.render_to_response(context)


class SpecificationDetailView(LoginRequiredMixin, DetailView):
    template_name = 'app_documents/specifications/specification_detail.html'
    model = Specification

    def get_context_data(self, **kwargs):
        context = super(SpecificationDetailView, self).get_context_data(**kwargs)
        specification = self.get_object()
        specification_booking = ProductStoreBooking.objects.filter(specification=specification)
        context['specification_booking'] = specification_booking
        invoices = Invoice.objects.filter(specification=specification)
        context['invoices'] = invoices
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        specification_creator = SpecificationCreator(self.object)
        specification_creator.create_specification()
        context['file'] = True
        return self.render_to_response(context)


class SpecificationToDeleteView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        obj = Specification.objects.get(pk=kwargs.get('pk'))
        if obj:
            if obj.to_delete:
                obj.to_delete = False
            else:
                obj.to_delete = True
            obj.save()
            return redirect('specification_detail', pk=kwargs.get('pk'))


def download_specification(request):
    fl_path = os.path.join(BASE_DIR, 'static', 'app_documents', 'layouts', 'specification.docx')
    filename = 'specification.docx'
    fl = open(fl_path, 'rb')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


class SpecificationBookingCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'app_documents/specifications/specification_booking.html'

    def get_context_data(self, **kwargs):
        context = super(SpecificationBookingCreateView, self).get_context_data(**kwargs)
        product_store_book_form_set = formset_factory(SpecificationBookingForm, extra=0)
        formset = product_store_book_form_set(initial=[{
            'specification': kwargs.get('specification_id')
        }])
        context['formset'] = formset
        context['answer'] = kwargs
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        product_store_book_form_set = formset_factory(SpecificationBookingForm)
        formset = product_store_book_form_set(request.POST)
        if formset.is_valid():
            for i, form in enumerate(formset):
                data = formset.cleaned_data[i]
                if form.is_valid() and data:
                    products_on_store = ProductStore.objects.filter(product=data['product'], store=data['store'])
                    for product_on_store in products_on_store:
                        product_on_store.quantity -= data['quantity']
                        product_on_store.booked += data['quantity']
                        product_on_store.save()
                    form.save()
            return redirect('specification_detail', pk=kwargs.get('specification_id'))
        else:
            context['formset'] = formset
            context['errors'] = formset.errors
        return self.render_to_response(context)


class SpecificationBookingDeleteView(LoginRequiredMixin, DeleteView):

    def get(self, request, *args, **kwargs):
        obj = ProductStoreBooking.objects.get(pk=kwargs.get('specification_booking_id'))
        if obj:
            product_on_store = ProductStore.objects.get(product=obj.product, store=obj.store)
            product_on_store.booked -= obj.quantity
            product_on_store.quantity += obj.quantity
            product_on_store.save()
            obj.delete()
            return redirect('specification_detail', pk=obj.specification.pk)


class SpecificationBookingEditView(LoginRequiredMixin, TemplateView):
    template_name = 'app_documents/specifications/specification_booking_edit.html'

    def get_context_data(self, **kwargs):
        context = super(SpecificationBookingEditView, self).get_context_data(**kwargs)
        object = ProductStoreBooking.objects.get(pk=kwargs.get('specification_booking_id'))
        form = SpecificationBookingForm(initial={'specification': object.specification,
                                                 'product': object.product,
                                                 'store': object.store,
                                                 'quantity': object.quantity,
                                                 'sum': object.sum}
                                        )
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = SpecificationBookingForm(request.POST)
        product_booking =  ProductStoreBooking.objects.get(pk=kwargs.get('specification_booking_id'))
        if form.is_valid():
            data = form.cleaned_data
            product_on_store = ProductStore.objects.get(product=product_booking.product, store=product_booking.store)
            product_on_store.booked -= product_booking.quantity
            product_on_store.quantity += product_booking.quantity
            product_on_store.quantity -= data['quantity']
            product_on_store.booked += data['quantity']
            product_on_store.save()
            product_booking.product = data['product']
            product_booking.specification = data['specification']
            product_booking.store = data['store']
            product_booking.quantity = data['quantity']
            product_booking.sum = product_booking.product.cost * product_booking.quantity
            product_booking.save()
            return redirect('specification_detail', pk=product_booking.specification.pk)
        else:
            context['errors'] = form.errors
        return self.render_to_response(context)


class InvoiceCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'app_documents/invoices/invoice_create.html'

    def get_context_data(self, **kwargs):
        context = super(InvoiceCreateView, self).get_context_data(**kwargs)
        try:
            specification = Specification.objects.get(id=kwargs.get('specification_id'))
            invoice_form = InvoiceForm(
                initial={'number': specification.number, 'specification': kwargs.get('specification_id')})
        except Specification.DoesNotExist:
            invoice_form = InvoiceForm()
        context['form'] = invoice_form
        context['specification_id'] = kwargs.get('specification_id')
        context['answer'] = kwargs
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        invoice_form = InvoiceForm(request.POST)
        if invoice_form.is_valid():
            invoice_form.save()
            return redirect('invoices_list')
        else:
            context['form'] = invoice_form
            context['errors'] = invoice_form.errors
        return self.render_to_response(context)


class InvoiceListView(LoginRequiredMixin, ListView):
    template_name = 'app_documents/invoices/invoices_list.html'
    queryset = Invoice.objects.all()
    context_object_name = 'invoices'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(InvoiceListView, self).get_context_data()
        filter_data = InvoiceFilterForm()
        context['filter'] = filter_data
        return context

    def post(self, request, *args, **kwargs):
        filter_data = InvoiceFilterForm(request.POST)
        self.object_list = self.get_queryset()
        if filter_data.is_valid():
            contractor = filter_data.cleaned_data['contractor']
            created_before = filter_data.cleaned_data['created_before']
            created_after = filter_data.cleaned_data['created_after']
            if contractor:
                self.object_list = self.object_list.filter(specification__contract__contractor=contractor)
            if created_after:
                self.object_list = self.object_list.filter(created__gt=created_after)
            if created_before:
                self.object_list = self.object_list.filter(created__lt=created_before)
        context = self.get_context_data()
        context['filter'] = filter_data
        return self.render_to_response(context)


class InvoiceDetailView(LoginRequiredMixin, DetailView):
    template_name = 'app_documents/invoices/invoice_detail.html'
    model = Invoice

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        specification_creator = InvoiceCreator(self.object)
        specification_creator.create_invoice()
        context['file'] = True
        return self.render_to_response(context)


class InvoiceToDeleteView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        obj = Invoice.objects.get(pk=kwargs.get('pk'))
        if obj:
            if obj.to_delete:
                obj.to_delete = False
            else:
                obj.to_delete = True
            obj.save()
            return redirect('invoice_detail', pk=kwargs.get('pk'))


def download_invoice(request):
    fl_path = os.path.join(BASE_DIR, 'static', 'app_documents', 'layouts', 'invoice.docx')
    filename = 'invoice.docx'
    fl = open(fl_path, 'rb')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response
