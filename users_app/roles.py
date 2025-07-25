from rolepermissions.roles import AbstractUserRole

class EventOrganiserRole(AbstractUserRole):
    available_permissions = {
        'create_event': True,
        'view_their_events': True,
        'view_all_events': True,
        'update_event': True,
        'delete_event': True,
    }

class EventAttendeeRole(AbstractUserRole):
    available_permissions = {
        'rsvp_events': True,
        'view_rsvpd_events': True,
        'view_all_events': True,

    }
