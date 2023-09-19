from django.contrib import admin

from blog.models import Blog

# Register your models here.
admin.site.register(Blog)


class BlogAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.groups.filter(name='Контент-менеджеры').exists()

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name='Контент-менеджеры').exists()

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name='Контент-менеджеры').exists()

