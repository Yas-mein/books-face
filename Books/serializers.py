from rest_framework import serializers
from .models import Book

class AllBooksSerializer(serializers.ModelSerializer):
    new_position = serializers.IntegerField()
    
    class Meta:
        model = Book
        fields = '__all__'