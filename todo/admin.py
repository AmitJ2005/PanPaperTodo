from django.contrib import admin
from .models import Task, Learning

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'due_date', 'completed')
    search_fields = ('title', 'user__username')
    list_filter = ('completed', 'due_date', 'user')

@admin.register(Learning)
class LearningAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'content')
    search_fields = ('user__username', 'content')
    list_filter = ('date', 'user')
