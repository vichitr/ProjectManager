# Generated by Django 2.0.1 on 2018-03-30 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0017_auto_20180330_0421'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='projects',
            field=models.ManyToManyField(related_name='myprojects', to='classroom.Project'),
        ),
    ]
