from django.urls import path

from main.views import webhook

urlpatterns = [
    path('webhook/', webhook),
]
