from django.contrib import admin

from .models import Application, Employee

# Register your models here.
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'surname', 'email', 'phone_number', 'job', 'created_at')
    list_filter = ('job',)
    search_fields = ('first_name', 'surname', 'email', 'phone_number', 'ni_number')


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('application', 'share_code', 'passport_number', 'created_at')
    search_fields = ('application__first_name', 'application__surname', 'share_code', 'passport_number')
