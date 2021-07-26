from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.forms import formset_factory, model_to_dict
from django.http import FileResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.base import View

from app_crm.forms import ContractorFilterForm, ContractorCommentForm, ContractorForm, ContactForm, \
    ContractorContactPersonForm, \
    ContractorFileForm, LeadFilterForm, LeadCommentForm, LeadForm, LeadContactPersonForm, ContractorRequisitesForm, \
    LeadContactForm
from app_crm.models import Contractor, ContractorComment, ContractorContactPersonContact, ContractorContactPerson, \
    ContractorFile, ContractorFileCategory, Lead, LeadComment, LeadContactPerson, LeadContactPersonContact, LeadStatus,\
    ContractorRequisites, LeadContact
from app_documents.models import Contract, Order


class ContractorListView(LoginRequiredMixin, ListView):
    template_name = 'app_crm/contractors/contractors_list.html'
    context_object_name = 'contractors'
    queryset = Contractor.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ContractorListView, self).get_context_data(**kwargs)
        contractors_filter = ContractorFilterForm()
        context['filter'] = contractors_filter
        return context

    def post(self, request, *args, **kwargs):
        contractors_filter = ContractorFilterForm(request.POST)
        self.object_list = self.get_queryset()
        if contractors_filter.is_valid():
            country = contractors_filter.cleaned_data['country']
            type_of_contractor = contractors_filter.cleaned_data['type_of_contractor']
            field_of_activity = contractors_filter.cleaned_data['field_of_activity']
            tag = contractors_filter.cleaned_data['tag']
            if country:
                self.object_list = self.object_list.filter(country=country)
            if type_of_contractor:
                self.object_list = self.object_list.filter(type_of_contractor=type_of_contractor)
            if field_of_activity:
                self.object_list = self.object_list.filter(field_of_activity=field_of_activity)
            if tag:
                self.object_list = self.object_list.filter(tag__icontains=tag)
        context = self.get_context_data()
        context['filter'] = contractors_filter
        return self.render_to_response(context)


class ContractorDetailView(LoginRequiredMixin, DetailView):
    model = Contractor
    template_name = 'app_crm/contractors/contractor_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ContractorDetailView, self).get_context_data(**kwargs)
        comments = ContractorComment.objects.filter(contractor=self.get_object()).order_by('-created')
        files_categories = ContractorFileCategory.objects.all()
        try:
            requisites = ContractorRequisites.objects.get(contractor=self.get_object())
            context['requisites'] = requisites
        except ObjectDoesNotExist:
            context['requisites'] = None
        contact_persons = ContractorContactPerson.objects.filter(contractor=self.get_object())
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
        comment = ContractorComment.objects.get(pk=kwargs.get('comment_pk'))
        comment_form = ContractorCommentForm(initial={'text': comment.text})
        context['comment_form'] = comment_form
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        request_data = {'text': request.POST['text']}
        comment_form = ContractorCommentForm(data=request_data)
        if comment_form.is_valid():
            comment = ContractorComment.objects.get(pk=kwargs.get('comment_pk'))
            comment.text = comment_form.cleaned_data['text']
            comment.save()
            return redirect('contractor_detail', kwargs.get('pk'))
        else:
            context['comment_form'] = comment_form
            return self.render_to_response(context)


class ContractorCommentDeleteView(LoginRequiredMixin, TemplateView):
    template_name = ''

    def get(self, request, *args, **kwargs):
        comment = ContractorComment.objects.get(pk=kwargs.get('comment_pk'))
        comment.text = '*Комментарий удален*'
        comment.save()
        return redirect('contractor_detail', kwargs.get('pk'))


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
        contractor = Contractor.objects.get(pk=kwargs.get('pk'))
        form = ContractorForm(initial={**model_to_dict(contractor)})
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = ContractorForm(request.POST)
        if form.is_valid():
            contractor = Contractor.objects.filter(pk=kwargs.get('pk')).update(**form.cleaned_data)
            return redirect('contractor_detail', pk=kwargs.get('pk'))
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


class ContractorRequisitesCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'app_crm/contractors/contractor_requisites_create.html'

    def get_context_data(self, **kwargs):
        context = super(ContractorRequisitesCreateView, self).get_context_data(**kwargs)
        form = ContractorRequisitesForm()
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = ContractorRequisitesForm(request.POST)
        contractor = Contractor.objects.get(pk=kwargs.get('contractor_id'))
        if form.is_valid():
            contractor_requisites = form.save(commit=False)
            contractor_requisites.contractor = contractor
            contractor_requisites.save()
            return redirect('contractor_detail', pk=kwargs.get('contractor_id'))
        else:
            context['form'] = form
            return self.render_to_response(context)


class ContractorRequisitesEditView(LoginRequiredMixin, TemplateView):
    template_name = 'app_crm/contractors/contractor_requisites_edit.html'

    def get_context_data(self, **kwargs):
        context = super(ContractorRequisitesEditView, self).get_context_data(**kwargs)
        contractor_requisites = ContractorRequisites.objects.get(pk=kwargs.get('requisites_pk'))
        form = ContractorRequisitesForm(initial={**model_to_dict(contractor_requisites)})
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = ContractorRequisitesForm(request.POST)
        contractor = Contractor.objects.get(pk=kwargs.get('pk'))
        if form.is_valid():
            contractor_requisites = ContractorRequisites.objects.filter(contractor=contractor).update(
                **form.cleaned_data)
            return redirect('contractor_detail', pk=kwargs.get('pk'))
        else:
            context['form'] = form
            return self.render_to_response(context)


class ContractorFileList(LoginRequiredMixin, TemplateView):
    template_name = 'app_crm/contractors/contractor_files_list.html'

    def get_context_data(self, **kwargs):
        context = super(ContractorFileList, self).get_context_data(**kwargs)
        contractor = Contractor.objects.get(pk=kwargs.get('pk'))
        files = ContractorFile.objects.all().filter(contractor=contractor)
        context['category_slug'] = 'Все'
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
        contractor = Contractor.objects.get(pk=kwargs.get('pk'))
        form = ContractorFileForm(initial={'contractor': contractor})
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = ContractorFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('contractor_files_list', kwargs.get('pk'), form.cleaned_data['category'].slug)
        else:
            context['form'] = form
        return self.render_to_response(context)


class ContractorContractListView(LoginRequiredMixin, TemplateView):
    template_name = 'app_crm/contractors/contractor_contracts_list.html'

    def get_context_data(self, **kwargs):
        context = super(ContractorContractListView, self).get_context_data(**kwargs)
        contracts = Contract.objects.filter(contractor=kwargs.get('pk'))
        context['contracts'] = contracts
        return context


class ContractorOrderListView(LoginRequiredMixin, TemplateView):
    template_name = 'app_crm/contractors/contractor_orders_list.html'

    def get_context_data(self, **kwargs):
        context = super(ContractorOrderListView, self).get_context_data(**kwargs)
        orders = Order.objects.filter(contract__contractor=kwargs.get('pk')).distinct()
        context['orders'] = orders
        return context


class ContractorContactPersonCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'app_crm/contractors/contact_person_create.html'

    def get_context_data(self, **kwargs):
        context = super(ContractorContactPersonCreateView, self).get_context_data(**kwargs)
        contact_person_form = ContractorContactPersonForm(initial={'contractor': kwargs.get('pk')})
        formset = formset_factory(ContactForm)
        context['formset'] = formset
        context['form'] = contact_person_form
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        contact_person_form = ContractorContactPersonForm(request.POST)
        contacts_formset = formset_factory(ContactForm)
        formset = contacts_formset(request.POST)
        if contact_person_form.is_valid():
            if formset.is_valid():
                contact_person = contact_person_form.save()
                for i, form in enumerate(formset):
                    data = formset.cleaned_data[i]
                    if form.is_valid() and data:
                        contact = ContractorContactPersonContact(contact_person=contact_person,
                                                                 type_of_contact=data['type_of_contact'],
                                                                 contact=data['contact'])
                        contact.save()
                return redirect('contractor_contact_person_detail', pk=contact_person.pk,
                                contractor_id=kwargs.get('pk'))
            else:
                context['formset'] = formset
        else:
            context['form'] = contact_person_form
            return self.render_to_response(context)


class ContractorContactPersonEditView(LoginRequiredMixin, TemplateView):
    template_name = 'app_crm/contractors/contact_person_edit.html'

    def get_context_data(self, **kwargs):
        context = super(ContractorContactPersonEditView, self).get_context_data(**kwargs)
        contact_person = ContractorContactPerson.objects.get(pk=kwargs.get('pk'))
        contact_person_form = ContractorContactPersonForm(
            initial={**model_to_dict(contact_person)})
        contact_person_contacts = ContractorContactPersonContact.objects.filter(pk=kwargs.get('pk'))
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
        contact_person_form = ContractorContactPersonForm(request.POST)
        contacts_formset = formset_factory(ContactForm)
        formset = contacts_formset(request.POST)
        if contact_person_form.is_valid() and formset.is_valid():
            form_data = contact_person_form.cleaned_data
            contact_person = ContractorContactPerson.objects.filter(pk=kwargs.get('pk')).update(**form_data)
            for i, form in enumerate(formset):
                data = formset.cleaned_data[i]
                if form.is_valid() and data:
                    contact_person_contact = ContractorContactPersonContact.objects.get(
                        contact_person=kwargs.get('pk'),
                        type_of_contact=data['type_of_contact'])
                    if contact_person_contact:
                        contact_person_contact.contact = data['contact']
                        contact_person_contact.save()
                    else:
                        new_contact = ContractorContactPersonContact(
                            contact_person=kwargs.get('pk'), type_of_contact=data['type_of_contact'],
                            contact=data['contact'])
                        new_contact.save()
            return redirect('contractor_contact_person_detail', pk=kwargs.get('pk'),
                            contractor_id=kwargs.get('contractor_id'))
        else:
            context['form'] = contact_person_form
            context['formset'] = formset
        return self.render_to_response(context)


class ContractorContactPersonDetailView(LoginRequiredMixin, DetailView):
    model = ContractorContactPerson
    template_name = 'app_crm/contractors/contact_person_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ContractorContactPersonDetailView, self).get_context_data(**kwargs)
        contacts = ContractorContactPersonContact.objects.filter(contact_person=self.get_object())
        context['contacts'] = contacts
        return context


class ContactPersonToDeleteView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        obj = ContractorContactPerson.objects.get(pk=kwargs.get('contact_person_pk'))
        if obj:
            if obj.to_delete:
                obj.to_delete = False
            else:
                obj.to_delete = True
            obj.save()
            return redirect('contractor_detail', pk=kwargs.get('pk'))


class LeadListView(LoginRequiredMixin, TemplateView):
    template_name = 'app_crm/leads/leads_list.html'

    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        leads = Lead.objects.all()
        lead_filter = LeadFilterForm()
        context['leads'] = leads
        context['filter'] = lead_filter
        return context

    def post(self, request, *args, **kwargs):
        filter_data = LeadFilterForm(request.POST)
        leads = Lead.objects.all()
        if filter_data.is_valid():
            status = filter_data.cleaned_data['status']
            responsible = filter_data.cleaned_data['responsible']
            field_of_activity = filter_data.cleaned_data['field_of_activity']
            tag = filter_data.cleaned_data['tag']
            if status:
                leads = leads.filter(status=status)
            if responsible:
                leads = leads.filter(responsible=responsible)
            if field_of_activity:
                leads = leads.filter(field_of_activity=field_of_activity)
            if tag:
                leads = leads.filter(tag__icontains=tag)
        context = self.get_context_data()
        context['leads'] = leads
        context['filter'] = filter_data
        return self.render_to_response(context)


class LeadDetailView(LoginRequiredMixin, DetailView):
    model = Lead
    template_name = 'app_crm/leads/lead_detail.html'

    def get_context_data(self, **kwargs):
        context = super(LeadDetailView, self).get_context_data(**kwargs)
        comments = LeadComment.objects.filter(lead=self.get_object()).order_by('-created')
        contact_persons = LeadContactPerson.objects.filter(lead=self.get_object())
        context['contact_persons'] = contact_persons
        context['comments'] = comments
        context['contacts'] = self.get_object().leads_contacts.all()
        comment_form = LeadCommentForm()
        context['comment_form'] = comment_form
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        request_data = {'text': request.POST['text']}
        comment_form = LeadCommentForm(data=request_data)
        if comment_form.is_valid():
            comment_form.instance.user_id = request.user.id
            comment_form.instance.lead_id = kwargs.get('pk')
            comment_form.save()
        else:
            context['comment_form'] = comment_form
        return self.render_to_response(context)


class LeadCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'app_crm/leads/lead_create.html'

    def get_context_data(self, **kwargs):
        context = super(LeadCreateView, self).get_context_data(**kwargs)
        form = LeadForm()
        context['form'] = form
        lead_contact_formset = formset_factory(LeadContactForm)
        formset = lead_contact_formset()
        context['formset'] = formset
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = LeadForm(request.POST)
        lead_contact_formset = formset_factory(LeadContactForm)
        formset = lead_contact_formset(request.POST)
        if form.is_valid() and formset.is_valid():
            lead = form.save(commit=False)
            lead.responsible = request.user
            lead.save()
            for i, form in enumerate(formset):
                data = formset.cleaned_data[i]
                if form.is_valid() and data != {}:
                    lead_contact = LeadContact(lead=lead, type_of_contact=data['type_of_contact'],
                                               contact=data['contact'])
                    lead_contact.save()
            return redirect('lead_detail', pk=lead.pk)
        else:
            context['form'] = form
            context['formset'] = formset
            return self.render_to_response(context)


class LeadEditView(LoginRequiredMixin, TemplateView):
    template_name = 'app_crm/leads/lead_edit.html'

    def get_context_data(self, **kwargs):
        context = super(LeadEditView, self).get_context_data(**kwargs)
        lead = Lead.objects.get(pk=kwargs.get('pk'))
        form = LeadForm(initial={**model_to_dict(lead)})
        context['form'] = form
        lead_contacts_data = [{'type_of_contact': lead_contact.type_of_contact, 'contact': lead_contact.contact}
                              for lead_contact in lead.leads_contacts.all()]
        lead_contact_formset = formset_factory(LeadContactForm)
        formset = lead_contact_formset(initial=lead_contacts_data)
        context['formset'] = formset
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = LeadForm(request.POST)
        lead_contact_formset = formset_factory(LeadContactForm)
        formset = lead_contact_formset(request.POST)
        if form.is_valid() and formset.is_valid():
            leads = Lead.objects.filter(pk=kwargs.get('pk')).update(**form.cleaned_data, responsible=request.user)
            for i, form in enumerate(formset):
                data = formset.cleaned_data[i]
                if form.is_valid() and data != {}:
                    try:
                        lead_contact = LeadContact.objects.get(lead=kwargs.get('pk'),
                                                               type_of_contact=data['type_of_contact'])
                        lead_contact.contact = data['contact']
                        lead_contact.save()
                    except LeadContact.DoesNotExist:
                        lead_contact = LeadContact(lead=kwargs.get('pk'), type_of_contact=data['type_of_contact'],
                                                   contact=data['contact'])
                        lead_contact.save()
            return redirect('lead_detail', pk=kwargs.get('pk'))
        else:
            context['form'] = form
            return self.render_to_response(context)


class LeadContactPersonCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'app_crm/leads/contact_person_create.html'

    def get_context_data(self, **kwargs):
        context = super(LeadContactPersonCreateView, self).get_context_data(**kwargs)
        contact_person_form = LeadContactPersonForm(initial={'lead': kwargs.get('pk')})
        formset = formset_factory(ContactForm)
        context['formset'] = formset
        context['form'] = contact_person_form
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        contact_person_form = LeadContactPersonForm(request.POST)
        contacts_formset = formset_factory(ContactForm)
        formset = contacts_formset(request.POST)
        if contact_person_form.is_valid():
            if formset.is_valid():
                contact_person = contact_person_form.save()
                for i, form in enumerate(formset):
                    data = formset.cleaned_data[i]
                    if form.is_valid() and data:
                        contact = LeadContactPersonContact(contact_person=contact_person,
                                                           type_of_contact=data['type_of_contact'],
                                                           contact=data['contact'])
                        contact.save()
                return redirect('lead_contact_person_detail', pk=contact_person.pk,
                                lead_id=kwargs.get('pk'))
            else:
                context['formset'] = formset
        else:
            context['form'] = contact_person_form
            return self.render_to_response(context)


class LeadContactPersonDetailView(LoginRequiredMixin, DetailView):
    model = LeadContactPerson
    template_name = 'app_crm/leads/contact_person_detail.html'

    def get_context_data(self, **kwargs):
        context = super(LeadContactPersonDetailView, self).get_context_data(**kwargs)
        contacts = LeadContactPersonContact.objects.filter(contact_person=self.get_object())
        context['contacts'] = contacts
        return context


class LeadContactPersonEditView(LoginRequiredMixin, TemplateView):
    template_name = 'app_crm/leads/contact_person_edit.html'

    def get_context_data(self, **kwargs):
        context = super(LeadContactPersonEditView, self).get_context_data(**kwargs)
        contact_person = LeadContactPerson.objects.get(pk=kwargs.get('contact_person_pk'))
        contact_person_form = LeadContactPersonForm(
            initial={**model_to_dict(contact_person)})
        contact_person_contacts = LeadContactPersonContact.objects.filter(pk=kwargs.get('contact_person_pk'))
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
        contact_person_form = LeadContactPersonForm(request.POST)
        contacts_formset = formset_factory(ContactForm)
        formset = contacts_formset(request.POST)
        if contact_person_form.is_valid() and formset.is_valid():
            form_data = contact_person_form.cleaned_data
            contact_person = LeadContactPerson.objects.filter(pk=kwargs.get('contact_person_pk')).update(**form_data)
            for i, form in enumerate(formset):
                data = formset.cleaned_data[i]
                if form.is_valid() and data != {}:
                    contact_person_contact = LeadContactPersonContact.objects.get(
                        contact_person=kwargs.get('contact_person_pk'),
                        type_of_contact=data['type_of_contact'])
                    if contact_person_contact:
                        contact_person_contact.contact = data['contact']
                        contact_person_contact.save()
                    else:
                        new_contact = ContractorContactPersonContact(
                            contact_person=kwargs.get('pk'),
                            type_of_contact=data['type_of_contact'],
                            contact=data['contact'])
                        new_contact.save()
            return redirect('lead_contact_person_detail',
                            pk=kwargs.get('pk'),
                            lead_id=form_data['lead'].id)
        else:
            context['form'] = contact_person_form
            context['formset'] = formset
        return self.render_to_response(context)


class LeadContactPersonToDeleteView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        obj = LeadContactPerson.objects.get(pk=kwargs.get('contact_person_pk'))
        if obj:
            if obj.to_delete:
                obj.to_delete = False
            else:
                obj.to_delete = True
            obj.save()
            return redirect('lead_detail', pk=kwargs.get('pk'))


class LeadCommentEditView(LoginRequiredMixin, TemplateView):
    template_name = 'app_crm/comment_edit.html'

    def get_context_data(self, **kwargs):
        context = super(LeadCommentEditView, self).get_context_data(**kwargs)
        comment = LeadComment.objects.get(pk=kwargs.get('comment_pk'))
        comment_form = LeadCommentForm(initial={'text': comment.text})
        context['comment_form'] = comment_form
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        request_data = {'text': request.POST['text']}
        comment_form = LeadCommentForm(data=request_data)
        if comment_form.is_valid():
            comment = LeadComment.objects.get(pk=kwargs.get('comment_pk'))
            comment.text = comment_form.cleaned_data['text']
            comment.save()
            return redirect('lead_detail', kwargs.get('lead_id'))
        else:
            context['comment_form'] = comment_form
            return self.render_to_response(context)


class LeadCommentDeleteView(LoginRequiredMixin, TemplateView):
    template_name = ''

    def get(self, request, *args, **kwargs):
        comment = LeadComment.objects.get(pk=kwargs.get('comment_id'))
        comment.text = '*Комментарий удален*'
        comment.save()
        return redirect('contractor_detail', kwargs.get('lead_id'))


class LeadContractorCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'app_crm/contractors/contractor_create.html'

    def get_context_data(self, **kwargs):
        context = super(LeadContractorCreateView, self).get_context_data(**kwargs)
        lead = Lead.objects.get(pk=kwargs.get('lead_id'))
        form = ContractorForm(initial={**model_to_dict(lead)})
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        lead = Lead.objects.get(pk=kwargs.get('lead_id'))
        form = ContractorForm(request.POST)
        if form.is_valid():
            contractor = form.save(commit=False)
            contractor.save()
            try:
                new_lead_status = LeadStatus.objects.get(title__icontains='Конвертирован')
            except ObjectDoesNotExist:
                new_lead_status = LeadStatus(title='Конвертирован', description='Лид переведен в контрагенты').save()
            lead.status = new_lead_status
            lead.save()
            lead_contact_persons = LeadContactPerson.objects.all().filter(lead=lead)
            for contact_person in lead_contact_persons:
                contractor_contact_person = ContractorContactPerson(**model_to_dict(contact_person))
                contractor_contact_person.save()
                contact_persons_contacts = LeadContactPersonContact.objects.all().filter(contact_person=contact_person)
                for contact_persons_contact in contact_persons_contacts:
                    new_contact = ContractorContactPersonContact(
                        contact_person=contractor_contact_person,
                        type_of_contact=contact_persons_contact.type_of_contact,
                        contact=contact_persons_contact.contact)
                    new_contact.save()
            return redirect('contractor_detail', pk=contractor.pk)
        else:
            context['form'] = form
            return self.render_to_response(context)


class LeadStatusSubstandard(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        obj = Lead.objects.get(pk=kwargs.get('pk'))
        if obj:
            obj.status = LeadStatus.objects.get(title__icontains='Некачественный')
            obj.save()
            return redirect('lead_detail', pk=kwargs.get('pk'))


class LeadStatusDeferred(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        obj = Lead.objects.get(pk=kwargs.get('pk'))
        if obj:
            obj.status = LeadStatus.objects.get(title__icontains='Отложенный')
            obj.save()
            return redirect('lead_detail', pk=kwargs.get('pk'))
