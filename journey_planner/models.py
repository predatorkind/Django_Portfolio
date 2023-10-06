from django.db import models

# Create your models here.
class Journey(models.Model):
    description = models.CharField(max_length=200)