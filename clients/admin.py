from django.contrib import admin
from clients.models import Client


admin.site.register(Client)
class ClientAdmin(admin.ModelAdmin):

    list_display = ('full_name', 'email',)
    search_fields = ('full_name', 'email')

