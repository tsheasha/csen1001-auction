from django import forms
from django.utils.translation import ugettext_lazy as _
from models import *
from django.contrib.auth.forms import UserCreationForm
from urlcrypt import lib as urlcrypt
import os
from auction.settings import EncodeAES
from auction.settings import CIPHER as cipher
class RegistrationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given username and password.
    """
    email = forms.EmailField(label=_("Email"))
    username = forms.RegexField(label=_("Username"), max_length=30, regex=r'^[\w.@+-]+$')
    password1 = forms.RegexField(label=_("Password"), widget=forms.PasswordInput,regex=r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?!.*\s).*$')
    password2 = forms.CharField(label=_("Password Confirmation"), widget=forms.PasswordInput)
    credit_number = forms.RegexField(label=_("Credit Card Number"), max_length=16, regex=r'^\d\d\d\d\d\d\d\d\d\d*', required=True)
    first_name = forms.CharField(label=_("XSS"))
    #first_name = forms.RegexField(label=_("First Name"), regex=r'\w+')
    last_name = forms.RegexField(label=_("Last Name"), regex=r'\w+')

    class Meta:
        model = UserProfile
        #model = MyUser
        fields = ('first_name', 'last_name')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=True)
        user.set_password(self.cleaned_data["password1"])
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["username"]
        user.save()
        credit_number = self.cleaned_data["credit_number"]
        encoded = EncodeAES(cipher, str(credit_number))
        user.credit_number = encoded
        user.save()
        return user

