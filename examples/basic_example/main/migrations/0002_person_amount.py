# Generated by Django 2.1.12 on 2020-05-01 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='amount',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
