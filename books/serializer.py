from rest_framework import serializers
from . import models

class UserManageBooksSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Book
        fields =[
            'title','author','isbn','publication_date','id'
        ]
        extra_kwargs ={
            'id':{'read_only':True}
        }