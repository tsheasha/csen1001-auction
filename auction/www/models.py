from django.db import models
from django.contrib.auth.models import User

class UserProfile(User):
    credit_number = models.TextField(null=True, blank=True, unique=True)
