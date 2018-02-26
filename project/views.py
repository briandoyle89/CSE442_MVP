# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from project.models import course, user, file

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse

def index(request):
    courses = course.objects.all()
    user = request.user
    return render(request, 'project/index.html', {'courses': courses})

def course_view(request, identity):
    this_course = course.objects.filter(identity=identity).first()
    files = file.objects.filter(course=course)
    user = request.user
    return render(request, 'project/class.html', {'this_course': this_course,
                                                  'files': files})

def register(request):
    """
    Registers the user and sends an email confirmation link.
    :param request:
    :return:
    """
    data = {
        'email': request.POST.get('email', ''),
        'user_name': request.POST.get('user_name', '')
    }

    user.objects.create(user_name=data['user_name'],
                        email=data['email'])
    courses = course.objects.all()

    return render(request, 'project/index.html', {'courses': courses})

