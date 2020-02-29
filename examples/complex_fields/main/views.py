from django.shortcuts import render

from .models import Person


def index(request):
    if Person.objects.count() == 0:
        person = Person(name="John")
        person.save()

    person = Person.objects.all()[0]

    return render(request, "index.html", {"object": person})
