from django.db import models
from teacher.models import Teacher

class Ders(models.Model):
    dersi_veren = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    ders_adi = models.CharField(max_length=255, verbose_name="Ders Adı")
    durum = models.CharField(max_length=255, verbose_name="Durum")
    aciklama = models.TextField(verbose_name="Açıklama")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.ders_adi
    
class DersBelgesi(models.Model):
    ders = models.ForeignKey(Ders, on_delete=models.CASCADE)
    kategori = models.CharField(max_length=255, verbose_name="Kategori")
    belge_adi = models.CharField(max_length=255, verbose_name="Belge Adı")
    belge = models.FileField(upload_to="ders_belgeleri/", verbose_name="Belge")
    def __str__(self):
        return f"{self.kategori} + {self.belge_adi}"


