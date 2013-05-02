from www.models import *
from django.contrib import admin

class UserProfileAdmin( admin.ModelAdmin ):
    list_display = ( 'id', 'username', )

admin.site.register(UserProfile)