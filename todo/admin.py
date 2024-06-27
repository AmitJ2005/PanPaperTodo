from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Task, Learning, Profile

class TaskInline(admin.TabularInline):
    model = Task
    extra = 0

class ProfileInline(admin.StackedInline):
    model = Profile

class LearningInline(admin.TabularInline):
    model = Learning
    extra = 0

class CustomUserAdmin(BaseUserAdmin):
    inlines = [ProfileInline, TaskInline, LearningInline]

# Unregister the default User admin and register the custom User admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'due_date', 'completed')
    search_fields = ('title', 'user__username')
    list_filter = ('completed', 'due_date', 'user')
    
    actions = ['mark_as_completed', 'mark_as_not_completed']
    readonly_fields = ('user', 'due_date')

    def mark_as_completed(self, request, queryset):
        queryset.update(completed=True)
    mark_as_completed.short_description = 'Mark selected tasks as completed'

    def mark_as_not_completed(self, request, queryset):
        queryset.update(completed=False)
    mark_as_not_completed.short_description = 'Mark selected tasks as not completed'

@admin.register(Learning)
class LearningAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'content_snippet')
    search_fields = ('user__username', 'content')
    list_filter = ('date', 'user')

    def content_snippet(self, obj):
        return obj.content[:50]  # Display first 50 characters
    content_snippet.short_description = 'Content Snippet'

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_picture')
    fieldsets = (
        (None, {
            'fields': ('user',)
        }),
        ('Profile Picture', {
            'fields': ('profile_picture',)
        }),
    )
