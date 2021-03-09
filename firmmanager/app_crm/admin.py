from django.contrib import admin

from app_crm.models import Contractor, TypeOfContractor, FieldOfActivity, ContractorStatus, ContractorComment, \
    ContactType, ContractorContact


@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'type_of_contractor', 'position', 'name', 'second_name', 'last_name', 'country')
    list_filter = ['type_of_contractor', ]


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


@admin.register(ContactType)
class ContactTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(ContractorContact)
class ContractorContactAdmin(admin.ModelAdmin):
    pass