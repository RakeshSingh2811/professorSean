from django.contrib import admin
from . import models
# Register your models
admin.site.register(models.User)
admin.site.register(models.Order)
