from django.contrib import admin
from todo.models import Todo


@admin.register(Todo)
# Register your models here.
class TodoAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'todo']