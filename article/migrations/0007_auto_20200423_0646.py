# Generated by Django 2.2.10 on 2020-04-23 06:46

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_ariticlepost_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ariticlepost',
            name='avatar',
            field=imagekit.models.fields.ProcessedImageField(upload_to='article/%Y%m%d'),
        ),
    ]
