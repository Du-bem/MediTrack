"""
Tests for repository pattern implementation
"""
import unittest
import os
import sys
from datetime import datetime, timedelta

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base, Patient, Doctor, PatientMedicalRecord, Appointment
from db.repository import (
    BaseRepository, PatientRepository, DoctorRepository, 
    AppointmentRepository, MedicalRecordRepository
)

class TestRepositories(unittest.TestCase):
    """Test cases for repositories"""
    
    def setUp(self):
        """Set up test database"""
        # Create in-memory SQLite database for testing
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
        # Create test data
        self.create_test_data()
    
    def tearDown(self):
        """Clean up after tests"""
        self.session.close()
    
    def create_test_data(self):
        """Create test data for repositories"""
        # Create patients
        self.patient1 = Patient(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="555-123-4567",
            dob=datetime(1985, 5, 15).date(),
            address="123 Main St",
            patient_id="P12345678",
            insurance_info="BlueCross #BC987654321"
        )
        
        self.patient2 = Patient(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            phone="555-987-6543",
            dob=datetime(1990, 8, 22).date(),
            address="456 Oak Ave",
            patient_id="P87654321",
            insurance_info="Aetna #AE123456789"
        )
        
        # Create doctors
        self.doctor1 = Doctor(
            first_name="Sarah",
            last_name="Williams",
            email="sarah.williams@example.com",
            phone="555-234-5678",
            dob=datetime(1975, 11, 8).date(),
            address="101 Medical Center Blvd",
            staff_id="D12345678",
            role="Doctor",
            department="Cardiology",
            hire_date=datetime(2010, 6, 15).date(),
            qualification="MD, Cardiology",
            specialisation="Cardiology",
            license_number="MD12345",
            certifications="Board Certified in Cardiology"
        )
        
        self.doctor2 = Doctor(
            first_name="Michael",
            last_name="Brown",
            email="michael.brown@example.com",
            phone="555-876-5432",
            dob=datetime(1980, 4, 20).date(),
            address="202 Hospital Dr",
            staff_id="D87654321",
            role="Doctor",
            department="Pediatrics",
            hire_date=datetime(2012, 9, 1).date(),
            qualification="MD, Pediatrics",
            specialisation="Pediatrics",
            license_number="MD54321",
            certifications="Board Certified in Pediatrics"
        )
        
        # Add to session and commit to get IDs
        self.session.add_all([self.patient1, self.patient2, self.doctor1, self.doctor2])
        self.session.commit()
        
        # Create medical records
        self.record1 = PatientMedicalRecord(
            patient_id=self.patient1.id,
            diagnosis="Hypertension",
            treatment_plan="Lifestyle changes, medication",
            notes="Patient advised to reduce sodium intake and exercise regularly",
            date_created=datetime(2022, 3, 15)
        )
        
        self.record2 = PatientMedicalRecord(
            patient_id=self.patient2.id,
            diagnosis="Influenza",
            treatment_plan="Bed rest and fluids",
            notes="Patient prescribed antiviral medication",
            date_created=datetime(2022, 5, 20)
        )
        
        # Create appointments
        self.appointment1 = Appointment(
            patient_id=self.patient1.id,
            doctor_id=self.doctor1.id,
            schedule_time=datetime.now() + timedelta(days=1),
            duration=30,
            status="scheduled",
            notes="Follow-up appointment"
        )
        
        self.appointment2 = Appointment(
            patient_id=self.patient2.id,
            doctor_id=self.doctor2.id,
            schedule_time=datetime.now() + timedelta(days=2),
            duration=45,
            status="scheduled",
            notes="Initial consultation"
        )
        
        # Add to session and commit
        self.session.add_all([self.record1, self.record2, self.appointment1, self.appointment2])
        self.session.commit()
    
    def test_patient_repository(self):
        """Test PatientRepository"""
        repo = PatientRepository(self.session)
        
        # Test get_by_id
        patient = repo.get_by_id(self.patient1.id)
        self.assertIsNotNone(patient)
        self.assertEqual(patient.first_name, "John")
        self.assertEqual(patient.last_name, "Doe")
        
        # Test get_all
        patients = repo.get_all()
        self.assertEqual(len(patients), 2)
        
        # Test search
        search_results = repo.search("Doe")
        self.assertEqual(len(search_results), 1)
        self.assertEqual(search_results[0].last_name, "Doe")
        
        # Test get_by_patient_id
        patient = repo.get_by_patient_id("P12345678")
        self.assertIsNotNone(patient)
        self.assertEqual(patient.first_name, "John")
        
        # Test create
        new_patient = Patient(
            first_name="Robert",
            last_name="Johnson",
            email="robert.johnson@example.com",
            phone="555-456-7890",
            dob=datetime(1978, 3, 10).date(),
            address="789 Pine St",
            patient_id="P23456789",
            insurance_info="UnitedHealth #UH567891234"
        )
        created_patient = repo.create(new_patient)
        self.assertIsNotNone(created_patient.id)
        
        # Test update
        patient = repo.get_by_id(self.patient1.id)
        patient.phone = "555-999-8888"
        updated_patient = repo.update(patient)
        self.assertEqual(updated_patient.phone, "555-999-8888")
        
        # Test delete
        patient_to_delete = repo.get_by_id(created_patient.id)
        result = repo.delete(patient_to_delete)
        self.assertTrue(result)
        deleted_patient = repo.get_by_id(created_patient.id)
        self.assertIsNone(deleted_patient)
    
    def test_doctor_repository(self):
        """Test DoctorRepository"""
        repo = DoctorRepository(self.session)
        
        # Test get_by_id
        doctor = repo.get_by_id(self.doctor1.id)
        self.assertIsNotNone(doctor)
        self.assertEqual(doctor.first_name, "Sarah")
        self.assertEqual(doctor.last_name, "Williams")
        
        # Test get_all
        doctors = repo.get_all()
        self.assertEqual(len(doctors), 2)
        
        # Test search
        search_results = repo.search("Cardiology")
        self.assertEqual(len(search_results), 1)
        self.assertEqual(search_results[0].specialisation, "Cardiology")
        
        # Test get_by_specialisation
        doctors = repo.get_by_specialisation("Pediatrics")
        self.assertEqual(len(doctors), 1)
        self.assertEqual(doctors[0].first_name, "Michael")
        
        # Test get_by_department
        doctors = repo.get_by_department("Cardiology")
        self.assertEqual(len(doctors), 1)
        self.assertEqual(doctors[0].first_name, "Sarah")
    
    def test_appointment_repository(self):
        """Test AppointmentRepository"""
        repo = AppointmentRepository(self.session)
        
        # Test get_by_id
        appointment = repo.get_by_id(self.appointment1.appointment_id)
        self.assertIsNotNone(appointment)
        self.assertEqual(appointment.patient_id, self.patient1.id)
        self.assertEqual(appointment.doctor_id, self.doctor1.id)
        
        # Test get_all
        appointments = repo.get_all()
        self.assertEqual(len(appointments), 2)
        
        # Test get_by_doctor
        doctor_appointments = repo.get_by_doctor(self.doctor1.id)
        self.assertEqual(len(doctor_appointments), 1)
        self.assertEqual(doctor_appointments[0].patient_id, self.patient1.id)
        
        # Test get_by_patient
        patient_appointments = repo.get_by_patient(self.patient2.id)
        self.assertEqual(len(patient_appointments), 1)
        self.assertEqual(patient_appointments[0].doctor_id, self.doctor2.id)
    
    def test_medical_record_repository(self):
        """Test MedicalRecordRepository"""
        repo = MedicalRecordRepository(self.session)
        
        # Test get_by_id
        record = repo.get_by_id(self.record1.record_id)
        self.assertIsNotNone(record)
        self.assertEqual(record.diagnosis, "Hypertension")
        
        # Test get_all
        records = repo.get_all()
        self.assertEqual(len(records), 2)
        
        # Test get_by_patient
        patient_records = repo.get_by_patient(self.patient1.id)
        self.assertEqual(len(patient_records), 1)
        self.assertEqual(patient_records[0].diagnosis, "Hypertension")
        
        # Test search_by_diagnosis
        diagnosis_records = repo.search_by_diagnosis("Influenza")
        self.assertEqual(len(diagnosis_records), 1)
        self.assertEqual(diagnosis_records[0].patient_id, self.patient2.id)

if __name__ == '__main__':
    unittest.main()

