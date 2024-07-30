from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from fixapi.models import Customer, Contractor, ServiceRequest
from .servicerequest import ServiceRequestSerializer
from .user import CustomerSerializer


class ProfileView(ViewSet):


    def list(self, request, pk=None):
        """Handle GET requests for single item

        Returns:
            Response -- JSON serialized instance
        """
        user = request.auth.user
        try:
            user_profile = Customer.objects.get(user=user)
            serializer = CustomerSerializer(user_profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            user_profile = Contractor.objects.get(user=user)
            serializer = ContractorSerializer(user_profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def update(self, request, pk=None):
        """Handle PUT requests

        Returns:
            Response -- Empty body with 204 status code
        """
        user = request.auth.user
        user.username = request.data.get("username", user.username)
        user.email = request.data.get("email", user.email)
        user.first_name = request.data.get("first_name", user.first_name)
        user.last_name = request.data.get("last_name", user.last_name)
        user.save()

        try:
            user_profile = Customer.objects.get(user=user)
        except Customer.DoesNotExist:
            user_profile = Contractor.objects.get(user=user)
        except Contractor.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)
        
        user_profile.phone_number = request.data["phone_number"]
        user_profile.address = request.data["address"]
        user_profile.save()

        
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    '''
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single item

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            void = Void.objects.get(pk=pk)
            void.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except Void.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    '''

    @action(methods=['get'], detail=False)
    def service_requests(self, request):

        user = request.auth.user
        ticket_status = self.request.query_params.get('status', None)

        try:
            current_user = Customer.objects.get(user=user)
            if ticket_status is None:
                service_requests = ServiceRequest.objects.filter(customer=current_user, date_completed__isnull=True)
            else:
                service_requests = ServiceRequest.objects.filter(customer=current_user, date_completed__isnull=False)
        except Customer.DoesNotExist:
            try:
                current_user = Contractor.objects.get(user=user)
                if ticket_status is None:
                    service_requests = ServiceRequest.objects.filter(contractor=current_user, date_completed__isnull=True)
                else:
                    service_requests = ServiceRequest.objects.filter(contractor=current_user, date_completed__isnull=False)
            except Contractor.DoesNotExist:
                return Response({'message': 'User not found as Customer or Contractor'}, status=status.HTTP_404_NOT_FOUND)

        serialized = ServiceRequestSerializer(service_requests, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
                 
'''
class ProfileSerializer(serializers.ModelSerializer):
    """JSON serializer"""

    class Meta:
        model = Void
        fields = ( 'id', 'sample_name', 'sample_description', )
'''
