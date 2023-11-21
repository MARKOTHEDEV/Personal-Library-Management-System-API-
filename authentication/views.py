from rest_framework import viewsets
from rest_framework.response import Response
from . import serializer
from rest_framework import status
from utils.response_data import response_data,Res


class RegisterUserViewset(viewsets.ViewSet):
    permission_classes = []
    serializer_class = serializer.RegisterUserSerializers

    def create(self,request,*args,**kwargs):
        serialized = self.serializer_class(data=request.data)
        serialized.is_valid(raise_exception=True)
        data = serialized.save()
        clean_data = self.serializer_class(instance=data)
        return Res(status=status.HTTP_201_CREATED,data=clean_data.data,message='Created Successfully')