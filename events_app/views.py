from django.utils import timezone
from datetime import timedelta

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated, AllowAny
from users_app.permissions import HasRolePermission

from events_app.models import *
from events_app.serializers import *

from rest_framework.pagination import PageNumberPagination
from django.db.models import Q


"""Reusable pagination class"""
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10  
    page_size_query_param = 'page_size'
    max_page_size = 100 

"""Get all the the events"""
class EventListAPIView(APIView):
    permission_classes = [AllowAny]
    pagination_class=StandardResultsSetPagination

    def get(self, request):
        period = request.query_params.get('period')
        location = request.query_params.get('location')
        keywords = request.query_params.get('keywords')

        now = timezone.now()
        start = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=7)

        if period == 'today':
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=1)
        elif period == 'week':
            start = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=7)
        elif period == 'month':
            start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            end = (start.replace(month=start.month + 1) 
                   if start.month < 12 else start.replace(year=start.year + 1, month=1))
        elif period == 'year':
            start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            end = start.replace(year=start.year + 1)

        events = Events.objects.filter(created_at__gte=start, created_at__lt=end).select_related('event_organiser')

        if location:
            events = events.filter(event_location__icontains=location)

        if keywords:
            events = events.filter
            (Q(event_name__icontains=keywords)|
             Q(event_location__icontains=keywords)|
             Q(event_date__icontains=keywords)|
             Q(event_organiser__first_name__icontains=keywords)|
             Q(event_organiser__last_name__icontains=keywords))

        paginator = self.pagination_class()
        paginated_events = paginator.paginate_queryset(events.order_by('-created_at'), request)

        serializer = EventsSerializer(paginated_events, many=True, context={'request': request})

        return paginator.get_paginated_response({
            'result_code': 0,
            'message': 'Events retrieved successfully',
            'data': serializer.data
        })

"""To allow organisers to create events"""
class EventCreateAPIView(APIView):
    permission_classes = [HasRolePermission, IsAuthenticated]
    required_permission = 'create_event'

    def post(self, request): 
        serializer = EventsSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()  
            return Response({
                'result_code':0,
                'message': 'Event created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
                'result_code':1,
                'message': 'The Event could not be created',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    
"""For updating of events"""
class EventUpdateAPIView(APIView):
    permission_classes = [HasRolePermission, IsAuthenticated]
    required_permission = 'update_event'

    def patch(self,request,id):
        event = get_object_or_404(Events, id=id)        
        serializer = EventsSerializer(event,data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()  
            return Response({
                'result_code':0,
                'message': 'Event updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
                'result_code':1,
                'message': 'The event could not be updated',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

"""For the deletion of events"""
class EventDeleteAPIView(APIView):
    permission_classes = [HasRolePermission, IsAuthenticated]
    required_permission = 'delete_event'

    def delete(self,request,id):
        try:
            event = get_object_or_404(Events, id=id) 
            event.delete()         
            return Response({
                    'result_code':0,
                    'message': 'Event deleted successfully'
                }, status=status.HTTP_200_OK)
        except Events.DoesNotExist:
            return Response({
                    'result_code':1,
                    'message': 'The event does not exist'
                }, status=status.HTTP_400_BAD_REQUEST)

"""To update the approval status of the registered attendees"""
class EventRegistrationApprovalAPIView(APIView):
    permission_classes = [HasRolePermission, IsAuthenticated]
    required_permission = 'update_event'

    def patch(self,request,id):
        event = get_object_or_404(EventRegistration, id=id)        
        serializer = EventRegistrationStatusUpdateSerializer(event,data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()  
            return Response({
                'result_code':0,
                'message': 'Registration status updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
                'result_code':1,
                'message': 'The registration status could not be updated',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

"""Funtionalities for RSVPing events"""
class EventRegisterAPIView(APIView):
    permission_classes = [HasRolePermission, IsAuthenticated]
    required_permission = 'rsvp_events'

    def post(self, request): 
        serializer = EventsRegistrationSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            event= serializer.validated_data['event']

            current_registrations=EventRegistration.objects.filter(event=event).count()
            available_seats=event.available_seats
            seats_left=available_seats-current_registrations

            if current_registrations>available_seats:
                return Response({
                'result_code':0,
                'message': 'Sorry, No more seats left.',
                'data': {}
            }, status=status.HTTP_400_BAD_REQUEST)
    
            serializer.save()  
            return Response({
                'result_code':0,
                'message': 'You have successfully registered for this event',
                'seats_left':seats_left,
                'data': serializer.data,
            }, status=status.HTTP_201_CREATED)
        return Response({
                'result_code':1,
                'message': 'Registration failed',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)