from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import UserRegisterForm


from django.views.generic.edit import CreateView

class SignUpView(SuccessMessageMixin, CreateView):
  template_name = 'auth/signup.html'
  success_url = reverse_lazy('login')
  form_class = UserRegisterForm
  success_message = "Your profile was created successfully"


# def login_request(request):
# 	if request.method == "POST":
# 		form = AuthenticationForm(request, data=request.POST)
# 		if form.is_valid():
# 			username = form.cleaned_data.get('username')
# 			password = form.cleaned_data.get('password')
# 			user = authenticate(username=username, password=password)
# 			if user is not None:
# 				login(request, user)
# 				messages.info(request, f"You are now logged in as {username}.")
# 				return redirect("base")
# 			else:
# 				messages.error(request,"Invalid username or password.")
# 		else:
# 			messages.error(request,"Invalid username or password.")
# 	form = AuthenticationForm()
# 	return render(request=request, template_name="auth/login.html", context={"login_form":form})
class LoginView(BaseLoginView):
    template_name = "auth/login.html"
    redirect_authenticated_user = True


login = LoginView.as_view()
signup = SignUpView.as_view()