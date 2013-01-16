# -*- encoding : utf-8 -*-

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf
from django.template import RequestContext
from django.http import Http404

from models import Controle, Conta
from forms import ContaForm, ControleForm, UploadContaForm
from datetime import datetime, date


def mes_corrente(request):
    controle = Controle.objects.get_or_create_current()

    return redirect(
        reverse(editar, kwargs={'mes': controle.mes, 'ano': controle.ano})
    )


def editar(request, mes, ano):
    if not mes or not ano:
        raise Http404

    controle = get_object_or_404(Controle, data__year=ano, data__month=mes)
    contas = controle.conta_set.all()
    form = ContaForm()
    ctx = {
        'form': form,
        'controle': controle,
        'contas': contas,
        'base_template': "controle/%s" % ('base_pjax.html' if request.is_ajax() else 'base.html'),
    }

    ctx.update(csrf(request))

    if request.method == 'POST':
        form = ContaForm(request.POST)

    return render_to_response('controle/editar.html', ctx, RequestContext(request))


def novo(request, mes=datetime.now().month, ano=datetime.now().year):
    data = date(ano, mes, 1)
    controle = Controle(data=data)
    form = ControleForm(instance=controle)

    ctx = {'form': form, 'controle': controle}
    ctx.update(csrf(request))

    return render_to_response('controle/novo.html', ctx, RequestContext(request))


@csrf_protect
def upload_conta(request, mes, ano, nome):
    conta = get_object_or_404(Conta, controle__data__year=ano, controle__data__month=mes, nome=nome)

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
    controle = Controle(owner=request.user)
    form = ControleForm(request.POST, request.FILES, instance=controle)

    try:
        form.errors
    except:
        pass

    try:
        form.save()
        return redirect(
            reverse(editar, kwargs={'mes': controle.mes, 'ano': controle.ano})
        )
    except:
        controle.data = date.today()
        return editar(request, controle.mes, controle.ano)


@csrf_protect
def salvar_conta(request, mes, ano, nome=None):
    controle = get_object_or_404(Controle, data__year=ano, data__month=mes)
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
    conta = get_object_or_404(Conta, controle__data__year=ano, controle__data__month=mes, nome=nome)
    conta.registrar_pagamento()

    return redirect(
        reverse(editar, kwargs={'mes': conta.controle.mes, 'ano': conta.controle.ano})
    )

