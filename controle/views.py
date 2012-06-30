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
    return redirect(
        reverse(editar, kwargs={'mes': datetime.now().month, 'ano': datetime.now().year})
    )


def editar(request, mes, ano):
    controle = get_object_or_404(Controle, ano=ano, mes=mes)
    contas = controle.conta_set.all()
    return render_to_response('controle/editar.html', {
        'controle': controle,
        'contas': contas,
    })


def novo(request, mes=datetime.now().month, ano=datetime.now().year):
    controle = Controle(ano=ano, mes=mes)
    form = ControleForm(instance=controle)

    ctx = {'form': form, 'controle': controle}
    ctx.update(csrf(request))

    return render_to_response('controle/novo.html', ctx)


def nova_conta(request, mes, ano):
    controle = get_object_or_404(Controle, ano=ano, mes=mes)
    form = ContaForm()

    if request.method == 'POST':
        form = ContaForm(request.POST)

    ctx = {'form': form, 'controle': controle}
    ctx.update(csrf(request))

    return render_to_response('controle/nova_conta.html', ctx)


def editar_conta(request, mes, ano, nome):
    controle = get_object_or_404(Controle, ano=ano, mes=mes)
    conta = get_object_or_404(controle.conta_set, nome=nome)
    form = ContaForm(instance=conta)

    ctx = {'form': form, 'conta': conta, 'controle': controle}
    ctx.update(csrf(request))

    return render_to_response('controle/editar_conta.html', ctx)


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
        return nova_conta(request, mes, ano)
