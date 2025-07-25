from django.urls import path
from events_app.views import *

urlpatterns = [
    path('create-event/', EventCreateAPIView.as_view(), name='create-event'),
    path('update-event/<int:id>/', EventUpdateAPIView.as_view(), name='update-event'),
    path('delete-event/<int:id>/', EventDeleteAPIView.as_view(), name='delete-event'),
    path('event-list/', EventListAPIView.as_view(), name='event-list'),

    path('event-rsvp/', EventRegisterAPIView.as_view(), name='event-rsvp'),
]
