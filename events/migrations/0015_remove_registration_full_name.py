# Generated by Django 5.0.4 on 2024-06-15 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_registration_contact_number_registration_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registration',
            name='full_name',
        ),
    ]
