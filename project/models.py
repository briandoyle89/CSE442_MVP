from django.db import models, IntegrityError
from datetime import datetime, timedelta

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, User
from django.db import models
from django.db.models import CASCADE
from django.db.models import Model, TextField
from django.core.validators import RegexValidator, ValidationError
from django.db.models.fields.files import ImageFieldFile, FileField
# Create your models here.

#Here we define the crux of the backend to get the project running.
#UserManager model--allows you  to create, manage & delete users.
class UserManager(BaseUserManager):
    def create_user(self, email, phone_number, date_of_birth, password=None):

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
    course_name = models.CharField(default='CSE100', max_length=40, unique=True, primary_key=True)


def validate_file_size(value):
    filesize = value.size

    if filesize > 4 * 1024 * 1024:
        raise ValidationError("The maximum file size that can be uploaded is 4MB")
    else:
        return value

#Model to upload files, & each uploaded file is associated with a user, hence keep a count too.
class file(models.Model):
    file_name = models.CharField(blank=False,  max_length=60)
    username = models.ForeignKey(User, on_delete=CASCADE, null=True, blank=True)
    course = models.ForeignKey(course, on_delete=CASCADE)
    file_link = models.FileField(upload_to='documents/', validators=[validate_file_size])
    votes = models.IntegerField(default=0)

    def upvote(self, user):
        # try:
        uservotes = UserVotes.objects.all()
        for vote in uservotes:
            if vote.user == user and vote.file == self and vote.vote_type == "down":
                vote.delete()
                self.post_votes.create(user=user, file=self, vote_type="up")
                self.votes += 2
                self.save()
                return
            if vote.user == user and vote.file == self and vote.vote_type == "up":
                vote.delete()
                self.votes -= 1
                self.save()
                return
        self.post_votes.create(user=user, file=self, vote_type="up")
        self.votes += 1
        self.save()
        return 'ok'


    def downvote(self, user):
        # try:
        uservotes = UserVotes.objects.all()
        for vote in uservotes:
            if vote.user == user and vote.file == self and vote.vote_type == "up":
                vote.delete()
                self.post_votes.create(user=user, file=self, vote_type="down")
                self.votes -= 2
                self.save()
                return
            if vote.user == user and vote.file == self and vote.vote_type == "down":
                vote.delete()
                self.votes += 1
                self.save()
                return
        self.post_votes.create(user=user, file=self, vote_type="down")
        self.votes -= 1
        self.save()
        # except IntegrityError:
        #     return 'already_downvoted'
        return 'ok'

class UserVotes(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name="user_votes")
    file = models.ForeignKey(file, on_delete=CASCADE, related_name="post_votes")
    vote_type = models.CharField(max_length=10)

    class Meta:
        unique_together = ('user', 'file', 'vote_type')

#Model to download files, & each downloaded file is associated with a user, hence keep a count too.
class downloaded_file(models.Model):
    file_downloaded = models.ForeignKey(file, on_delete=CASCADE, null=True, blank=True)
    username = models.ForeignKey(User, on_delete=CASCADE, null=True, blank=True)
