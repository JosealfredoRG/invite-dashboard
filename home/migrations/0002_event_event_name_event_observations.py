# Generated by Django 4.1.12 on 2024-09-17 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_name',
            field=models.CharField(default='nombre del evento', max_length=255),
        ),
        migrations.AddField(
            model_name='event',
            name='observations',
            field=models.TextField(blank=True, null=True),
        ),
    ]
