from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, TemplateView

from app_organizations.forms import WorkerForm
from app_organizations.models import Organization, Bank, Worker


class OrganizationCreateView(LoginRequiredMixin, CreateView):
    template_name = 'app_organizations/organization_create.html'
    model = Organization
    fields = ('title', 'address', 'tin', 'pprnie', 'registration')
    success_url = '/organizations'


class OrganizationListView(LoginRequiredMixin, ListView):
    template_name = 'app_organizations/organizations_list.html'
    context_object_name = 'organizations'
    queryset = Organization.objects.all()


class OrganizationDetailView(LoginRequiredMixin, DetailView):
    template_name = 'app_organizations/organization_detail.html'
    model = Organization


class BankListView(LoginRequiredMixin, ListView):
    template_name = 'app_organizations/banks_list.html'
    queryset = Bank.objects.all()
    context_object_name = 'banks'


class BankCreateView(LoginRequiredMixin, CreateView):
    template_name = 'app_organizations/bank_create.html'
    model = Bank
    fields = ('title', 'short_code', 'address', 'payment_account', 'correspondent_account', 'recipient')
    success_url = '/organizations/banks'


class BankDetailView(LoginRequiredMixin, DetailView):
    template_name = 'app_organizations/bank_detail.html'
    model = Bank


class WorkerListView(LoginRequiredMixin, ListView):
    template_name = 'app_organizations/workers_list.html'
    queryset = Worker.objects.all()
    context_object_name = 'workers'


class WorkerCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'app_organizations/worker_create.html'

    def get_context_data(self, **kwargs):
        context = super(WorkerCreateView, self).get_context_data(**kwargs)
        form = WorkerForm()
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = WorkerForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            name = form.cleaned_data['name']
            second_name = form.cleaned_data['second_name']
            last_name = form.cleaned_data['last_name']
            position = form.cleaned_data['position']
            organization = form.cleaned_data['organization']
            serial_number = form.cleaned_data['serial_number']
            number = form.cleaned_data['number']
            issued_by = form.cleaned_data['issued_by']
            date = form.cleaned_data['date']
            date_of_birth = form.cleaned_data['date_of_birth']
            department_code = form.cleaned_data['department_code']
            worker = Worker(user=user, name=name, second_name=second_name, last_name=last_name, position=position,
                            organization=organization, serial_number=serial_number, number=number, issued_by=issued_by,
                            date=date, date_of_birth=date_of_birth, department_code=department_code)
            worker.save()
            return redirect('worker_detail', worker.pk)
        else:
            context['errors'] = form.errors
            context['form'] = form
        return self.render_to_response(context)


class WorkerEditView(LoginRequiredMixin, UpdateView):
    template_name = 'app_organizations/worker_edit.html'
    model = Worker
    fields = ('user', 'name', 'second_name', 'last_name', 'position', 'organization', 'serial_number', 'number', 'issued_by',
              'date', 'date_of_birth', 'department_code')
    success_url = '/organizations/workers'


class WorkerDetailView(LoginRequiredMixin, DetailView):
    template_name = 'app_organizations/worker_detail.html'
    model = Worker
