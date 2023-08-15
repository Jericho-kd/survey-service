from django.contrib import messages
from django.db import transaction
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.handlers.wsgi import WSGIRequest
from django.forms.formsets import formset_factory
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from .forms import UserRegisterForm, SurveyForm, QuestionForm, OptionForm, AnswerForm, BaseAnswerFormSet
from .models import Survey, Question, Answer, Choice, Option


class SignUpView(SuccessMessageMixin, CreateView):
  template_name = 'auth/signup.html'
  success_url = reverse_lazy('login')
  form_class = UserRegisterForm
  success_message = "Your profile was created successfully"


class LoginView(BaseLoginView):
    template_name = "auth/login.html"
    redirect_authenticated_user = True


class HomePageView(TemplateView):
    template_name = "homepage.html"


login = LoginView.as_view()
signup = SignUpView.as_view()
homepage = HomePageView.as_view()


@login_required
def survey_list(request: WSGIRequest) -> HttpResponse:
    """User can view all their surveys"""
    surveys = Survey.objects.order_by("-publish_date").all()
    return render(request, "survey/list.html", {"surveys": surveys})


@login_required
def survey_detail(request: WSGIRequest, pk: int) -> HttpResponse:
    """User can view an active survey"""
    try:
        survey = Survey.objects.get(pk=pk, is_active=True)
    except Survey.DoesNotExist:
        raise Http404()

    questions = survey.questions.all()

    host = request.get_host()
    public_path = reverse_lazy("surveys:survey-start", args=[pk])
    public_url = f"{request.scheme}://{host}{public_path}"
    num_submissions = survey.choices.filter(is_complete=True).count()
    return render(
        request,
        "survey/detail.html",
        {
            "survey": survey,
            "public_url": public_url,
            "questions": questions,
            "num_submissions": num_submissions,
        },
    )


def survey_start(request: WSGIRequest, pk: int) -> HttpResponse:
    """User start a survey"""

    survey = get_object_or_404(Survey, pk=pk, is_active=True)
    if request.method == "POST":
        sub = Choice.objects.create(survey=survey)
        return redirect("surveys:survey-submit", survey_pk=pk, sub_pk=sub.pk)

    return render(request, "survey/start.html", {"survey": survey})


def survey_submit(request: WSGIRequest, survey_pk: int, sub_pk: int) -> HttpResponse:
    """Submit survey"""

    try:
        survey = Survey.objects.prefetch_related("questions__options").get(pk=survey_pk, is_active=True)
    except Survey.DoesNotExist:
        raise Http404()

    try:
        sub = survey.choices.get(pk=sub_pk, is_complete=False)
    except Choice.DoesNotExist:
        raise Http404()
    
    correct_choices = Option.objects.filter(is_correct=True).order_by('question_id').values()
    questions = survey.questions.all()
    options = [q.options.all() for q in questions]
    form_kwargs = {"empty_permitted": False, "options": options}
    AnswerFormSet = formset_factory(AnswerForm, extra=len(questions), formset=BaseAnswerFormSet)

    correct_answers = 0
    if request.method == "POST":
        formset = AnswerFormSet(request.POST, form_kwargs=form_kwargs)
        if formset.is_valid():
            with transaction.atomic():
                for form in formset:
                    Answer.objects.create(option_id=form.cleaned_data["option"], choice_id=sub_pk)
                   # think about proper way to compute number of right answers

                sub.is_complete = True
                sub.save()
            return redirect("surveys:survey-results", pk=survey_pk)
    else:
        formset = AnswerFormSet(form_kwargs=form_kwargs)

    question_forms = zip(questions, formset)
    return render(
        request,
        "survey/submit.html",
        {"survey": survey, "question_forms": question_forms, "formset": formset},
    )


def survey_results(request: WSGIRequest, pk: int) -> HttpResponse:
    """User receives results"""

    survey = get_object_or_404(Survey, pk=pk, is_active=True)
    return render(request, "survey/results.html", {"survey": survey})