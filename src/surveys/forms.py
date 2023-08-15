from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Survey, Question, Option

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name']


class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ["survey_name"]


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["question_title"]


class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ["option_title", "is_correct"]


class AnswerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        options = kwargs.pop("options")
        choices = {(o.pk, o.option_title) for o in options}
        super().__init__(*args, **kwargs)
        option_field = forms.ChoiceField(choices=choices, widget=forms.Select, required=True)
        self.fields["option"] = option_field


class BaseAnswerFormSet(forms.BaseFormSet):
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs["options"] = kwargs["options"][index]
        return kwargs
