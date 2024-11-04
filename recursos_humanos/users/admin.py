from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import UserModel, ConversationThreadModel, ConversationMessageModel


class UserAdmin(BaseUserAdmin):

    list_display = ('id', 'username', 'first_name', 'middle_name',
                    'last_name', 'contract_type', 'base_salary', 'vacation_days',
                    'job_title', 'department', 'plant', 'created_at', 'updated_at',
                    'is_active', 'is_staff', 'is_superuser')

    add_fieldsets = (
        (
            None, {
                'classes': ('wide',),
                'fields': ('username', 'first_name', 'middle_name', 'last_name', 'password1', 'password2', 'contract_type', 'base_salary', 'vacation_days',
                           'job_title', 'department', 'plant', 'groups', 'is_active', 'is_staff', 'is_superuser',)
            }
        ),
    )

    fieldsets = (
        (
            None, {
                'fields': ('username', 'first_name', 'middle_name', 'last_name', 'password', 'contract_type', 'base_salary', 'vacation_days',
                           'job_title', 'department', 'plant', 'groups', 'is_active', 'is_staff', 'is_superuser', 'created_at', 'updated_at')
            }
        ),
    )

    readonly_fields = ('created_at', 'updated_at')


admin.site.register(UserModel, UserAdmin)
admin.site.register(ConversationMessageModel)
admin.site.register(ConversationThreadModel)
