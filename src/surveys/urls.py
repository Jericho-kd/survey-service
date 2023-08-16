from django.urls import path
from . import views


app_name = "surveys" 

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("surveys/", views.survey_list, name="survey-list"),
    path("surveys/<int:pk>/", views.survey_detail, name="survey-detail"),
    path("surveys/<int:pk>/start/", views.survey_start, name="survey-start"),
    path("surveys/<int:survey_pk>/submit/<int:sub_pk>/", views.survey_submit, name="survey-submit"),
    path("surveys/<int:pk>/results/", views.survey_results, name="survey-results"),
]