from django.contrib import admin

from app_crm.models import Contractor, TypeOfContractor, FieldOfActivity, ContractorStatus, ContractorComment, \
    ContactPersonContactType, ContractorContactPersonContact, ContractorContactPerson, ContractorFileCategory, \
    ContractorFile, LeadStatus, Lead, ContractorRequisites, LeadContact, LeadContactPerson, LeadContactPersonContact, \
    LeadContactType


@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'type_of_contractor', 'position', 'name', 'second_name', 'last_name', 'country')
    list_filter = ['type_of_contractor', ]


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


@admin.register(ContractorComment)
class ContractorCommentAdmin(admin.ModelAdmin):
    pass


@admin.register(ContactPersonContactType)
class ContactPersonContactTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(ContractorContactPersonContact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['contact_person', 'type_of_contact', 'contact']


@admin.register(ContractorContactPerson)
class ContractorContactPersonAdmin(admin.ModelAdmin):
    list_display = ['contractor', 'last_name', 'name', 'position']


@admin.register(ContractorFileCategory)
class ContractorFileCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(ContractorFile)
class ContractorFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'contractor', 'description', 'category')
    list_filter = ['category',]
    search_fields = ('contractor__title', 'title')


@admin.register(LeadStatus)
class LeadStatusAdmin(admin.ModelAdmin):
    list_display = ['title', ]


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    pass


@admin.register(LeadContact)
class LeadContactAdmin(admin.ModelAdmin):
    list_display = ['lead', 'type_of_contact', 'contact']


@admin.register(LeadContactPerson)
class LeadContactPersonAdmin(admin.ModelAdmin):
    list_display = ['lead', 'last_name', 'name', 'position']


@admin.register(LeadContactPersonContact)
class LeadContactPersonContactAdmin(admin.ModelAdmin):
    list_display = ['contact_person', 'type_of_contact', 'contact']


@admin.register(LeadContactType)
class LeadContactTypeAdmin(admin.ModelAdmin):
    list_display = ['title',]
