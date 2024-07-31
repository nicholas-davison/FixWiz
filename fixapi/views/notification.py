from django.http import HttpResponseServerError
from datetime import date
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from fixapi.models import Notification, Customer

class NotificationView(ViewSet):

    def list(self, request):
        current_user = Customer.objects.get(user=request.auth.user)
        try:
            notifications = Notification.objects.filter(customer=current_user, read=False)
            serializer = NotificationSerializer(notifications, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)
        
    def partial_update(self, request, pk=None):
        try:
            notification = Notification.objects.get(pk=pk)
            # Update only the fields provided in the request
            if 'read' in request.data:
                notification.read = request.data['read']
            notification.save()
            return Response({'status': 'notification updated'}, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response({'error': 'notification not found'}, status=status.HTTP_404_NOT_FOUND)

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'link', 'read', 'created_at']