# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from project.models import *
from .forms import *
import os
from django.conf import settings
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
import re

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User


#Views render html pages located in the tempelates directory.
#Main Page
def index(request):
    return render(request, 'project/index.html')
#Login
def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        this_user = authenticate(request, username=username, password=password)
        if this_user is not None:
            login(request, this_user)
            print(request.user)
            return redirect(course_list)
        else:
            return render(request, 'project/index.html', {'error_message': "Please Log In."})
    return render(request, 'project/index.html')
#Registration
def register(request):
    return render(request, 'project/register.html')

#Check valid user/registration.
def check_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        print(str(len(username)))
        if len(username) < 3:
            return render(request, 'project/index.html', {
                'message': "Username not valid, must be three characters, letters, numbers and underscore and start with a letter or number."})
        if not re.match('^[A-Za-z0-9]+[A-Za-z0-9_]+[A-Za-z0-9_]+$', username):
            return render(request, 'project/index.html', {
                'message': "Username not valid, must be three characters, letters, numbers and underscore and start with a letter or number."})

        try:
            user = User.objects.create_user(username=username,
                                password=password,
                                email=email)
            user.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            return redirect(index)
        except IntegrityError:
            return render(request, 'project/index.html', {'message': "Username Already Exists."})

#View list of courses after login.
@login_required
def course_list(request):

    ##if not user redirect to index w/ message need to sign in
    courses = course.objects.all()
    user = request.user
    return render(request, 'project/dashboard.html', {'courses': courses,
                                                      'user': user})
#View courses for which 'this' user downloaded/uploaded files.
@login_required
def course_view(request, identity):

    if request.method == "POST":
        course_name = request.POST.get("course_name")
        files = file.objects.filter(course=course.objects.get(course_name=course_name))
        user_votes = UserVotes.objects.all()
        user = request.user
        return render(request, 'project/class_view.html', {'files': files,
                                                           'course_name': course_name,
                                                           'user_votes': user_votes,
                                                           'user': user
                                                           })
#Rest are self-explanotary4
@login_required
def file_upload(request):
    this_user = request.user

    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        print("here2")
        if form.is_valid():
            fileuploading = form.save(commit=False)
            fileuploading.username = request.user
            file_name = fileuploading.file_name
            print("here1")
            if re.match('^[A-Za-z0-9]+[A-Za-z0-9_\s]+[A-Za-z0-9_]+$', file_name):
                print("here")
            file_name =  fileuploading.file_name
            if re.match('^[A-Za-z0-9]+[A-Za-z0-9_]+[A-Za-z0-9_]+$', file_name):
                fileuploading.save()
                courses = course.objects.all()
                return render(request, 'project/dashboard.html', {'courses': courses})
            else:
                return render(request, 'project/file_upload.html', {'form': form,
                                                                    'message': "Please enter a valid file name."})
        else:
            return render(request, 'project/file_upload.html', {'form': form})
    else:
        form = FileForm()
        return render(request, 'project/file_upload.html', {'form': form})


@login_required
def download(request, file_chosen):
    if not request.user.is_authenticated:
        return redirect(index)
    file_path = settings.MEDIA_ROOT + '/' + file_chosen
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            file_object = file.objects.get(file_link=file_chosen)
            file_downloaded = downloaded_file.objects.create(file_downloaded=file_object, username=request.user)
            file_downloaded.save()
            print(file_downloaded.file_downloaded)
            print(request.user)
            return response
    raise Http404

@login_required()
def upvote(request, file_chosen):
    course_name = request.POST.get('course_is')
    file_chosen = file.objects.get(id=file_chosen)
    user_votes = UserVotes.objects.all()
    files = file.objects.all()
    file_chosen.upvote(request.user)
    return render(request, 'project/class_view.html', {'files': files,
                                                       'course_name': course_name,
                                                       'user_votes': user_votes,
                                                       'user': request.user
                                                       })

@login_required()
def downvote(request, file_chosen):
    course_name = request.POST.get('course_is')
    file_chosen = file.objects.get(id=file_chosen)
    user_votes = UserVotes.objects.all()
    files = file.objects.all()
    file_chosen.downvote(request.user)
    return render(request, 'project/class_view.html', {'files': files,
                                                       'course_name': course_name,
                                                       'user_votes': user_votes,
                                                       'user': request.user
                                                       })

@login_required
def my_uploads(request):
    this_user = request.user
    files = file.objects.all()
    user_votes = UserVotes.objects.all()
    file_list = []
    print(this_user)
    for file_object in files:
        if file_object.username == this_user:
            print(file_object.username)
            print(file_object)
            file_list.append(file_object)

    return render(request, 'project/myuploads.html', {'file_list': file_list,
                                                        'user_votes': user_votes,
                                                      'user': this_user
                                                      })

@login_required
def file_search(request):
    if request.method == 'POST':
        search_term = request.POST.get("search")
        user_votes = UserVotes.objects.all()
        similar_files = file.objects.filter(file_name__contains=search_term)
        if len(similar_files) == 0:
            return render(request, 'project/file_search.html', {'similar_files': similar_files,
                                                                'user_votes': user_votes,
                                                                'no_files': "There are no matching files."})

        return render(request, 'project/file_search.html', {'similar_files': similar_files,
                                                        'user_votes': user_votes})

    else:
        courses = course.objects.all()
        return render(request, 'project/dashboard.html', {'courses': courses,
                                                          'user': request.user
                                                          })

@login_required
def my_downloads(request):
    this_user = request.user
    downloaded_files = downloaded_file.objects.all()
    user_votes = UserVotes.objects.all()
    file_list = []
    for dl_file in downloaded_files:
        if dl_file.username == this_user:
            this_file = dl_file.file_downloaded
            file_list.append(this_file)

    return render(request, 'project/mydownloads.html', {'file_list': file_list,
                                                        'user_votes': user_votes,
                                                        'user': this_user
                                                        })

def logout_view(request):
    logout(request)
    return redirect(index)

def aboutus(request):
    return render(request, 'project/aboutUS.html')


