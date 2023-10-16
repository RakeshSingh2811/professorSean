from django.db import models
from django.contrib import auth
from course.models import Course


class User(auth.models.User, auth.models.PermissionsMixin):
    type = models.CharField(max_length=7, default='student', editable=False)

    def __str__(self):
        return self.username


class Order(models.Model):
    email = models.EmailField(max_length=254)
    paid = models.BooleanField(default="False")
    amount = models.IntegerField(default=0)
    description = models.CharField(default=None, max_length=800)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.email
