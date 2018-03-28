from django.db import models
from datetime import datetime, timedelta

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, User
from django.db import models
from django.db.models import CASCADE
from django.db.models import Model, TextField
from django.db.models.fields.files import ImageFieldFile, FileField
# Create your models here.

#Here we define the crux of the backend to get the project running.
#UserManager model--allows you  to create, manage & delete users.
class UserManager(BaseUserManager):
    def create_user(self, email, phone_number, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """


        user.set_password(password)
        user.save(using=self._db)
        return user
#Model to link the no of dowwnloads &  uploads with a certain user.
class user(User, PermissionsMixin):
    submissions = models.IntegerField(default=0, null=True,)
    downloads = models.IntegerField(default=0, null=True,)
    objects = UserManager()
#Course List
class course(models.Model):
    course_name = models.CharField(blank=True, null=True, max_length=40)
#Model to upload files, & each uploaded file is associated with a user, hence keep a count too.
class file(models.Model):
    file_name = models.CharField(blank=True, max_length=60)
    username = models.ForeignKey(User, on_delete=CASCADE, null=True, blank=True)
    course = models.ForeignKey(course, on_delete=CASCADE, null=True, blank=True)
    file_link = models.FileField(upload_to='documents/')
#Model to download files, & each downloaded file is associated with a user, hence keep a count too.
class downloaded_file(models.Model):
    file_downloaded = models.ForeignKey(file, on_delete=CASCADE, null=True, blank=True)
    username = models.ForeignKey(User, on_delete=CASCADE, null=True, blank=True)
