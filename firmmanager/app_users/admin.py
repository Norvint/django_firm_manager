from django.contrib import admin

from app_users.models import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass