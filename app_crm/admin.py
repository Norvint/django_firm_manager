from django.contrib import admin

from app_crm.models import Contractor, TypeOfContractor, FieldOfActivity, ContractorStatus, ContractorComment, \
    ContactPersonContactType, ContractorContactPersonContact, ContractorContactPerson, ContractorFileCategory, \
    ContractorFile, LeadStatus, Lead, ContractorRequisites, LeadContact, LeadContactPerson, LeadContactPersonContact, \
    LeadContactType, ContractorContactType, ContractorContact


class ContractorContactInline(admin.TabularInline):
    model = ContractorContact


class ContractorCommentInline(admin.TabularInline):
    model = ContractorComment
    extra = 0


class ContractorFileInline(admin.StackedInline):
    model = ContractorFile
    extra = 0


@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'type_of_contractor', 'position', 'name', 'second_name', 'last_name', 'country',
                    'to_delete')
    list_filter = ['type_of_contractor', ]
    inlines = [ContractorContactInline, ContractorCommentInline, ContractorFileInline]


@admin.register(ContractorContactType)
class ContractorContactTypeAdmin(admin.ModelAdmin):
    list_display = ['title',]


@admin.register(ContractorRequisites)
class ContractorRequisitesAdmin(admin.ModelAdmin):
    pass


@admin.register(TypeOfContractor)
class TypeOfContractorAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(FieldOfActivity)
class FieldOfActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(ContractorStatus)
class ContractorStatusAdmin(admin.ModelAdmin):
    pass


@admin.register(ContactPersonContactType)
class ContactPersonContactTypeAdmin(admin.ModelAdmin):
    pass


class ContractorContactPersonContactInline(admin.TabularInline):
    model = ContractorContactPersonContact


@admin.register(ContractorContactPerson)
class ContractorContactPersonAdmin(admin.ModelAdmin):
    list_display = ['pk', 'contractor', 'last_name', 'name', 'position']
    inlines = [ContractorContactPersonContactInline]


@admin.register(ContractorFileCategory)
class ContractorFileCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(LeadStatus)
class LeadStatusAdmin(admin.ModelAdmin):
    list_display = ['title', ]


class LeadContactInline(admin.TabularInline):
    model = LeadContact


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    inlines = [LeadContactInline]


class LeadContactPersonContactInline(admin.TabularInline):
    model = LeadContactPersonContact


@admin.register(LeadContactPerson)
class LeadContactPersonAdmin(admin.ModelAdmin):
    list_display = ['lead', 'last_name', 'name', 'position']
    inlines = [LeadContactPersonContactInline]


@admin.register(LeadContactType)
class LeadContactTypeAdmin(admin.ModelAdmin):
    list_display = ['title',]
