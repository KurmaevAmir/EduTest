from django.urls import path

from . import views

app_name = "constructor"
urlpatterns = [
    path("test/", views.TestCreateView.as_view(), name='test_create'),
    path("test/<int:pk>", views.TestUpdateView.as_view(), name='test_update'),
    path("test/<int:pk>/question/<int:number>", views.QuestionCreateView.as_view(), name='question')
]
