# Generated by Django 4.2.6 on 2024-03-02 01:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_alter_lead_email_alter_lead_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='about',
            name='created',
        ),
        migrations.RemoveField(
            model_name='about',
            name='update',
        ),
    ]
