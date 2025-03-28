"""
Database initialization script for MediTrack
"""
import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base, Person, Patient, Staff, Doctor, PatientMedicalRecord, Prescription, LabTest, Appointment
import json
from datetime import datetime, timedelta
import random

logger = logging.getLogger(__name__)

def init_db(db_url, echo=False):
    """
    Initialize the database
    
    Args:
        db_url: Database URL
        echo: Whether to echo SQL statements
    
    Returns:
        SQLAlchemy engine and session
    """
    # Create engine and session
    engine = create_engine(db_url, echo=echo)
    Session = sessionmaker(bind=engine)
    
    # Create tables
    Base.metadata.create_all(engine)
    
    logger.info(f"Database initialized at {db_url}")
    
    return engine, Session

def load_sample_data(session):
    """
    Load sample data into the database
    
    Args:
        session: SQLAlchemy session
    """
    try:
        # Check if data already exists
        if session.query(Patient).count() > 0:
            logger.info("Sample data already exists in the database")
            return
        
        # Create sample patients
        patients = [
            Patient(
                first_name="John",
                last_name="Doe",
                email="john.doe@example.com",
                phone="(555) 123-4567",
                dob=datetime(1985, 5, 15).date(),
                address="123 Main St, Anytown, USA",
                patient_id="P12345678",
                insurance_info="BlueCross #BC987654321"
            ),
            Patient(
                first_name="Jane",
                last_name="Smith",
                email="jane.smith@example.com",
                phone="(555) 987-6543",
                dob=datetime(1990, 8, 22).date(),
                address="456 Oak Ave, Somewhere, USA",
                patient_id="P87654321",
                insurance_info="Aetna #AE123456789"
            ),
            Patient(
                first_name="Robert",
                last_name="Johnson",
                email="robert.johnson@example.com",
                phone="(555) 456-7890",
                dob=datetime(1978, 3, 10).date(),
                address="789 Pine St, Nowhere, USA",
                patient_id="P23456789",
                insurance_info="UnitedHealth #UH567891234"
            )
        ]
        
        # Add patients to session
        for patient in patients:
            session.add(patient)
        
        # Create sample doctors
        doctors = [
            Doctor(
                first_name="Sarah",
                last_name="Williams",
                email="sarah.williams@example.com",
                phone="(555) 234-5678",
                dob=datetime(1975, 11, 8).date(),
                address="101 Medical Center Blvd, Anytown, USA",
                staff_id="D12345678",
                role="Doctor",
                department="Cardiology",
                hire_date=datetime(2010, 6, 15).date(),
                qualification="MD, Cardiology",
                specialisation="Cardiology",
                license_number="MD12345",
                certifications="Board Certified in Cardiology"
            ),
            Doctor(
                first_name="Michael",
                last_name="Brown",
                email="michael.brown@example.com",
                phone="(555) 876-5432",
                dob=datetime(1980, 4, 20).date(),
                address="202 Hospital Dr, Somewhere, USA",
                staff_id="D87654321",
                role="Doctor",
                department="Pediatrics",
                hire_date=datetime(2012, 9, 1).date(),
                qualification="MD, Pediatrics",
                specialisation="Pediatrics",
                license_number="MD54321",
                certifications="Board Certified in Pediatrics"
            )
        ]
        
        # Add doctors to session
        for doctor in doctors:
            session.add(doctor)
        
        # Commit to get IDs
        session.commit()
        
        # Create sample medical records
        medical_records = [
            PatientMedicalRecord(
                patient_id=patients[0].id,
                diagnosis="Hypertension",
                treatment_plan="Lifestyle changes, medication",
                notes="Patient advised to reduce sodium intake and exercise regularly",
                date_created=datetime(2022, 3, 15)
            ),
            PatientMedicalRecord(
                patient_id=patients[1].id,
                diagnosis="Influenza",
                treatment_plan="Bed rest and fluids",
                notes="Patient prescribed antiviral medication",
                date_created=datetime(2022, 5, 20)
            ),
            PatientMedicalRecord(
                patient_id=patients[2].id,
                diagnosis="Type 2 Diabetes",
                treatment_plan="Diet control, exercise, medication",
                notes="Patient advised to monitor blood sugar levels regularly",
                date_created=datetime(2022, 4, 10)
            )
        ]
        
        # Add medical records to session
        for record in medical_records:
            session.add(record)
        
        # Commit to get IDs
        session.commit()
        
        # Create sample prescriptions
        prescriptions = [
            Prescription(
                record_id=medical_records[0].record_id,
                medication="Lisinopril",
                dosage="10mg",
                frequency="Once daily",
                start_date=datetime(2022, 3, 15).date(),
                end_date=datetime(2022, 9, 15).date(),
                instructions="Take with food",
                is_active=True
            ),
            Prescription(
                record_id=medical_records[1].record_id,
                medication="Oseltamivir",
                dosage="75mg",
                frequency="Twice daily",
                start_date=datetime(2022, 5, 20).date(),
                end_date=datetime(2022, 5, 30).date(),
                instructions="Take with food",
                is_active=False
            ),
            Prescription(
                record_id=medical_records[2].record_id,
                medication="Metformin",
                dosage="500mg",
                frequency="Twice daily",
                start_date=datetime(2022, 4, 10).date(),
                end_date=datetime(2022, 10, 10).date(),
                instructions="Take with meals",
                is_active=True
            )
        ]
        
        # Add prescriptions to session
        for prescription in prescriptions:
            session.add(prescription)
        
        # Create sample lab tests
        lab_tests = [
            LabTest(
                record_id=medical_records[0].record_id,
                test_name="Blood Pressure",
                test_type="Vital Sign",
                ordered_date=datetime(2022, 3, 15).date(),
                result_date=datetime(2022, 3, 15).date(),
                result="140/90 mmHg",
                reference_range="120/80 mmHg",
                is_abnormal=True
            ),
            LabTest(
                record_id=medical_records[1].record_id,
                test_name="Influenza Test",
                test_type="Diagnostic",
                ordered_date=datetime(2022, 5, 20).date(),
                result_date=datetime(2022, 5, 20).date(),
                result="Positive",
                reference_range="Negative",
                is_abnormal=True
            ),
            LabTest(
                record_id=medical_records[2].record_id,
                test_name="HbA1c",
                test_type="Blood Test",
                ordered_date=datetime(2022, 4, 10).date(),
                result_date=datetime(2022, 4, 12).date(),
                result="7.2%",
                reference_range="<5.7%",
                is_abnormal=True
            )
        ]
        
        # Add lab tests to session
        for lab_test in lab_tests:
            session.add(lab_test)
        
        # Create sample appointments
        now = datetime.now()
        appointments = [
            Appointment(
                patient_id=patients[0].id,
                doctor_id=doctors[0].id,
                schedule_time=now + timedelta(days=1, hours=10),
                duration=30,
                status="scheduled",
                notes="Follow-up appointment"
            ),
            Appointment(
                patient_id=patients[1].id,
                doctor_id=doctors[1].id,
                schedule_time=now + timedelta(days=2, hours=14),
                duration=45,
                status="scheduled",
                notes="Initial consultation"
            ),
            Appointment(
                patient_id=patients[2].id,
                doctor_id=doctors[0].id,
                schedule_time=now - timedelta(days=5, hours=-9),
                duration=30,
                status="completed",
                notes="Regular check-up"
            )
        ]
        
        # Add appointments to session
        for appointment in appointments:
            session.add(appointment)
        
        # Commit all changes
        session.commit()
        
        logger.info("Sample data loaded successfully")
    
    except Exception as e:
        session.rollback()
        logger.error(f"Error loading sample data: {e}")
        raise

if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Get database URL from environment or use default
    db_url = os.getenv("DB_URL", "sqlite:///meditrack.db")
    
    # Initialize database
    engine, Session = init_db(db_url)
    
    # Create a session
    session = Session()
    
    try:
        # Load sample data
        load_sample_data(session)
    finally:
        # Close session
        session.close()

