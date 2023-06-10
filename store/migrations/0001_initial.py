# Generated by Django 4.2.2 on 2023-06-10 21:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Kategoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Klient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imie', models.CharField(max_length=255)),
                ('nazwisko', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('nr_telefonu', models.CharField(max_length=255)),
                ('data_urodzenia', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Koszyk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_stworzenia', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Produkt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=255)),
                ('opis', models.TextField()),
                ('cena', models.DecimalField(decimal_places=2, max_digits=8)),
                ('ilosc_na_magazynie', models.IntegerField()),
                ('ostatnia_aktualizacja', models.DateTimeField(auto_now=True)),
                ('kategoria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='store.kategoria')),
            ],
        ),
        migrations.CreateModel(
            name='Promocja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opis', models.CharField(max_length=255)),
                ('rabat', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Zamowienie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_zlozenia', models.DateTimeField(auto_now_add=True)),
                ('stan_płatnosci', models.CharField(choices=[('P', 'W trakcie'), ('C', 'Zakończone'), ('F', 'Niepowodzenie')], default='P', max_length=1)),
                ('klient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='store.klient')),
            ],
        ),
        migrations.CreateModel(
            name='AdresKlienta',
            fields=[
                ('miasto', models.CharField(max_length=255)),
                ('ulica', models.CharField(max_length=255)),
                ('klient', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='store.klient')),
            ],
        ),
        migrations.CreateModel(
            name='ZamowienieSzczegoly',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ilosc', models.PositiveSmallIntegerField()),
                ('cena_jednostkowa', models.DecimalField(decimal_places=2, max_digits=8)),
                ('produkt', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='store.produkt')),
                ('zamowienie', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='store.zamowienie')),
            ],
        ),
        migrations.AddField(
            model_name='produkt',
            name='promocje',
            field=models.ManyToManyField(to='store.promocja'),
        ),
        migrations.CreateModel(
            name='KoszykSzczegoly',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ilosc', models.PositiveSmallIntegerField()),
                ('koszyk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.koszyk')),
                ('produkt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.produkt')),
            ],
        ),
    ]