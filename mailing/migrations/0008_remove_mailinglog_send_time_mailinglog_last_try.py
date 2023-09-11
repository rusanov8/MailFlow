# Generated by Django 4.2.4 on 2023-09-06 14:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0007_mailing_end_time_alter_mailing_frequency_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailinglog',
            name='send_time',
        ),
        migrations.AddField(
            model_name='mailinglog',
            name='last_try',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата и время последней попытки'),
            preserve_default=False,
        ),
    ]
