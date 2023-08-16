from django.db import models
from django.utils import timezone
from typing import Any


class Survey(models.Model):
    """Survey on a specific topic"""

    survey_name = models.CharField(max_length=150)
    publish_date = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    answers: dict[str, Any] = {}

    def __str__(self) -> str:
        return f"Survey '{self.survey_name}'"
    

class Question(models.Model):
    """A survey question"""

    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE)
    question_title = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"Question '{self.question_title}'"
    

class Option(models.Model):
    """Option for question"""

    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    option_title = models.CharField(max_length=200)
    is_correct = models.BooleanField()

    class Meta:
        ordering = ['?']

    def __str__(self) -> str:
        return f"Option '{self.option_title}' for {self.question}"


class Choice(models.Model):
    """Set of answers to a survey's questions"""

    survey = models.ForeignKey(Survey, related_name='choices', on_delete=models.CASCADE)
    is_complete = models.BooleanField(default=False)


class Answer(models.Model):
    """An answer for particular survey's question"""

    choice = models.ForeignKey(Choice, related_name='choice', on_delete=models.CASCADE)
    option = models.ForeignKey(Option, related_name='option', on_delete=models.CASCADE)
