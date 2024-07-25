from django.http import HttpResponseServerError
from datetime import date
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from fixapi.models import Contractor, Customer, ServiceRequest, ServiceRequestCategory, Category
from .category import CategorySerializer


class ServiceRequestView(ViewSet):

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized instance
        """
        current_user = Customer.objects.get(user=request.auth.user)

        service_request = ServiceRequest()
        service_request.date_created = date.today()
        service_request.customer = current_user
        service_request.urgency_level = request.data["urgency_level"]
        service_request.description = request.data["description"]
        service_request.title = request.data["title"]

        category_ids = request.data.get('category_ids', [])

        try:
            service_request.save()
            for category_id in category_ids:
                try:
                    category = Category.objects.get(id=category_id)
                    service_request_category = ServiceRequestCategory(service_request=service_request, category=category)
                    service_request_category.save()
                except Category.DoesNotExist:
                    return Response({'error': f'Category with id {category_id} does not exist.'}, status=400)
            serializer = ServiceRequestSerializer(service_request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single item

        Returns:
            Response -- JSON serialized instance
        """
        try:
            current_user = Contractor.objects.get(user=request.auth.user)
        except Contractor.DoesNotExist:
            current_user = Customer.objects.get(user=request.auth.user)
            try:
                service_request = ServiceRequest.objects.get(pk=pk, customer=current_user)
                serializer = ServiceRequestSerializer(service_request)
                return Response(serializer.data)
            except ServiceRequest.DoesNotExist:
                return Response({"reason": "Nice try but thats not your ticket!"}, status=status.HTTP_401_UNAUTHORIZED)
            
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            service_request = ServiceRequest.objects.get(pk=pk)
            if 'urgency_level' in request.data:
                service_request.urgency_level = request.data['urgency_level']
            if 'title' in request.data:
                service_request.title = request.data['title']
            if 'description' in request.data:
                service_request.description = request.data['description']
            if 'contractor' in request.data:
                service_request.contractor = request.data['contractor']
            if 'date_claimed' in request.data:
                service_request.date_claimed = request.data['date_claimed']
            if 'date_completed' in request.data:
                service_request.date_completed = request.data['date_completed']

            if 'category_ids' in request.data:
                category_ids = request.data['category_ids']
                categories = Category.objects.filter(id__in=category_ids)
                service_request.request_categories.set(categories)

            service_request.save()

        except service_request.DoesNotExist:
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
            service_request = ServiceRequest.objects.get(pk=pk)
            service_request.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except ServiceRequest.DoesNotExist as ex:
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

    #category = CategorySerializer(many=False)
    class Meta:
        model = ServiceRequestCategory
        fields = ( 'category', )

class ServiceRequestSerializer(serializers.ModelSerializer):
    """JSON serializer"""

    categories = CategorySerializer(many=True, source='get_categories')
    class Meta:
        model = ServiceRequest
        fields = ( 'id', 'title', 'date_created', 'urgency_level', 'customer', 'description', 'categories', 'contractor', 'date_claimed', 'date_completed', )



