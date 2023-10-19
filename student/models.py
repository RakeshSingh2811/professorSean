from django.db import models
from django.contrib import auth
from course.models import Course


class User(auth.models.User, auth.models.PermissionsMixin):
    type = models.CharField(max_length=7, default='student', editable=False)

    def __str__(self):
        return self.username


class Order(models.Model):
    email = models.EmailField(max_length=254)
    amount = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    stripe_payment_intent = models.CharField(
        max_length=200
    )
    # This field can be changed as status
    has_paid = models.BooleanField(
        default=False,
        verbose_name='Payment Status'
    )

    def __str__(self):
        return self.email
