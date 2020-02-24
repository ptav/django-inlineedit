from django.db import models
from ckeditor.fields import RichTextField


class Person(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=30)
    user_type = models.CharField(choices=[
        ("Admin", "Admin"),
        ("User", "User")
    ], max_length=30, default="User", verbose_name="account type")
    user_age = models.IntegerField(null=True, verbose_name="age")
    user_description = RichTextField(null=True, verbose_name="description")
    custom_styling_user_description = RichTextField(null=True, verbose_name="description")
