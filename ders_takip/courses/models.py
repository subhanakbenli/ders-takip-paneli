from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from teacher.models import Teacher
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
import os

class Course(models.Model):
    STATU_CHOICES = [
        ("aktif", "Aktif"),
        ("iptal", "İptal"),
        ("arsiv", "Arşiv"),
    ]

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="teacher")
    name = models.CharField(max_length=255, verbose_name="name")
    description = models.TextField(verbose_name="description", blank=True, null=True)
    statu_pano = models.CharField(max_length=255, choices=STATU_CHOICES, verbose_name="statu_pano", default="aktif")
    start_year = models.CharField(max_length=255, verbose_name="start_year", null=True, blank=True)
    end_year = models.CharField(max_length=255, verbose_name="end_year", null=True, blank=True)    
    dilekce_required = models.BooleanField(default=False, verbose_name="dilekce_required")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created_at")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class CourseFile(models.Model):
    STATU_CHOICES = [
        ("aktif", "Aktif"),
        ("iptal", "İptal"),
        ("arsiv", "Arşiv"),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="course")
    category = models.CharField(max_length=255, verbose_name="category", null=True, blank=True)
    name = models.CharField(max_length=255, verbose_name="file_name", null=True, blank=True)
    type = models.CharField(max_length=255, verbose_name="type", null=True, blank=True)
    statu_pano = models.CharField(max_length=255, choices=STATU_CHOICES, verbose_name="statu_pano", default="aktif")
    current_version = models.OneToOneField(
        'CourseFileVersion',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='current_file',
        verbose_name="current_version"
    )
    
    
    start_date = models.CharField(max_length=255, verbose_name="start_date", null=True, blank=True)
    sisteme_giris_tarihi  = models.DateField(verbose_name="sisteme_giris_tarihi", null=True, blank=True)
    gun_sayisi = models.CharField(max_length=255, verbose_name="gun_sayisi", null=True, blank=True)
    uyari_date = models.DateField(verbose_name="uyari_date", null=True, blank=True)
    end_date = models.CharField(max_length=255, verbose_name="end_date", null=True, blank=True)

    dilekce_name = models.CharField(max_length=255, verbose_name="dilekce_name", null=True, blank=True)
    description = models.TextField(verbose_name="description", blank=True, null=True)    
    etkinlik_no = models.CharField(max_length=255, verbose_name="etkinlik_no", null=True, blank=True)
    etkinlik_tarihi = models.DateField(verbose_name="etkinklik_tarihi", null=True, blank=True)
    ogretmen_adi = models.CharField(max_length=255, verbose_name="ogretmen_adi", null=True, blank=True)
    sinif= models.CharField(max_length=255, verbose_name="sinif", null=True, blank=True)
    sehir = models.CharField(max_length=255, verbose_name="sehir", null=True, blank=True)
    katilimcilar = models.CharField(max_length=255, verbose_name="katilanlar", null=True, blank=True)
    etkinlik_adi = models.CharField(max_length=255, verbose_name="etkinlik_adi", null=True, blank=True)
    egitim_olusturma_tarihi = models.DateField(verbose_name="egitim_olusturma_tarihi", null=True, blank=True)
    katilimci_kodu = models.CharField(max_length=255, verbose_name="katilimci_kodu", null=True, blank=True)
    egitim_kayit_no_1 = models.CharField(max_length=255, verbose_name="egitim_kayit_no_1", null=True, blank=True)
    egitim_kayit_no_2 = models.CharField(max_length=255, verbose_name="egitim_kayit_no_2", null=True, blank=True)
    egitim_kayit_no_3 = models.CharField(max_length=255, verbose_name="egitim_kayit_no_3", null=True, blank=True)
    etkinlik_aciklamasi = models.TextField(verbose_name="etkinlik_aciklamasi", blank=True, null=True)
    kodu = models.CharField(max_length=255, verbose_name="kodu", null=True, blank=True)
    katilimci_sayisi = models.CharField(max_length=255, verbose_name="katilimci_sayisi", null=True, blank=True)        
    verilen_not = models.CharField(max_length=255, verbose_name="verilen_not", null=True, blank=True)
    guncelleme_tarihi = models.DateField(verbose_name="guncellenme_tarihi", null=True, blank=True)
    description_1 = models.TextField(verbose_name="description_1", blank=True, null=True)
    description_2 = models.TextField(verbose_name="description_2", blank=True, null=True)
    description_3= models.TextField(verbose_name="description_3", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created_at")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.category} - {self.name}"
    @classmethod
    def get_files_in_warning_period(cls):
        today = timezone.now().date()
        try:
            warning_files = cls.objects.filter(
                uyari_date__lte=today,
                end_date__gt=today.strftime('%Y-%m-%d'),
                statu_pano="aktif",
                sisteme_giris_tarihi__isnull=True
            )
            return warning_files
        except Exception as e:
            print(f"Hata oluştu: {str(e)}")
            return cls.objects.none()

def unique_file_path(instance, filename):
    base_name, extension = os.path.splitext(filename)
    base_name = base_name.replace(' ', '_')  # Dosya adında boşlukları kaldır
    folder_path = ''  # Dosyanın kaydedileceği klasör

    full_path = os.path.join(folder_path, filename)
    counter = 2

    # Aynı adda bir dosya varsa sıra numarası ekle
    while os.path.exists(full_path):
        new_filename = f"{base_name}_{counter}{extension}"
        print(new_filename)
        full_path = os.path.join(folder_path, new_filename)
        counter += 1

    return os.path.join(folder_path, os.path.basename(full_path))

class CourseFileVersion(models.Model):
    course_file = models.ForeignKey(CourseFile, on_delete=models.CASCADE, related_name="versions")
    file = models.FileField(upload_to=unique_file_path, verbose_name="file", null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="uploaded_at")
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.course_file.name} - Version {self.id}"


@receiver(pre_save, sender=Course)
def update_course_files_statu_pano(sender, instance, **kwargs):
    if instance.pk:  # Sadece mevcut nesneler için çalıştır
        previous_instance = Course.objects.get(pk=instance.pk)
        # Eğer `statu` değiştiyse
        if previous_instance.statu_pano != instance.statu_pano:
            # `CourseFile` nesnelerinin `statu` alanını güncelle
            instance.coursefile_set.filter(statu_pano=previous_instance.statu_pano).update(statu_pano=instance.statu_pano)
