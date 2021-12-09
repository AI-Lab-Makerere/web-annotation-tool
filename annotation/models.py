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
    batches = models.IntegerField(default=0)
    annotated = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Annotator(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    leader = models.ForeignKey(Leader, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Batch(models.Model):
    leader = models.ForeignKey(Leader, null=True, blank=True, on_delete=models.SET_NULL)
    annotator = models.ForeignKey(Annotator, null=True, blank=True, on_delete=models.SET_NULL)
    batch_name = models.CharField(max_length=255)
    batch_file = models.FileField(upload_to='files', blank=True)
    is_annotated = models.BooleanField(default=False)
    is_annotated_twice = models.BooleanField(default=False)
    annotated_file = models.FileField(upload_to='files', blank=True)
    review = models.CharField(max_length=255, null=True, blank=True,)
    comment = models.TextField(null=True, blank=True)
    incomplete_file = models.BooleanField(default=False)
    last_updated = models.DateField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.batch_name


class Attribute(models.Model):
    leader = models.ForeignKey(Leader, on_delete=models.CASCADE)
    attribute_file = models.FileField(upload_to='files', blank=True)

    def __str__(self):
        return self.leader.user.username


class IncompleteBatch(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    incomplete_file = models.FileField(upload_to='files', blank=True)

    def __str__(self):
        return self.batch.batch_name
