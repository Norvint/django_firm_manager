import mimetypes
import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.http import HttpResponse, FileResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, UpdateView, TemplateView
from django.views.generic.base import View

from app_crm.forms import ContractorFilterForm, ContractorCommentForm, ContractorForm, ContactForm, ContactPersonForm, \
    ContractorFileForm
from app_crm.models import Contractor, ContractorComment, ContractorContact, ContactPerson, ContractorFile, \
    ContractorFileCategory
from app_documents.models import Contract, Order
from firmmanager.settings import BASE_DIR


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
            tag = filter_data.cleaned_data['tag']
            if country:
                self.object_list = self.object_list.filter(country=country)
            if type_of_contractor:
                self.object_list = self.object_list.filter(type_of_contractor=type_of_contractor)
            if field_of_activity:
                self.object_list = self.object_list.filter(field_of_activity=field_of_activity)
            if tag:
                self.object_list = self.object_list.filter(tag__icontains=tag)
        context = self.get_context_data()
        context['filter'] = filter_data
        return self.render_to_response(context)


class ContractorDetailView(LoginRequiredMixin, DetailView):
    model = Contractor
    template_name = 'app_crm/contractors/contractor_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ContractorDetailView, self).get_context_data(**kwargs)
        comments = ContractorComment.objects.filter(contractor=self.get_object()).order_by('-created')
        files_categories = ContractorFileCategory.objects.all()
        contact_persons = ContactPerson.objects.filter(contractor=self.get_object())
        context['contact_persons'] = contact_persons
        context['comments'] = comments
        comment_form = ContractorCommentForm()
        context['files_categories'] = files_categories
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


class ContractorCommentEditView(LoginRequiredMixin, TemplateView):
    template_name = 'app_crm/comment_edit.html'

    def get_context_data(self, **kwargs):
        context = super(ContractorCommentEditView, self).get_context_data(**kwargs)
        comment = ContractorComment.objects.get(pk=kwargs.get('comment_id'))
        comment_form = ContractorCommentForm(initial={'text': comment.text})
        context['comment_form'] = comment_form
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        request_data = {'text': request.POST['text']}
        comment_form = ContractorCommentForm(data=request_data)
        if comment_form.is_valid():
            comment = ContractorComment.objects.get(pk=kwargs.get('comment_id'))
            comment.text = comment_form.cleaned_data['text']
            comment.save()
            return redirect('contractor_detail', kwargs.get('contractor_id'))
        else:
            context['comment_form'] = comment_form
            return self.render_to_response(context)


class ContractorCommentDeleteView(LoginRequiredMixin, TemplateView):
    template_name = ''

    def get(self, request, *args, **kwargs):
        comment = ContractorComment.objects.get(pk=kwargs.get('comment_id'))
        comment.text = '*Комментарий удален*'
        comment.save()
        return redirect('contractor_detail', kwargs.get('contractor_id'))


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
            contractor = form.save(commit=False)
            contractor.responsible = request.user
            contractor.save()
            return redirect('contractor_detail', pk=contractor.pk)
        else:
            context['form'] = form
            return self.render_to_response(context)


class ContractorEditView(LoginRequiredMixin, TemplateView):
    template_name = 'app_crm/contractors/contractor_edit.html'

    def get_context_data(self, **kwargs):
        context = super(ContractorEditView, self).get_context_data(**kwargs)
        contractor = Contractor.objects.get(pk=kwargs.get('contractor_id'))
        contractor_initial_data = {'title': contractor.title, 'status': contractor.status,
                                   'type_of_contractor': contractor.type_of_contractor,
                                   'field_of_activity': contractor.field_of_activity, 'position': contractor.position,
                                   'position_en': contractor.position_en, 'appeal': contractor.appeal,
                                   'appeal_en': contractor.appeal_en, 'name': contractor.name,
                                   'second_name': contractor.second_name, 'last_name': contractor.last_name,
                                   'country': contractor.country, 'tel': contractor.tel,
                                   'legal_address': contractor.legal_address,
                                   'actual_address': contractor.actual_address, 'requisites': contractor.requisites,
                                   'tag': contractor.tag}
        form = ContractorForm(initial=contractor_initial_data)
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = ContractorForm(request.POST)
        if form.is_valid():
            contractor = Contractor.objects.filter(pk=kwargs.get('contractor_id')).update(
                title=form.cleaned_data['title'], status=form.cleaned_data['status'],
                type_of_contractor=form.cleaned_data['type_of_contractor'],
                field_of_activity=form.cleaned_data['field_of_activity'], position=form.cleaned_data['position'],
                position_en=form.cleaned_data['position_en'], appeal=form.cleaned_data['appeal'],
                appeal_en=form.cleaned_data['appeal_en'], name=form.cleaned_data['name'],
                second_name=form.cleaned_data['second_name'], last_name=form.cleaned_data['last_name'],
                country=form.cleaned_data['country'], tel=form.cleaned_data['tel'],
                legal_address=form.cleaned_data['legal_address'], actual_address=form.cleaned_data['actual_address'],
                requisites=form.cleaned_data['requisites'], tag=form.cleaned_data['tag'],
                responsible=request.user)
            return redirect('contractor_detail', pk=kwargs.get('contractor_id'))
        else:
            context['form'] = form
            return self.render_to_response(context)


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


class ContractorFileList(LoginRequiredMixin, TemplateView):
    template_name = 'app_crm/contractors/contractor_files_list.html'

    def get_context_data(self, **kwargs):
        context = super(ContractorFileList, self).get_context_data(**kwargs)
        contractor = Contractor.objects.get(pk=kwargs.get('contractor_id'))
        category_slug = kwargs.get('category_slug')
        if category_slug != "all":
            files = ContractorFile.objects.all().filter(contractor=contractor, category__slug=category_slug)
        else:
            files = ContractorFile.objects.all().filter(contractor=contractor)
        files_categories = ContractorFileCategory.objects.all()
        context['files_categories'] = files_categories
        context['files'] = files
        context['contractor'] = contractor
        return context

    def post(self, request, *args, **kwargs):
        pass

    def download(request, **kwargs):
        obj = ContractorFile.objects.get(id=kwargs.get('file_id'))
        filename = obj.file.path
        response = FileResponse(open(filename, 'rb'))
        return response


class ContractorFileCreate(LoginRequiredMixin, TemplateView):
    template_name = 'app_crm/contractors/contractor_file_create.html'

    def get_context_data(self, **kwargs):
        context = super(ContractorFileCreate, self).get_context_data(**kwargs)
        contractor = Contractor.objects.get(pk=kwargs.get('contractor_id'))
        form = ContractorFileForm(initial={'contractor': contractor})
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = ContractorFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('contractor_files_list', kwargs.get('contractor_id'), form.cleaned_data['category'].slug)
        else:
            context['form'] = form
            context['errors'] = form.errors
        return self.render_to_response(context)


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
                        contact = ContractorContact(contact_person=contact_person,
                                                    type_of_contact=data['type_of_contact'],
                                                    contact=data['contact'])
                        contact.save()
                return redirect('contact_person_detail', pk=contact_person.pk,
                                contractor_id=kwargs.get('contractor_id'))
            else:
                context['formset'] = formset
                context['errors'] = formset.errors
        else:
            context['form'] = contact_person_form
            return self.render_to_response(context)


class ContactPersonEditView(LoginRequiredMixin, TemplateView):
    template_name = 'app_crm/contractors/contact_person_edit.html'

    def get_context_data(self, **kwargs):
        context = super(ContactPersonEditView, self).get_context_data(**kwargs)
        contact_person = ContactPerson.objects.get(pk=kwargs.get('pk'))
        contact_person_form = ContactPersonForm(
            initial={'contractor': contact_person.contractor, 'name': contact_person.name,
                     'second_name': contact_person.second_name, 'last_name': contact_person.last_name,
                     'position': contact_person.position, 'tag': contact_person.tag})
        contact_person_contacts = ContractorContact.objects.filter(pk=kwargs.get('pk'))
        contacts_data = []
        for contact_person_contact in contact_person_contacts:
            contacts_data.append(
                {'type_of_contact': contact_person_contact.type_of_contact, 'contact': contact_person_contact.contact})
        contacts_formset = formset_factory(ContactForm)
        formset = contacts_formset(initial=contacts_data)
        context['formset'] = formset
        context['form'] = contact_person_form
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        contact_person_form = ContactPersonForm(request.POST)
        contacts_formset = formset_factory(ContactForm)
        formset = contacts_formset(request.POST)
        if contact_person_form.is_valid() and formset.is_valid():
            form_data = contact_person_form.cleaned_data
            contact_person = ContactPerson.objects.filter(pk=kwargs.get('pk')).update(name=form_data['name'],
                                                                                      second_name=form_data[
                                                                                          'second_name'],
                                                                                      last_name=form_data['last_name'],
                                                                                      position=form_data['position'],
                                                                                      contractor=form_data[
                                                                                          'contractor'],
                                                                                      tag=form_data['tag'])
            for i, form in enumerate(formset):
                data = formset.cleaned_data[i]
                if form.is_valid() and data:
                    contact_person_contact = ContractorContact.objects.get(contact_person=kwargs.get('pk'),
                                                                           type_of_contact=data['type_of_contact'])
                    if contact_person_contact:
                        contact_person_contact.contact = data['contact']
                        contact_person_contact.save()
                    else:
                        new_contact = ContractorContact(worker=kwargs.get('pk'), type_of_contact=data['type_of_contact'],
                                                    contact=data['contact'])
                        new_contact.save()
            return redirect('contact_person_detail', pk=kwargs.get('pk'), contractor_id=kwargs.get('contractor_id'))
        else:
            context['form'] = contact_person_form
            context['formset'] = formset
        return self.render_to_response(context)


class ContactPersonDetailView(LoginRequiredMixin, DetailView):
    model = ContactPerson
    template_name = 'app_crm/contractors/contact_person_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ContactPersonDetailView, self).get_context_data(**kwargs)
        contacts = ContractorContact.objects.filter(contact_person=self.get_object())
        context['contacts'] = contacts
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
            return redirect('contractor_detail', pk=kwargs.get('contractor_id'))
