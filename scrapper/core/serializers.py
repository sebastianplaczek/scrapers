from rest_framework import serializers
from core.models import LinksToScrap,UsersLinks
from django.contrib.auth.models import User
from rest_framework.authtoken.views import Token

class LinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinksToScrap
        fields = ['link','item_name','create_date','service','active','deactivate_date']

class UserLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersLinks
        fields = ['id','user','linktoscrap','active','create_date']



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields = ['id','username','password']
        extra_kwargs = { 'password' : {
            'write_only' : True,
            'requied' : True
        }}

    def create(self,validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user

class LinkNestedSerializer(serializers.ModelSerializer):
    linktoscrap = LinksSerializer()

    class Meta:
        model= UsersLinks
        fields = '__all__'







