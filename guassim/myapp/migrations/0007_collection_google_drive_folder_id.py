# Generated by Django 5.1.1 on 2024-10-30 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_alter_category_slug_alter_collection_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='google_drive_folder_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]