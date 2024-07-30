from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User
from fixapi.models import Customer
from fixapi.models import Contractor


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for Users

    Arguments:
        serializers
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email', 'is_active', 'date_joined')

class CustomerSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    class Meta:
        model = Customer
        fields = ('id', 'user', 'phone_number', 'address')


class ContractorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Contractor
        fields = ('id','user', 'phone_number', 'address')


class Users(ViewSet):
    """Users for FixWiz
    Purpose: Allow a user to communicate with the FixWiz database to GET PUT POST and DELETE Users.
    Methods: GET PUT(id) POST
"""


    def retrieve(self, request, pk=None):
        """Handle GET requests for single customer
        Purpose: Allow a user to communicate with the FixWiz database to retrieve  one user
        Methods:  GET
        Returns:
            Response -- JSON serialized customer instance
        """
        try:
            contractor = Contractor.objects.get(pk=pk)
            serializer = ContractorSerializer(contractor, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to user resource"""
        users = User.objects.all()
        serializer = UserSerializer(
            users, many=True, context={'request': request})
        return Response(serializer.data)