from rest_framework import viewsets
from rest_framework.response import Response
from . import serializer
from rest_framework import status
from utils.response_data import response_data,Res
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.settings import api_settings
from rest_framework.exceptions import AuthenticationFailed
class RegisterUserViewset(viewsets.ViewSet):
    permission_classes = []
    serializer_class = serializer.RegisterUserSerializers

    def create(self,request,*args,**kwargs):
        serialized = self.serializer_class(data=request.data)
        serialized.is_valid(raise_exception=True)
        data = serialized.save()
        clean_data = self.serializer_class(instance=data)
        return Res(status=status.HTTP_201_CREATED,data=clean_data.data,message='Created Successfully')
    


class LoginView(TokenObtainPairView):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = serializer.LoginSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES



class CustomTokenRefreshView(TokenRefreshView):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = serializer.CustomTokenRefreshSerializer



    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except AuthenticationFailed as e:
            # data = response_data(401, str(e), [])
            return Res(401, str(e), [])
        return Res(200,
            "Token Refresh successful",
            {"tokens": serializer.validated_data},)