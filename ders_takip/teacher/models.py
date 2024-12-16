from django.db import models
from django.contrib.auth.models import User


class Teacher(models.Model):
    name = models.CharField(max_length=255, verbose_name="name")
    surname = models.CharField(max_length=255, verbose_name="surname")
    description = models.TextField(verbose_name="description", blank=True, null=True)
    def __str__(self):
        return self.name + " " + self.surname