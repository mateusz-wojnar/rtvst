from typing import Any, List, Optional, Tuple
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.db.models.aggregates import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . import models

# Register your models here.

class FilterMagazynowy(admin.SimpleListFilter):
    title ='Magazyn'
    parameter_name='magazyn'

    def lookups(self, request, model_admin):
        return [
            ('<25','Niski')
        ]
    
    def queryset(self, request, queryset: QuerySet):
        if self.value() == "<25":
            return queryset.filter(ilosc_na_magazynie__lt=25)

@admin.register(models.Produkt)
class ProduktAdmin(admin.ModelAdmin):
    autocomplete_fields = ['kategoria']
    prepopulated_fields = {
        'slug': ['nazwa']
    }
    actions = ['wyczysc_magazyn']
    list_display=['nazwa','cena_jednostkowa','status_magazynowy','kategoria_nazwa']
    list_editable=['cena_jednostkowa']
    search_fields=['nazwa']
    list_per_page=15
    list_select_related=['kategoria']
    list_filter= ['kategoria','ostatnia_aktualizacja',FilterMagazynowy]

    def kategoria_nazwa(self,produkt):
        return produkt.kategoria.nazwa

    @admin.display(ordering='ilosc_na_magazynie')
    def status_magazynowy(self, produkt):
        if produkt.ilosc_na_magazynie < 25:
            return 'Niski'
        return 'OK'
    
    @admin.action(description='Wyczyść stan magazynu')
    def wyczysc_magazyn(self, request, queryset: QuerySet):
        updated_count = queryset.update(ilosc_na_magazynie=0)
        self.message_user(
            request,
            f'{updated_count} produktów zostało zaaktualizowanych',
            # messages.ERROR
        )


@admin.register(models.Klient)
class KlientAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','email','ilosc_zamowien']
    list_per_page=15
    list_select_related = ['user']
    ordering = ['user__first_name','user__last_name']
    search_fields=['first_name__istartswith','last_name__istartswith']
    

    @admin.display(ordering='ilosc_zamowien')
    def ilosc_zamowien(self, klient):
        url = (
            reverse('admin:store_zamowienie_changelist')
            + '?'
            + urlencode({
                'klient_id': str(klient.id)
            }))
        return format_html('<a href="{}">{} zamówień</a>', url,klient.ilosc_zamowien)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            ilosc_zamowien=Count('zamowienie')
        )


class ZamowienieSzczegolyInline(admin.TabularInline):
    autocomplete_fields=['produkt']
    min_num = 1
    max_num = 10
    extra=0
    model = models.ZamowienieSzczegoly
    

@admin.register(models.Zamowienie)
class ZamowienieAdmin(admin.ModelAdmin):
    autocomplete_fields = ['klient']
    inlines=[ZamowienieSzczegolyInline]
    list_display = ['id','data_zlozenia','klient']

@admin.register(models.Kategoria)
class KategoriaAdmin(admin.ModelAdmin):
    list_display = ['nazwa','ilosc_produktow']
    search_fields =['nazwa']

    @admin.display(ordering='ilosc_produktow')
    def ilosc_produktow(self, kategoria):
        url = (
            reverse('admin:store_produkt_changelist') 
            + '?'
            + urlencode({
                'kategoria__id': str(kategoria.id)
            }))
        return format_html('<a href="{}">{}</a>',url,kategoria.ilosc_produktow)
         
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            ilosc_produktow=Count('produkty')
        )
