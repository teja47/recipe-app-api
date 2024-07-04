"""views for the recipe APIs"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

class RecipeViewSet(viewsets.ModelViewSet): #modelviewset will support all the CRUD operations.
    """view for manage recipe APIs"""
    serializer_class = RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication] 
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrive recipes for auth user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """return the serialzer class for request"""
        if self.action == 'list':
            return RecipeSerializer #no need to put () at the end bcz we are referancing class not object of the class
        return self.serializer_class

    def perform_create(self,serializer):
        """create a new recipe"""
        serializer.save(user=self.request.user)