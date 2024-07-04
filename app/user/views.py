"""
views for the user API"""

from rest_framework import generics, authentication, permissions #generices will handle the request in standardized way also give us to 
#override some of the behaviour.
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings  import api_settings
from user.serializers import UserSerializer, AuthTokenSerializer

class CreateUserView(generics.CreateAPIView): #createAPIView handles the HTTP post request that designed for creating the objecs inthe db.
    """Create a new user in the system."""
    serializer_class = UserSerializer #tell django which serializer to use.

class CreateTokenView(ObtainAuthToken): #normal obtainauthtoken uses username and pasword to validate
    #but our username is email, so in serializer we have modified it and here we are using it below.
    """create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView): #retrive -get, update-patch/put for single model instance.
    """manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication] #tellig here this is a token authentication.
    permission_classes = [permissions.IsAuthenticated] #telling here users who are successfully auth can access this endpoint.

    def get_object(self):
        """Retrive and return the authenticated user"""
        return self.request.user  #when ever object is required for put,patch,get generic view will call this method.
                                #also it run thru the serializer.