from django.db import models
from authentication.models import User
# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=225,)
    isbn = models.CharField(max_length=15,null=True,default=None)
    publication_date = models.DateField()

    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f'user: {self.user.full_name} , Title: {self.title}'