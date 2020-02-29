from django.db import models
from ckeditor.fields import RichTextField


USER_CHOICES = [
    ("admin", "Admin"),
    ("user", "User"),
]


class Person(models.Model):
    name = models.CharField(max_length=30)
    approved = models.BooleanField(default=True)
    category = models.CharField(max_length=30, choices=USER_CHOICES, default="user")
    age = models.IntegerField(null=True, blank=True, verbose_name="age")
    notes = models.TextField(blank=True)
    description_explicit = models.TextField(blank=True)
    description_implicit = RichTextField(blank=True)
    description_toolbar = models.TextField(blank=True)
