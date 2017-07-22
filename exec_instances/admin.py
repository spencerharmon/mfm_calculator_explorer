from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(ExecInstance)
admin.site.register(AEPS)
admin.site.register(Site)
admin.site.register(RegisteredElement)
