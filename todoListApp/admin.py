from django.contrib import admin

# Register your models here.
from todoListApp.models import TodoList, TodoListTask


class TodoListAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_user')


class TodoListTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'todo_list')

admin.site.register(TodoList, TodoListAdmin)
admin.site.register(TodoListTask, TodoListTaskAdmin)