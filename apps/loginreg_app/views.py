# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from models import *
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    if "id" not in request.session:
        request.session["id"] = 0
    return render(request, 'loginreg_app/index.html')

def register(request):
    if "valid" not in request.session:
        request.session["valid"] = "Register"
    errors = User.objects.reg_validator(request.POST)
    if len(errors):
        for error in errors.iteritems():
            messages.error(request, error)
        return redirect('/')
    else:
        new = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = request.POST['password'])
        print new
        request.session["id"] = new.id
        return redirect('/success')

def login(request):
    if "valid" not in request.session:
        request.session["valid"] = "Login"
    request.session["valid"] = "Login"
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for error in errors.itervalues():
            messages.error(request, error)
        return redirect('/')
    login_info = User.objects.get(email=request.POST['email'])
    if login_info == []:
        messages.error(request, "Invalid login credentials.")
        return redirect('/')
    elif len(errors):
        messages.error(request, "Invalid email or password")
        return redirect('/')
    else:
        hash = bcrypt.hashpw("request.POST['password']".encode(), bcrypt.gensalt())
        bcrypt.checkpw("request.POST['password']".encode(), hash)
        request.session['id'] = login_info.id
        return redirect('/success')

def success(request):
    if request.session['valid'] == "Register":
        messages.success(request, "You are registered!")
    id = request.session['id']
    user = User.objects.get(id = id)
    context = {
        "name": user.first_name,
    }
    return render(request, "loginreg_app/success.html", context)
