from django.db import models
from ckeditor.fields import RichTextField


USER_CHOICES = [
    ("a", "Admin"),
    ("b", "User"),
]

INTEGER_CHOICES = [
    (0, "Zero"),
    (1, "One"),
    (2, "Two"),
    (3, "Three"),
]

class Person(models.Model):
    name = models.CharField(max_length=30)
    approved = models.BooleanField(default=True)
    category = models.CharField(max_length=30, choices=USER_CHOICES, default="user")
    intchoices = models.IntegerField(choices=INTEGER_CHOICES, default=0)
    age = models.IntegerField(null=True, blank=True, verbose_name="age")
    notes = models.TextField(blank=True)


    description_explicit = models.TextField(blank=True)
    description_implicit = RichTextField(blank=True)
    description_toolbar = models.TextField(blank=True)

    amount = models.FloatField(blank=True, null=True)

    website = models.ForeignKey("Website", null=True, on_delete=models.CASCADE)

    date = models.DateField(null=True,blank=True)


class Website(models.Model):
    url = models.URLField("URL")
    label = models.CharField("Label", max_length=32)
