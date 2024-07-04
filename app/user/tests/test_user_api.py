"""
Test for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
 
CREATE_USER_URL = reverse('user:create') #in urls.py will find the app_name= user.
TOKEN_URL = reverse('user:token') 
ME_URL = reverse('user:me')
def create_user(**params):
    """create and return a new user"""
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creatng a user is successful."""
        payload = {
            'email': 'test@example.com',
            'password': 'pass123',
            'name': 'test name'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)


    def test_user_with_email_exists_error(self):
        """test error returned if user with email exists."""
        payload={
            'email': 'test@example.com',
            'password': 'pass123',
            'name': 'test name'           
        }
        create_user(**payload) #adding ** is ntg but email='test@example' password= 'pass123' name= 'test name'
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_password_too_short_error(self):
        """test an error is returned if password less than 5 chars"""
        payload={
            'email': 'test@example.com',
            'password': 'p3',
            'name': 'test name'           
        }   
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists= get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)    
    
    def test_create_token_for_users(self):
        """test generates token for vaild credentails"""
        user_details= {
            'name': 'testnew name',
            'email': 'test22new@example.com',
            'password': 'Pass13'
        }

        create_user(**user_details)

        payload= {
            'email': user_details['email'],
            'password': user_details['password'],

        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token',res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_create_token_bad_credentails(self):
        """test return error if credits invaild"""
        create_user(email='test24@example.com', password='pass123') #user created successfully.
        payload ={'email':'test24@example.com','password': 'basishd'}

        res = self.client.post(TOKEN_URL,payload) #vaildating the user credits which is wrong.

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_credentails(self):
        """test return error if password is blank"""
        #here no need to create user bcz before creating user it should though the bad request.
        payload ={'email':'test@example.com','password': ''}

        res = self.client.post(TOKEN_URL,payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_retrive_user_unauthorized(self): #not logged in(class name) but doing a get request.
        """test auth is required for users."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateuserApiTests(TestCase):
    """test API requests that require auth"""

    def setUp(self):
        self.user = create_user(
            email='test222@example.com',
            password='pass233',
            name='test222',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user) #force authenticaing so that no need repeat in below methods.
    
    def test_retrive_profile_success(self):
        """test retriving profile for logged in user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email,
        })
    
    def test_post_me_not_allowed(self):
        """test POST not allowed for 'me' endpoint"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """test updating user profile for authenticated user"""
        payload = {
            'name': 'updated name',
            'password': 'updatedpass'
        }

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

