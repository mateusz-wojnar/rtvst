from django.urls import path, include
from rest_framework_nested import routers
from . import views
from pprint import pprint

router = routers.DefaultRouter()
router.register('produkty',views.ProduktViewSet, basename='produkty')
router.register('kategorie',views.KategoriaViewSet,'szczegoly-kategorii')
router.register('koszyki',views.KoszykViewSet)
router.register('klienci',views.KlientViewSet)

produkty_router = routers.NestedDefaultRouter(router,'produkty',lookup='produkt')
produkty_router.register('opinie',views.OpiniaViewSet, basename='produkt-opinia')

koszyki_router = routers.NestedDefaultRouter(router, 'koszyki', lookup='koszyk')
koszyki_router.register('produkty', views.KoszykSzczegolyViewSet, basename='koszyk-produkty')
# URLConf
urlpatterns = [
    path('',include(router.urls)),
    path('',include(produkty_router.urls)),
    path('',include(koszyki_router.urls))
    # path('produkty/',views.ListaProduktow.as_view()),
    # path('kategorie/',views.ListaKategorii.as_view()),
    # path('produkty/<int:pk>/',views.SzczegolyProduktu.as_view()),
    # path('kategorie/<int:pk>/',views.KatagoriaViewSet.as_view(),name='szczegoly-kategorii')
]