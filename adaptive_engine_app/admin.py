from django.contrib import admin

# Register your models here.
from .models import Component, Version

admin.site.register(Component)
admin.site.register(Version)
admin.site.register(Result)
