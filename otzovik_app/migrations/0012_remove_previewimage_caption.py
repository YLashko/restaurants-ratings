# Generated by Django 3.2.9 on 2022-08-24 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('otzovik_app', '0011_alter_previewimage_preview_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='previewimage',
            name='caption',
        ),
    ]
