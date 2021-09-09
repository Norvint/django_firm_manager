import mimetypes
import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory, model_to_dict
from django.http import HttpResponse, FileResponse
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, TemplateView, FormView

from app_organizations.forms import WorkerForm, OrganizationFileForm, ContactForm
from app_organizations.models import Organization, Worker, OrganizationFile, WorkerContact
from firmmanager import settings


class OrganizationCreateView(LoginRequiredMixin, CreateView):
    template_name = 'app_organizations/organization_create.html'
    model = Organization
    fields = (
        'title', 'title_en', 'tin', 'kpp', 'pprnie', 'registration', 'registration_en', 'position', 'position_en',
        'appeal', 'appeal_en', 'name', 'second_name', 'last_name', 'name_en', 'second_name_en', 'last_name_en',
        'legal_address', 'legal_address_en', 'actual_address', 'requisites', 'requisites_en')
    success_url = '/organizations'


class OrganizationEditView(LoginRequiredMixin, UpdateView):
    template_name = 'app_organizations/organization_edit.html'
    model = Organization
    fields = (
        'title', 'title_en', 'tin', 'kpp', 'pprnie', 'registration', 'registration_en', 'position', 'position_en',
        'appeal', 'appeal_en', 'name', 'second_name', 'last_name', 'name_en', 'second_name_en', 'last_name_en',
        'legal_address', 'legal_address_en', 'actual_address', 'requisites', 'requisites_en')
    success_url = '/organizations'


class OrganizationListView(LoginRequiredMixin, ListView):
    template_name = 'app_organizations/organizations_list.html'
    context_object_name = 'organizations'
    queryset = Organization.objects.all()


class OrganizationDetailView(LoginRequiredMixin, DetailView):
    template_name = 'app_organizations/organization_detail.html'
    model = Organization


class OrganizationFileList(LoginRequiredMixin, TemplateView):
    template_name = 'app_organizations/organization_files.html'

    def get_context_data(self, **kwargs):
        context = super(OrganizationFileList, self).get_context_data(**kwargs)
        organization = Organization.objects.get(pk=kwargs.get('pk'))
        files = OrganizationFile.objects.all().filter(organization=organization)
        context['files'] = files
        context['organization'] = organization
        return context

    def post(self, request, *args, **kwargs):
        pass

    def download(request, *args, **kwargs):
        obj = OrganizationFile.objects.get(id=kwargs.get('file_id'))
        filename = obj.file.path
        response = FileResponse(open(filename, 'rb'))
        return response


class OrganizationFileCreate(LoginRequiredMixin, TemplateView):
    template_name = 'app_organizations/organization_file_create.html'

    def get_context_data(self, **kwargs):
        context = super(OrganizationFileCreate, self).get_context_data(**kwargs)
        organization = Organization.objects.get(pk=kwargs.get('pk'))
        form = OrganizationFileForm(initial={'organization': organization})
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = OrganizationFileForm(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid():
            form.save()
            return redirect('organization_files_list', kwargs.get('pk'))
        else:
            context['form'] = form
            context['errors'] = form.errors
        return self.render_to_response(context)


def download_organization_file(request, **kwargs):
    file_object = OrganizationFile.objects.get(pk=kwargs.get('pk'))
    file = file_object.file
    fl_path = os.path.join(settings.MEDIA_ROOT, 'app_organizations', 'organization_files', file.name)
    fl = open(fl_path, 'rb')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % file.name
    return response


class WorkerListView(LoginRequiredMixin, ListView):
    template_name = 'app_organizations/workers_list.html'
    queryset = Worker.objects.all()
    context_object_name = 'workers'


class WorkerCreateView(LoginRequiredMixin, FormView):
    template_name = 'app_organizations/worker_create.html'
    form_class = WorkerForm

    def get_context_data(self, **kwargs):
        context = super(WorkerCreateView, self).get_context_data(**kwargs)
        formset = formset_factory(ContactForm)
        context['formset'] = formset
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = WorkerForm(request.POST)
        contacts_formset = formset_factory(ContactForm)
        formset = contacts_formset(request.POST)
        if form.is_valid() and formset.is_valid():
            worker = Worker(**form.cleaned_data)
            worker.save()
            for i, contact_form in enumerate(formset):
                data = formset.cleaned_data[i]
                if contact_form.is_valid() and data:
                    contact = WorkerContact(worker=worker, type_of_contact=data['type_of_contact'],
                                            contact=data['contact'])
                    contact.save()
            return redirect('worker_detail', worker.pk)
        else:
            context['form'] = form
            context['formset'] = formset
        return self.render_to_response(context)


class WorkerEditView(LoginRequiredMixin, TemplateView):
    template_name = 'app_organizations/worker_edit.html'

    def get_context_data(self, **kwargs):
        context = super(WorkerEditView, self).get_context_data(**kwargs)
        worker = Worker.objects.get(pk=kwargs.get('pk'))
        form = WorkerForm(initial={**model_to_dict(worker)})
        contacts_formset = formset_factory(ContactForm)
        worker_contacts = WorkerContact.objects.filter(worker=kwargs.get('pk'))
        contacts_data = [{'type_of_contact': worker_contact.type_of_contact, 'contact': worker_contact.contact} for
                         worker_contact in worker_contacts]
        formset = contacts_formset(initial=contacts_data)
        context['form'] = form
        context['formset'] = formset
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = WorkerForm(request.POST)
        contacts_formset = formset_factory(ContactForm)
        formset = contacts_formset(request.POST)
        if form.is_valid() and formset.is_valid():
            Worker.objects.filter(pk=kwargs.get('pk')).update(**form.cleaned_data)
            for i, form in enumerate(formset):
                data = formset.cleaned_data[i]
                if form.is_valid() and data:
                    worker_contact = WorkerContact.objects.get(worker=kwargs.get('pk'),
                                                               type_of_contact=data['type_of_contact'])
                    if worker_contact:
                        worker_contact.contact = data['contact']
                        worker_contact.save()
                    else:
                        new_contact = WorkerContact(worker=kwargs.get('pk'), type_of_contact=data['type_of_contact'],
                                                    contact=data['contact'])
                        new_contact.save()
            return redirect('worker_detail', kwargs.get('pk'))
        else:
            context['form'] = form
            context['formset'] = formset
        return self.render_to_response(context)


class WorkerDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'app_organizations/worker_detail.html'

    def get_context_data(self, **kwargs):
        context = super(WorkerDetailView, self).get_context_data(**kwargs)
        worker = Worker.objects.get(pk=kwargs.get('pk'))
        worker_contacts = WorkerContact.objects.filter(worker=worker)
        context['object'] = worker
        context['worker_contacts'] = worker_contacts
        return context
