from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from fixapi.models import Category


class CategoryView(ViewSet):
    """Void view set"""

    def list(self, request):
        """Handle GET requests for all items

        Returns:
            Response -- JSON serialized array
        """
        try:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)


class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer"""

    class Meta:
        model = Category
        fields = ( 'id', 'name' )
