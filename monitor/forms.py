from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Server, Notification

class ServerForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_method = 'POST'
    class Meta:
        model = Server
        fields = '__all__'


class NotificationForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_method = 'POST'
    class Meta:
        model = Notification
        fields = '__all__'
