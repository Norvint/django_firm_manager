from django.contrib import admin

from app_organizations.models import Worker, Organization, OrganizationFile


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('name', 'second_name', 'last_name', 'position')


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'tin', 'pprnie')


@admin.register(OrganizationFile)
class OrganizationFileAdmin(admin.ModelAdmin):
    pass
