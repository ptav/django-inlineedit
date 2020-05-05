from django.contrib import admin

from .models import Person, Website


admin.site.register(Person)
admin.site.register(Website)