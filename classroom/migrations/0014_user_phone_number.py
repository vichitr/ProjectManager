# Generated by Django 2.0.1 on 2018-03-28 13:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0013_user_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]
