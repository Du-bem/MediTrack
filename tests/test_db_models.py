"""
Tests for database models
"""
import unittest
import os
import sys
from datetime import datetime, timedelta

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base, Person, Patient, Staff, Doctor, PatientMedicalRecord, Prescription, LabTest, Appointment

class TestDatabaseModels(unittest.TestCase):
    """Test cases for database models"""
    
    def setUp(self):
        """Set up test database"""
        # Create in-memory SQLite database for testing
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def tearDown(self):
        """Clean up after tests"""
        self.session.close()
    
    def test_patient_creation(self):
        """Test creating a patient"""
        # Create a patient
        patient = Patient(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="555-123-4567",
            dob=datetime(1985, 5, 15).date(),
            address="123 Main St",
            patient_id="P12345678",
            insurance_info="BlueCross #BC987654321"
        )
        
        # Add to session and commit
        self.session.add(patient)
        self.session.commit()
        
        # Query the patient
        queried_patient = self.session.query(Patient).filter_by(email="john.doe@example.com").first()
        
        # Assert patient was created correctly
        self.assertIsNotNone(queried_patient)
        self.assertEqual(queried_patient.first_name, "John")
        self.assertEqual(queried_patient.last_name, "Doe")
        self.assertEqual(queried_patient.patient_id, "P12345678")
    
    def test_doctor_creation(self):
        """Test creating a doctor"""
        # Create a doctor
        doctor = Doctor(
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
        
        # Add to session and commit
        self.session.add(doctor)
        self.session.commit()
        
        # Query the doctor
        queried_doctor = self.session.query(Doctor).filter_by(email="sarah.williams@example.com").first()
        
        # Assert doctor was created correctly
        self.assertIsNotNone(queried_doctor)
        self.assertEqual(queried_doctor.first_name, "Sarah")
        self.assertEqual(queried_doctor.last_name, "Williams")
        self.assertEqual(queried_doctor.specialisation, "Cardiology")
        self.assertEqual(queried_doctor.license_number, "MD12345")
    
    def test_medical_record_creation(self):
        """Test creating a medical record"""
        # Create a patient first
        patient = Patient(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="555-123-4567",
            dob=datetime(1985, 5, 15).date(),
            address="123 Main St",
            patient_id="P12345678",
            insurance_info="BlueCross #BC987654321"
        )
        self.session.add(patient)
        self.session.commit()
        
        # Create a medical record
        medical_record = PatientMedicalRecord(
            patient_id=patient.id,
            diagnosis="Hypertension",
            treatment_plan="Lifestyle changes, medication",
            notes="Patient advised to reduce sodium intake and exercise regularly",
            date_created=datetime(2022, 3, 15)
        )
        
        # Add to session and commit
        self.session.add(medical_record)
        self.session.commit()
        
        # Query the medical record
        queried_record = self.session.query(PatientMedicalRecord).filter_by(patient_id=patient.id).first()
        
        # Assert medical record was created correctly
        self.assertIsNotNone(queried_record)
        self.assertEqual(queried_record.diagnosis, "Hypertension")
        self.assertEqual(queried_record.treatment_plan, "Lifestyle changes, medication")
    
    def test_prescription_creation(self):
        """Test creating a prescription"""
        # Create a patient first
        patient = Patient(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="555-123-4567",
            dob=datetime(1985, 5, 15).date(),
            address="123 Main St",
            patient_id="P12345678",
            insurance_info="BlueCross #BC987654321"
        )
        self.session.add(patient)
        self.session.commit()
        
        # Create a medical record
        medical_record = PatientMedicalRecord(
            patient_id=patient.id,
            diagnosis="Hypertension",
            treatment_plan="Lifestyle changes, medication",
            notes="Patient advised to reduce sodium intake and exercise regularly",
            date_created=datetime(2022, 3, 15)
        )
        self.session.add(medical_record)
        self.session.commit()
        
        # Create a prescription
        prescription = Prescription(
            record_id=medical_record.record_id,
            medication="Lisinopril",
            dosage="10mg",
            frequency="Once daily",
            start_date=datetime(2022, 3, 15).date(),
            end_date=datetime(2022, 9, 15).date(),
            instructions="Take with food",
            is_active=True
        )
        
        # Add to session and commit
        self.session.add(prescription)
        self.session.commit()
        
        # Query the prescription
        queried_prescription = self.session.query(Prescription).filter_by(record_id=medical_record.record_id).first()
        
        # Assert prescription was created correctly
        self.assertIsNotNone(queried_prescription)
        self.assertEqual(queried_prescription.medication, "Lisinopril")
        self.assertEqual(queried_prescription.dosage, "10mg")
        self.assertEqual(queried_prescription.frequency, "Once daily")
        self.assertTrue(queried_prescription.is_active)
    
    def test_lab_test_creation(self):
        """Test creating a lab test"""
        # Create a patient first
        patient = Patient(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="555-123-4567",
            dob=datetime(1985, 5, 15).date(),
            address="123 Main St",
            patient_id="P12345678",
            insurance_info="BlueCross #BC987654321"
        )
        self.session.add(patient)
        self.session.commit()
        
        # Create a medical record
        medical_record = PatientMedicalRecord(
            patient_id=patient.id,
            diagnosis="Hypertension",
            treatment_plan="Lifestyle changes, medication",
            notes="Patient advised to reduce sodium intake and exercise regularly",
            date_created=datetime(2022, 3, 15)
        )
        self.session.add(medical_record)
        self.session.commit()
        
        # Create a lab test
        lab_test = LabTest(
            record_id=medical_record.record_id,
            test_name="Blood Pressure",
            test_type="Vital Sign",
            ordered_date=datetime(2022, 3, 15).date(),
            result_date=datetime(2022, 3, 15).date(),
            result="140/90 mmHg",
            reference_range="120/80 mmHg",
            is_abnormal=True
        )
        
        # Add to session and commit
        self.session.add(lab_test)
        self.session.commit()
        
        # Query the lab test
        queried_lab_test = self.session.query(LabTest).filter_by(record_id=medical_record.record_id).first()
        
        # Assert lab test was created correctly
        self.assertIsNotNone(queried_lab_test)
        self.assertEqual(queried_lab_test.test_name, "Blood Pressure")
        self.assertEqual(queried_lab_test.test_type, "Vital Sign")
        self.assertEqual(queried_lab_test.result, "140/90 mmHg")
        self.assertTrue(queried_lab_test.is_abnormal)
    
    def test_appointment_creation(self):
        """Test creating an appointment"""
        # Create a patient first
        patient = Patient(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="555-123-4567",
            dob=datetime(1985, 5, 15).date(),
            address="123 Main St",
            patient_id="P12345678",
            insurance_info="BlueCross #BC987654321"
        )
        self.session.add(patient)
        
        # Create a doctor
        doctor = Doctor(
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
        self.session.add(doctor)
        self.session.commit()
        
        # Create an appointment
        appointment_time = datetime.now() + timedelta(days=1)
        appointment = Appointment(
            patient_id=patient.id,
            doctor_id=doctor.id,
            schedule_time=appointment_time,
            duration=30,
            status="scheduled",
            notes="Follow-up appointment"
        )
        
        # Add to session and commit
        self.session.add(appointment)
        self.session.commit()
        
        # Query the appointment
        queried_appointment = self.session.query(Appointment).filter_by(patient_id=patient.id).first()
        
        # Assert appointment was created correctly
        self.assertIsNotNone(queried_appointment)
        self.assertEqual(queried_appointment.doctor_id, doctor.id)
        self.assertEqual(queried_appointment.duration, 30)
        self.assertEqual(queried_appointment.status, "scheduled")
        self.assertEqual(queried_appointment.notes, "Follow-up appointment")

if __name__ == '__main__':
    unittest.main()

