from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, UpdateView, TemplateView
from django.views.generic.base import View

from app_crm.forms import ContractorFilterForm, ContractorCommentForm, ContractorForm, ContactForm, ContactPersonForm
from app_crm.models import Contractor, ContractorComment, Contact, ContactPerson
from app_documents.models import Contract, Order


class ContractorListView(LoginRequiredMixin, ListView):
    template_name = 'app_crm/contractors/contractors_list.html'
    context_object_name = 'contractors'
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

    def get_context_data(self, **kwargs):
        context = super(ContractorCreateView, self).get_context_data(**kwargs)
        form = ContractorForm()
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
              'last_name', 'country', 'requisites']
    success_url = '/crm/contractors'


class ContractorToDeleteView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        obj = Contractor.objects.get(pk=kwargs.get('pk'))
        if obj:
            if obj.to_delete:
                obj.to_delete = False
            else:
                obj.to_delete = True
            obj.save()
            return redirect('contractor_detail', pk=kwargs.get('pk'))


class ContractorContractListView(LoginRequiredMixin, TemplateView):
    template_name = 'app_crm/contractors/contractor_contracts_list.html'

    def get_context_data(self, **kwargs):
        context = super(ContractorContractListView, self).get_context_data(**kwargs)
        contracts = Contract.objects.filter(contractor=kwargs.get('contractor_id'))
        context['contracts'] = contracts
        return context


class ContractorOrderListView(LoginRequiredMixin, TemplateView):
    template_name = 'app_crm/contractors/contractor_orders_list.html'

    def get_context_data(self, **kwargs):
        context = super(ContractorOrderListView, self).get_context_data(**kwargs)
        orders = Order.objects.filter(contract__contractor=kwargs.get('contractor_id')).distinct()
        context['orders'] = orders
        return context


class ContactPersonCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'app_crm/contractors/contact_person_create.html'

    def get_context_data(self, **kwargs):
        context = super(ContactPersonCreateView, self).get_context_data(**kwargs)
        contact_person_form = ContactPersonForm(initial={'contractor': kwargs.get('contractor_id')})
        formset = formset_factory(ContactForm)
        context['formset'] = formset
        context['form'] = contact_person_form
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        contact_person_form = ContactPersonForm(request.POST)
        contacts_formset = formset_factory(ContactForm)
        formset = contacts_formset(request.POST)
        if contact_person_form.is_valid():
            if formset.is_valid():
                contact_person = contact_person_form.save()
                for i, form in enumerate(formset):
                    data = formset.cleaned_data[i]
                    if form.is_valid() and data:
                        contact = Contact(contact_person=contact_person, type_of_contact=data['type_of_contact'],
                                          contact=data['contact'])
                        contact.save()
                return redirect('contact_person_detail', pk=contact_person.pk, contractor_id=kwargs.get('contractor_id'))
            else:
                context['formset'] = formset
                context['errors'] = formset.errors
        else:
            context['form'] = contact_person_form
            return self.render_to_response(context)


class ContactPersonDetailView(LoginRequiredMixin, DetailView):
    model = ContactPerson
    template_name = 'app_crm/contractors/contact_person_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ContactPersonDetailView, self).get_context_data(**kwargs)
        contacts = Contact.objects.filter(contact_person=self.get_object())
        context['contacts'] = contacts
        return context


class ContactPersonListView(LoginRequiredMixin, TemplateView):
    template_name = 'app_crm/contractors/contact_persons_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ContactPersonListView, self).get_context_data(**kwargs)
        contact_persons = ContactPerson.objects.filter(contractor=kwargs.get('contractor_id'))
        context['contact_persons'] = contact_persons
        return context


class ContactPersonToDeleteView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        obj = ContactPerson.objects.get(pk=kwargs.get('pk'))
        if obj:
            if obj.to_delete:
                obj.to_delete = False
            else:
                obj.to_delete = True
            obj.save()
            return redirect('contact_persons_list', contractor_id=kwargs.get('contractor_id'))
