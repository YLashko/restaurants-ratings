# Generated by Django 4.1 on 2023-05-16 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('otzovik_app', '0031_alter_address_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='city',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='otzovik_app.city'),
            preserve_default=False,
        ),
    ]