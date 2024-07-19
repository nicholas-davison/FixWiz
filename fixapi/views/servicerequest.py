from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from fixapi.models import Contractor, Customer, ServiceRequest, ServiceRequestCategory
from .category import CategorySerializer


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
            service_request = ServiceRequest.objects.get(pk=pk)
            serializer = ServiceRequestSerializer(service_request)
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
        """Handle GET requests for all service requests"""
        try:
            service_requests = ServiceRequest.objects.filter(contractor=None)
            serializer = ServiceRequestSerializer(service_requests, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ServiceRequestCategorySerializer(serializers.ModelSerializer):
    """JSON serializer"""

    category = CategorySerializer(many=False)
    class Meta:
        model = ServiceRequestCategory
        fields = ( 'category', )

class ServiceRequestSerializer(serializers.ModelSerializer):
    """JSON serializer"""

    categories = ServiceRequestCategorySerializer(many=True)
    class Meta:
        model = ServiceRequest
        fields = ( 'id', 'date_created', 'urgency_level', 'customer', 'categories', 'contractor' )

