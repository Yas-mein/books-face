

from .serializers import *
from rest_framework import generics
# from django.urls import reverse
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from django_filters import rest_framework as filters
# from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
######################3

class BookFilter(FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Book
        fields = ['title']

class BookListAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = AllBooksSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        data = response.data
        for book_data in data:
            book_id = book_data['id']
            favorite_url = reverse('toggle_favorite_book', args=[book_id])
            book_data['favorite_url'] = favorite_url
        return Response(data)


class BUpdateAPI(generics.UpdateAPIView):
    serializer_class = AllBooksSerializer
    queryset = Book.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.new_position = request.data.get('new_position')
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

################

class oneBOOK(generics.RetrieveUpdateDestroyAPIView):
        queryset = Book.objects.all()
        serializer_class = AllBooksSerializer


class ToggleFavoriteBook(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = AllBooksSerializer

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_favorite = not instance.is_favorite
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class FavoriteBooksList(generics.ListAPIView):
    queryset = Book.objects.filter(is_favorite=True)
    serializer_class = AllBooksSerializer