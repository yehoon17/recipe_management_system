# Generated by Django 4.2.11 on 2024-03-31 03:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_alter_rating_value'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Review',
        ),
    ]
