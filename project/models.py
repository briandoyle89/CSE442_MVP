from django.db import models
from datetime import datetime, timedelta

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models import CASCADE
from django.db.models import Model, TextField
from django.db.models.fields.files import ImageFieldFile, FileField
# Create your models here.

class user(models.Model):
    user_name = models.CharField(blank=True, max_length=40)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    password = models.CharField(max_length=10)
    submissions = models.IntegerField(default=0)
    downloads = models.IntegerField(default=0)

    def __str__(self):
        return self.user_name

    # class Meta:
    #     db_table = user


class course(models.Model):
    course_name = models.CharField(blank=True, max_length=40)

    def __str__(self):
        return self.course_name

    # class Meta:
    #     db_table = course

class file(models.Model):
    file_name = models.CharField(blank=True, max_length=60)
    upload_date = models.DateField(auto_now=True, editable=False)
    user = models.ForeignKey(user, on_delete=CASCADE, null=True, blank=True)
    course = models.ForeignKey(course, on_delete=CASCADE, null=True, blank=True)
    file_link = models.FileField()

    # class Meta:
    #     db_table = file