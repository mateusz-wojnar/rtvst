# Generated by Django 4.2.2 on 2023-06-10 23:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_klient_kod_pocztowy_and_more'),
    ]

    operations = [
        migrations.RunSQL("""
            INSERT INTO store_kategoria (nazwa)
            VALUES ('kategoria1')
        ""","""
            DELETE FROM store_kategoria
            WHERE nazwa='kategoria1'
        """)
    ]
