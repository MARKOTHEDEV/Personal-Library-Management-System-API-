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

    class BookIsbnStatus(models.TextChoices):
        bad_isbn='bad_isbn'#this should tell the user that the isbn is wrong
        saved_isbn='saved_isbn'#this tells the front end that hey! we have save the extra details please show it for them
        blank_isbn='blank_isbn' # this means it black mostly it wont be blanck becuase that just a defualt valuea
    status =   models.CharField(choices= BookIsbnStatus.choices,max_length=40,default=BookIsbnStatus.blank_isbn)
    def __str__(self):
        if not self.user:
            return ' Title: {self.title}'
        return f'user: {self.user.full_name} , Title: {self.title}'