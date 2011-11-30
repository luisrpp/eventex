from django import forms
from django.utils.translation import ugettext_lazy as _

class SubscriptionForm(forms.Form):
    name = forms.CharField(label=_('Nome'), max_length=100)
    cpf = forms.CharField(label=_('CPF'), max_length=11, min_length=11)
    email = forms.CharField(label=_('E-mail'))
    phone = forms.CharField(label=_('Telefone'), required=False, max_length=20)