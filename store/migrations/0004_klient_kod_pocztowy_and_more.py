# Generated by Django 4.2.2 on 2023-06-10 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_produkt_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='klient',
            name='kod_pocztowy',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddIndex(
            model_name='klient',
            index=models.Index(fields=['imie', 'nazwisko'], name='store_klien_imie_4f5d09_idx'),
        ),
        migrations.AlterModelTable(
            name='klient',
            table='store_klient',
        ),
    ]
