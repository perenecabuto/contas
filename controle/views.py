# -*- encoding : utf-8 -*-

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf
from models import Controle, Conta
from forms import ContaForm, ControleForm
from datetime import datetime


def index(request):
    controles = Controle.objects.all()
    return render_to_response('controle/index.html', {'controles': controles})


def mes_corrente(request):
    controle = Controle.get_current()

    return redirect(
        reverse(editar, kwargs={'mes': controle.mes, 'ano': controle.ano})
    )


def editar(request, mes, ano):
    controle = get_object_or_404(Controle, ano=ano, mes=mes)
    contas = controle.conta_set.all()

    form = ContaForm()

    if request.method == 'POST':
        form = ContaForm(request.POST)

    ctx = {'form': form, 'controle': controle, 'contas': contas}
    ctx.update(csrf(request))

    return render_to_response('controle/editar.html', ctx)


def novo(request, mes=datetime.now().month, ano=datetime.now().year):
    controle = Controle(ano=ano, mes=mes)
    form = ControleForm(instance=controle)

    ctx = {'form': form, 'controle': controle}
    ctx.update(csrf(request))

    return render_to_response('controle/novo.html', ctx)


@csrf_protect
def salvar(request):
    controle = Controle()
    form = ControleForm(request.POST, request.FILES, instance=controle)

    try:
        form.save()
        return redirect(
            reverse(editar, kwargs={'mes': controle.mes, 'ano': controle.ano})
        )
    except:
        return novo(request)


@csrf_protect
def salvar_conta(request, mes, ano, nome=None):
    controle = get_object_or_404(Controle, ano=ano, mes=mes)
    conta = Conta(controle=controle)

    qs = controle.conta_set.filter(nome=nome)

    if qs.exists():
        conta = qs.get()

    form = ContaForm(request.POST, request.FILES, instance=conta)

    try:
        form.save()
        return redirect(
            reverse(editar, kwargs={'mes': controle.mes, 'ano': controle.ano})
        )
    except:
        request.POST['show_form'] = True
        return editar(request, mes, ano)


@csrf_protect
def registrar_pagamento(request, mes, ano, nome):
    conta = get_object_or_404(Conta, controle__ano=ano, controle__mes=mes, nome=nome)
    conta.registrar_pagamento()

    return redirect(
        reverse(editar, kwargs={'mes': conta.controle.mes, 'ano': conta.controle.ano})
    )
