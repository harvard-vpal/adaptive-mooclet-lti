from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Mooclet)
admin.site.register(Version)
admin.site.register(Variable)
admin.site.register(Value)
admin.site.register(Policy)