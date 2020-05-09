from django.shortcuts import render

from .models import Person, Website


def index(request, template="index"):
    if Person.objects.count() == 0:
        web = Website(label="WeDidIt", url="https://www.wedidit.app")
        web.save()

        person = Person(name="John", age=20, website=web)
        person.save()

    person = Person.objects.all()[0]

    return render(request, f"{template}.html", {"object": person})
