# Generated by Django 4.2.2 on 2023-06-10 21:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='produkt',
            old_name='cena',
            new_name='cena_jednostkowa',
        ),
    ]