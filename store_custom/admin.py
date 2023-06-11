from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import ProduktAdmin
from store.models import Produkt
from tags.models import ProduktTag

# Register your models here.
class TagInline(GenericTabularInline):
    autocomplete_fields=['nazwa']
    model = ProduktTag

class CustomProduktAdmin(ProduktAdmin):
    inlines=[TagInline]

admin.site.unregister(Produkt)
admin.site.register(Produkt, CustomProduktAdmin)