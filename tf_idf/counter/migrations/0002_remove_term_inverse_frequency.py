# Generated by Django 3.2 on 2024-04-02 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('counter', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='term',
            name='inverse_frequency',
        ),
    ]