from django.contrib import admin
from posts.models import Message, Channel


class MessageInline(admin.TabularInline):
    model = Message


class ChannelAdmin(admin.ModelAdmin):
    model = Channel
    inlines = [MessageInline]


admin.site.register(Channel, ChannelAdmin)
