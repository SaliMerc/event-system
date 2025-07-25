from django.db import models

from users_app.models import CustomUser

class Events(models.Model):
    event_name=models.CharField(max_length=50)
    event_location=models.CharField(max_length=50)
    event_date=models.DateTimeField()
    event_organiser=models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='events')
    available_seats=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.event_name
    
class EventRegistration(models.Model):
    APPROVAL_CHOICES = [
        ('approved', 'Approved'),
        ('not_approved', 'Not Approved'),
    ]
    event=models.ForeignKey(Events, on_delete=models.CASCADE, related_name='registered_events')
    event_attendee=models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='registered_attendees')
    approval_status=models.CharField(max_length=50, choices=APPROVAL_CHOICES, default='not_approved')
    registered_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_attendee.first_name} has registered for {self.event.event_name}"
    
    