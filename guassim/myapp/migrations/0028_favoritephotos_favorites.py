# Generated by Django 5.1.1 on 2024-11-02 20:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0027_alter_favorites_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='favoritephotos',
            name='favorites',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.favorites'),
        ),
    ]
