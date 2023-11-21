from django.test import TestCase
from rest_framework.test import APITestCase,APIClient
from django.urls import reverse
from rest_framework import  status
from authentication.models import User


class TestSetUpAuthenticatedEndPoint(APITestCase):
    
    
    def setUp(self) -> None:
        'because this is a protected route we need to create a user and force auth it so we can test freely'
        self.user_payload ={
        "email":"marko@gmail.com",
        "password":"backup2020",
        "first_name":"Nwokolo",
        "last_name":"Matthew"
        } 
        self.book ={
            "title": "hello world",
            "author": "wrendfc",
            "isbn": "9780140328721d",
            "publication_date": "2023-11-21"
        }
        self.user = self.createUserSetUp()

        self.client =APIClient()
        self.client.force_authenticate(user=self.user)
        
        self.book_url_create = reverse('managebook-list')
        self.book_url_list = reverse('managebook-list')
        # self.book_url_patch = reverse('managebook-patch')
        return super().setUp()
    

    def tearDown(self) -> None:
        return super().tearDown()
    
    def createUserSetUp(self):
        user =User.objects.create_user(**self.user_payload)
        return user
    

    def test_creation_of_book_empty_request(self):
        resp = self.client.post(self.book_url_create,)

        self.assertEqual(resp.status_code,status.HTTP_400_BAD_REQUEST)

    def test_creation_of_book(self):
        resp = self.client.post(self.book_url_create,data=self.book)

        self.assertEqual(resp.status_code,status.HTTP_201_CREATED)


    def test_delete_book(self):
        resp = self.client.post(self.book_url_create,data=self.book)
        data =resp.json()
        self.assertEqual(resp.status_code,status.HTTP_201_CREATED)
        self.book_url_delete = reverse('managebook-detail',args=[data['id']])
        delete_resp = self.client.delete(self.book_url_delete,)
        self.assertEqual(delete_resp.status_code,status.HTTP_204_NO_CONTENT)

    def test_delete_book_with_wrongid(self):
        self.book_url_delete = reverse('managebook-detail',args=[34])
        delete_resp = self.client.delete(self.book_url_delete,)
        self.assertEqual(delete_resp.status_code,status.HTTP_404_NOT_FOUND)

    def test_update_data(self):
        resp = self.client.post(self.book_url_create,data=self.book)
        data =resp.json()
        self.assertEqual(resp.status_code,status.HTTP_201_CREATED)

        self.book_url_update = reverse('managebook-detail',args=[data['id']])
        update_resp = self.client.patch(self.book_url_update,)
        self.assertEqual(update_resp.status_code,status.HTTP_200_OK)

    

    def test_update_data_withwrong_id(self):

        self.book_url_update = reverse('managebook-detail',args=[77])
        update_resp = self.client.patch(self.book_url_update,)
        self.assertEqual(update_resp.status_code,status.HTTP_404_NOT_FOUND)
