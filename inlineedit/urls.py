from django.urls import path

from . import views

app_name = 'inlineedit'

urlpatterns = [
    path('', views.inlineedit_form_submit, name="inlineedit"),
]
