from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.auth.decorators import login_required

from todoListApp.views.viewTask import TodoListTaskCreateView, TodoListTaskDeleteView, TodoListTaskUpdateView, TodoListTaskDetailView, TodoListTaskListView
from todoListApp.views.viewTodo import TodoListCreateView, TodoListDeleteView, TodoListUpdateView, TodoListDetailView, TodoListListView

admin.autodiscover()

login_url = '/'
urlpatterns = patterns('',
                       #login view
                       url(r'^$', 'todoListApp.views.viewUser.loginUser', name='inicio'),

                       #close sesion -> need to be login
                       url(r'^cerrar-sesion/$', 'todoListApp.views.viewUser.close_user_sesion', name='cerrar_sesion'),

                       #register new user
                       url(r'^registrar-usuario/$', 'todoListApp.views.viewUser.register_users',
                           name='registrar_usuario'),

                       #main view -> need to be login
                       url(r'^principal/$', 'todoListApp.views.viewMain.main', name='principal'),

                       #about view
                       url(r'^sobre/$', 'todoListApp.views.viewMain.about', name='sobre'),

                       #list of task from the id of todo list
                       url(r'lista_tareas_de_todolist/(?P<id_todo_list>\d+)/$',
                           'todoListApp.views.viewTask.lists_taks_of_todo_list', name="lista_tareas_de_todolist"),

                       #taks
                       #ListView
                       url(r'^tareas_registrados/$', login_required(TodoListTaskListView.as_view(), login_url),
                           name='tareas_registradas'),
                       #DetailView
                       url(r'^tarea/(?P<pk>\d+)/detalles/$',
                           login_required(TodoListTaskDetailView.as_view(), login_url),
                           name='tarea_detalles'),
                       #CreateView
                       url(r'tarea/agregar/$', login_required(TodoListTaskCreateView.as_view(), login_url),
                           name='tarea_guardar'),
                       #UpdateView
                       url(r'tarea/(?P<pk>\d+)/$', login_required(TodoListTaskUpdateView.as_view(), login_url),
                           name='tarea_modificar'),
                       #DeleteView
                       url(r'tarea/(?P<pk>\d+)/eliminar/$', login_required(TodoListTaskDeleteView.as_view(), login_url),
                           name='tarea_eliminar'),
                       #todos
                       #ListView
                       url(r'^todolist_registrados/$', login_required(TodoListListView.as_view(), login_url),
                           name='todolist_registrados'),
                       #DetailView
                       url(r'^todolist/(?P<pk>\d+)/detalles/$', login_required(TodoListDetailView.as_view(), login_url),
                           name='todolist_detalles'),
                       #CreateView
                       url(r'todolist/agregar/$', login_required(TodoListCreateView.as_view(), login_url),
                           name='todolist_guardar'),
                       #UpdateView
                       url(r'todolist/(?P<pk>\d+)/$', login_required(TodoListUpdateView.as_view(), login_url),
                           name='todolist_modificar'),
                       #DeleteView
                       url(r'todolist/(?P<pk>\d+)/eliminar/$', login_required(TodoListDeleteView.as_view(), login_url),
                           name='todolist_eliminar'),

                       #admin
                       #admin view
                       url(r'^admin/', include(admin.site.urls)),
)
