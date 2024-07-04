"""
Tests for models.

"""
from decimal import Decimal
from django.test import TestCase #using testcase instead of simpletestcase bcz this one have access to DB.
from django.contrib.auth import get_user_model
from core import models
class ModelTest(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """test creating user with email is sucessful. """ #these are called docstring explains the purpose of the test.
        email = "test@example.com"
        password = "Pass123"
        user = get_user_model().objects.create_user(
            email = email,
            password = password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
    
    def test_new_user_email_normalized(self):
        """test email is normailzed for new users"""
        sample_emails= [
            ['test1@EXAMPLE.COM', 'test1@example.com'],
            ['Test2@EXAMPLE.COM', 'Test2@example.com']
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'samplw121')
    
    def test_create_superuser(self):
        """Test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            'test1@example.com',
            'Pass123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
    
    def test_create_recipe(self):
        """test creating a recipe succesfully."""
        user = get_user_model().objects.create_user(
            email= 'tests@example.com',
            password= 'pass123',
        )
        recipe = models.Recipe.objects.create(
            user = user,
            title = 'sample recipe title',
            time_minutes =5,
            price = Decimal('5.50'),
            description = 'sample descrip'
        )

        self.assertEqual(str(recipe), recipe.title)
