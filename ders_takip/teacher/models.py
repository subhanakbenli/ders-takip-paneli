from django.db import models
from django.contrib.auth.models import User


class Teacher(models.Model):
    ad = models.CharField(max_length=255, verbose_name="Ad")
    soyad = models.CharField(max_length=255, verbose_name="Soyad")
    telefon = models.CharField(max_length=255, verbose_name="Telefon")
    email = models.EmailField(max_length=255, verbose_name="Email")
    aciklama = models.TextField(verbose_name="Açıklama")
    def __str__(self):
        return self.ad + " " + self.soyad