# Generated by Django 3.2.9 on 2022-09-30 19:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('otzovik_app', '0023_profilecuisinestatistics'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='otzovik_app.profile')),
            ],
        ),
    ]
