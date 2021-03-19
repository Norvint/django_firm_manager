from django.contrib import admin

from app_organizations.models import Worker, Organization, Bank, OrganizationFile


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('name', 'second_name', 'last_name', 'position')


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'tin', 'pprnie')


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_code', 'payment_account', 'recipient')


@admin.register(OrganizationFile)
class OrganizationFileAdmin(admin.ModelAdmin):
    pass
