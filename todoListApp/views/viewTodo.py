# -*- coding: utf-8 -*-
__author__ = 'elio'

from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView
from django.core.urlresolvers import reverse_lazy
from django.utils import timezone
from django.db.models import Q

from todoListApp.models import TodoListTask, TodoList
from todoListApp.forms import TodoListForm

"""
    Generic Based View  - Vistas de todos list
"""


class TodoListDetailView(DetailView):
    #se especifica el path de la template a utilizar por la vista
    template_name = "todos/todolist_detail.html"

    #guarda la fecha del utilmo acceso
    def get_object(self):
        # Call the superclass
        object = super(TodoListDetailView, self).get_object()
        # Record the last accessed date
        object.updated_at = timezone.now()
        object.save()
        # Return the object
        return object


    #se define el modelo o queryset, el cual retorna la lista de objetos

    def get_queryset(self):
        return TodoList.objects.all()

    def get_context_data(self, **kwargs):
        context = super(TodoListDetailView, self).get_context_data(**kwargs)
        """
            Se consultan las tareas del todo list seleccionado en la vista,
            y se agrega al contexto de las plantillas para mostrarlos en las plantillas
        """
        context['tareas'] = TodoListTask.objects.filter(todo_list=self.object)

        return context


class TodoListCreateView(CreateView):
    #Modelo utilizado por la vista, es igual al query_set
    model = TodoList
    #utiliza un formulario personalizado
    form_class = TodoListForm

    success_url = reverse_lazy('todolist_registrados')
    #se especifica el path de la template a utilizar por la vista
    template_name = "todos/todolist_form.html"

    """
    Elimina la necesidad de seleccionar el usuario que crea la lista todo
    En vez de eso, selecciona el usuario que la crea, directamente de la sesion de usuario
    """

    def form_valid(self, form):
        form.instance.created_user = self.request.user
        return super(TodoListCreateView, self).form_valid(form)


    """
    Filtra la clave foranea, para no mostrar al usuario logueado en la lista de usuario a compartir
    """

    def get_context_data(self, **kwargs):
        context = super(TodoListCreateView, self).get_context_data(**kwargs)
        #se cargan en la lista todos los usuarios pero sin agregar al usuario logueado o el usuario que crea el registro
        context['form'].fields['share_with'].queryset = User.objects.filter(~Q(username=self.request.user))
        return context


class TodoListUpdateView(UpdateView):
    #Modelo utilizado por la vista, es igual al query_set
    model = TodoList
    #utiliza un formulario personalizado
    form_class = TodoListForm
    success_url = reverse_lazy('todolist_registrados')
    #se especifica el path de la template a utilizar por la vista
    template_name = "todos/todolist_form.html"

    """
    Elimina la necesidad de seleccionar el usuario que crea la lista todo
    En vez de eso, selecciona el usuario que la crea, directamente de la sesion de usuario
    """

    def form_valid(self, form):
        form.instance.created_user = self.request.user
        return super(TodoListUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TodoListUpdateView, self).get_context_data(**kwargs)
        #se cargan en la lista todos los usuarios pero sin agregar al usuario logueado o el usuario que crea el registro
        context['form'].fields['share_with'].queryset = User.objects.filter(~Q(username=self.request.user))
        return context


class TodoListDeleteView(DeleteView):
    #Modelo utilizado por la vista, es igual al query_set
    model = TodoList
    success_url = reverse_lazy('todolist_registrados')
    #se especifica el path de la template a utilizar por la vista
    template_name = "todos/todolist_confirm_delete.html"


class TodoListListView(ListView):
    #se especifica el path de la template a utilizar por la vista
    template_name = 'todos/todolist_list.html'

    #se define el modelo o queryset, el cual retorna la lista de objetos del usuario actualmente logueado
    def get_queryset(self):
        return TodoList.objects.filter(created_user=self.request.user)
