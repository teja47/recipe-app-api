"""
Test django admin modifications

"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

class AdminSiteTest(TestCase):
    """Test for Django admin."""

    def setUp(self):
        """Create user and client."""
        self.client = Client() 
        #client is a django test client allow us to do the HTTP request for testing.
        #simpleTestCase cannot do HTTP, only testCase.
        self.admin_user = get_user_model().objects.create_superuser(
            email = 'amdin1@example.com',
            password = 'Pass123',
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email = 'usertest@example.com',
            password = 'Pass123',
            name = 'test user'
        )

    def test_users_list(self):
        """Test that users are listed on page.""" #3. testing of all user list
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
    
    def test_edit_user_page(self):
        """Test that users are listed on page.""" #2. test of user page edit.
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
    
    def test_create_user_page(self):
        """test to create user page works"""  #1.just to test if create user page is working or not
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)