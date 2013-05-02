# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import PasswordChangeForm
from django import forms
from django.utils import translation

from userprofiles import settings as up_settings
from userprofiles.contrib.emailverification.forms import ChangeEmailForm
from userprofiles.contrib.emailverification.models import EmailVerification



@login_required
def email_change(request):
    post_change_redirect = reverse('django.contrib.auth.views.password_change_done')
    password_change_form = PasswordChangeForm
    if request.method == 'POST':
        print 'it is post'
        password_form = password_change_form(user=request.user, data=request.POST)
        email_form = ChangeEmailForm(request.POST)
        if password_form.is_valid():
            password_form.save()
            return redirect(post_change_redirect)
        if email_form.is_valid():
            verification = email_form.save(request.user)
            return redirect('userprofiles_email_change_requested')
        email_form = ChangeEmailForm()
        password_form = password_change_form(user=request.user)
    else:
        email_form = ChangeEmailForm()
        password_form = password_change_form(user=request.user)

    return render(request, 'userprofiles/email_change.html', {'email_form': email_form, 'password_form': password_form, 'password_length_valid':True})

def email_change_save(request):
    post_change_redirect = reverse('django.contrib.auth.views.password_change_done')
    password_change_form = PasswordChangeForm
    if request.method == 'POST':
        password_form = password_change_form(user=request.user, data=request.POST)
        email_form = ChangeEmailForm(request.POST)
        if password_form.is_valid():
            password_form.save()
            return redirect(post_change_redirect)
        if email_form.is_valid():
            verification = email_form.save(request.user)
            return redirect('userprofiles_email_change_requested')
        password_form = password_change_form(user=request.user)
    else:
        email_form = ChangeEmailForm()
        password_form = password_change_form(user=request.user)

    return render(request, 'userprofiles/email_change.html', {'email_form': email_form, 'password_form': password_form, 'password_length_valid':True})

def password_change_save(request):
    password_length_valid = True
    post_change_redirect = reverse('django.contrib.auth.views.password_change_done')
    password_change_form = PasswordChangeForm
    if request.method == 'POST':
        password_form = password_change_form(user=request.user, data=request.POST)
        email_form = ChangeEmailForm(request.POST)
        if password_form.is_valid():
            print len(password_form.cleaned_data["new_password1"])
            if len(password_form.cleaned_data["new_password1"]) > 7:
                password_form.save()
                return redirect(post_change_redirect)
            else :
                password_length_valid = False
        if email_form.is_valid():
            verification = email_form.save(request.user)
            return redirect('userprofiles_email_change_requested')
        email_form = ChangeEmailForm()
    else:
        email_form = ChangeEmailForm()
        password_form = password_change_form(user=request.user)

    return render(request, 'userprofiles/email_change.html', {'email_form': email_form, 'password_form': password_form, 'password_length_valid': password_length_valid})


@login_required
def email_change_requested(request):
    return render(request, 'userprofiles/email_change_requested.html', {
        'expiration_days': up_settings.EMAIL_VERIFICATION_DAYS})


@login_required
def email_change_approve(request, token, code):
    try:
        verification = EmailVerification.objects.get(token=token, code=code,
            user=request.user, is_expired=False, is_approved=False)

        verification.is_approved = True
        verification.save()
        messages.success(request, _(u'E-mail address changed to %(email)s' % {
            'email': verification.new_email}))
    except EmailVerification.DoesNotExist:
        messages.error(request,
            _(u'Unable to change e-mail address. Confirmation link is invalid.'))

    return redirect(up_settings.EMAIL_VERIFICATION_DONE_URL)
