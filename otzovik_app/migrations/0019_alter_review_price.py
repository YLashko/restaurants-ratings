# Generated by Django 3.2.9 on 2022-09-09 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otzovik_app', '0018_alter_review_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='price',
            field=models.IntegerField(default=1),
        ),
    ]
