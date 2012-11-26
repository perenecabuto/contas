# -*- encoding : utf-8 -*-

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf

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

        return render_to_response('controle/upload_conta.html', ctx)


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


def tree_widget(request):
    return render_to_response('controle/tree_widget.html', {
        'tree': tree(request)
    })


def tree_json(request):
    import json
    from django.http import HttpResponse

    data = tree(request)

    return HttpResponse(json.dumps(data['children']), mimetype='application/json')


def tree(request):
    from django.core.urlresolvers import reverse

    from nodefs.lib.model import NodeManager
    from nodefs.lib import conf

    from django_nodefs.selectors import ModelSelector, ModelFileSelector

    from contas.conf import nodefs_schema

    conf.node_profiles = nodefs_schema.schema
    root_node = NodeManager().search_by_path('/')

    def build_tree(node):
        tree = {'id': node.id, 'label': node.pattern, 'children': []}

        nodeselector = node.abstract_node.selector

        if isinstance(nodeselector, ModelSelector):
            obj = nodeselector.get_object(node)
            url = None

            if issubclass(nodeselector.model_class, Controle):
                url = reverse('controle.views.editar', kwargs={'mes': obj.mes, 'ano': obj.ano})

            elif issubclass(nodeselector.model_class, Conta) and isinstance(nodeselector, ModelFileSelector):
                url = obj.arquivo.url

            if url:
                tree['label'] = "<a href='%s'>%s</a>" % (url, node.pattern)

                if url in request.GET.get('current_url', ''):
                    tree['selected'] = True

        for cnode in node.children:
            tree['children'].append(build_tree(cnode))

        if not tree['children']:
            del tree['children']

        return tree

    return build_tree(root_node)

