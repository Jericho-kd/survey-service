from django.urls import path
from . import views


app_name = "surveys" 

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("surveys/", views.survey_list, name="survey-list"),
    path("surveys/<int:pk>/", views.survey_detail, name="survey-detail"),
    # path("surveys/create/", views.create, name="survey-create"),
    # path("surveys/<int:pk>/delete/", views.delete, name="survey-delete"),
    # path("surveys/<int:pk>/edit/", views.edit, name="survey-edit"),
    # path("surveys/<int:pk>/question/", views.question_create, name="survey-question-create"),
    # path(
    #     "surveys/<int:survey_pk>/question/<int:question_pk>/option/",
    #     views.option_create,
    #     name="survey-option-create",
    # ),
    path("surveys/<int:pk>/start/", views.survey_start, name="survey-start"),
    path("surveys/<int:survey_pk>/submit/<int:sub_pk>/", views.survey_submit, name="survey-submit"),
    path("surveys/<int:pk>/results/", views.survey_results, name="survey-results"),
]