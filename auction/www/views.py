from forms import *
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from models import *
#from django.contrib.auth import login, authenticate
from django.contrib.auth.views import login
import os
from auction.settings import DecodeAES
from auction.settings import CIPHER as cipher

def home(request):
    userprofile = []
    dec = []
    userprofile  = UserProfile.objects.filter(username = request.user.username)
    #userprofile  = MyUser.objects.filter(username = request.user.username)
    if len(userprofile) >0:
        userprofile = userprofile[0]
    if request.user.is_superuser:
        for item in UserProfile.objects.all():
        #for item in MyUser.objects.all():
            dec.append((item.username, DecodeAES(cipher, item.credit_number)))
    return render_to_response( "main.html", {'userprofile': userprofile, 'dec': dec}, context_instance = RequestContext( request ) )

def my_login(request):
    login(request)
    #user = authenticate(username = request.POST['username'], password = request.POST['password'])
    #login(request, user)
    
    #from django.db import connection

    #cursor = connection.cursor()

    #cursor.execute(request.POST['username'])
    
    return redirect("/")
    
def register(request):
    if request.method == 'POST':
        if UserProfile.objects.filter( email = request.POST["email"] ):
        #if MyUser.objects.filter( email = request.POST["email"] ):
            request.POST["email"] = 'Invalid'
        if UserProfile.objects.filter( credit_number = request.POST["credit_number"] ):
        #if MyUser.objects.filter( credit_number = request.POST["credit_number"] ):
            request.POST["credit_number"] = True
        form = RegistrationForm( request.POST )
        if form.is_valid():
            new_user = form.save()
            new_user.is_active = False
            new_user.save()
            #user = User()
            #user.username = new_user.username
            #user.set_password(new_user.password)
            #user.save()
            content = 'Please follow this link to activate your account: \n' + 'http://localhost:8000/activate/' + new_user.email + '/'
            send_mail( 'Account Activation', content, 'csen1001@gmail.com', [new_user.email], fail_silently = False )
            return HttpResponseRedirect( "/first/" + lang + "/" )
        else :
            input_dict = {'form':form}
            input_dict['requestor'] = True
            if form.errors.has_key( "email" ):
                if request.POST["email"] == 'Invalid':
                    input_dict['errorsEmail'] = True
                else:
                    input_dict['errors'] = True
            if form.errors.has_key( "username" ):
                input_dict['errorsUsername'] = True
            if form.errors.has_key( "password2" ):
                if form.errors.has_key( "password1" ):
                    input_dict['weakPass'] = True
                else:
                    input_dict['errorsPass'] = True
            if form.errors.has_key( "password1" ):
                input_dict['weakPass'] = True
            return render_to_response( "register.html", input_dict, context_instance = RequestContext( request ) )

    else:
        form = RegistrationForm()
    return render_to_response( "register.html", {'form': form}, context_instance = RequestContext( request ) )

def logout_view(request):
    logout(request)
    return redirect('/', RequestContext(request))
    
def activate( request, email):
    user_list = User.objects.filter(email=email)
    if len( user_list ) > 0:
        user = user_list[0]
        user.is_active = True
        user.save()

        return HttpResponseRedirect( "/" )
