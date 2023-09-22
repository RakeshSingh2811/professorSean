from django.contrib import admin
from . import models

admin.site.register(models.Course)
admin.site.register(models.Chapter)
admin.site.register(models.Topic)
# Register your models here.
