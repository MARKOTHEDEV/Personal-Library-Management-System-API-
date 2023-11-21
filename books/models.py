from django.db import models
from authentication.models import User
# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=225,)
    isbn = models.CharField(max_length=15,null=True,default=None)
    publication_date = models.DateField()
    extra_info = models.JSONField(null=True,default=None)

    user = models.ForeignKey(User,on_delete=models.CASCADE,default=None,null=True)

    def __str__(self):
        if not self.user:
            return ' Title: {self.title}'
        return f'user: {self.user.full_name} , Title: {self.title}'