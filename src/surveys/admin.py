from django.contrib import admin
from .models import Survey, Question, Option, Choice, Answer


admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Choice)
admin.site.register(Answer)