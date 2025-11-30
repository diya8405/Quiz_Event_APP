from django.contrib import admin
from .models import Quiz, Question, Answer, UserSubmission, UserAnswer, Event


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'description')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'quiz', 'text_preview', 'question_type', 'created_at')
    list_filter = ('question_type', 'quiz', 'created_at')
    search_fields = ('text',)
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Question Text'


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'text', 'is_correct')
    list_filter = ('is_correct',)
    search_fields = ('text',)


@admin.register(UserSubmission)
class UserSubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'quiz', 'score', 'submitted_at')
    list_filter = ('quiz', 'submitted_at')
    search_fields = ('user_name',)


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'submission', 'question', 'answer', 'is_correct')
    list_filter = ('is_correct',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date', 'location')
    list_filter = ('date',)
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'date'
