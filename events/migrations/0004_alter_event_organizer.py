# Generated by Django 5.0.4 on 2024-06-11 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_alter_event_organizer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='organizer',
            field=models.TextField(blank=True, null=True),
        ),
    ]
