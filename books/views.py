from django.shortcuts import render
from rest_framework import viewsets
from . import serializer,models,permissions
from utils.pagination import LargeResultsSetPagination
from django.utils.decorators import method_decorator
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_ratelimit.decorators import ratelimit


@method_decorator(ratelimit(key='ip', rate='12/m', method='GET'), name='list')
class UserManageBooksViewset(viewsets.ModelViewSet):
    serializer_class = serializer.UserManageBooksSerializer
    queryset = models.Book.objects.all()
    permission_classes = [ permissions.IsAuthenticated,permissions.IsOwner]
    pagination_class=LargeResultsSetPagination
    

    def get_queryset(self):
        'this function just help filter the list to get only logged in user data'
        return super().get_queryset().filter(user=self.request.user)
    def perform_create(self, serializer):
        'this function just help me add the logged in user as the owner of the instance'
        serializer.save(user = self.request.user)
        return super().perform_create(serializer)
    