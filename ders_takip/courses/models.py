from django.db import models
from teacher.models import Teacher

class Course(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="teacher")
    name = models.CharField(max_length=255, verbose_name="name")
    statu = models.CharField(max_length=255, verbose_name="statu",)
    description = models.TextField(verbose_name="description", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created_at")
    is_finish = models.BooleanField(default=False, verbose_name="is_finish")
    def __str__(self):
        return self.name


class CourseFile(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="course")
    category= models.CharField(max_length=255, verbose_name="category")
    name = models.CharField(max_length=255, verbose_name="file_name")
    file = models.FileField(upload_to='uploads/', verbose_name="file")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created_at")

    def __str__(self):
        return f"{self.category} - {self.name}"



