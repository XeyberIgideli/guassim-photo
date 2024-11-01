# Generated by Django 5.1.1 on 2024-10-30 12:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_remove_collection_google_drive_id_collection_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('google_drive_id', models.CharField(max_length=50)),
                ('alt_text', models.TextField(blank=True, null=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='myapp.collection')),
            ],
            options={
                'verbose_name': 'Collection Photo',
                'verbose_name_plural': 'Collection Photos',
            },
        ),
    ]