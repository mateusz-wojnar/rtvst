from django.contrib import admin
from django.core.validators import MinValueValidator
from django.conf import settings
from django.db import models
from uuid import uuid4

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
    kategoria = models.ForeignKey(Kategoria, on_delete=models.PROTECT,related_name='produkty')
    promocje = models.ManyToManyField(Promocja, blank=True)

    def __str__(self) -> str:
        return self.nazwa
    
    class Meta:
        ordering=['nazwa']
        verbose_name_plural = 'Produkty'



class Koszyk(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    data_stworzenia = models.DateTimeField(auto_now_add=True)
    

class KoszykSzczegoly(models.Model):
    koszyk = models.ForeignKey(Koszyk, on_delete=models.CASCADE, related_name='produkty')
    produkt = models.ForeignKey(Produkt, on_delete=models.CASCADE)
    ilosc = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1,message='Minimalna ilość to 1')]
    )

    class Meta:
        unique_together = [['koszyk','produkt']]

class Klient(models.Model):
    nr_telefonu = models.CharField(max_length=255,null=True, blank=True)
    data_urodzenia = models.DateField(null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    
    def email(self):
        return self.user.email

    class Meta:
        db_table = 'store_klient'
        ordering=['user__first_name','user__last_name']
        verbose_name_plural = 'Klienci'
        permissions = [
            ('zobacz_historie','Może zobaczyć historię')
        ]

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
        permissions = [
            ('anuluj zamowienie', 'Może anulować zamówienia')
        ]

class ZamowienieSzczegoly(models.Model):
    zamowienie = models.ForeignKey(Zamowienie, on_delete=models.PROTECT)
    produkt = models.ForeignKey(Produkt, on_delete=models.PROTECT, related_name='zamowioneprodukty')
    ilosc = models.PositiveSmallIntegerField()
    cena_jednostkowa = models.DecimalField(max_digits=8,decimal_places=2)

    class Meta:
        verbose_name_plural = 'Produkty szczegółowe'


class Opinia(models.Model):
    produkt = models.ForeignKey(Produkt, on_delete=models.CASCADE, related_name='opinie')
    nazwa = models.CharField(max_length=255)
    opis = models.TextField()
    data = models.DateField(auto_now_add=True)