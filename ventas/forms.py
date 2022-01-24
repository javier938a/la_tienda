from cProfile import label
from dataclasses import fields
from django import forms
from django.contrib.admin import widgets as wd
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserForm(UserCreationForm):
    class Meta:
        model=User
