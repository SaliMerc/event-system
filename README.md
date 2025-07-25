Event Management System- Django REST Framework

Project Purpose

This project is a robust event management system for both event organisers and attendees

Tech Stack

- Backend Framework: Django 4.x
- API Framework: Django REST Framework (DRF)
- Database: SQLite
- Authentication: Token Authentication (JWT)
- Validation: Django model validators + DRF serializers
- Testing: Postman collection

Features Implemented

1. Event creation
2. Event update
3. Event deletion
4. Events list view
5. Event Registration
6. Registration approval
7. User signup
8. User login

Setup Instructions

Prerequisites

- Python 3.9+
- pip (Python package manager)
- Virtualenv (recommended)

Installation

1. Clone the repository:
   ```bash
   git clone (https://github.com/SaliMerc/user-management-system/)
   cd UserManagement
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   Linux: source venv/bin/activate
   On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser (admin account):
   ```bash
   python manage.py createsuperuser
   ```

Running the Development Server
```bash
python manage.py runserver
```
The API will be available at `http://localhost:8000/api/`

Postman Collection

The repository includes a Postman collection (`https://salinemercy.postman.co/workspace/Saline-Mercy's-Workspace~7d90ad68-1f65-4df4-8a66-051acda73610/collection/44878844-4764ff37-39a8-4d36-be6d-4417d732b6eb?action=share&source=copy-link&creator=44878844`) with pre-configured requests for all API endpoints. 


API ENDPOINTS   
1. User Login

   Endpoint: /api/users/login/  
   Method: POST  
   Request Body:    
      ```json
      {
       "username": "string",
       "password": "string"
      }
   ```
   Response:  
      ```json
      {
       "message": "string",
       "access": "string",
       "refresh": "string"
      }
      ```
2. User signup

   Endpoint: /api/users/create/  
   Method: POST  
   Headers:  
   Content-Type: form-data  
   
   Request Body:  
      ```json
      {
        "id": "integer",
        "password": "string",
        "username": "string",
        "email": "string",
        "first_name": "string",
        "last_name": "string",
        "role": "string",
      }
      ```
   Response:  
      ```json
       {
           "username": "string",
           "email": "string",
           "first_name": "string",
           "last_name": "string",
           "role": "string",
       }
      ```
3. Create event

   Endpoint: /api/events/create-event/  
   Method: POST  
   Headers:  Authorization ${Bearer}
   Content-Type: form-data  
   
   Request Body:  
      ```json
      {
        "id": "integer",
        "event_name": "Parteeeey",
        "event_location": "Nairobi",
        "event_date": "2025-08-11T02:03:46.145000Z",
        "event_organiser_name": "katy perry",
        "available_seats": 40,
      }
      ```
   Response:  
      ```json
       {
    "result_code": 0,
    "message": "Event created successfully",
    "data": {
        "id": 7,
        "event_name": "Parteeeey",
        "event_location": "Nairobi",
        "event_date": "2025-08-11T02:03:46.145000Z",
        "event_organiser_name": "katy perry",
        "available_seats": 40,
        "created_at": "2025-07-25T13:29:03.653890Z"
    }
}
      ```

4. Update an event

   Endpoint: /api/events/update-event/id/  
   Method: PATCH 
   Headers:  Authorization ${Bearer}
   Content-Type: form-data  
   
   Request Body:  
      ```json
      {
        "event_name": "Parteeeey",
        "event_location": "Nairobi",
        "event_date": "2025-08-11T02:03:46.145000Z",
        "available_seats": 40,
      }
      ```
   Response:  
      ```json
       {
    "result_code": 0,
    "message": "Event updated successfully",
    "data": {
        "id": 7,
        "event_name": "Parteeeey",
        "event_location": "Nairobi",
        "event_date": "2025-08-11T02:03:46.145000Z",
        "event_organiser_name": "katy perry",
        "available_seats": 40,
        "created_at": "2025-07-25T13:29:03.653890Z"
    }
}
      ```
5. Delete an event

   Endpoint: /api/events/delete-event/id/  
   Method: DELETE  
   Headers:  Authorization ${Bearer}
   Content-Type: form-data  
    
   Response:  
      ```json
       {
    "result_code": 0,
    "message": "Event deleted successfully"
}
      ```

6. Approve a registered attendee

   Endpoint: /api/events/event-registration-approval/id/  
   Method: PATCH 
   Headers:  Authorization ${Bearer}
   Content-Type: form-data  
   
   Request Body:  
      ```json
      {
        "approval_status": "approved",
      }
      ```
   Response:  
      ```json
    {
    "result_code": 0,
    "message": "Registration status updated successfully",
    "data": {
        "id": 4,
        "event_attendee": 8,
        "approval_status": "approved"
    }
} 
      ```

7. View all events

   Endpoint: /api/events/event-list/  
   Method: GET 
   Headers:  Authorization ${Bearer}
   Content-Type: json
   
      ```
   Response:  
      ```json
    {
       "result_code": 0,
       "message": "Events retrieved successfully",
       "data": 
      [
        
           {
               "id": 4,
               "event_name": "Parteeeey",
               "event_location": "Nairobi",
               "event_date": "2025-08-11T02:03:46.145000Z",
               "event_organiser_name": "katy perry",
               "available_seats": 40,
               "created_at": "2025-07-25T11:57:11.753815Z"
           }
   
      ]
        }
      ```

   3. RSVP An event

   Endpoint: /api/events/event-rsvp/  
   Method: POST  
   Headers:  Authorization ${Bearer}
   Content-Type: form-data  
   
   Request Body:  
      ```json
      {
        "event": "integer",
      }
      ```
   Response:  
      ```json
    {
    "result_code": 0,
    "message": "You have successfully registered for this event",
    "seats_left": 36,
    "data": {
        "id": 23,
        "event": 4,
        "event_name": "Parteeeey",
        "event_attendee": 8,
        "approval_status": "not_approved",
        "registered_on": "2025-07-25T12:48:57.454751Z"
    }
   }
      ```



