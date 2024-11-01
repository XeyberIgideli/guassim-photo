# Generated by Django 5.1.1 on 2024-10-31 16:43

import myapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_alter_photo_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='drive_folder_id',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='collection',
            name='image',
            field=models.ImageField(help_text='Please add name', max_length=255, null=True, upload_to=myapp.models.unique_image_path, verbose_name='Image name'),
        ),
    ]
