from decimal import Decimal
from rest_framework import serializers
from .models import Produkt, Kategoria, Opinia, Koszyk, KoszykSzczegoly, Klient


class KategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kategoria
        fields = ['id','nazwa','ilosc_produktow']

    ilosc_produktow = serializers.IntegerField(read_only=True)

class ProduktSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produkt
        fields = ['id','nazwa','opis','slug','ilosc_na_magazynie','cena_jednostkowa','cena_z_vat','kategoria']
    # id = serializers.IntegerField()
    # nazwa = serializers.CharField(max_length=255)
    # cena = serializers.DecimalField(max_digits=8,decimal_places=2, source='cena_jednostkowa')
    cena_z_vat = serializers.SerializerMethodField(method_name='oblicz_vat')

    def oblicz_vat(self,produkt: Produkt):
        return produkt.cena_jednostkowa * Decimal(1.23)

class OpiniaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opinia
        fields = ['id','data','nazwa','opis']

    def create(self, validated_data):
        produkt_id = self.context['produkt_id']
        return Opinia.objects.create(produkt_id=produkt_id, **validated_data)
    
class SimpleProduktSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produkt
        fields = ['id','nazwa','cena_jednostkowa']

class KoszykSzczegolySerializer(serializers.ModelSerializer):
    produkt = SimpleProduktSerializer()
    suma = serializers.SerializerMethodField()

    def get_suma(self, koszyk_szczegoly: KoszykSzczegoly):
        return koszyk_szczegoly.ilosc * koszyk_szczegoly.produkt.cena_jednostkowa

    class Meta:
        model = KoszykSzczegoly
        fields = ['id','produkt','ilosc','suma']

class KoszykSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    produkty = KoszykSzczegolySerializer(many=True, read_only=True)
    suma = serializers.SerializerMethodField()

    def get_suma(self, koszyk: Koszyk):
       return sum([prod.ilosc * prod.produkt.cena_jednostkowa  for prod in koszyk.produkty.all()]) 

    class Meta:
        model = Koszyk
        fields = ['id','produkty', 'suma']

class DodajProduktKoszykaSerializer(serializers.ModelSerializer):
    produkt_id = serializers.IntegerField()

    def validate_produkt_id(self, value):
        if not Produkt.objects.filter(pk=value).exists():
            raise serializers.ValidationError('Produkt z danym id nie istnieje')
        return value


    def save(self, **kwargs):
        koszyk_id = self.context['koszyk_id']
        produkt_id = self.validated_data['produkt_id']
        ilosc = self.validated_data['ilosc']

        try:
            koszyk_szczegoly = KoszykSzczegoly.objects.get(koszyk_id=koszyk_id, produkt_id=produkt_id)
            koszyk_szczegoly.ilosc += ilosc
            koszyk_szczegoly.save()
            self.instance = koszyk_szczegoly
        except KoszykSzczegoly.DoesNotExist:
            self.instance = KoszykSzczegoly.objects.create(koszyk_id=koszyk_id, **self.validated_data)

        return self.instance

    class Meta:
        model = KoszykSzczegoly
        fields = ['id','produkt_id','ilosc']

class AktualizujProduktKoszykaSerializer(serializers.ModelSerializer):
    class Meta:
        model = KoszykSzczegoly
        fields = ['ilosc']

class KlientSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Klient
        fields = ['id','user_id','data_urodzenia','nr_telefonu']



    # def create(self, validated_data): ## called by save
    #     produkt = Produkt(**validated_data)
    #     produkt.other=1
    #     produkt.save()
    #     return produkt
    
    # def update(self, instance, validated_data): ## called by save depending on serializer
    #     instance.cena_jednostkowa = validated_data.get('cena_jednostkowa')
    #     instance.save()
    #     return instance
    
    # walidacja hasla
    # def validate(self, data):
    #     if data['password'] != data['confirm_password']:
    #         return serializers.ValidationError('Hasła nie są takie same')
    #     return data
    

    # {
    #     "nazwa": "testowy produkt2",   
    #     "slug": "testowy-produkt2",
    #     "ilosc_na_magazynie": 50,
    #     "cena_jednostkowa": 2346.67,
    #     "kategoria": "http://127.0.0.1:8000/store/kategorie/10/"
    # }

    # /store/koszyki/db82eb98-abb7-4a36-aa34-81b403c702da/

    # acces token usertest1 djangodjango
    # "refresh": eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4Njc3MTMzNSwiaWF0IjoxNjg2Njg0OTM1LCJqdGkiOiI4ZjljNjgwMTViN2Y0Y2IyYTdkZDZhYmVmZjJkMGJkNSIsInVzZXJfaWQiOjV9.Lnsbp1I51f88hZnEkQvcZK4Clvs2A9EOZkF5c8WvkKs
    # "access": eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg2NzcxMzM1LCJpYXQiOjE2ODY2ODQ5MzUsImp0aSI6ImRjNmQwM2UxOTc3MjRkNmViNDRmOTRjYTIxZWE5NTA0IiwidXNlcl9pZCI6NX0.SeXL1ZZy24GiySHRx61jx3Qf1IcPxGfOlixsfv2Nbbo