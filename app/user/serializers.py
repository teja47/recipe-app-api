"""serializers for the users API view"""
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """serializer for the user object"""
 
    class Meta:  #this is where we tell the DRF,  the model, fields, extraargs that we want to pass
        #to the serialize set.
        model = get_user_model() #serializer need to know which model its representing, 'USER'-here
        fields = ['email', 'password', 'name'] #is_staff, is_active shouldbe set by admin, so not mentioning here.
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
    
    def create(self, validated_data):  #here we are overwriting the normal create behaviour.
        #serializers only called after the validation of the data,like min_length=5 
        """create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)
    
    def update(self, instance, validated_data):
        """update and return user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password) #by doing this password will not saved like a text,
            #it will be hashed.
            user.save()
        return user

    
class AuthTokenSerializer(serializers.Serializer):
    """serializer for the user auth token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style = {'input_type': 'password'},
        trim_whitespace = False,
    )

    def validate(self, attrs):
        """validate and authenticate the user."""
        email = attrs.get('email') #willget these attrs from view.py
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username = email,
            password = password
        )

        if not user:
            msg = _('unable to validate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')
        
        attrs['user'] = user
        
        return attrs