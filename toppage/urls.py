from django.urls import path

from . import views

app_name = "toppage"
urlpatterns = [path("", views.index, name="index")]
