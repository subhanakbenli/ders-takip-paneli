from django.db import models

# Create your models here.
from django.db import models

class Ogretmen(models.Model):
    ad_soyad = models.CharField(max_length=255, verbose_name="Ad Soyad")
    telefon = models.CharField(max_length=255, verbose_name="Telefon")
    email = models.EmailField(max_length=255, verbose_name="Email")
    aciklama = models.TextField(verbose_name="Açıklama")
    def __str__(self):
        return self.ad_soyad

class Ders(models.Model):
    dersi_veren = models.ForeignKey(Ogretmen, on_delete=models.CASCADE)
    ders_adi = models.CharField(max_length=255, verbose_name="Ders Adı")
    durum = models.CharField(max_length=255, verbose_name="Durum")
    aciklama = models.TextField(verbose_name="Açıklama")
    def __str__(self):
        return self.ders_adi
    
class DersBelgesi(models.Model):
    ders = models.ForeignKey(Ders, on_delete=models.CASCADE)
    kategori = models.CharField(max_length=255, verbose_name="Kategori")
    belge_adi = models.CharField(max_length=255, verbose_name="Belge Adı")
    belge = models.FileField(upload_to="ders_belgeleri/", verbose_name="Belge")
    def __str__(self):
        return f"{self.kategori} + {self.belge_adi}"

