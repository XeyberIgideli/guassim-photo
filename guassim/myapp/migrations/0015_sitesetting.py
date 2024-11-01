# Generated by Django 5.1.1 on 2024-10-31 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_rename_drive_folder_id_photo_google_drive_photo_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Site title')),
                ('description', models.TextField(verbose_name='Site description')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='site_logos/', verbose_name='Logo')),
                ('favicon', models.ImageField(blank=True, null=True, upload_to='favicons/', verbose_name='Favicon')),
                ('is_active', models.BooleanField(default=True, verbose_name='Acttive')),
            ],
            options={
                'verbose_name': 'Site Settings',
                'verbose_name_plural': 'Site Settings',
            },
        ),
    ]