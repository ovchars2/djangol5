from django.contrib import admin
from .models import Server, ServerGroup, Notification

# Register your models here.
admin.site.register(Server)
admin.site.register(ServerGroup)
admin.site.register(Notification)