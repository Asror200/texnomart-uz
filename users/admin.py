from django.contrib import admin
from django.utils.html import format_html

from users.models import User


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',
                    'username', 'email', 'data_of_birth',
                    'phone_number', 'data_joined', 'last_login',
                    'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    list_filter = ('data_joined', 'is_active', 'is_staff', 'is_superuser')

    def get_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" class="rounded-circle" style="width: 50px; height: 50px;" />',
                               obj.image.url)
        return format_html('<span> No image </span>')

    get_image.short_description = 'Image'
