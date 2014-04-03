# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView
from django.core.urlresolvers import reverse_lazy
from django.utils import timezone
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q

from todoListApp.models import TodoListTask, TodoList
from todoListApp.forms import UserProfileForm, TodoListForm, TodoListTaskForm


"""
    Vista utilizada para loguear al usuario
"""


def loginUser(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/')
    form = AuthenticationForm(request.POST or None)
    if form.is_valid:
        if 'username' and 'password' in request.POST:
            usuario = request.POST['username']
            clave = request.POST['password']
            access = authenticate(username=usuario, password=clave)
            if access is not None:
                if access.is_active:
                    login(request, access)
                    return HttpResponseRedirect('/principal')
                else:
                    return render_to_response('users/no_activo.html', context_instance=RequestContext(request))
            else:
                return render_to_response('users/no_usuario.html', context_instance=RequestContext(request))
    return render_to_response('users/login.html', {'formulario': form}, context_instance=RequestContext(request))


"""
    Vista utilizada para cerrar sesion del usuario logueado
"""


@login_required(login_url='/')
def cerrar_sesion(request):
    logout(request)
    return HttpResponseRedirect('/')


"""
    Vista utilizada para redireccionar al usuario luego de loguearse
"""


@login_required(login_url='/')
def principal(request):
    object_list = TodoList.objects.filter(share_with=request.user).order_by("-created_at")
    return render_to_response('main.html', {'object_list': object_list}, context_instance=RequestContext(request))


"""
    Vista utilizada para registrar los datos de un nuevo usuario
"""


def registrar_usuario(request):
    form = UserProfileForm(request.POST or None)
    if form.is_valid():
        cd = form.cleaned_data
        User.objects.create_user(
            # default parameters
            username=cd.get('username'),
            email=cd.get('email'),
            password=cd.get('password1'),
            # parameters **kargs
            first_name=cd.get('first_name'),
            last_name=cd.get('last_name'),
        )
        return HttpResponseRedirect('/')
    return render_to_response('users/registrar_usuario.html', {'formulario': form},
                              context_instance=RequestContext(request))


"""
    Vista utilizada para mostrar la lista de tareas del todo list, vista personalizada y
    mas especifica que la utilizada por los class based views
"""


def lista_tareas_de_todo_list(request, id_todo_list):
    if request.method == "GET":
        todo_list = get_object_or_404(TodoList, pk=id_todo_list)
        tareas = todo_list.todolisttask_set.all()
        return render_to_response('tasks/list_of_tasks.html', {'tareas': tareas, 'todo_list': todo_list},
                                  context_instance=RequestContext(request))
    return HttpResponseRedirect('/principal')


"""
    Vista utilizada para mostrar información del desarrollador
"""


def sobre(request):
    if request.method == "GET":
        return render_to_response('config/about.html', {}, context_instance=RequestContext(request))
    return HttpResponseRedirect('/')

#####################################################class based views######################################################
"""
    Vistas de tareas pertenecientes a un todo list
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


##########################################################################################################################

"""
    Vistas de todos list
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
