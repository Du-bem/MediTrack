"""
Domain entities for MediTrack
These classes represent the core business entities and their behavior
"""
from datetime import datetime, date
import json

class Person:
    """Base class for all persons in the system"""
    
    def __init__(self, first_name, last_name, dob, email, phone, address=None, id=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob if isinstance(dob, date) else datetime.strptime(dob, "%Y-%m-%d").date()
        self.email = email
        self.phone = phone
        self.address = address
    
    def get_full_name(self):
        """Get the full name of the person"""
        return f"{self.first_name} {self.last_name}"
    
    def get_age(self):
        """Calculate the age of the person"""
        today = date.today()
        born = self.dob
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    
    def to_dict(self):
        """Convert the person to a dictionary"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.get_full_name(),
            "dob": self.dob.strftime("%Y-%m-%d"),
            "age": self.get_age(),
            "email": self.email,
            "phone": self.phone,
            "address": self.address
        }

class Patient(Person):
    """Patient entity extending Person"""
    
    def __init__(self, first_name, last_name, dob, email, phone, patient_id, 
                 insurance_info=None, reg_date=None, address=None, id=None):
        super().__init__(first_name, last_name, dob, email, phone, address, id)
        self.patient_id = patient_id
        self.insurance_info = insurance_info
        self.reg_date = reg_date if reg_date else date.today()
        self.medical_history = []
    
    def add_medical_record(self, medical_record):
        """Add a medical record to the patient's history"""
        self.medical_history.append(medical_record)
    
    def get_medical_history(self):
        """Get the patient's medical history"""
        return self.medical_history
    
    def update_insurance(self, new_insurance_info):
        """Update the patient's insurance information"""
        self.insurance_info = new_insurance_info
    
    def to_dict(self):
        """Convert the patient to a dictionary"""
        patient_dict = super().to_dict()
        patient_dict.update({
            "patient_id": self.patient_id,
            "insurance_info": self.insurance_info,
            "reg_date": self.reg_date.strftime("%Y-%m-%d")
        })
        return patient_dict

class Staff(Person):
    """Staff entity extending Person"""
    
    def __init__(self, first_name, last_name, dob, email, phone, staff_id, 
                 role, department, qualification=None, hire_date=None, address=None, id=None):
        super().__init__(first_name, last_name, dob, email, phone, address, id)
        self.staff_id = staff_id
        self.role = role
        self.department = department
        self.qualification = qualification
        self.hire_date = hire_date if hire_date else date.today()
    
    def to_dict(self):
        """Convert the staff to a dictionary"""
        staff_dict = super().to_dict()
        staff_dict.update({
            "staff_id": self.staff_id,
            "role": self.role,
            "department": self.department,
            "qualification": self.qualification,
            "hire_date": self.hire_date.strftime("%Y-%m-%d")
        })
        return staff_dict

class Doctor(Staff):
    """Doctor entity extending Staff"""
    
    def __init__(self, first_name, last_name, dob, email, phone, staff_id, 
                 role, department, specialisation, license_number, 
                 certifications=None, qualification=None, hire_date=None, address=None, id=None):
        super().__init__(first_name, last_name, dob, email, phone, staff_id, 
                         role, department, qualification, hire_date, address, id)
        self.specialisation = specialisation
        self.license_number = license_number
        self.certifications = certifications if certifications else []
    
    def get_patients_count(self):
        """Get the number of patients assigned to this doctor"""
        # This would typically query the database
        return len(self.get_appointments_today())
    
    def get_appointments_today(self):
        """Get the doctor's appointments for today"""
        # This would typically query the database
        return []
    
    def prescribe_medication(self, patient, medication, dosage, frequency, start_date, end_date, instructions=None):
        """Prescribe medication to a patient"""
        # This would typically create a prescription in the database
        pass
    
    def to_dict(self):
        """Convert the doctor to a dictionary"""
        doctor_dict = super().to_dict()
        doctor_dict.update({
            "specialisation": self.specialisation,
            "license_number": self.license_number,
            "certifications": self.certifications
        })
        return doctor_dict

class PatientMedicalRecord:
    """Medical record for a patient"""
    
    def __init__(self, patient, diagnosis, treatment_plan, notes=None, 
                 date_created=None, record_id=None):
        self.record_id = record_id
        self.patient = patient
        self.diagnosis = diagnosis
        self.treatment_plan = treatment_plan
        self.notes = notes
        self.date_created = date_created if date_created else datetime.now()
        self.prescriptions = []
        self.lab_tests = []
    
    def add_prescription(self, prescription):
        """Add a prescription to the medical record"""
        self.prescriptions.append(prescription)
    
    def add_lab_test(self, lab_test):
        """Add a lab test to the medical record"""
        self.lab_tests.append(lab_test)
    
    def update_diagnosis(self, new_diagnosis):
        """Update the diagnosis"""
        self.diagnosis = new_diagnosis
    
    def to_dict(self):
        """Convert the medical record to a dictionary"""
        return {
            "record_id": self.record_id,
            "patient_id": self.patient.id if hasattr(self.patient, 'id') else None,
            "patient_name": self.patient.get_full_name() if hasattr(self.patient, 'get_full_name') else None,
            "diagnosis": self.diagnosis,
            "treatment_plan": self.treatment_plan,
            "notes": self.notes,
            "date_created": self.date_created.strftime("%Y-%m-%d %H:%M:%S"),
            "prescriptions": [p.to_dict() for p in self.prescriptions],
            "lab_tests": [t.to_dict() for t in self.lab_tests]
        }

class Prescription:
    """Prescription entity"""
    
    def __init__(self, medical_record, medication, dosage, frequency, 
                 start_date, end_date, instructions=None, is_active=True, prescription_id=None):
        self.prescription_id = prescription_id
        self.medical_record = medical_record
        self.medication = medication
        self.dosage = dosage
        self.frequency = frequency
        self.start_date = start_date if isinstance(start_date, date) else datetime.strptime(start_date, "%Y-%m-%d").date()
        self.end_date = end_date if isinstance(end_date, date) else datetime.strptime(end_date, "%Y-%m-%d").date()
        self.instructions = instructions
        self.is_active = is_active
    
    def refill(self, new_end_date):
        """Refill the prescription with a new end date"""
        self.end_date = new_end_date if isinstance(new_end_date, date) else datetime.strptime(new_end_date, "%Y-%m-%d").date()
        self.is_active = True
    
    def discontinue(self):
        """Discontinue the prescription"""
        self.is_active = False
    
    def to_dict(self):
        """Convert the prescription to a dictionary"""
        return {
            "prescription_id": self.prescription_id,
            "record_id": self.medical_record.record_id if hasattr(self.medical_record, 'record_id') else None,
            "medication": self.medication,
            "dosage": self.dosage,
            "frequency": self.frequency,
            "start_date": self.start_date.strftime("%Y-%m-%d"),
            "end_date": self.end_date.strftime("%Y-%m-%d"),
            "instructions": self.instructions,
            "is_active": self.is_active
        }

class LabTest:
    """Lab test entity"""
    
    def __init__(self, medical_record, test_name, test_type, ordered_date, 
                 result_date=None, result=None, reference_range=None, 
                 is_abnormal=False, test_id=None):
        self.test_id = test_id
        self.medical_record = medical_record
        self.test_name = test_name
        self.test_type = test_type
        self.ordered_date = ordered_date if isinstance(ordered_date, date) else datetime.strptime(ordered_date, "%Y-%m-%d").date()
        self.result_date = result_date
        self.result = result
        self.reference_range = reference_range
        self.is_abnormal = is_abnormal
    
    def add_result(self, result_date, result, reference_range=None, is_abnormal=False):
        """Add result to the lab test"""
        self.result_date = result_date if isinstance(result_date, date) else datetime.strptime(result_date, "%Y-%m-%d").date()
        self.result = result
        self.reference_range = reference_range
        self.is_abnormal = is_abnormal
    
    def flag_abnormal(self, is_abnormal=True):
        """Flag the test result as abnormal"""
        self.is_abnormal = is_abnormal
    
    def to_dict(self):
        """Convert the lab test to a dictionary"""
        return {
            "test_id": self.test_id,
            "record_id": self.medical_record.record_id if hasattr(self.medical_record, 'record_id') else None,
            "test_name": self.test_name,
            "test_type": self.test_type,
            "ordered_date": self.ordered_date.strftime("%Y-%m-%d"),
            "result_date": self.result_date.strftime("%Y-%m-%d") if self.result_date else None,
            "result": self.result,
            "reference_range": self.reference_range,
            "is_abnormal": self.is_abnormal
        }

class Appointment:
    """Appointment entity"""
    
    def __init__(self, patient, doctor, schedule_time, duration, 
                 status="scheduled", notes=None, appointment_id=None):
        self.appointment_id = appointment_id
        self.patient = patient
        self.doctor = doctor
        self.schedule_time = schedule_time if isinstance(schedule_time, datetime) else datetime.strptime(schedule_time, "%Y-%m-%d %H:%M")
        self.duration = duration  # Duration in minutes
        self.status = status
        self.notes = notes
    
    def reschedule(self, new_schedule_time):
        """Reschedule the appointment"""
        self.schedule_time = new_schedule_time if isinstance(new_schedule_time, datetime) else datetime.strptime(new_schedule_time, "%Y-%m-%d %H:%M")
        self.status = "rescheduled"
    
    def cancel(self):
        """Cancel the appointment"""
        self.status = "cancelled"
    
    def complete(self):
        """Mark the appointment as completed"""
        self.status = "completed"
    
    def to_dict(self):
        """Convert the appointment to a dictionary"""
        return {
            "appointment_id": self.appointment_id,
            "patient_id": self.patient.id if hasattr(self.patient, 'id') else None,
            "patient_name": self.patient.get_full_name() if hasattr(self.patient, 'get_full_name') else None,
            "doctor_id": self.doctor.id if hasattr(self.doctor, 'id') else None,
            "doctor_name": self.doctor.get_full_name() if hasattr(self.doctor, 'get_full_name') else None,
            "schedule_time": self.schedule_time.strftime("%Y-%m-%d %H:%M"),
            "duration": self.duration,
            "status": self.status,
            "notes": self.notes
        }

