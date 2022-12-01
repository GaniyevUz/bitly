from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, PasswordInput

from apps.models import Url, User


class UrlForm(forms.ModelForm):
    # long_name = forms.URLField(max_length=255)

    class Meta:
        model = Url
        exclude = ('short_name', 'clicked_count')


class UserForm(ModelForm):
    confirm_password = CharField(widget=PasswordInput(attrs={"autocomplete": "current-password"}), )

    def clean_password(self):
        password = self.data.get('password')
        confirm_password = self.data.get('confirm_password')
        if confirm_password != password:
            raise ValidationError('Parolni tekshir')
        return make_password(password)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')
