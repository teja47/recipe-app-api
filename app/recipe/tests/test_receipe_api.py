"""test for recipe API."""
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Recipe
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPES_URL = reverse('recipe:recipe-list')

def detail_url(recipe_id):
    """Create and return a recipe detail URL"""
    return reverse('recipe:recipe-detail', args= [recipe_id])

def create_recipe(user, **params):
    """create and return a sample recipe."""
    defaults = {
        'title': 'sample recipe title',
        'time_minutes' : 22,
        'price' : Decimal(5.25),
        'description' : 'sample descrip',
        'link' : 'http://sample.com/recipe.pdf',
    }
    defaults.update(params) #here updating/overriding default dict if anything is provided in the params.
        #eg: create_recipe(link='http://somelink.com') this will override above link rest willbe default.

    recipe = Recipe.objects.create(user =user, **defaults)
    return recipe

class PublicRecipeAPITest(TestCase):
    """test unauth API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateRecipeApiTest(TestCase):
    """test auth API REQUESTS"""
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'pass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrive_recipes(self):
        """test receiving alist of recipes"""
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    
    def test_recipe_list_limited_to_user(self):
        """test list of recipes is limited to auth user."""
        other_user =get_user_model().objects.create_user(
            'some@example.com',
            'pass123'
        )
        create_recipe(user = other_user)
        create_recipe(user = self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user = self.user)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_recipe_detail(self):
        """test get recipe detail"""
        recipe = create_recipe(user = self.user)
        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)    

    def test_create_recipe(self):
        """test creating recipe"""
        payload = {
            'title': 'sample recipe',
            'time_minutes' : 5,
            'price' : Decimal('3.4')

        }
        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id= res.data['id'])
        for k,v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)

        


