# Generated by Django 2.2.10 on 2020-04-22 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ariticlepost',
            name='body',
            field=models.TextField(default=''),
        ),
    ]