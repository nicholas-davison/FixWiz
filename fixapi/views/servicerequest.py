from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from fixapi.models import Contractor, Customer, ServiceRequest


class ServiceRequestView(ViewSet):

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized instance
        """
        void = Void()
        void.sample_name = request.data["name"]
        void.sample_description = request.data["description"]

        try:
            void.save()
            serializer = VoidSerializer(void)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single item

        Returns:
            Response -- JSON serialized instance
        """
        try:
            void = Void.objects.get(pk=pk)
            serializer = VoidSerializer(void)
            return Response(serializer.data)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            void = Void.objects.get(pk=pk)
            void.sample_name = request.data["name"]
            void.sample_description = request.data["description"]
            void.save()
        except Void.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return HttpResponseServerError(ex)

        return Response(None, status=status.HTTP_204_NO_CONTENT)

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

    def list(self, request):
        """Handle GET requests for all service requests

        Returns:
            Response -- JSON serialized array
            ** try getting a customer, and filter the service requests based on the customer. except it that customer does not exists, then return them all.
        """
        try:
            current_user = Customer.objects.get(user=request.auth.user)
            service_requests = ServiceRequest.objects.filter(customer=current_user)
        except Customer.DoesNotExist:
            current_user = Contractor.objects.get(user=request.auth.user)
            service_requests = ServiceRequest.objects.all()

        serializer = ServiceRequestSerializer(service_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class ServiceRequestSerializer(serializers.ModelSerializer):
    """JSON serializer"""

    class Meta:
        model = ServiceRequest
        fields = ( 'id', 'date_created', 'urgency_level', 'customer' )
