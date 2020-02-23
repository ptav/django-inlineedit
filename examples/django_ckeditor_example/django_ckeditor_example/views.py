from django.shortcuts import render
from django_ckeditor_example.models import Person


def index(request):
    try:
        person = Person.objects.get(id=1)
    except Person.DoesNotExist:
        person = Person(id=1, name="John")
        person.save()
    return render(request, "index.html", {"Person": person})
