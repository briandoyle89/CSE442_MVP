# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from project.models import course, user, file

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse

def index(request):
    courses = course.objects.all()
    return render(request, 'project/index.html', courses)