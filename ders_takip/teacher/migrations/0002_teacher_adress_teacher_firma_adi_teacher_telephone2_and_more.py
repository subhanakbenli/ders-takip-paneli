# Generated by Django 5.1.4 on 2025-01-11 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='adress',
            field=models.TextField(blank=True, null=True, verbose_name='adress'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='firma_adi',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='firma_adi'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='telephone2',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='telephone2'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='title'),
        ),
    ]
