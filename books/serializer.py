from rest_framework import serializers
from . import models
import requests
class UserManageBooksSerializer(serializers.ModelSerializer):

    extra_info = serializers.SerializerMethodField()
    def create(self, validated_data):
        book = models.Book.objects.create(**validated_data)
        self.request_extra_info(book)
        return book

    def get_extra_info(self,book:models.Book):
        if book.status == models.Book.BookIsbnStatus.bad_isbn:
            return None
        return book.extra_info

    def request_extra_info(self,book:models.Book):
        url = f'https://openlibrary.org/isbn/{book.isbn}.json'
        # try:
        resp = requests.get(url=url)
        if resp.status_code ==200:
            data = resp.json()
            book.status=models.Book.BookIsbnStatus.saved_isbn
            book.extra_info=data
            book.save()
        else:
            book.status=models.Book.BookIsbnStatus.bad_isbn
            book.save()
    
    def update(self, instance, validated_data):
        super().update(instance, validated_data) 
        isbn = validated_data.get('isbn',None)
        if isbn:
            self.request_extra_info(instance)

        return instance
    class Meta:
        model = models.Book
        fields =[
            'title','author','isbn','publication_date','id','extra_info','status'
        ]
        extra_kwargs ={
            'id':{'read_only':True}
        }

