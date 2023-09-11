from django.contrib import admin

from mailing.models import Message, Mailing, MailingLog
# Register your models here.

admin.site.register(Message)
class MessageAdmin(admin.ModelAdmin):

    list_display = ('subject',)
    search_fields = ('subject', 'body')


admin.site.register(Mailing)
class MailingAdmin(admin.ModelAdmin):

    list_display = ('pk', 'send_time', 'status', 'message',)
    list_filter = ('send_time', 'status', 'frequency',)


admin.site.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):

    list_display = ('mailing', 'send_time', 'status',)
    list_filter = ('status', 'frequency')