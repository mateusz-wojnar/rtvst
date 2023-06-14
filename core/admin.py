from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import ProduktAdmin
from store.models import Produkt
from tags.models import ProduktTag
from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2",'email','first_name','last_name'),
            },
        ),
    )

class TagInline(GenericTabularInline):
    autocomplete_fields=['nazwa']
    model = ProduktTag

class CustomProduktAdmin(ProduktAdmin):
    inlines=[TagInline]

admin.site.unregister(Produkt)
admin.site.register(Produkt, CustomProduktAdmin)