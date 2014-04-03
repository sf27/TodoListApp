# -*- coding: utf-8 -*-
__author__ = 'elio'


from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response

from todoListApp.forms import UserProfileForm


def loginUser(request):
    """
        Vista utilizada para verificar el acceso a la aplicación
    """
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


@login_required(login_url='/')
def close_user_sesion(request):
    """
        Vista utilizada para cerrar la sesión del usuario logueado
    """
    logout(request)
    return HttpResponseRedirect('/')


def register_users(request):
    """
        Vista utilizada para registrar los datos de un nuevo usuario
    """
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

