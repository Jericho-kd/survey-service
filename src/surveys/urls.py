from django.urls import path
from . import views


app_name = "surveys" 

urlpatterns = [
    # path("", views.homepage, name="homepage"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login")
]