# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.localflavor.br.forms import BRCPFField
from subscriptions.models import Subscription
from subscriptions.validators import CpfValidator

class SubscriptionForm(forms.ModelForm):

    cpf = BRCPFField(label=_(u'CPF'), required=True, validators=[CpfValidator])

    class Meta:
        model = Subscription
        exclude = ('created_at', 'paid')
    
    def clean(self):
        super(SubscriptionForm, self).clean()

        if not self.cleaned_data.get('email') and \
            not self.cleaned_data.get('phone'):

            raise forms.ValidationError(
                _(u'Informe seu e-mail ou telefone.'))
        
        return self.cleaned_data

    def _unique_check(self, field_name, error_message):
        param = { field_name: self.cleaned_data[field_name] }

        try:
            s = Subscription.objects.get(**param)
        except Subscription.DoesNotExist:
            return self.cleaned_data[field_name]
        raise forms.ValidationError(error_message)
    
    def clean_cpf(self):
        return self._unique_check('cpf', _(u'CPF já inscrito.'))
    
    def clean_email(self):
        return self._unique_check('email', _(u'E-mail já inscrito.'))