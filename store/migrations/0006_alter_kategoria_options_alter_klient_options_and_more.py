# Generated by Django 4.2.2 on 2023-06-11 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20230611_0120'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='kategoria',
            options={'ordering': ['nazwa'], 'verbose_name_plural': 'Kategorie'},
        ),
        migrations.AlterModelOptions(
            name='klient',
            options={'ordering': ['imie', 'nazwisko'], 'verbose_name_plural': 'Klienci'},
        ),
        migrations.AlterModelOptions(
            name='produkt',
            options={'ordering': ['nazwa'], 'verbose_name_plural': 'Produkty'},
        ),
        migrations.AlterModelOptions(
            name='zamowienie',
            options={'ordering': ['-id'], 'verbose_name_plural': 'Zamówienia'},
        ),
        migrations.RemoveField(
            model_name='klient',
            name='kod_pocztowy',
        ),
    ]
