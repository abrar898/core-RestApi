from django.urls import include, path
from home.views import LoginAPI, PersonAPI, index, person, login, PeopleViewSet,RegisterAPI

from rest_framework.routers import DefaultRouter
# Define the router
router = DefaultRouter()
router.register(r'people', PeopleViewSet, basename='people')
urlpatterns=router.urls

urlpatterns=[
    path('',include(router.urls)),
    path('index/',index),
    path('login/',LoginAPI.as_view(),),
    path('register/',RegisterAPI.as_view(),),
    path('person/',person),
    path('login/',login),
    # when you use API class view then we have to add urls in different manner
    #  path('person_api_class')
    # when we call the route person we call the api view decorator method 
    
    # if we write person then we call api-view class
    path('persons/',PersonAPI.as_view())
]