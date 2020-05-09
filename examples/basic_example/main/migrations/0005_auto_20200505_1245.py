# Generated by Django 2.1.12 on 2020-05-05 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_person_intchoices'),
    ]

    operations = [
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(verbose_name='URL')),
                ('label', models.CharField(max_length=32, verbose_name='Label')),
            ],
        ),
        migrations.AddField(
            model_name='person',
            name='website',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Website'),
        ),
    ]