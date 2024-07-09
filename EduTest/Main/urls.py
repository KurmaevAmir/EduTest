from django.urls import path, include

from . import views

app_name = 'Main'
urlpatterns = [
    path("", views.HomePageView.as_view(), name='home'),
    path("test/<int:pk>/", views.TestDescriptionView.as_view(), name='test_description'),
    path("test/assign/create/<int:pk>/", views.TestAssignmentView.as_view(), name='test_assign_create'),
    path("test/<int:option_id>/question/<int:question_number>/", views.TestFormView.as_view(), name='test_form'),
    path("test/result/<int:pk>/", views.TestResultView.as_view(), name='test_result')
]
