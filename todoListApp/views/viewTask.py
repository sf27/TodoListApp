# -*- coding: utf-8 -*-
__author__ = 'elio'

from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView
from django.core.urlresolvers import reverse_lazy
from django.utils import timezone
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q

from todoListApp.models import TodoListTask, TodoList
from todoListApp.forms import TodoListTaskForm


def lists_taks_of_todo_list(request, id_todo_list):
    """
        Vista utilizada para mostrar la lista de tareas del todo list, vista personalizada y
        mas especifica que la utilizada por los class based views
    """
    if request.method == "GET":
        todo_list = get_object_or_404(TodoList, pk=id_todo_list)
        tareas = todo_list.todolisttask_set.all()
        return render_to_response('tasks/list_of_tasks.html', {'tareas': tareas, 'todo_list': todo_list},
                                  context_instance=RequestContext(request))
    return HttpResponseRedirect('/principal')




"""
    Generic Based View  - Vistas de tareas pertenecientes a un todo list
"""


class TodoListTaskDetailView(DetailView):
    #se especifica la template a utilizar por la vista
    template_name = 'tasks/todolisttask_detail.html'

    #se define el modelo o queryset, el cual retorna la lista de objetos del usuario actualmente logueado
    def get_queryset(self):
        return TodoListTask.objects.filter(created_user=self.request.user)

    #guarda la fecha del utilmo acceso
    def get_object(self):
        # Call the superclass
        object = super(TodoListTaskDetailView, self).get_object()
        # Record the last accessed date
        object.updated_at = timezone.now()
        object.save()
        # Return the object
        return object


class TodoListTaskCreateView(CreateView):
    #Modelo utilizado por la vista, es igual al query_set
    model = TodoListTask
    #utiliza un formulario personalizado
    form_class = TodoListTaskForm

    success_url = reverse_lazy('tareas_registradas')
    #se especifica la template a utilizar por la vista
    template_name = 'tasks/todolisttask_form.html'

    """
    Filtra la clave foranea, para solo mostrar los todo list creado por el usuario y no todos los todo list
    """

    def get_context_data(self, **kwargs):
        context = super(TodoListTaskCreateView, self).get_context_data(**kwargs)
        #muestra la lista de todo list a los que puede agregar tareas (Las compartidas con el o Las creadas por el mismo)
        context['form'].fields['todo_list'].queryset = TodoList.objects.filter(
            Q(created_user=self.request.user) | Q(share_with=self.request.user)).distinct()
        return context

    """
    Elimina la necesidad de seleccionar el usuario que crea la lista todo
    En vez de eso, selecciona el usuario que la crea, directamente de la sesion de usuario
    """

    def form_valid(self, form):
        form.instance.created_user = self.request.user
        return super(TodoListTaskCreateView, self).form_valid(form)


class TodoListTaskUpdateView(UpdateView):
    #Modelo utilizado por la vista, es igual al query_set
    model = TodoListTask
    #utiliza un formulario personalizado
    form_class = TodoListTaskForm

    success_url = reverse_lazy('tareas_registradas')
    #se especifica la template a utilizar por la vista
    template_name = 'tasks/todolisttask_form.html'

    """
    Filtra la clave foranea, para solo mostrar los todo list creado por el usuario y no todos los todo list
    """

    def get_context_data(self, **kwargs):
        context = super(TodoListTaskUpdateView, self).get_context_data(**kwargs)
        #muestra la lista de todo list a los que puede agregar tareas (Las compartidas con el o Las creadas por el mismo)
        context['form'].fields['todo_list'].queryset = TodoList.objects.filter(
            Q(created_user=self.request.user) | Q(share_with=self.request.user)).distinct()
        return context

    """
    Elimina la necesidad de seleccionar el usuario que crea la lista todo
    En vez de eso, selecciona el usuario que la crea, directamente de la sesion de usuario
    """

    def form_valid(self, form):
        form.instance.created_user = self.request.user

        return super(TodoListTaskUpdateView, self).form_valid(form)


class TodoListTaskDeleteView(DeleteView):
    #Modelo utilizado por la vista, es igual al query_set
    model = TodoListTask

    success_url = reverse_lazy('tareas_registradas')
    #se especifica la template a utilizar por la vista
    template_name = 'tasks/todolisttask_confirm_delete.html'


class TodoListTaskListView(ListView):
    # Especifica la template a utilizar por la vista
    template_name = 'tasks/todolisttask_list.html'

    #se define el modelo o queryset, el cual retorna la lista de objetos del usuario actualmente logueado
    def get_queryset(self):
        return TodoListTask.objects.filter(created_user=self.request.user)

