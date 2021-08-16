from django.contrib import admin

from app_organizations.models import Worker, Organization, OrganizationFile, WorkerContact, WorkerContactType


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'second_name', 'last_name', 'position')


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'tin', 'pprnie')


@admin.register(WorkerContactType)
class WorkerContactTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(WorkerContact)
class WorkerContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'worker', 'type_of_contact', 'contact')


@admin.register(OrganizationFile)
class OrganizationFileAdmin(admin.ModelAdmin):
    pass
