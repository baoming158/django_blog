# Generated by Django 2.2.10 on 2020-04-23 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0005_ariticlepost_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='ariticlepost',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='article/%Y%m%d/'),
        ),
    ]
