# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.localflavor.br.forms import BRCPFField
from django.core.validators import EMPTY_VALUES
from subscriptions.models import Subscription

class PhoneWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets=(
            forms.TextInput(attrs=attrs),
            forms.TextInput(attrs=attrs))
        super(PhoneWidget, self).__init__(widgets, attrs)

    def decompress (self, value):
        if not value:
            return [None, None]
        return value.split('-')

class PhoneField(forms.MultiValueField):
    widget=PhoneWidget
    
    def __init__(self, *args, **kwargs):
        fields=(
            forms.IntegerField(),
            forms.IntegerField())
        super(PhoneField,self).__init__(fields, *args, **kwargs)
    
    def compress(self, data_list):
        if not data_list:
            return none         
        if data_list[0] in EMPTY_VALUES:
            raise  forms.ValidationError(u'DDD inválido.')
        if data_list[1] in EMPTY_VALUES:
            raise  forms.ValidationError(u'Número inválido.')
        return '%s-%s'  %tuple(data_list)

class SubscriptionForm(forms.ModelForm):

    cpf = BRCPFField(label=_(u'CPF'), required=True)
    phone = PhoneField(label=_(u'Telefone'), required=False)

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