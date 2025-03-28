"""
Database models for MediTrack using SQLAlchemy ORM
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, Text, ForeignKey, Float
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Person(Base):
    """Base class for all persons in the system"""
    __tablename__ = 'persons'
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True)
    phone = Column(String(20))
    dob = Column(Date, nullable=False)
    address = Column(String(255))
    
    # Discriminator column for inheritance
    type = Column(String(50))
    
    __mapper_args__ = {
        'polymorphic_identity': 'person',
        'polymorphic_on': type
    }

class Patient(Person):
    """Patient model extending Person"""
    __tablename__ = 'patients'
    
    id = Column(Integer, ForeignKey('persons.id'), primary_key=True)
    patient_id = Column(String(20), unique=True, nullable=False)
    insurance_info = Column(String(255))
    reg_date = Column(Date, default=datetime.now().date)
    
    # Relationships
    medical_records = relationship("PatientMedicalRecord", back_populates="patient")
    appointments = relationship("Appointment", back_populates="patient")
    
    __mapper_args__ = {
        'polymorphic_identity': 'patient',
    }

class Staff(Person):
    """Staff model extending Person"""
    __tablename__ = 'staff'
    
    id = Column(Integer, ForeignKey('persons.id'), primary_key=True)
    staff_id = Column(String(20), unique=True, nullable=False)
    role = Column(String(50), nullable=False)
    department = Column(String(50))
    hire_date = Column(Date, default=datetime.now().date)
    qualification = Column(String(255))
    
    __mapper_args__ = {
        'polymorphic_identity': 'staff',
    }

class Doctor(Staff):
    """Doctor model extending Staff"""
    __tablename__ = 'doctors'
    
    id = Column(Integer, ForeignKey('staff.id'), primary_key=True)
    specialisation = Column(String(100), nullable=False)
    license_number = Column(String(50), unique=True, nullable=False)
    certifications = Column(Text)  # Stored as JSON string
    
    # Relationships
    appointments = relationship("Appointment", back_populates="doctor")
    
    __mapper_args__ = {
        'polymorphic_identity': 'doctor',
    }

class PatientMedicalRecord(Base):
    """Medical record for a patient"""
    __tablename__ = 'patient_medical_records'
    
    record_id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    date_created = Column(DateTime, default=datetime.now)
    diagnosis = Column(Text, nullable=False)
    treatment_plan = Column(Text, nullable=False)
    notes = Column(Text)
    
    # Relationships
    patient = relationship("Patient", back_populates="medical_records")
    prescriptions = relationship("Prescription", back_populates="medical_record")
    lab_tests = relationship("LabTest", back_populates="medical_record")

class Prescription(Base):
    """Prescription model"""
    __tablename__ = 'prescriptions'
    
    prescription_id = Column(Integer, primary_key=True)
    record_id = Column(Integer, ForeignKey('patient_medical_records.record_id'), nullable=False)
    medication = Column(String(100), nullable=False)
    dosage = Column(String(50), nullable=False)
    frequency = Column(String(50), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    instructions = Column(Text)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    medical_record = relationship("PatientMedicalRecord", back_populates="prescriptions")

class LabTest(Base):
    """Lab test model"""
    __tablename__ = 'lab_tests'
    
    test_id = Column(Integer, primary_key=True)
    record_id = Column(Integer, ForeignKey('patient_medical_records.record_id'), nullable=False)
    test_name = Column(String(100), nullable=False)
    test_type = Column(String(50), nullable=False)
    ordered_date = Column(Date, nullable=False)
    result_date = Column(Date)
    result = Column(Text)
    reference_range = Column(String(100))
    is_abnormal = Column(Boolean, default=False)
    
    # Relationships
    medical_record = relationship("PatientMedicalRecord", back_populates="lab_tests")

class Appointment(Base):
    """Appointment model"""
    __tablename__ = 'appointments'
    
    appointment_id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    doctor_id = Column(Integer, ForeignKey('doctors.id'), nullable=False)
    schedule_time = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=False)  # Duration in minutes
    status = Column(String(20), default='scheduled')  # scheduled, completed, cancelled
    notes = Column(Text)
    
    # Relationships
    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")

