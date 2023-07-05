# Generated by Django 4.1 on 2023-05-16 09:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('otzovik_app', '0028_rename_company_restaurant_company_profile_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='address',
            name='city',
        ),
        migrations.AddField(
            model_name='address',
            name='city_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='otzovik_app.city'),
        ),
    ]
