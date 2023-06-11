from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.

class Promocja(models.Model):
    opis = models.CharField(max_length=255)
    rabat = models.FloatField()

class Kategoria(models.Model):
    nazwa = models.CharField(max_length=255)
    def __str__(self) -> str:
        return self.nazwa
    
    class Meta:
        ordering = ['nazwa']
        verbose_name_plural = 'Kategorie'

class Produkt(models.Model):
    nazwa = models.CharField(max_length=255) # varchar 255
    slug = models.SlugField()
    opis = models.TextField(null=True, blank=True)
    cena_jednostkowa = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0,message="Minimalna cena to 0 zł")]
        )
    ilosc_na_magazynie = models.IntegerField(
        validators=[MinValueValidator(0,message="Minimalny stan magazynowy to 0")]
    )
    ostatnia_aktualizacja = models.DateTimeField(auto_now=True)
    kategoria = models.ForeignKey(Kategoria, on_delete=models.PROTECT)
    promocje = models.ManyToManyField(Promocja, blank=True)

    def __str__(self) -> str:
        return self.nazwa
    
    class Meta:
        ordering=['nazwa']
        verbose_name_plural = 'Produkty'



class Koszyk(models.Model):
    data_stworzenia = models.DateTimeField(auto_now_add=True)

class Klient(models.Model):
    imie = models.CharField(max_length=255)
    nazwisko = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    nr_telefonu = models.CharField(max_length=255)
    data_urodzenia = models.DateField()

    def __str__(self) -> str:
        return f'{self.imie} {self.nazwisko}'

    class Meta:
        db_table = 'store_klient'
        indexes = [
            models.Index(fields=['imie','nazwisko'])
        ]
        ordering=['imie','nazwisko']
        verbose_name_plural = 'Klienci'

class AdresKlienta(models.Model):
    miasto = models.CharField(max_length=255)
    ulica = models.CharField(max_length=255)
    klient = models.OneToOneField(Klient, on_delete=models.CASCADE, primary_key=True)

class Zamowienie(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'W trakcie'),
        (PAYMENT_STATUS_COMPLETE, 'Zakończone'),
        (PAYMENT_STATUS_FAILED, 'Niepowodzenie')
    ]

    data_zlozenia = models.DateTimeField(auto_now_add=True)
    stan_płatnosci = models.CharField(max_length=1,choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    klient = models.ForeignKey(Klient, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.id

    class Meta:
        ordering=['-id']
        verbose_name_plural = 'Zamówienia'

class ZamowienieSzczegoly(models.Model):
    zamowienie = models.ForeignKey(Zamowienie, on_delete=models.PROTECT)
    produkt = models.ForeignKey(Produkt, on_delete=models.PROTECT)
    ilosc = models.PositiveSmallIntegerField()
    cena_jednostkowa = models.DecimalField(max_digits=8,decimal_places=2)

    class Meta:
        verbose_name_plural = 'Produkty szczegółowe'

class KoszykSzczegoly(models.Model):
    koszyk = models.ForeignKey(Koszyk, on_delete=models.CASCADE)
    produkt = models.ForeignKey(Produkt, on_delete=models.CASCADE)
    ilosc = models.PositiveSmallIntegerField()
