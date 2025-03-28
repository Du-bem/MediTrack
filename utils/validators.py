"""
Validation utilities for MediTrack
"""
import re
from datetime import datetime

def validate_email(email):
    """Validate email format"""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        raise ValueError("Invalid email format")
    return True

def validate_phone(phone):
    """Validate phone number format"""
    # Allow various phone formats
    phone_pattern = r'^(\+\d{1,3}[- ]?)?$$?\d{3}$$?[- ]?\d{3}[- ]?\d{4}$'
    if not re.match(phone_pattern, phone):
        raise ValueError("Invalid phone number format")
    return True

def validate_date(date_str, format="%Y-%m-%d"):
    """Validate date format"""
    try:
        datetime.strptime(date_str, format)
        return True
    except ValueError:
        raise ValueError(f"Invalid date format. Expected format: {format}")

def validate_datetime(datetime_str, format="%Y-%m-%d %H:%M"):
    """Validate datetime format"""
    try:
        datetime.strptime(datetime_str, format)
        return True
    except ValueError:
        raise ValueError(f"Invalid datetime format. Expected format: {format}")

def validate_patient_id(patient_id):
    """Validate patient ID format"""
    # Patient ID should start with 'P' followed by alphanumeric characters
    pattern = r'^P[A-Z0-9]{8}$'
    if not re.match(pattern, patient_id):
        raise ValueError("Invalid patient ID format. Expected format: P followed by 8 alphanumeric characters")
    return True

def validate_doctor_id(doctor_id):
    """Validate doctor ID format"""
    # Doctor ID should start with 'D' followed by alphanumeric characters
    pattern = r'^D[A-Z0-9]{8}$'
    if not re.match(pattern, doctor_id):
        raise ValueError("Invalid doctor ID format. Expected format: D followed by 8 alphanumeric characters")
    return True

def validate_required_fields(data, required_fields):
    """Validate that all required fields are present"""
    missing_fields = [field for field in required_fields if field not in data or data[field] is None]
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
    return True

def validate_appointment_time(time_str, working_hours=(9, 17)):
    """Validate that appointment time is within working hours"""
    try:
        appointment_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        hour = appointment_time.hour
        
        if not (working_hours[0] <= hour < working_hours[1]):
            raise ValueError(f"Appointment time must be between {working_hours[0]}:00 and {working_hours[1]}:00")
        
        return True
    except ValueError as e:
        if "format" in str(e):
            raise ValueError("Invalid datetime format. Expected format: YYYY-MM-DD HH:MM")
        raise

