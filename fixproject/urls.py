from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from fixapi.models import *
from fixapi.views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'customers', Customers, 'customer')
router.register(r'users', Users, 'user')
router.register(r'service_requests', ServiceRequestView, 'service_request')
router.register(r'profile', ProfileView, 'profile')
router.register(r'categories', CategoryView, 'category')
router.register(r'service_request_categories', ServiceRequestCategoryView, 'service_request_category')


urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-token-auth', obtain_auth_token),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]

