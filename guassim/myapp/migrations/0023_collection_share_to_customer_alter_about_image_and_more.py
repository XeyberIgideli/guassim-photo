# Generated by Django 5.1.1 on 2024-11-02 09:14

import django.db.models.deletion
import functools
import myapp.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0022_category_name_az_category_name_en_category_name_ru'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='share_to_customer',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='about',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=functools.partial(myapp.utils.unique_image_path, *(), **{'folder_name': 'about'}), verbose_name='Profile Photo'),
        ),
        migrations.AlterField(
            model_name='collection',
            name='image',
            field=models.ImageField(help_text='Please add image', max_length=255, null=True, upload_to=functools.partial(myapp.utils.unique_image_path, *(), **{'folder_name': 'collections'}), verbose_name='Image'),
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.photo')),
            ],
        ),
    ]