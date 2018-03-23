from django.db import models
from datetime import datetime, timedelta

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, User
from django.db import models
from django.db.models import CASCADE
from django.db.models import Model, TextField
from django.db.models.fields.files import ImageFieldFile, FileField
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, phone_number, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """

        user.set_password(password)
        user.save(using=self._db)
        return user

class user(User, PermissionsMixin):
    submissions = models.IntegerField(default=0)
    downloads = models.IntegerField(default=0)
    objects = UserManager()

class course(models.Model):
    course_name = models.CharField(blank=True, max_length=40)

class file(models.Model):
    file_name = models.CharField(blank=True, max_length=60)
    username = models.ForeignKey(User, on_delete=CASCADE, null=True, blank=True)
    course = models.ForeignKey(course, on_delete=CASCADE, null=True, blank=True)
    file_link = models.FileField(upload_to='documents/')

class downloaded_file(models.Model):
    file_downloaded = models.ForeignKey(file, on_delete=CASCADE, null=True, blank=True)
    username = models.ForeignKey(User, on_delete=CASCADE, null=True, blank=True)