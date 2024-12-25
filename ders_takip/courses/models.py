from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from teacher.models import Teacher

class Course(models.Model):
    STATU_CHOICES = [
        ("aktif", "Aktif"),
        ("iptal", "İptal"),
        ("arsiv", "Arşiv"),
    ]

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="teacher")
    name = models.CharField(max_length=255, verbose_name="name")
    statu = models.CharField(max_length=255, choices=STATU_CHOICES, verbose_name="statu", null=True, blank=True)
    description = models.TextField(verbose_name="description", blank=True, null=True)
    
    start_date = models.CharField(max_length=255, verbose_name="start_date", null=True, blank=True)
    end_date = models.CharField(max_length=255, verbose_name="end_date", null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created_at")
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)

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
    statu = models.CharField(max_length=255, choices=STATU_CHOICES, verbose_name="statu", null=True, blank=True)
    

    is_uploaded = models.BooleanField(default=False)
    dilekce_name = models.CharField(max_length=255, verbose_name="dilekce_name", null=True, blank=True)
    dilekce_is_uploaded = models.BooleanField(default=False)
    current_version = models.OneToOneField(
        'CourseFileVersion',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='current_file',
        verbose_name="current_version"
    )
    
    start_date = models.CharField(max_length=255, verbose_name="start_date", null=True, blank=True)
    end_date = models.CharField(max_length=255, verbose_name="end_date", null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created_at")
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.category} - {self.name}"


class CourseFileVersion(models.Model):
    course_file = models.ForeignKey(CourseFile, on_delete=models.CASCADE, related_name="versions")
    version_number = models.PositiveIntegerField(verbose_name="version_number")
    file = models.FileField(upload_to='uploads/', verbose_name="file", null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="uploaded_at")
    uploaded_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.course_file.name} - Version {self.version_number}"


@receiver(pre_save, sender=Course)
def update_course_files_statu(sender, instance, **kwargs):
    if instance.pk:  # Only run on updates
        previous_instance = Course.objects.get(pk=instance.pk)
        if previous_instance.statu != instance.statu and instance.statu in ["iptal", "arsiv"]:
            instance.coursefile_set.filter(statu="aktif").update(statu=instance.statu)


