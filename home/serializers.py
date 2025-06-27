from rest_framework import serializers
from .models import Person,Color
from django.contrib.auth.models import User

# create a user requires three given things
class RegisterSerializer(serializers.Serializer):
    username=serializers.CharField()
    email=serializers.EmailField()
    password=serializers.CharField()
    
    
    # to check the user name has already in a database or not
    def validate(self,data):
        if data['username']:
            if User.objects.filter(uername=data['username']).exists():
                raise serializers.ValidationError('username is already taken')
     # to check the user email has already in a database or not
    def validate(self,data):
        if data['email']:
            if User.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError('email is already taken')
        return data
    
    def create(self,validated_data):
        user=User.objects.create(username=validated_data['username'],email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        print(validated_data)
        return validated_data


class LoginSerializer(serializers.Serializer):
    username= serializers.CharField()
    password=serializers.CharField()




# Validation of data
class ColorSerializer(serializers.ModelSerializer):

    class Meta: 
        model=Color
        fields=['color_name','id']

class PeopleSerializer(serializers.ModelSerializer):
    color=ColorSerializer()
    color_info=serializers.SerializerMethodField()
    class Meta: 
        model=Person
        fields='__all__'
        # depth=1
    # add validate to the prefix name age dob  with the prefix validate_age validate_name
    # def validate_age(self,data):
    #     print(data)
    #     return data
    
    def get_color_info(self,obj):
        color_obj=Color.objects.get(id=obj.color.id)
        return {'color_name':color_obj.color_name,'hex_code':'#000'}    
    
    def validate(self,data): 
        special_characters="!@#$%^&*()_+-?/.,:<>"
        if any (c in special_characters for c in data['name']):
            raise serializers.ValidationError('name cannot contain special character')
        
        
        # if data['age']< 18:
        #     raise serializers.ValidationError('age should be greater than 18')
        
        return data
            