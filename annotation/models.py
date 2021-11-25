from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Name(models.Model):
    project_name = models.CharField(max_length=255)

    def __str__(self):
        return self.project_name


class Category(models.Model):
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.category


class CustomUser(AbstractUser):
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    is_admin = models.BooleanField(default=True)
    is_team_leader = models.BooleanField(default=False)
    is_annotator = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Leader(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    annotators = models.IntegerField(default=0)
    uploads = models.IntegerField(default=0)
    annotated = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
