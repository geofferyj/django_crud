# Generated by Django 3.2.7 on 2021-09-09 19:59

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('spellchecker', '0002_rename_jobid_matchederror_job_id'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='matchederror',
            managers=[
                ('serializeable', django.db.models.manager.Manager()),
            ],
        ),
    ]