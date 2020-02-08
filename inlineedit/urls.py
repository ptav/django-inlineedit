from django.urls import path

from . import views

app_name = 'inlineedit'

urlpatterns = [
    path('inlineedit_form_submit/', views.inlineedit_form_submit),
]
