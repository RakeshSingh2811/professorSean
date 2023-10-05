from django.db import models
from django.contrib import auth
from course.models import Course


class User(auth.models.User, auth.models.PermissionsMixin):
    type = models.CharField(max_length=7, default='student', editable=False)

    def __str__(self):
        return self.username


class Subsription(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
