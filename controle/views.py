# -*- encoding : utf-8 -*-

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf
from django.template import RequestContext

from models import Controle, Conta
from forms import ContaForm, ControleForm, UploadContaForm
from datetime import datetime


def mes_corrente(request):
    controle = Controle.get_current()

    return redirect(
        reverse(editar, kwargs={'mes': controle.mes, 'ano': controle.ano})
    )


def editar(request, mes, ano):
    controle = get_object_or_404(Controle, ano=ano, mes=mes)
    contas = controle.conta_set.all()
    form = ContaForm()

    ctx = {
        'form': form,
        'controle': controle,
        'contas': contas,
        'base_template': 'controle/base.html' if not '_pjax' in request.GET else 'controle/base_pjax.html',
    }

    ctx.update(csrf(request))

    if request.method == 'POST':
        form = ContaForm(request.POST)

    return render_to_response('controle/editar.html', ctx, RequestContext(request))


def novo(request, mes=datetime.now().month, ano=datetime.now().year):
    controle = Controle(ano=ano, mes=mes)
    form = ControleForm(instance=controle)

    ctx = {'form': form, 'controle': controle}
    ctx.update(csrf(request))

    return render_to_response('controle/novo.html', ctx, RequestContext(request))


@csrf_protect
def upload_conta(request, mes, ano, nome):
    conta = get_object_or_404(Conta, controle__ano=ano, controle__mes=mes, nome=nome)

    if request.method == 'POST':
        conta.arquivo = request.FILES.get('arquivo')
        conta.save()

        return redirect(
            reverse(editar, kwargs={'mes': conta.controle.mes, 'ano': conta.controle.ano})
        )
    else:
        form = UploadContaForm(request.POST, request.FILES, instance=conta)

        ctx = {'form': form, 'conta': conta, 'controle': conta.controle}
        ctx.update(csrf(request))

        return render_to_response('controle/upload_conta.html', ctx, RequestContext(request))


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
        return editar(request, controle.mes, controle.ano)


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

