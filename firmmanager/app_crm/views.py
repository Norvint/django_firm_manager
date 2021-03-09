from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, TemplateView

from app_crm.forms import ContractorFilterForm, ContractorCommentForm, ContractorForm, ContractorContactForm
from app_crm.models import Contractor, ContractorComment
from app_documents.models import Contract, Specification, Invoice


class ContractorListView(LoginRequiredMixin, ListView):
    template_name = 'app_crm/contractors/contractors_list.html'
    context_object_name = 'clients_list'
    queryset = Contractor.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ContractorListView, self).get_context_data()
        filter = ContractorFilterForm()
        context['filter'] = filter
        return context

    def post(self, request, *args, **kwargs):
        filter_data = ContractorFilterForm(request.POST)
        self.object_list = self.get_queryset()
        if filter_data.is_valid():
            country = filter_data.cleaned_data['country']
            type_of_contractor = filter_data.cleaned_data['type_of_contractor']
            field_of_activity = filter_data.cleaned_data['field_of_activity']
            if country:
                self.object_list = self.object_list.filter(country=country)
            if type_of_contractor:
                self.object_list = self.object_list.filter(type_of_contractor=type_of_contractor)
            if field_of_activity:
                self.object_list = self.object_list.filter(field_of_activity=field_of_activity)
        context = self.get_context_data()
        context['filter'] = filter_data
        return self.render_to_response(context)


class ContractorDetailView(LoginRequiredMixin, DetailView):
    model = Contractor
    template_name = 'app_crm/contractors/contractor_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ContractorDetailView, self).get_context_data(**kwargs)
        comments = ContractorComment.objects.filter(contractor=self.get_object()).order_by('-created')
        context['comments'] = comments
        comment_form = ContractorCommentForm()
        context['comment_form'] = comment_form
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        request_data = {'text': request.POST['text']}
        comment_form = ContractorCommentForm(data=request_data)
        if comment_form.is_valid():
            comment_form.instance.user_id = request.user.id
            comment_form.instance.contractor_id = kwargs.get('pk')
            comment_form.save()
        else:
            context['comment_form'] = comment_form

        return self.render_to_response(context)


class ContractorCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'app_crm/contractors/contractor_create.html'
    # success_url = '/crm/contractors'

    def get_context_data(self, **kwargs):
        context = super(ContractorCreateView, self).get_context_data(**kwargs)
        form = ContractorForm()
        formset = formset_factory(ContractorContactForm)
        context['formset'] = formset
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = ContractorForm(request.POST)
        if form.is_valid():
            contractor = form.save()
            return redirect('contractor_detail', pk=contractor.pk)
        else:
            context['form'] = form
            return self.render_to_response(context)



class ContractorEditView(LoginRequiredMixin, UpdateView):
    template_name = 'app_crm/contractors/contractor_edit.html'
    model = Contractor
    fields = ['title', 'status', 'type_of_contractor', 'field_of_activity', 'position', 'appeal', 'name', 'second_name',
              'last_name', 'country', 'phone', 'email', 'requisites']
    success_url = '/crm/contractors'


class ContractorContractListView(LoginRequiredMixin, TemplateView):
    template_name = 'app_crm/contractors/contractor_contracts_list.html'

    def get_context_data(self, **kwargs):
        context = super(ContractorContractListView, self).get_context_data(**kwargs)
        contracts = Contract.objects.filter(contractor=kwargs.get('contractor_id'))
        context['contracts'] = contracts
        return context


class ContractorSpecificationListView(LoginRequiredMixin, TemplateView):
    template_name = 'app_crm/contractors/contractor_specifications_list.html'

    def get_context_data(self, **kwargs):
        context = super(ContractorSpecificationListView, self).get_context_data(**kwargs)
        specifications = Specification.objects.filter(contract__contractor=kwargs.get('contractor_id')).distinct()
        context['specifications'] = specifications
        return context


class ContractorInvoiceListView(LoginRequiredMixin, TemplateView):
    template_name = 'app_crm/contractors/contractor_invoices_list.html'

    def get_context_data(self, **kwargs):
        context = super(ContractorInvoiceListView, self).get_context_data(**kwargs)
        invoices = Invoice.objects.filter(specification__contract__contractor=kwargs.get('contractor_id')).distinct()
        context['invoices'] = invoices
        return context
