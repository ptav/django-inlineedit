# Generated by Django 2.2.12 on 2020-05-08 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20200505_1245'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
