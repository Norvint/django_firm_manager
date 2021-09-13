from django.contrib import admin

from app_organizations.models import Worker, Organization, OrganizationFile, WorkerContact, WorkerContactType


class WorkerContactInline(admin.TabularInline):
    model = WorkerContact


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'second_name', 'last_name', 'position')
    inlines = [WorkerContactInline]


class OrganizationFileInline(admin.StackedInline):
    model = OrganizationFile
    extra = 0


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'tin', 'pprnie')
    inlines = [OrganizationFileInline]


@admin.register(WorkerContactType)
class WorkerContactTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')