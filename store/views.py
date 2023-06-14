from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet ## readonly model
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, DjangoModelPermissions
from rest_framework import status
from rest_framework.decorators import action
from .models import Produkt, Kategoria, ZamowienieSzczegoly, Opinia, Koszyk, KoszykSzczegoly, Klient
from .serializers import ProduktSerializer, KategoriaSerializer, OpiniaSerializer, KoszykSerializer, \
KoszykSzczegolySerializer, DodajProduktKoszykaSerializer, AktualizujProduktKoszykaSerializer, KlientSerializer
from .filters import ProduktFilter
from .permissions import IsAdminOrReadOnly, FullDjangoModelPermissions, ViewKlientHistoryPersmission
# Create your views here.

class ProduktViewSet(ModelViewSet):
    queryset = Produkt.objects.all()
    serializer_class = ProduktSerializer 
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProduktFilter
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['nazwa','opis']
    ordering_fields = ['cena_jednostkowa','ostatnia_aktualizacja']

    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request,pk, *args, **kwargs):
        if ZamowienieSzczegoly.objects.filter(produkt_id=kwargs['pk']).count() > 0:
            return Response({'error':'produkt nie może zostać usunięty ponieważ jest w conajmniej jednym zamówieniu'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

class KategoriaViewSet(ModelViewSet):
    queryset = Kategoria.objects.annotate(ilosc_produktow=Count('produkty')).all()
    serializer_class = KategoriaSerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request,pk, *args, **kwargs):
        kategoria = get_object_or_404(Kategoria, pk=pk)
        if kategoria.produkty.count() > 0:
            return Response({'error': 'kategoria nie może zostać usunięta ponieważ zawiera conajmniej 1 produkt'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        kategoria.delete()
        return super().destroy(request, *args, **kwargs)

    # def delete(self, request,pk):
    #     kategoria = get_object_or_404(Kategoria, pk=pk)
    #     if kategoria.produkty.count() > 0:
    #         return Response({'error': 'kategoria nie może zostać usunięta ponieważ zawiera conajmniej 1 produkt'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     kategoria.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

class OpiniaViewSet(ModelViewSet):
    serializer_class = OpiniaSerializer
    
    def get_queryset(self):
        return Opinia.objects.filter(produkt_id=self.kwargs['produkt_pk'])
    
    def get_serializer_context(self):
        return{'produkt_id': self.kwargs['produkt_pk']}
    
class KoszykViewSet(CreateModelMixin,
                    RetrieveModelMixin,
                    DestroyModelMixin,
                    GenericViewSet):
    queryset = Koszyk.objects.prefetch_related('produkty__produkt').all()
    serializer_class = KoszykSerializer

class KoszykSzczegolyViewSet(ModelViewSet):
    http_method_names = ['get','post','patch','delete']
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return DodajProduktKoszykaSerializer
        elif self.request.method == "PATCH":
                return AktualizujProduktKoszykaSerializer
        return KoszykSzczegolySerializer
    
    def get_serializer_context(self):
        return {'koszyk_id': self.kwargs['koszyk_pk']}

    def get_queryset(self):
        return KoszykSzczegoly.objects \
            .filter(koszyk_id=self.kwargs['koszyk_pk']) \
            .select_related('produkt')

    
class KlientViewSet(ModelViewSet):
    queryset = Klient.objects.all()
    serializer_class = KlientSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, permission_classes=[ViewKlientHistoryPersmission])
    def history(self, request, pk):
        serializer = KlientSerializer()
        return Response('not implemented yet')

    @action(detail = False, methods = ['GET','PUT'], permission_classes = [IsAuthenticated])
    def me(self,request):
        (klient, created) = Klient.objects.get_or_create(user_id=request.user.id)
        if request.method == 'GET':            
            serializer = KlientSerializer(klient)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = KlientSerializer(klient, data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)



    
