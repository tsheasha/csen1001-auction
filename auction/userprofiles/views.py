# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from userprofiles import settings as up_settings
from userprofiles.utils import get_form_class
from django.contrib import messages
from django.utils import translation
from django.template import RequestContext


def registration(request):
    RegistrationForm = get_form_class(up_settings.REGISTRATION_FORM)

    if request.method == 'POST':
        form = RegistrationForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            new_user = form.save()
            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            request.session['login'] = "first"

            # Automatically log this user in
            if up_settings.AUTO_LOGIN:

                if up_settings.EMAIL_ONLY:
                    username = form.cleaned_data['email']

                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)

            return redirect(up_settings.REGISTRATION_REDIRECT)

    else:
        form = RegistrationForm()

    import random
    x = random.randint(1, 7)
    try:
        next = request.GET['next']
    except:
        next = ''
    return render(request, 'userprofiles/registration.html', {'form': form, 'pic_num': x,'next':next})


def registration_complete(request):
    messages.info(request, translation.gettext("An activation mail has been sent, please activate your account in order to login"))
    return redirect('/', context_instance=RequestContext(request))
    # return render(request, 'userprofiles/registration_complete.html', {
    #     'account_verification_active': up_settings.USE_ACCOUNT_VERIFICATION,
    #     'expiration_days': up_settings.ACCOUNT_VERIFICATION_DAYS,
    # })
