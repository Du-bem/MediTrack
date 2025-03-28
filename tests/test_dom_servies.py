"""
Tests for domain services
"""
import unittest
import os
import sys
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from domain.services import (
    PatientService, DoctorService, AppointmentService, 
    MedicalRecordService, SearchService, FileExportService
)

class TestPatientService(unittest.TestCase):
    """Test cases for PatientService"""
    
    def setUp(self):
        """Set up test environment"""
        self.patient_repo = MagicMock()
        self.patient_service = PatientService(self.patient_repo)
    
    def test_create_patient(self):
        """Test creating a patient"""
        # Mock the repository create method
        self.patient_repo.create.return_value = MagicMock(
            id=1,
            first_name="John",
            last_name="Doe",
            dob=datetime(1985, 5, 15).date(),
            email="john.doe@example.com",
            phone="555-123-4567",
            address="123 Main St",
            patient_id="P12345678",
            insurance_info="BlueCross #BC987654321",
            reg_date=datetime.now().date()
        )
        
        # Call the service method
        patient = self.patient_service.create_patient(
            "John", "Doe", "1985-05-15", "john.doe@example.com", 
            "555-123-4567", "123 Main St", "BlueCross #BC987654321"
        )
        
        # Assert the repository method was called
        self.patient_repo.create.assert_called_once()
        
        # Assert the returned patient has the correct attributes
        self.assertEqual(patient.first_name, "John")
        self.assertEqual(patient.last_name, "Doe")
        self.assertEqual(patient.email, "john.doe@example.com")
        self.assertEqual(patient.patient_id, "P12345678")
    
    def test_get_patient(self):
        """Test getting a patient"""
        # Mock the repository get_by_id method
        self.patient_repo.get_by_id.return_value = MagicMock(
            id=1,
            first_name="John",
            last_name="Doe",
            dob=datetime(1985, 5, 15).date(),
            email="john.doe@example.com",
            phone="555-123-4567",
            address="123 Main St",
            patient_id="P12345678",
            insurance_info="BlueCross #BC987654321",
            reg_date=datetime.now().date()
        )
        
        # Call the service method
        patient = self.patient_service.get_patient(1)
        
        # Assert the repository method was called
        self.patient_repo.get_by_id.assert_called_once_with(1)
        
        # Assert the returned patient has the correct attributes
        self.assertEqual(patient.first_name, "John")
        self.assertEqual(patient.last_name, "Doe")
        self.assertEqual(patient.email, "john.doe@example.com")
        self.assertEqual(patient.patient_id, "P12345678")
    
    def test_search_patients(self):
        """Test searching for patients"""
        # Mock the repository search method
        self.patient_repo.search.return_value = [
            MagicMock(
                id=1,
                first_name="John",
                last_name="Doe",
                dob=datetime(1985, 5, 15).date(),
                email="john.doe@example.com",
                phone="555-123-4567",
                address="123 Main St",
                patient_id="P12345678",
                insurance_info="BlueCross #BC987654321",
                reg_date=datetime.now().date()
            )
        ]
        
        # Call the service method
        patients = self.patient_service.search_patients("Doe")
        
        # Assert the repository method was called
        self.patient_repo.search.assert_called_once_with("Doe")
        
        # Assert the returned list has the correct length
        self.assertEqual(len(patients), 1)
        
        # Assert the returned patient has the correct attributes
        self.assertEqual(patients[0].first_name, "John")
        self.assertEqual(patients[0].last_name, "Doe")
        self.assertEqual(patients[0].email, "john.doe@example.com")
        self.assertEqual(patients[0].patient_id, "P12345678")
    
    def test_update_patient(self):
        """Test updating a patient"""
        # Mock the repository get_by_id and update methods
        patient_model = MagicMock(
            id=1,
            first_name="John",
            last_name="Doe",
            dob=datetime(1985, 5, 15).date(),
            email="john.doe@example.com",
            phone="555-123-4567",
            address="123 Main St",
            patient_id="P12345678",
            insurance_info="BlueCross #BC987654321",
            reg_date=datetime.now().date()
        )
        self.patient_repo.get_by_id.return_value = patient_model
        self.patient_repo.update.return_value = patient_model
        
        # Call the service method
        patient = self.patient_service.update_patient(1, "phone", "555-999-8888")
        
        # Assert the repository methods were called
        self.patient_repo.get_by_id.assert_called_once_with(1)
        self.patient_repo.update.assert_called_once()
        
        # Assert the patient model was updated
        self.assertEqual(patient_model.phone, "555-999-8888")

class TestAppointmentService(unittest.TestCase):
    """Test cases for AppointmentService"""
    
    def setUp(self):
        """Set up test environment"""
        self.appointment_repo = MagicMock()
        self.patient_repo = MagicMock()
        self.doctor_repo = MagicMock()
        self.appointment_service = AppointmentService(
            self.appointment_repo, self.patient_repo, self.doctor_repo
        )
    
    def test_create_appointment(self):
        """Test creating an appointment"""
        # Mock the repository methods
        patient_model = MagicMock(id=1)
        doctor_model = MagicMock(id=2)
        self.patient_repo.get_by_id.return_value = patient_model
        self.doctor_repo.get_by_id.return_value = doctor_model
        
        # Mock the is_time_available method
        self.appointment_service.is_time_available = MagicMock(return_value=True)
        
        # Mock the appointment model
        appointment_model = MagicMock(
            appointment_id=1,
            patient_id=1,
            doctor_id=2,
            schedule_time=datetime.now() + timedelta(days=1),
            duration=30,
            status="scheduled",
            notes="Follow-up appointment"
        )
        self.appointment_repo.create.return_value = appointment_model
        
        # Call the service method
        appointment = self.appointment_service.create_appointment(
            1, 2, datetime.now() + timedelta(days=1), 30, "Follow-up appointment"
        )
        
        # Assert the repository methods were called
        self.patient_repo.get_by_id.assert_called_once_with(1)
        self.doctor_repo.get_by_id.assert_called_once_with(2)
        self.appointment_repo.create.assert_called_once()
        
        # Assert the returned appointment has the correct attributes
        self.assertEqual(appointment.patient, patient_model)
        self.assertEqual(appointment.doctor, doctor_model)
        self.assertEqual(appointment.duration, 30)
        self.assertEqual(appointment.status, "scheduled")
        self.assertEqual(appointment.notes, "Follow-up appointment")
    
    def test_is_time_available(self):
        """Test checking if a time slot is available"""
        # Mock the repository get_by_doctor method
        appointment1 = MagicMock(
            schedule_time=datetime(2023, 1, 1, 10, 0),
            duration=30,
            status="scheduled"
        )
        appointment2 = MagicMock(
            schedule_time=datetime(2023, 1, 1, 11, 0),
            duration=30,
            status="scheduled"
        )
        self.appointment_repo.get_by_doctor.return_value = [appointment1, appointment2]
        
        # Test with a non-conflicting time
        result = self.appointment_service.is_time_available(
            1, datetime(2023, 1, 1, 9, 0), 30
        )
        self.assertTrue(result)
        
        # Test with a conflicting time
        result = self.appointment_service.is_time_available(
            1, datetime(2023, 1, 1, 10, 15), 30
        )
        self.assertFalse(result)
    
    def test_find_available_slots(self):
        """Test finding available appointment slots"""
        # Mock the is_time_available method
        self.appointment_service.is_time_available = MagicMock(side_effect=[
            True, False, True, True, False, True, True, True
        ])
        
        # Mock the get_appointments_for_doctor method
        self.appointment_service.get_appointments_for_doctor = MagicMock(return_value=[])
        
        # Call the service method
        slots = self.appointment_service.find_available_slots(1, datetime(2023, 1, 1).date(), 30)
        
        # Assert the correct number of slots were returned
        self.assertEqual(len(slots), 5)

class TestSearchService(unittest.TestCase):
    """Test cases for SearchService"""
    
    def setUp(self):
        """Set up test environment"""
        self.patient_repo = MagicMock()
        self.doctor_repo = MagicMock()
        self.appointment_repo = MagicMock()
        self.medical_record_repo = MagicMock()
        self.search_service = SearchService(
            self.patient_repo, self.doctor_repo, 
            self.appointment_repo, self.medical_record_repo
        )
    
    def test_search_patients(self):
        """Test searching for patients"""
        # Mock the repository search method
        self.patient_repo.search.return_value = [
            MagicMock(
                id=1,
                first_name="John",
                last_name="Doe",
                dob=datetime(1985, 5, 15).date(),
                email="john.doe@example.com",
                phone="555-123-4567",
                address="123 Main St",
                patient_id="P12345678",
                insurance_info="BlueCross #BC987654321",
                reg_date=datetime.now().date()
            )
        ]
        
        # Call the service method
        patients = self.search_service.search_patients("Doe")
        
        # Assert the repository method was called
        self.patient_repo.search.assert_called_once_with("Doe")
        
        # Assert the returned list has the correct length
        self.assertEqual(len(patients), 1)
        
        # Assert the returned patient has the correct attributes
        self.assertEqual(patients[0].first_name, "John")
        self.assertEqual(patients[0].last_name, "Doe")
    
    def test_filter_results(self):
        """Test filtering search results"""
        # Create test data
        item1 = MagicMock(name="Item 1", category="A", price=10)
        item2 = MagicMock(name="Item 2", category="B", price=20)
        item3 = MagicMock(name="Item 3", category="A", price=30)
        
        results = [item1, item2, item3]
        
        # Test filtering by category
        filtered = self.search_service.filter_results(results, {"category": "A"})
        self.assertEqual(len(filtered), 2)
        self.assertEqual(filtered[0].name, "Item 1")
        self.assertEqual(filtered[1].name, "Item 3")
        
        # Test filtering by price
        filtered = self.search_service.filter_results(results, {"price": 20})
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].name, "Item 2")
        
        # Test filtering by multiple criteria
        filtered = self.search_service.filter_results(results, {"category": "A", "price": 10})
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].name, "Item 1")

if __name__ == '__main__':
    unittest.main()

