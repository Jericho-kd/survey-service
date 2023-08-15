from django.db import models


class Survey(models.Model):
    """Survey on a specific topic"""

    name = models.CharField(max_length=150)
    publish_date = models.DateTimeField()
    description = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    # class Meta:
    #     verbose_name = "survey"
    #     verbose_name_plural = "surveys"

    def __str__(self) -> str:
        return f"Survey '{self.name}'"
    

class Question(models.Model):
    """A survey question"""

    SELECT = "select"
    SELECT_MULTIPLE = "select-multiple"

    QUESTION_TYPES = [
        (SELECT, "Select"),
        (SELECT_MULTIPLE, "Select multiple"),
    ]

    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField(name="Text")
    type = models.CharField(name="Type", max_length=200, choices=QUESTION_TYPES, default=SELECT)

    # class Meta:
    #     verbose_name = "question"
    #     verbose_name_plural = "questions"

    def __str__(self) -> str:
        return f"Question '{self.text}'"
    

class Option(models.Model):
    """Set of possible options for question"""

    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    option_set = models.CharField(max_length=200)


class Choice(models.Model):
    """Set of answers to a survey's questions"""

    survey = models.ForeignKey(Survey, related_name='choices', on_delete=models.CASCADE)
    is_complete = models.BooleanField(default=False)


class Answer(models.Model):
    """An answer for particular survey's question"""

    choice = models.ForeignKey(Choice, related_name='choice', on_delete=models.CASCADE)
    option = models.ForeignKey(Option, related_name='option', on_delete=models.CASCADE)
