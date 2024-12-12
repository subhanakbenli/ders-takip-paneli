from django.db import models

class DersBilgisi(models.Model):
    ders_adi = models.CharField(max_length=255, verbose_name="Birisinin Vereceği Ders")
    durum = models.CharField(max_length=255, verbose_name="Durum")
    yukleme_miktari = models.PositiveIntegerField(verbose_name="Yükleme Miktarı", default=0)

    def __str__(self):
        return self.ders_adi
