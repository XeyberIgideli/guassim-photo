# Generated by Django 5.1.1 on 2024-11-03 13:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0030_favorites_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='favorites',
            name='photo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='myapp.photo'),
        ),
    ]
