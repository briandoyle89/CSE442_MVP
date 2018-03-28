from django.contrib import admin
from .models import *

# Register your models here.
#Synchronise admin/super user

admin.site.register(user)
admin.site.register(course)
admin.site.register(file)
