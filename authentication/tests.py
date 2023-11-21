from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import  status
# Create your tests here.


class TestSetUp(APITestCase):
    
    
    def setUp(self) -> None:
        self.register_url = reverse('adduser-list')    
        self.login_url = reverse('login')    
        self.refresh_token_url = reverse('token-refresh')
        self.user_payload ={
            "email":"marko@gmail.com",
            "password":"backup2020",
            "first_name":"Nwokolo",
            "last_name":"Matthew"
        } 

        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()
    

    def test_create_user_withincompleteinfo(self):
        res =self.client.post(self.register_url,)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)


    def test_create_user_with_completedate(self):
        res =self.client.post(self.register_url,data=self.user_payload)
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)

    def test_login_with_empty_data(self):
        res =self.client.post(self.login_url,)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)


    def test_login_without_password(self):
        data = {
         'email':self.user_payload['email'],
        }
        res =self.client.post(self.login_url,data=data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)


    def test_login_without_email(self):
        data = {
         'password':self.user_payload['password'],
        }
        res =self.client.post(self.login_url,data=data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_login_with_completepayload(self):
        self.createUserSetUp()
        data = {
         'email':self.user_payload['email'],
         'password':self.user_payload['password'],
        }
        res =self.client.post(self.login_url,data=data)
        self.assertEqual(res.status_code,status.HTTP_200_OK)


    def createUserSetUp(self):
        res =self.client.post(self.register_url,data=self.user_payload)
        