from django_filters.rest_framework import FilterSet
from .models import Produkt

class ProduktFilter(FilterSet):
    class Meta:
        model = Produkt
        fields = {
            'kategoria_id': ['exact'],
            'cena_jednostkowa': ['gt','lt']
        }