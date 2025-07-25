from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from users_app.roles import EventOrganiserRole, EventAttendeeRole
from rolepermissions.roles import assign_role

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('organiser', 'Organiser'),
        ('attendee', 'Attendee'),
    ]
    
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=191,unique=True)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='attendee')
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            self.assign_role_permissions()
    
    def assign_role_permissions(self):
        """Assign role permissions based on user role"""
        
        role_mapping = {
            'organiser': EventOrganiserRole,
            'attendee': EventAttendeeRole,
        }
        
        role_class = role_mapping.get(self.role)
        if role_class:
            assign_role(self, role_class)

    def __str__(self):
        return self.email