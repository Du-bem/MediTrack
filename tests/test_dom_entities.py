"""
Tests for domain entities
"""
import unittest
import os
import sys
from datetime import datetime, timedelta

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from domain.entities import (
    Person, Patient, Staff, Doctor, PatientMedicalRecord, 
    Prescription, LabTest, Appointment
)

class TestDomainEntities(unittest.TestCase):
    """Test cases for domain entities"""
    
    def test_person(self):
        """Test Person entity"""
        # Create a person
        person = Person(
            first_name="John",
            last_name="Doe",
            dob="1985-05-15",
            email="john.doe@example.com",
            phone="555-123-4567",
            address="123 Main St"
        )
        
        # Test attributes
        self.assertEqual(person.first_name, "John")
        self.assertEqual(person.last_name, "Doe")
        self.assertEqual(person.email, "john.doe@example.com")
        
        # Test methods
        self.assertEqual(person.get_full_name(), "John Doe")
        
        # Calculate expected age
        today = datetime.now().date()
        born = datetime.strptime("1985-05-15", "%Y-%m-%d").date()
        expected_age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        
        self.assertEqual(person.get_age(), expected_age)
        
        # Test to_dict
        person_dict = person.to_dict()
        self.assertEqual(person_dict["first_name"], "John")
        self.assertEqual(person_dict["last_name"], "Doe")
        self.assertEqual(person_dict["full_name"], "John Doe")
    
    def test_patient(self):
        """Test Patient entity"""
        # Create a patient
        patient = Patient(
            first_name="John",
            last_name="Doe",
            dob="1985-05-15",
            email="john.doe@example.com",
            phone="555-123-4567",
            address="123 Main St",
            patient_id="P12345678",
            insurance_info="BlueCross #BC987654321"
        )
        
        # Test attributes
        self.assertEqual(patient.first_name, "John")
        self.assertEqual(patient.last_name, "Doe")
        self.assertEqual(patient.patient_id, "P12345678")
        self.assertEqual(patient.insurance_info, "BlueCross #BC987654321")
        
        # Test methods
        self.assertEqual(patient.get_full_name(), "John Doe")
        self.assertEqual(len(patient.get_medical_history()), 0)
        
        # Test add_medical_record
        record = PatientMedicalRecord(
            patient=patient,
            diagnosis="Hypertension",
            treatment_plan="Lifestyle changes, medication"
        )
        patient.add_medical_record(record)
        self.assertEqual(len(patient.get_medical_history()), 1)
        
        # Test update_insurance
        patient.update_insurance("Aetna #AE123456789")
        self.assertEqual(patient.insurance_info, "Aetna #AE123456789")
        
        # Test to_dict
        patient_dict = patient.to_dict()
        self.assertEqual(patient_dict["patient_id"], "P12345678")
        self.assertEqual(patient_dict["insurance_info"], "Aetna #AE123456789")
    
    def test_doctor(self):
        """Test Doctor entity"""
        # Create a doctor
        doctor = Doctor(
            first_name="Sarah",
            last_name="Williams",
            dob="1975-11-08",
            email="sarah.williams@example.com",
            phone="555-234-5678",
            address="101 Medical Center Blvd",
            staff_id="D12345678",
            role="Doctor",
            department="Cardiology",
            specialisation="Cardiology",
            license_number="MD12345",
            certifications=["Board Certified in Cardiology"]
        )
        
        # Test attributes
        self.assertEqual(doctor.first_name, "Sarah")
        self.assertEqual(doctor.last_name, "Williams")
        self.assertEqual(doctor.specialisation, "Cardiology")
        self.assertEqual(doctor.license_number, "MD12345")
        
        # Test methods
        self.assertEqual(doctor.get_full_name(), "Sarah Williams")
        self.assertEqual(doctor.get_patients_count(), 0)
        
        # Test to_dict
        doctor_dict = doctor.to_dict()
        self.assertEqual(doctor_dict["specialisation"], "Cardiology")
        self.assertEqual(doctor_dict["license_number"], "MD12345")
    
    def test_patient_medical_record(self):
        """Test PatientMedicalRecord entity"""
        # Create a patient
        patient = Patient(
            first_name="John",
            last_name="Doe",
            dob="1985-05-15",
            email="john.doe@example.com",
            phone="555-123-4567",
            patient_id="P12345678"
        )
        
        # Create a medical record
        record = PatientMedicalRecord(
            patient=patient,
            diagnosis="Hypertension",
            treatment_plan="Lifestyle changes, medication",
            notes="Patient advised to reduce sodium intake and exercise regularly"
        )
        
        # Test attributes
        self.assertEqual(record.patient, patient)
        self.assertEqual(record.diagnosis, "Hypertension")
        self.assertEqual(record.treatment_plan, "Lifestyle changes, medication")
        
        # Test methods
        prescription = Prescription(
            medical_record=record,
            medication="Lisinopril",
            dosage="10mg",
            frequency="Once daily",
            start_date="2022-03-15",
            end_date="2022-09-15"
        )
        record.add_prescription(prescription)
        self.assertEqual(len(record.prescriptions), 1)
        
        lab_test = LabTest(
            medical_record=record,
            test_name="Blood Pressure",
            test_type="Vital Sign",
            ordered_date="2022-03-15"
        )
        record.add_lab_test(lab_test)
        self.assertEqual(len(record.lab_tests), 1)
        
        record.update_diagnosis("Hypertension Stage 1")
        self.assertEqual(record.diagnosis, "Hypertension Stage 1")
        
        # Test to_dict
        record_dict = record.to_dict()
        self.assertEqual(record_dict["diagnosis"], "Hypertension Stage 1")
        self.assertEqual(record_dict["treatment_plan"], "Lifestyle changes, medication")
        self.assertEqual(len(record_dict["prescriptions"]), 1)
        self.assertEqual(len(record_dict["lab_tests"]), 1)
    
    def test_prescription(self):
        """Test Prescription entity"""
        # Create a patient and medical record
        patient = Patient(
            first_name="John",
            last_name="Doe",
            dob="1985-05-15",
            email="john.doe@example.com",
            phone="555-123-4567",
            patient_id="P12345678"
        )
        
        record = PatientMedicalRecord(
            patient=patient,
            diagnosis="Hypertension",
            treatment_plan="Lifestyle changes, medication"
        )
        
        # Create a prescription
        prescription = Prescription(
            medical_record=record,
            medication="Lisinopril",
            dosage="10mg",
            frequency="Once daily",
            start_date="2022-03-15",
            end_date="2022-09-15",
            instructions="Take with food"
        )
        
        # Test attributes
        self.assertEqual(prescription.medication, "Lisinopril")
        self.assertEqual(prescription.dosage, "10mg")
        self.assertEqual(prescription.frequency, "Once daily")
        self.assertTrue(prescription.is_active)
        
        # Test methods
        prescription.discontinue()
        self.assertFalse(prescription.is_active)
        
        prescription.refill("2023-03-15")
        self.assertTrue(prescription.is_active)
        self.assertEqual(prescription.end_date, datetime.strptime("2023-03-15", "%Y-%m-%d").date())
        
        # Test to_dict
        prescription_dict = prescription.to_dict()
        self.assertEqual(prescription_dict["medication"], "Lisinopril")
        self.assertEqual(prescription_dict["dosage"], "10mg")
        self.assertEqual(prescription_dict["frequency"], "Once daily")
        self.assertTrue(prescription_dict["is_active"])
    
    def test_lab_test(self):
        """Test LabTest entity"""
        # Create a patient and medical record
        patient = Patient(
            first_name="John",
            last_name="Doe",
            dob="1985-05-15",
            email="john.doe@example.com",
            phone="555-123-4567",
            patient_id="P12345678"
        )
        
        record = PatientMedicalRecord(
            patient=patient,
            diagnosis="Hypertension",
            treatment_plan="Lifestyle changes, medication"
        )
        
        # Create a lab test
        lab_test = LabTest(
            medical_record=record,
            test_name="Blood Pressure",
            test_type="Vital Sign",
            ordered_date="2022-03-15"
        )
        
        # Test attributes
        self.assertEqual(lab_test.test_name, "Blood Pressure")
        self.assertEqual(lab_test.test_type, "Vital Sign")
        self.assertIsNone(lab_test.result)
        self.assertFalse(lab_test.is_abnormal)
        
        # Test methods
        lab_test.add_result("2022-03-15", "140/90 mmHg", "120/80 mmHg", True)
        self.assertEqual(lab_test.result, "140/90 mmHg")
        self.assertEqual(lab_test.reference_range, "120/80 mmHg")
        self.assertTrue(lab_test.is_abnormal)
        
        lab_test.flag_abnormal(False)
        self.assertFalse(lab_test.is_abnormal)
        
        # Test to_dict
        lab_test_dict = lab_test.to_dict()
        self.assertEqual(lab_test_dict["test_name"], "Blood Pressure")
        self.assertEqual(lab_test_dict["test_type"], "Vital Sign")
        self.assertEqual(lab_test_dict["result"], "140/90 mmHg")
        self.assertFalse(lab_test_dict["is_abnormal"])
    
    def test_appointment(self):
        """Test Appointment entity"""
        # Create a patient and doctor
        patient = Patient(
            first_name="John",
            last_name="Doe",
            dob="1985-05-15",
            email="john.doe@example.com",
            phone="555-123-4567",
            patient_id="P12345678"
        )
        
        doctor = Doctor(
            first_name="Sarah",
            last_name="Williams",
            dob="1975-11-08",
            email="sarah.williams@example.com",
            phone="555-234-5678",
            staff_id="D12345678",
            role="Doctor",
            department="Cardiology",
            specialisation="Cardiology",
            license_number="MD12345"
        )
        
        # Create an appointment
        appointment_time = datetime.now() + timedelta(days=1)
        appointment = Appointment(
            patient=patient,
            doctor=doctor,
            schedule_time=appointment_time.strftime("%Y-%m-%d %H:%M"),
            duration=30,
            status="scheduled",
            notes="Follow-up appointment"
        )
        
        # Test attributes
        self.assertEqual(appointment.patient, patient)
        self.assertEqual(appointment.doctor, doctor)
        self.assertEqual(appointment.duration, 30)
        self.assertEqual(appointment.status, "scheduled")
        
        # Test methods
        new_time = (appointment_time + timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
        appointment.reschedule(new_time)
        self.assertEqual(appointment.status, "rescheduled")
        
        appointment.cancel()
        self.assertEqual(appointment.status, "cancelled")
        
        appointment.complete()
        self.assertEqual(appointment.status, "completed")
        
        # Test to_dict
        appointment_dict = appointment.to_dict()
        self.assertEqual(appointment_dict["duration"], 30)
        self.assertEqual(appointment_dict["status"], "completed")
        self.assertEqual(appointment_dict["notes"], "Follow-up appointment")

if __name__ == '__main__':
    unittest.main()

