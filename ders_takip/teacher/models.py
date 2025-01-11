from django.db import models
from django.contrib.auth.models import User


class Teacher(models.Model):
    name = models.CharField(max_length=255, verbose_name="name")
    surname = models.CharField(max_length=255, verbose_name="surname")
    title = models.CharField(max_length=255, verbose_name="title", blank=True, null=True)
    firma_adi = models.CharField(max_length=255, verbose_name="firma_adi", blank=True, null=True)
    description = models.TextField(verbose_name="description", blank=True, null=True)
    telephone = models.CharField(max_length=255, verbose_name="telephone", blank=True, null=True)
    telephone2 = models.CharField(max_length=255, verbose_name="telephone2", blank=True, null=True)
    mail = models.EmailField(max_length=255, verbose_name="mail", blank=True, null=True)
    adress = models.TextField(verbose_name="adress", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.name + " " + self.surname