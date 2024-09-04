from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
   
    class Meta:
       model = User
       fields =  ['username', 'password', 'phone', 'address', 'gender', 'age', 'description' ,'first_name', 'last_name' ,'email']
         
    def create(self,validated_data ):
       user = User.objects.create_user(
           username=validated_data['username'],
           password=validated_data['password'],
           phone=validated_data.get('phone', ''),
           address=validated_data.get('address', ''),
           gender=validated_data.get('gender', User.Gender.UNSET),
           age=validated_data.get('age', None),
           description=validated_data.get('description', ''),
           first_name = validated_data.get('first_name',),
           last_name = validated_data.get('last_name',),
           email = validated_data.get('email', ''),
       )  
       return user
       
       
       
       
       
       
       