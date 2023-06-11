from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, connection
from django.db.models import Q, F, Value, Func, ExpressionWrapper, DecimalField
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from django.db.models.functions import Concat
from django.contrib.contenttypes.models import ContentType
from store.models import Produkt, ZamowienieSzczegoly, Zamowienie, Klient, Kategoria
from tags.models import ProduktTag

# Create your views here.
# request -> response
# request handler
# action

# @transaction.atomic()
def say_hello(request): ## LOOKUP TYPES QUERY SETS
    queryset = Produkt.objects.filter(Q(ilosc_na_magazynie__lt = 10) | ~Q(cena_jednostkowa__lt = 20)) ##gt, gte, lt, lte, range, contains, icontains, startswith, endswith, year, month, day, isnull
    queryset2 = Produkt.objects.filter(kategoria__id=1).order_by('cena_jednostkowa')
    queryset3 = Produkt.objects.all()[5:5] ## offset, limit
    queryset4 = Produkt.objects.values_list('id','nazwa','kategoria__nazwa') ## inner join values, values_list
    queryset5 = Produkt.objects.filter(id__in=ZamowienieSzczegoly.objects.values('produkt_id').distinct()).order_by('nazwa') ## nested queries
    queryset6 = Produkt.objects.only('id','nazwa') ## raczej nie uzywac

    # prefetch_related gdy jest relacja wiele to wielu
    queryset7 = Produkt.objects.select_related('kategoria__').all() ## join select_related jak jeden produkt ma jedna kategorie
    queryset8 = Zamowienie.objects.select_related('klient').prefetch_related('zamowienieszczegoly_set__produkt').order_by('-data_zlozenia')[:5]

    ### agregacje
    result = Produkt.objects.filter(kategoria__id = 1).aggregate(count = Count('id'), min_cena = Min('cena_jednostkowa'))

    ## expressions
    queryset9 = Klient.objects.annotate(new_id=F('id')+ 1)

    ## database func
    queryset10 = Klient.objects.annotate(
        imie_nazwisko =Func(F('imie'), Value(' '), F('nazwisko'), function='CONCAT')
    )
    queryset10v2 = Klient.objects.annotate(
        imie_nazwisko = Concat('imie', Value(' '), 'nazwisko')
    )

    ## grouping ilosc zamowien klienta
    queryset11 = Klient.objects.annotate(
        ilosc_zamowien = Count('zamowienie')
    )

    ## Expression wrapper
    cena_promocyjna = ExpressionWrapper(F('cena_jednostkowa') * 0.8, output_field=DecimalField(decimal_places=2))
    queryset12 = Produkt.objects.annotate(
        cena_promocyjna=cena_promocyjna
    )

    ##Querying generic relationships

    content_type = ContentType.objects.get_for_model(Produkt)

    queryset13 = ProduktTag.objects \
        .select_related('nazwa') \
        .filter(
        content_type=content_type,
        object_id =1
    )

    ##Custom managers
    ProduktTag.obj.get_tags_for(Produkt,1)
    
    ## creating objects, insert into
    # kategoria = Kategoria()
    # kategoria.nazwa = "Karta dźwiękowa"
    # kategoria.save()

    ## updating objects, update
    # kategoria = Kategoria.objects.get(pk=16)
    # kategoria.nazwa = "Karta dźwiękowa"
    # kategoria.save()

    #Kategoria.objects.filter(pk=16).update(nazwa='coś')

    ## deleting objects
    # kategoria = Kategoria(pk=11)
    # kategoria.delete()

    # Kategoria.objects.filter(id__gt=5).delete()

    ## Transactions
    # with transaction.atomic():
    #     zamowienie = Zamowienie()
    #     zamowienie.klient_id = 1
    #     zamowienie.save()

    #     item = ZamowienieSzczegoly()
    #     item.zamowienie = zamowienie
    #     item.produkt_id = 1
    #     item.ilosc = 1
    #     item.cena_jednostkowa = 10
    #     item.save()

    ## Raw sql
    # querysetraw = Produkt.objects.raw('SELECT id, nazwa FROM store_produkt')

    with connection.cursor() as cursor:
        cursor.execute()
        cursor.callproc('get_klient', [1,2,3])


    return render(request, 'hello.html', {'name': 'Mosh', 'tags': list(queryset13)})


