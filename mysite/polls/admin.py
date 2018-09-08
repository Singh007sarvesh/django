from django.contrib import admin

from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
   model = Choice


class QuestionAdmin(admin.ModelAdmin):
   model = Question
   inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)