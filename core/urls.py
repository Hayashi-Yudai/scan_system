from django.urls import path

from . import views

app_name = "core"
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('move/', views.move, name='move'),
    path('save/', views.save, name='save'),
    path('scan/', views.scan, name='scan'),
    path('gpib/', views.gpib, name='gpib'),
]
