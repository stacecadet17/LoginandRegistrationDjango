# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
NAME_REGEX = re.compile(r"^[-a-zA-Z']+$")
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")

# Create your models here.
class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        #first name
        if len(postData['first_name']) < 1:
            errors['first_name'] = "Must enter a name!"
        elif len(postData['first_name']) < 2:
            errors['first_name'] = "must contain at least two characters!"
        elif not NAME_REGEX.match(postData['first_name']):
            errors['first_name'] = "First name contains invalid characters"
        #Last name
        if len(postData['last_name']) < 1:
            errors['last_name'] = "Must enter a name!"
        elif len(postData['last_name']) < 2:
            errors['last_name'] = "must contain at least two characters!"
        elif not NAME_REGEX.match(postData['first_name']):
            errors['last_name'] = "Last name contains invalid characters"
        #email
        if len(postData['email']) < 1:
            errors['email'] = "Must enter an email address"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "not a valid email"
        if User.objects.filter(email=postData['email']):
            errors['email'] = "Sorry, that email is already taken"
        if len(postData['password']) < 8:
            errors['password'] = "password must contain at least eight characters"
        elif not postData['password'] ==postData['password_conf']:
            errors['password'] =  "Passwords do not match!"
        return errors
    def login_validator(self, postData):
        errors = {}
        #email
        if len(postData['email'])< 1:
            errors['email'] = "Must enter an email address!"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Not a valid email address"
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least eight characters long'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
