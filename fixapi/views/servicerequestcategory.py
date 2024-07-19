from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from fixapi.models import ServiceRequestCategory, ServiceRequest
from .category import CategorySerializer


class ServiceRequestCategoryView(ViewSet):
    """Void view set"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized instance
        """
        service_request_category = ServiceRequestCategory()
        service_request_category.service_request = request.data["service_request"]
        service_request_category.category = request.data["category"]

        try:
            service_request_category.save()
            serializer = ServiceRequestCategorySerializer(service_request_category)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single item

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            service_request_category = ServiceRequestCategory.objects.get(pk=pk)
            service_request_category.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except service_request_category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests for all items

        Returns:
            Response -- JSON serialized array
        """
        try:
            service_request = ServiceRequest.objects.get(pk=request.data['service_request'])
            service_request_category = ServiceRequestCategory.objects.filter(service_request=service_request)
            serializer = ServiceRequestCategorySerializer(service_request_category, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)


class ServiceRequestCategorySerializer(serializers.ModelSerializer):
    """JSON serializer"""
    category = CategorySerializer()
    class Meta:
        model = ServiceRequestCategory
        fields = ( 'id', 'service_request', 'category' )
