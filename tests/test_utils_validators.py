"""
Tests for validation utilities
"""
import unittest
import os
import sys
from datetime import datetime

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.validators import (
    validate_email, validate_phone, validate_date, validate_datetime,
    validate_patient_id, validate_doctor_id, validate_required_fields,
    validate_appointment_time
)

class TestValidators(unittest.TestCase):
    """Test cases for validators"""
    
    def test_validate_email(self):
        """Test email validation"""
        # Valid emails
        self.assertTrue(validate_email("john.doe@example.com"))
        self.assertTrue(validate_email("jane_smith123@company-name.co.uk"))
        self.assertTrue(validate_email("user+tag@domain.org"))
        
        # Invalid emails
        with self.assertRaises(ValueError):
            validate_email("not_an_email")
        
        with self.assertRaises(ValueError):
            validate_email("missing@domain")
        
        with self.assertRaises(ValueError):
            validate_email("@domain.com")
        
        with self.assertRaises(ValueError):
            validate_email("user@.com")
    
    def test_validate_phone(self):
        """Test phone validation"""
        # Valid phone numbers
        self.assertTrue(validate_phone("555-123-4567"))
        self.assertTrue(validate_phone("(555) 123-4567"))
        self.assertTrue(validate_phone("5551234567"))
        self.assertTrue(validate_phone("+1 555-123-4567"))
        
        # Invalid phone numbers
        with self.assertRaises(ValueError):
            validate_phone("123-456")
        
        with self.assertRaises(ValueError):
            validate_phone("not-a-phone")
        
        with self.assertRaises(ValueError):
            validate_phone("555-123-45678")
    
    def test_validate_date(self):
        """Test date validation"""
        # Valid dates
        self.assertTrue(validate_date("2023-01-01"))
        self.assertTrue(validate_date("2023-12-31"))
        
        # Invalid dates
        with self.assertRaises(ValueError):
            validate_date("2023-13-01")
        
        with self.assertRaises(ValueError):
            validate_date("2023-01-32")
        
        with self.assertRaises(ValueError):
            validate_date("not-a-date")
        
        # Different format
        self.assertTrue(validate_date("01/15/2023", format="%m/%d/%Y"))
        
        with self.assertRaises(ValueError):
            validate_date("2023-01-01", format="%m/%d/%Y")
    
    def test_validate_datetime(self):
        """Test datetime validation"""
        # Valid datetimes
        self.assertTrue(validate_datetime("2023-01-01 12:30"))
        self.assertTrue(validate_datetime("2023-12-31 23:59"))
        
        # Invalid datetimes
        with self.assertRaises(ValueError):
            validate_datetime("2023-13-01 12:30")
        
        with self.assertRaises(ValueError):
            validate_datetime("2023-01-01 25:00")
        
        with self.assertRaises(ValueError):
            validate_datetime("not-a-datetime")
        
        # Different format
        self.assertTrue(validate_datetime("01/15/2023 12:30 PM", format="%m/%d/%Y %I:%M %p"))
        
        with self.assertRaises(ValueError):
            validate_datetime("2023-01-01 12:30", format="%m/%d/%Y %I:%M %p")
    
    def test_validate_patient_id(self):
        """Test patient ID validation"""
        # Valid patient IDs
        self.assertTrue(validate_patient_id("P12345678"))
        self.assertTrue(validate_patient_id("PABCDEFGH"))
        
        # Invalid patient IDs
        with self.assertRaises(ValueError):
            validate_patient_id("12345678")
        
        with self.assertRaises(ValueError):
            validate_patient_id("P1234567")  # Too short
        
        with self.assertRaises(ValueError):
            validate_patient_id("P123456789")  # Too long
        
        with self.assertRaises(ValueError):
            validate_patient_id("D12345678")  # Wrong prefix
    
    def test_validate_doctor_id(self):
        """Test doctor ID validation"""
        # Valid doctor IDs
        self.assertTrue(validate_doctor_id("D12345678"))
        self.assertTrue(validate_doctor_id("DABCDEFGH"))
        
        # Invalid doctor IDs
        with self.assertRaises(ValueError):
            validate_doctor_id("12345678")
        
        with self.assertRaises(ValueError):
            validate_doctor_id("D1234567")  # Too short
        
        with self.assertRaises(ValueError):
            validate_doctor_id("D123456789")  # Too long
        
        with self.assertRaises(ValueError):
            validate_doctor_id("P12345678")  # Wrong prefix
    
    def test_validate_required_fields(self):
        """Test required fields validation"""
        # Valid data
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone": "555-123-4567"
        }
        
        self.assertTrue(validate_required_fields(data, ["first_name", "last_name"]))
        self.assertTrue(validate_required_fields(data, ["first_name", "last_name", "email", "phone"]))
        
        # Invalid data
        with self.assertRaises(ValueError):
            validate_required_fields(data, ["first_name", "last_name", "address"])
        
        data["email"] = None
        with self.assertRaises(ValueError):
            validate_required_fields(data, ["first_name", "last_name", "email"])
    
    def test_validate_appointment_time(self):
        """Test appointment time validation"""
        # Valid appointment times
        self.assertTrue(validate_appointment_time("2023-01-01 09:00"))
        self.assertTrue(validate_appointment_time("2023-01-01 16:30"))
        
        # Invalid appointment times
        with self.assertRaises(ValueError):
            validate_appointment_time("2023-01-01 08:00")  # Before working hours
        
        with self.assertRaises(ValueError):
            validate_appointment_time("2023-01-01 17:00")  # After working hours
        
        # Custom working hours
        self.assertTrue(validate_appointment_time("2023-01-01 08:00", working_hours=(8, 18)))
        
        with self.assertRaises(ValueError):
            validate_appointment_time("2023-01-01 07:00", working_hours=(8, 18))

if __name__ == '__main__':
    unittest.main()

