# from django.shortcuts import render

# # Create your views here.
# from rest_framework.decorators import api_view
# from rest_framework.response import Response

# @api_view(['GET','POST','PUT'])
# def index(request):
#     COURSES={
#         'Course_name':'python',
#         'learn':{'flask','django','tornado','fastAPi'},
#         'Course_provider':'Scaler',
#     }
#     if request.method=='GET':
#         print('You hit a GET method!');
#         return Response(COURSES)
#     elif request.method=='POST':
#         data=request.data
#         print("*****")
#         print(data['name'])
#         print("****")
#         print('You hit a POST method!');
#         return Response(COURSES)
#     elif request.method=='PUT':
#         print('You hit a PUT method!');
#         return Response(COURSES)
    # return Response({"message": "Hello, world!"})
    
    # SERIALIZER : you pass some data and it convert to the jason response
    # its help you to convert all of your query set and all of your data 
    # django queries and the data you can get from the django covert to the jason file
#    if you want to save some data  you can directly convert jason response
#    into a query set and save into a database
# basically its a class that convert the data in the form of a query set into a jason response
# TYPES OF SERIALIZERS:
#     MODEL SERIALIZERS

# from rest_framework import serializers
from functools import partial
from urllib import request
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework import viewsets
# status code in DRF 
from rest_framework import status

from rest_framework.views import APIView
from home.models import Person
from home.serializers import LoginSerializer, PeopleSerializer,RegisterSerializer
# import a token :
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate
# import the user model
from django.contrib.auth.models import User
# Permission policy: and also import permission classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

# token atuhtentication
from rest_framework.authentication import TokenAuthentication 

# import pagindation
from django.core.paginator import Paginator
#  import Action Policy
from rest_framework.decorators import action

class LoginAPI(APIView):
    def post(self,request):
        data=request.data
        serializer=LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                'status':False,
                'message':serializer.errors
            },status.HTTP_400_BAD_REQUEST)
            # this method the check the username and password correct or not
        print(serializer.data)
        user=authenticate(username=serializer.data['username'],password=serializer.data['password'])
        print(user)
        if not user:
            return Response({
                'status':False,
                'message':'invalid credentials'
            },status.HTTP_400_BAD_REQUEST)
        token=Token.onjects.get_or_create(user=user)
        print(token)
        return Response({
            'status':True,
            'message':'user login',
            'token':str(token)
        },status.HTTP_201_CREATED)




# create an api for register the user  by using class RegisterAPI and APIView class
# to create a user we need email password username
class RegisterAPI(APIView):
    def post(self,request):
        data=request.data
        serializer=RegisterSerializer(data=data)
        
        if not serializer.is_valid():
            return Response({
                'status':False,
                'message':serializer.errors
            },status.HTTP_400_BAD_REQUEST)
            
        serializer.save()
        return Response({'status':True,'message':'user created'},status.HTTP_201_CREATED)
            
         
        

@api_view(['GET','POST'])

def index(request):
    if request.method=='GET':
        json_response={
            'name':'Scaler',
            'course':['C++','Python'],
            'method':'GET'
        }
        # print(json_response)
    else:
        data=request.data
        print(data)
        json_response={
            'name':'scaler',
            'courses':['C++','Python'],
            'method':'POST'
        }
        
        return Response(json_response)
  
  
  
  
@api_view(['POST'])  
def login(request):
    data=request.data
    serializer=LoginSerializer(data=data)
    if serializer.is_valid():
        data=serializer.data
        print(data)
        return Response({'message':'success'})
    
    return Response(serializer.errors)
      
    # creating an API to help us toget all the people which will help us again to create the people
  
class PersonAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    def get(self,request):
    
        print(request.user)
        objs=Person.objects.all()
        # objs=Person.objects.filter(color__isnull=False)
        page=request.GET.get('page',1)
        pag_size=3
        paginator=Paginator(objs,pag_size)
        print(paginator.page(page))
        serializer=PeopleSerializer(paginator.page(page),many=True) 
        return Response(serializer.data)
    # except Exception as e:
    #     return Response({
    #         'status':False,
    #         'message':'invalid page'
    #     })
        # return Response({"message":"This is a get request"})
        
    def post(self,request):
        data=request.data
        serializer=PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
        # return Response({"message":"This is a post request"})
  
    def put(self,request):
        data=request.data
        serializer=PeopleSerializer(data=data)
        if serializer.is_valid():
           serializer.save()
           return Response(serializer.data)
        
        return Response(serializer.errors)
    
        # return Response({"message":"This is a put request"})
  
    def patch(self,request):
        data=request.data
        obj=Person.objects.get(id=data['id'])
        serializer=PeopleSerializer(obj,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
        # return Response({"message":"This is a patch request"})
  
    def delete(self,request):
        data=request.data
        obj=Person.objects.get(id=data['id'])
        obj.delete()
        return Response({'message':'person deleted'})
    
        # return Response({"message":"This is a delete request"})
      
   
@api_view(['GET','POST','PUT','PATCH','DELETE'])  
def person(request):
    if request.method == 'GET':
        objs=Person.objects.filter(color__isnull=False)
        serializer=PeopleSerializer(objs,many=True) 
        return Response(serializer.data)
    
    elif request.method== 'POST':
        data=request.data
        serializer=PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    elif request.method=='PUT':
        data=request.data
        serializer=PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    elif request.method=='PATCH':
        data=request.data
        obj=Person.objects.get(id=data['id'])
        serializer=PeopleSerializer(obj,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)
    
    else:
        data=request.data
        obj=Person.objects.get(id=data['id'])
        obj.delete()
        return Response({'message':'person deleted'})

    # patch support partial updation and put does not 
    # support partial updation its means Put update all 
    # the values but the Patch can update only partial values 
    
        
class PeopleViewSet(viewsets.ModelViewSet):   
    serializer_class=PeopleSerializer
    queryset=Person.objects.all()     
    # to allow the which methos is created ir not only two method or requires
# suppose we want to create an api that should be able to only  get
#     we want to apply only two method get and post
#     model view said is capable of handling all the methods like whether its a put patch get method
#     if we crreate an api and we don't want to update the api we use the keyword called http method name
#     
# here is the method naem and we only allow get and post method
    # you want to limit he api request
    http_method_names=['get','post']

    def  list(self,request):
        search=request.GET.get('search')
        queryset=self.queryset
        if search:
            queryset=queryset=queryset.filter(name__startswith=search)
        
        serializer=PeopleSerializer(queryset,many=True)
        return Response({'status':200,'data': serializer.data},status=status.HTTP_200_OK)
            # serializer.save()
            # progrmer use to show the error messages is helpful for frontend developer 

    
    @action(detail=True,methods=['GET','post'])
    def    send_mail_to_person(self,request,pk):
        obj=Person.objects.get(pk=pk)
        # print(pk)
        serializer=PeopleSerializer(obj)
        return Response({
           'status':True,
           'message':'email sent successfully',
           'data':serializer.data
        }) 
    
