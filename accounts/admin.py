from django.contrib import admin
from accounts.models import Customer

@admin.register(Customer)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    list_editable = ['first_name', 'last_name']