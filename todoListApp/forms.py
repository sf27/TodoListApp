# -*- coding: utf-8 -*-
__author__ = 'elio'
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from todoListApp.models import TodoList, TodoListTask

"""
    Formulario personalizado para registrar un nuevo usuario al sistema
"""


class UserProfileForm(ModelForm):
    """
        Se agregaron dos nuevos campos para verificar la contraseña
    """
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput,
                                error_messages={'required': ('Debe ingresar su contraseña.'),
                                                'invalid': ('Ingrese un contraseña valida')})
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput,
                                error_messages={'required': ('Debe ingresar de nuevo su contraseña.'),
                                                'invalid': ('Ingrese un contraseña valida')})

    class Meta:
        #modelo a utilizar, el modelo de usuario del sistema de django
        model = User
        #los campos a utilizar provenientos del modelo de django
        fields = ('username', 'first_name', 'last_name', 'email')
        #se le cambian los nombres
        labels = {
            'username': ("Usuario"),
            'first_name': ('Nombre'),
            'last_name': ('Apellido'),
            'email': ('Email'),
        }
        #texto de ayuda al usuario
        help_texts = {
            'username': ('Obligatorio. 30 caracteres o menos. Letras, números y @ / / + / -. / _ Caracteres'),
            'first_name': ('Ejemplo: Pedro'),
            'last_name': ('Ejemplo: Martinez'),
            'email': ('Ejemplo: example@gmail.com'),
        }
        #modifica los mensajes de error arrojados por el formulario
        error_messages = {
            'username': {
                'required': ('Debe ingresar su usuario.'),
                'invalid': ('Ingrese un usuario valido')
            },
            'first_name': {
                'required': ('Debe ingresar su nombre.'),
                'invalid': ('Ingrese un dato valido')
            },
            'last_name': {
                'required': ('Debe ingresar su apellido.'),
                'invalid': ('Ingrese un dato valido')
            },
            'email': {
                'required': ('Debe ingresar su correo electronico.'),
                'invalid': ('Ingrese un dato valido')
            },
        }

    """
        Se verifica que las contraseñas coincidan
    """

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

    """
        Se establece el password en el modelo y se guarda
    """

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserProfileForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    """
        Configuración inicial del formulario para agregar atributos a los campos (clases css y placeholders)
    """

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese su usuario'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese su nombre'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese su apellido'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese su email'})
        self.fields['email'].required = True
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese su contraseña'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Repita su coontraseña'})


"""
    Formulario personalizado utilizar en las class based views del modelo todo list
"""


class TodoListForm(ModelForm):
    class Meta:
        #modelo a utilizar
        model = TodoList
        #se excluye el campo created_user para evitar que el usuario deba seleccionarlo de un combo
        exclude = ('created_user',)
        #se le cambian los nombres
        labels = {
            'title': ("Titulo"),
            'description': ('Descripción'),
            'share_with': ('Compartido con:'),
        }
        #texto de ayuda al usuario
        help_texts = {
            'title': ('Ejemplo: Rebajar'),
            'description': ('Ejemplo: Bajar dos kilos al mes'),
            'share_with': ('Ejemplo: root, toor'),
        }
        #modifica los mensajes de error arrojados por el formulario
        error_messages = {
            'title': {
                'required': ('Debe ingresar un titulo válido.'),
                'invalid': ('Ingrese un titulo valido')
            },
            'description': {
                'required': ('Debe ingresar una descripción.'),
                'invalid': ('Ingrese una descripción valida')
            },
        }

    """
        Configuración inicial del formulario para agregar atributos a los campos (clases css y placeholders)
    """

    def __init__(self, *args, **kwargs):
        super(TodoListForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese un titulo'})
        self.fields['description'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Ingrese una descripcion'})
        #lista, no utiliza placeholder
        self.fields['share_with'].widget.attrs.update({'class': 'form-control'})


class TodoListTaskForm(ModelForm):
    class Meta:
        #modelo a utilizar por el formulario
        model = TodoListTask
        #se excluye el campo created_user para evitar que el usuario deba seleccionarlo de un combo
        exclude = ('created_user',)
        #se le cambian los nombres
        labels = {
            'title': ("Titulo"),
            'description': ('Descripción'),
            'priority': ('Prioridad'),
            'check': ('Hecha'),
            'todo_list': ('Todo list asociada'),
        }
        #texto de ayuda al usuario
        help_texts = {
            'title': ('Ejemplo: Tomar mas agua'),
            'description': ('Ejemplo: Dos litros de agua diarío'),
            'priority': ('Seleccione de la lista'),
            'check': ('Si ya cumplió la tarea, marque el campo'),
            'todo_list': ('Selecciona la lista a la cual pertenece la tarea'),
        }
        #modifica los mensajes de error arrojados por el formulario
        error_messages = {
            'title': {
                'required': ('Debe ingresar un titulo válido.'),
                'invalid': ('Ingrese un titulo valido')
            },
            'description': {
                'required': ('Debe ingresar una descripción.'),
                'invalid': ('Ingrese una descripción valida')
            },
            'priority': {
                'required': ('Debe seleccionar una prioridad.'),
                'invalid': ('Ingrese una prioridad valida')
            },
            'todo_list': {
                'required': ('Debe seleccionar un todo list.'),
                'invalid': ('Ingrese un todo list valido')
            },
        }

    """
        Configuración inicial del formulario para agregar atributos a los campos (clases css y placeholders)
    """

    def __init__(self, *args, **kwargs):
        super(TodoListTaskForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ingrese un titulo'})
        self.fields['description'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Ingrese una descripcion'})
        self.fields['priority'].widget.attrs.update({'class': 'form-control'})
        self.fields['check'].widget.attrs.update({'class': 'form-control radio'})
        self.fields['todo_list'].widget.attrs.update({'class': 'form-control'})
