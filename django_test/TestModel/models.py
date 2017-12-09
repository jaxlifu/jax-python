from django.db import models

# Create your models here.
from django.db import models


class Test(models.Model):
    name = models.CharField(unique=True,max_length=20)
    age = models.IntegerField()
    number = models.IntegerField(unique=True)
    _id = models.IntegerField(primary_key=True)
