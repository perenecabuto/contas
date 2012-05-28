# -*- encoding : utf-8 -*-

from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf
from models import Controle, Conta  # , ContaForm
from widgets import ContaForm


def index(request):
    controle = Controle.get_current()
    contas = controle.conta_set.all()
    return render_to_response('controle/index.html', {'contas': contas})


def new(request):
    form = ContaForm()

    if request.method == 'POST':
        form = ContaForm(request.POST)

    c = {'form': form}
    c.update(csrf(request))

    return render_to_response('controle/new.html', c)


def edit(request, id):
    conta = Conta.objects.get(pk=id)
    form = ContaForm(instance=conta)

    c = {'form': form, 'conta': conta}
    c.update(csrf(request))

    return render_to_response('controle/edit.html', c)


@csrf_protect
def save(request, id=None):
    conta = Conta()

    if id:
        conta = Conta.objects.get(pk=id)

    form = ContaForm(request.POST, request.FILES, instance=conta)

    try:
        form.save()
        return redirect(index)
    except:
        return new(request)
