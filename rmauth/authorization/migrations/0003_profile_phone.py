# Generated by Django 4.0.6 on 2022-07-23 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0002_requisites_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=models.CharField(default=None, max_length=13, null=True),
        ),
    ]
