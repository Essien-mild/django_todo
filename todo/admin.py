from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'priority', 'deadline', 'created_at')
    list_filter = ('priority', 'deadline')
    search_fields = ('title', 'description')