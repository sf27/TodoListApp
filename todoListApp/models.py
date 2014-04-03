# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

"""
    Modelo de los todo lists
"""
class TodoList(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(help_text='Describe la lista')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_user = models.ForeignKey(User)
    share_with = models.ManyToManyField(User, related_name="todoList", blank=True, null=True)

    def __str__(self):
        return self.title


"""
    Modelo de las tareas asociadas a un todo list
"""
class TodoListTask(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(help_text='Describe la tarea')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    HIGH, MEDIUM, LOW = 'Alta', 'Media', 'Baja'
    PRIORIDAD_OPTIONS = (
        (HIGH, 'ALTA'),
        (MEDIUM, 'MEDIA'),
        (LOW, 'BAJA'),
    )
    priority = models.CharField(max_length=6,
                                choices=PRIORIDAD_OPTIONS,
                                default=LOW)
    check = models.BooleanField(default=False)
    todo_list = models.ForeignKey(TodoList)
    created_user = models.ForeignKey(User)

    def __str__(self):
        return self.title


