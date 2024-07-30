""" from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from fixapi.models import Customer
from .user import UserSerializer


class CustomerSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    class Meta:
        model = Customer
        fields = ('id', 'user', 'phone_number', 'address')


class Customers(ViewSet):

    def update(self, request, pk=None):

        customer = Customer.objects.get(user=request.auth.user)
        customer.user.last_name = request.data["last_name"]
        customer.user.email = request.data["email"]
        customer.address = request.data["address"]
        customer.phone_number = request.data["phone_number"]
        customer.user.save()
        customer.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
 """