from rest_framework import serializers
from events_app.models import EventRegistration, Events

class EventsSerializer(serializers.ModelSerializer):
    event_organiser_name=serializers.SerializerMethodField()
    class Meta:
        model = Events
        fields = ['id','event_name','event_location','event_date','event_organiser_name','available_seats','created_at']
        read_only_fields = ['created_at','event_organiser_name','event_organiser']
    
    def get_event_organiser_name(self, obj):
        return f"{obj.event_organiser.first_name} {obj.event_organiser.last_name}"
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['event_organiser'] = request.user 
        return super().create(validated_data)


class EventsRegistrationSerializer(serializers.ModelSerializer):
    event_name=serializers.SerializerMethodField()
    class Meta:
        model = Events
        fields = ['id','event_name','approval_status','registered_on']
        read_only_fields = ['registered_on']
    
    def get_event_name(self, obj):
        return obj.event.event_name
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['event_attendee'] = request.user 
        return super().create(validated_data)