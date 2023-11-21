from django.shortcuts import render
from rest_framework import viewsets
from . import serializer,models,permissions
from utils.pagination import LargeResultsSetPagination

class UserManageBooksViewset(viewsets.ModelViewSet):
    serializer_class = serializer.UserManageBooksSerializer
    queryset = models.Book.objects.all()
    permission_classes = [ permissions.IsAuthenticated,permissions.IsOwner]
    pagination_class=LargeResultsSetPagination
    

    def get_queryset(self):
        'this function just help filter the list to get only logged in user data'
        return super().get_queryset().filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
        return super().perform_create(serializer)
    

    