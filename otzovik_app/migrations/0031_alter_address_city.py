# Generated by Django 4.1 on 2023-05-16 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('otzovik_app', '0030_rename_city_name_address_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='otzovik_app.city'),
            preserve_default=False,
        ),
    ]
