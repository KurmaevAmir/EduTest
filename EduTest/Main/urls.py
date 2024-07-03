from django.urls import path, include

from . import views

app_name = 'Main'
urlpatterns = [
    path("", views.HomePageView.as_view(), name='home'),
]
