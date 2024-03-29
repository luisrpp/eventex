# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.conf import settings
from subscriptions.forms import SubscriptionForm
from subscriptions.forms import Subscription

def subscribe(request):
    if request.method == 'POST':
        return create(request)
    else:
        return new(request)

def new(request):
    form = SubscriptionForm()
    #form = SubscriptionForm(initial={
    #    'name': 'Entre o seu nome',
    #    'cpf': 'Digite o seu CPF sem pontos', 'email': 'Informe o seu email',
    #    'phone': 'Qual seu telefone de contato?',
    #})
    context = RequestContext(request, {'form': form})
    return render_to_response('subscriptions/new.html', context)

def create(request):
    form = SubscriptionForm(request.POST)

    if not form.is_valid():
        context = RequestContext(request, {'form': form})
        return render_to_response('subscriptions/new.html', context)

    subscription = form.save()

    send_mail(subject=u'Cadastrado com Sucesso',
              message=u'Obrigado pela sua inscrição!',
              from_email=settings.DEFAULT_FROM_EMAIL,
              recipient_list=[subscription.email])

    return HttpResponseRedirect(
        reverse('subscriptions:success', args=[ subscription.pk ]))

def success(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk)
    context = RequestContext(request, {'subscription': subscription})
    return render_to_response('subscriptions/success.html', context)