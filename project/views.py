# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from project.models import course, user, file

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse


def index(request):
    return render(request, 'project/index.html')

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        for users in user.objects.all():
            if username == users.user_name:
                print(username)
                return redirect(login)
    return render(request, 'project/index.html')

def register(request):
    return render(request, 'project/register.html')


def check_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        user.objects.create(user_name=username,
                            password=password,
                            email=email)
        return redirect(login)


def course_list(request):
    courses = course.objects.all()
    user = request.user
    return render(request, 'project/courses.html', {'courses': courses})


def course_view(request, identity):
    this_course = course.objects.filter(identity=identity).first()
    files = file.objects.filter(course=course)
    user = request.user
    return render(request, 'project/class.html', {'this_course': this_course,
                                                  'files': files})



