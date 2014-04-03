# -*- coding: utf-8 -*-


from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from todoListApp.models import TodoList


__author__ = 'elio'


@login_required(login_url='/')
def main(request):
    """
        Vista utilizada para redireccionar al usuario luego de loguearse, la plantilla principal
    """
    object_list = TodoList.objects.filter(share_with=request.user).order_by("-created_at")
    return render_to_response('main.html', {'object_list': object_list}, context_instance=RequestContext(request))


@login_required(login_url='/')
def about(request):
    """
        Vista utilizada para mostrar información del desarrollador
    """
    if request.method == "GET":
        return render_to_response('config/about.html', {}, context_instance=RequestContext(request))
    return HttpResponseRedirect('/')
