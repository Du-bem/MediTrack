"""
Domain services for MediTrack
These services implement the business logic of the application
"""
import logging
from datetime import datetime, date, timedelta
import uuid
import re

logger = logging.getLogger(__name__)

class PatientService:
    """Service for patient-related operations"""
    
    def __init__(self, patient_repository):
        self.patient_repository = patient_repository
    
    def create_patient(self, first_name, last_name, dob, email, phone, address=None, insurance_info=None):
        """Create a new patient"""
        from domain.entities import Patient
        from db.models import Patient as PatientModel
        
        # Generate a unique patient ID
        patient_id = f"P{uuid.uuid4().hex[:8].upper()}"
        
        # Create the patient model
        patient_model = PatientModel(
            first_name=first_name,
            last_name=last_name,
            dob=dob if isinstance(dob, date) else datetime.strptime(dob, "%Y-%m-%d").date(),
            email=email,
            phone=phone,
            address=address,
            patient_id=patient_id,
            insurance_info=insurance_info
        )
        
        # Save to database
        created_patient = self.patient_repository.create(patient_model)
        
        # Create and return domain entity
        return Patient(
            first_name=created_patient.first_name,
            last_name=created_patient.last_name,
            dob=created_patient.dob,
            email=created_patient.email,
            phone=created_patient.phone,
            address=created_patient.address,
            patient_id=created_patient.patient_id,
            insurance_info=created_patient.insurance_info,
            reg_date=created_patient.reg_date,
            id=created_patient.id
        )
    
    def get_patient(self, patient_id):
        """Get a patient by ID"""
        from domain.entities import Patient
        
        # Try to get by database ID first
        try:
            id_int = int(patient_id)
            patient_model = self.patient_repository.get_by_id(id_int)
        except ValueError:
            # If not an integer, try to get by patient_id field
            patient_model = self.patient_repository.get_by_patient_id(patient_id)
        
        if not patient_model:
            return None
        
        # Convert to domain entity
        return Patient(
            first_name=patient_model.first_name,
            last_name=patient_model.last_name,
            dob=patient_model.dob,
            email=patient_model.email,
            phone=patient_model.phone,
            address=patient_model.address,
            patient_id=patient_model.patient_id,
            insurance_info=patient_model.insurance_info,
            reg_date=patient_model.reg_date,
            id=patient_model.id
        )
    
    def search_patients(self, search_term):
        """Search for patients"""
        from domain.entities import Patient
        
        patient_models = self.patient_repository.search(search_term)
        
        # Convert to domain entities
        return [
            Patient(
                first_name=p.first_name,
                last_name=p.last_name,
                dob=p.dob,
                email=p.email,
                phone=p.phone,
                address=p.address,
                patient_id=p.patient_id,
                insurance_info=p.insurance_info,
                reg_date=p.reg_date,
                id=p.id
            ) for p in patient_models
        ]
    
    def update_patient(self, patient_id, field, value):
        """Update a patient field"""
        # Get the patient
        patient_model = None
        
        # Try to get by database ID first
        try:
            id_int = int(patient_id)
            patient_model = self.patient_repository.get_by_id(id_int)
        except ValueError:
            # If not an integer, try to get by patient_id field
            patient_model = self.patient_repository.get_by_patient_id(patient_id)
        
        if not patient_model:
            return None
        
        # Update the field
        if hasattr(patient_model, field):
            # Handle date fields
            if field == 'dob' and not isinstance(value, date):
                value = datetime.strptime(value, "%Y-%m-%d").date()
            
            setattr(patient_model, field, value)
            updated_patient = self.patient_repository.update(patient_model)
            
            # Convert to domain entity
            from domain.entities import Patient
            return Patient(
                first_name=updated_patient.first_name,
                last_name=updated_patient.last_name,
                dob=updated_patient.dob,
                email=updated_patient.email,
                phone=updated_patient.phone,
                address=updated_patient.address,
                patient_id=updated_patient.patient_id,
                insurance_info=updated_patient.insurance_info,
                reg_date=updated_patient.reg_date,
                id=updated_patient.id
            )
        else:
            raise ValueError(f"Invalid field: {field}")

class DoctorService:
    """Service for doctor-related operations"""
    
    def __init__(self, doctor_repository):
        self.doctor_repository = doctor_repository
    
    def create_doctor(self, first_name, last_name, dob, email, phone, specialisation, 
                      license_number, department="General", certifications=None, 
                      address=None, qualification=None):
        """Create a new doctor"""
        from domain.entities import Doctor
        from db.models import Doctor as DoctorModel
        
        # Generate a unique staff ID
        staff_id = f"D{uuid.uuid4().hex[:8].upper()}"
        
        # Create the doctor model
        doctor_model = DoctorModel(
            first_name=first_name,
            last_name=last_name,
            dob=dob if isinstance(dob, date) else datetime.strptime(dob, "%Y-%m-%d").date(),
            email=email,
            phone=phone,
            address=address,
            staff_id=staff_id,
            role="Doctor",
            department=department,
            qualification=qualification,
            specialisation=specialisation,
            license_number=license_number,
            certifications=certifications
        )
        
        # Save to database
        created_doctor = self.doctor_repository.create(doctor_model)
        
        # Create and return domain entity
        return Doctor(
            first_name=created_doctor.first_name,
            last_name=created_doctor.last_name,
            dob=created_doctor.dob,
            email=created_doctor.email,
            phone=created_doctor.phone,
            address=created_doctor.address,
            staff_id=created_doctor.staff_id,
            role=created_doctor.role,
            department=created_doctor.department,
            qualification=created_doctor.qualification,
            specialisation=created_doctor.specialisation,
            license_number=created_doctor.license_number,
            certifications=created_doctor.certifications,
            hire_date=created_doctor.hire_date,
            id=created_doctor.id
        )
    
    def get_doctor(self, doctor_id):
        """Get a doctor by ID"""
        from domain.entities import Doctor
        
        # Try to get by database ID
        doctor_model = self.doctor_repository.get_by_id(doctor_id)
        
        if not doctor_model:
            return None
        
        # Convert to domain entity
        return Doctor(
            first_name=doctor_model.first_name,
            last_name=doctor_model.last_name,
            dob=doctor_model.dob,
            email=doctor_model.email,
            phone=doctor_model.phone,
            address=doctor_model.address,
            staff_id=doctor_model.staff_id,
            role=doctor_model.role,
            department=doctor_model.department,
            qualification=doctor_model.qualification,
            specialisation=doctor_model.specialisation,
            license_number=doctor_model.license_number,
            certifications=doctor_model.certifications,
            hire_date=doctor_model.hire_date,
            id=doctor_model.id
        )
    
    def search_doctors(self, search_term):
        """Search for doctors"""
        from domain.entities import Doctor
        
        doctor_models = self.doctor_repository.search(search_term)
        
        # Convert to domain entities
        return [
            Doctor(
                first_name=d.first_name,
                last_name=d.last_name,
                dob=d.dob,
                email=d.email,
                phone=d.phone,
                address=d.address,
                staff_id=d.staff_id,
                role=d.role,
                department=d.department,
                qualification=d.qualification,
                specialisation=d.specialisation,
                license_number=d.license_number,
                certifications=d.certifications,
                hire_date=d.hire_date,
                id=d.id
            ) for d in doctor_models
        ]
    
    def get_doctors_by_specialisation(self, specialisation):
        """Get doctors by specialisation"""
        from domain.entities import Doctor
        
        doctor_models = self.doctor_repository.get_by_specialisation(specialisation)
        
        # Convert to domain entities
        return [
            Doctor(
                first_name=d.first_name,
                last_name=d.last_name,
                dob=d.dob,
                email=d.email,
                phone=d.phone,
                address=d.address,
                staff_id=d.staff_id,
                role=d.role,
                department=d.department,
                qualification=d.qualification,
                specialisation=d.specialisation,
                license_number=d.license_number,
                certifications=d.certifications,
                hire_date=d.hire_date,
                id=d.id
            ) for d in doctor_models
        ]

class AppointmentService:
    """Service for appointment-related operations"""
    
    def __init__(self, appointment_repository, patient_repository, doctor_repository):
        self.appointment_repository = appointment_repository
        self.patient_repository = patient_repository
        self.doctor_repository = doctor_repository
    
    def create_appointment(self, patient_id, doctor_id, schedule_time, duration, notes=None):
        """Create a new appointment"""
        from domain.entities import Appointment
        from db.models import Appointment as AppointmentModel
        
        # Get patient and doctor
        patient_model = self.patient_repository.get_by_id(patient_id)
        doctor_model = self.doctor_repository.get_by_id(doctor_id)
        
        if not patient_model or not doctor_model:
            raise ValueError("Patient or doctor not found")
        
        # Check for scheduling conflicts
        if not self.is_time_available(doctor_id, schedule_time, duration):
            raise ValueError("The selected time conflicts with an existing appointment")
        
        # Create the appointment model
        appointment_model = AppointmentModel(
            patient_id=patient_id,
            doctor_id=doctor_id,
            schedule_time=schedule_time if isinstance(schedule_time, datetime) else datetime.strptime(schedule_time, "%Y-%m-%d %H:%M"),
            duration=duration,
            notes=notes
        )
        
        # Save to database
        created_appointment = self.appointment_repository.create(appointment_model)
        
        # Create and return domain entity
        return Appointment(
            patient=patient_model,
            doctor=doctor_model,
            schedule_time=created_appointment.schedule_time,
            duration=created_appointment.duration,
            status=created_appointment.status,
            notes=created_appointment.notes,
            appointment_id=created_appointment.appointment_id
        )
    
    def get_appointment(self, appointment_id):
        """Get an appointment by ID"""
        from domain.entities import Appointment
        
        # Get the appointment
        appointment_model = self.appointment_repository.get_by_id(appointment_id)
        
        if not appointment_model:
            return None
        
        # Get patient and doctor
        patient_model = self.patient_repository.get_by_id(appointment_model.patient_id)
        doctor_model = self.doctor_repository.get_by_id(appointment_model.doctor_id)
        
        # Convert to domain entity
        return Appointment(
            patient=patient_model,
            doctor=doctor_model,
            schedule_time=appointment_model.schedule_time,
            duration=appointment_model.duration,
            status=appointment_model.status,
            notes=appointment_model.notes,
            appointment_id=appointment_model.appointment_id
        )
    
    def get_appointments_for_doctor(self, doctor_id, date=None):
        """Get appointments for a doctor"""
        from domain.entities import Appointment
        
        # Get the appointments
        appointment_models = self.appointment_repository.get_by_doctor(doctor_id, date)
        
        # Convert to domain entities
        appointments = []
        for a in appointment_models:
            patient_model = self.patient_repository.get_by_id(a.patient_id)
            doctor_model = self.doctor_repository.get_by_id(a.doctor_id)
            
            appointments.append(Appointment(
                patient=patient_model,
                doctor=doctor_model,
                schedule_time=a.schedule_time,
                duration=a.duration,
                status=a.status,
                notes=a.notes,
                appointment_id=a.appointment_id
            ))
        
        return appointments
    
    def get_appointments_for_patient(self, patient_id, date=None):
        """Get appointments for a patient"""
        from domain.entities import Appointment
        
        # Get the appointments
        appointment_models = self.appointment_repository.get_by_patient(patient_id, date)
        
        # Convert to domain entities
        appointments = []
        for a in appointment_models:
            patient_model = self.patient_repository.get_by_id(a.patient_id)
            doctor_model = self.doctor_repository.get_by_id(a.doctor_id)
            
            appointments.append(Appointment(
                patient=patient_model,
                doctor=doctor_model,
                schedule_time=a.schedule_time,
                duration=a.duration,
                status=a.status,
                notes=a.notes,
                appointment_id=a.appointment_id
            ))
        
        return appointments
    
    def find_available_slots(self, doctor_id, date, duration=30):
        """Find available appointment slots for a doctor on a specific date"""
        # Get the doctor's working hours (assuming 9 AM to 5 PM)
        working_start = 9  # 9 AM
        working_end = 17   # 5 PM
        
        # Get all appointments for the doctor on the specified date
        appointments = self.get_appointments_for_doctor(doctor_id, date)
        
        # Convert date string to datetime if needed
        if isinstance(date, str):
            date = datetime.strptime(date, "%Y-%m-%d").date()
        
        # Create a list of all possible time slots
        all_slots = []
        current_time = datetime.combine(date, datetime.min.time().replace(hour=working_start))
        end_time = datetime.combine(date, datetime.min.time().replace(hour=working_end))
        
        while current_time < end_time:
            all_slots.append(current_time)
            current_time += timedelta(minutes=duration)
        
        # Remove slots that conflict with existing appointments
        available_slots = []
        for slot in all_slots:
            if self.is_time_available(doctor_id, slot, duration):
                available_slots.append(slot)
        
        return available_slots
    
    def is_time_available(self, doctor_id, schedule_time, duration):
        """Check if a time slot is available for a doctor"""
        # Get all appointments for the doctor on the same day
        if isinstance(schedule_time, str):
            schedule_time = datetime.strptime(schedule_time, "%Y-%m-%d %H:%M")
        
        date = schedule_time.date()
        appointments = self.appointment_repository.get_by_doctor(doctor_id, date)
        
        # Calculate the end time of the proposed appointment
        end_time = schedule_time + timedelta(minutes=duration)
        
        # Check for conflicts with existing appointments
        for appointment in appointments:
            # Skip cancelled appointments
            if appointment.status == "cancelled":
                continue
                
            # Calculate the end time of the existing appointment
            existing_end_time = appointment.schedule_time + timedelta(minutes=appointment.duration)
            
            # Check for overlap
            if (schedule_time < existing_end_time and end_time > appointment.schedule_time):
                return False
        
        return True
    
    def reschedule_appointment(self, appointment_id, new_schedule_time):
        """Reschedule an appointment"""
        # Get the appointment
        appointment_model = self.appointment_repository.get_by_id(appointment_id)
        
        if not appointment_model:
            raise ValueError("Appointment not found")
        
        # Check if the new time is available
        if not self.is_time_available(appointment_model.doctor_id, new_schedule_time, appointment_model.duration):
            raise ValueError("The selected time conflicts with an existing appointment")
        
        # Update the appointment
        appointment_model.schedule_time = new_schedule_time if isinstance(new_schedule_time, datetime) else datetime.strptime(new_schedule_time, "%Y-%m-%d %H:%M")
        appointment_model.status = "rescheduled"
        
        # Save to database
        updated_appointment = self.appointment_repository.update(appointment_model)
        
        # Get patient and doctor
        patient_model = self.patient_repository.get_by_id(updated_appointment.patient_id)
        doctor_model = self.doctor_repository.get_by_id(updated_appointment.doctor_id)
        
        # Create and return domain entity
        from domain.entities import Appointment
        return Appointment(
            patient=patient_model,
            doctor=doctor_model,
            schedule_time=updated_appointment.schedule_time,
            duration=updated_appointment.duration,
            status=updated_appointment.status,
            notes=updated_appointment.notes,
            appointment_id=updated_appointment.appointment_id
        )
    
    def cancel_appointment(self, appointment_id):
        """Cancel an appointment"""
        # Get the appointment
        appointment_model = self.appointment_repository.get_by_id(appointment_id)
        
        if not appointment_model:
            raise ValueError("Appointment not found")
        
        # Update the appointment
        appointment_model.status = "cancelled"
        
        # Save to database
        updated_appointment = self.appointment_repository.update(appointment_model)
        
        # Get patient and doctor
        patient_model = self.patient_repository.get_by_id(updated_appointment.patient_id)
        doctor_model = self.doctor_repository.get_by_id(updated_appointment.doctor_id)
        
        # Create and return domain entity
        from domain.entities import Appointment
        return Appointment(
            patient=patient_model,
            doctor=doctor_model,
            schedule_time=updated_appointment.schedule_time,
            duration=updated_appointment.duration,
            status=updated_appointment.status,
            notes=updated_appointment.notes,
            appointment_id=updated_appointment.appointment_id
        )

class MedicalRecordService:
    """Service for medical record-related operations"""
    
    def __init__(self, medical_record_repository, patient_repository):
        self.medical_record_repository = medical_record_repository
        self.patient_repository = patient_repository
    
    def create_medical_record(self, patient_id, diagnosis, treatment_plan, notes=None):
        """Create a new medical record"""
        from domain.entities import PatientMedicalRecord
        from db.models import PatientMedicalRecord as MedicalRecordModel
        
        # Get the patient
        patient_model = self.patient_repository.get_by_id(patient_id)
        
        if not patient_model:
            raise ValueError("Patient not found")
        
        # Create the medical record model
        medical_record_model = MedicalRecordModel(
            patient_id=patient_id,
            diagnosis=diagnosis,
            treatment_plan=treatment_plan,
            notes=notes
        )
        
        # Save to database
        created_record = self.medical_record_repository.create(medical_record_model)
        
        # Create and return domain entity
        return PatientMedicalRecord(
            patient=patient_model,
            diagnosis=created_record.diagnosis,
            treatment_plan=created_record.treatment_plan,
            notes=created_record.notes,
            date_created=created_record.date_created,
            record_id=created_record.record_id
        )
    
    def get_medical_record(self, record_id):
        """Get a medical record by ID"""
        from domain.entities import PatientMedicalRecord
        
        # Get the medical record
        record_model = self.medical_record_repository.get_by_id(record_id)
        
        if not record_model:
            return None
        
        # Get the patient
        patient_model = self.patient_repository.get_by_id(record_model.patient_id)
        
        # Create and return domain entity
        return PatientMedicalRecord(
            patient=patient_model,
            diagnosis=record_model.diagnosis,
            treatment_plan=record_model.treatment_plan,
            notes=record_model.notes,
            date_created=record_model.date_created,
            record_id=record_model.record_id
        )
    
    def get_medical_records_for_patient(self, patient_id):
        """Get all medical records for a patient"""
        from domain.entities import PatientMedicalRecord
        
        # Get the patient
        patient_model = self.patient_repository.get_by_id(patient_id)
        
        if not patient_model:
            raise ValueError("Patient not found")
        
        # Get the medical records
        record_models = self.medical_record_repository.get_by_patient(patient_id)
        
        # Convert to domain entities
        return [
            PatientMedicalRecord(
                patient=patient_model,
                diagnosis=r.diagnosis,
                treatment_plan=r.treatment_plan,
                notes=r.notes,
                date_created=r.date_created,
                record_id=r.record_id
            ) for r in record_models
        ]
    
    def update_medical_record(self, record_id, field, value):
        """Update a medical record field"""
        # Get the medical record
        record_model = self.medical_record_repository.get_by_id(record_id)
        
        if not record_model:
            raise ValueError("Medical record not found")
        
        # Update the field
        if hasattr(record_model, field):
            setattr(record_model, field, value)
            updated_record = self.medical_record_repository.update(record_model)
            
            # Get the patient
            patient_model = self.patient_repository.get_by_id(updated_record.patient_id)
            
            # Create and return domain entity
            from domain.entities import PatientMedicalRecord
            return PatientMedicalRecord(
                patient=patient_model,
                diagnosis=updated_record.diagnosis,
                treatment_plan=updated_record.treatment_plan,
                notes=updated_record.notes,
                date_created=updated_record.date_created,
                record_id=updated_record.record_id
            )
        else:
            raise ValueError(f"Invalid field: {field}")

class SearchService:
    """Service for search operations"""
    
    def __init__(self, patient_repository, doctor_repository, appointment_repository, medical_record_repository):
        self.patient_repository = patient_repository
        self.doctor_repository = doctor_repository
        self.appointment_repository = appointment_repository
        self.medical_record_repository = medical_record_repository
    
    def search_patients(self, search_term):
        """Search for patients"""
        from domain.entities import Patient
        
        patient_models = self.patient_repository.search(search_term)
        
        # Convert to domain entities
        return [
            Patient(
                first_name=p.first_name,
                last_name=p.last_name,
                dob=p.dob,
                email=p.email,
                phone=p.phone,
                address=p.address,
                patient_id=p.patient_id,
                insurance_info=p.insurance_info,
                reg_date=p.reg_date,
                id=p.id
            ) for p in patient_models
        ]
    
    def search_doctors(self, search_term):
        """Search for doctors"""
        from domain.entities import Doctor
        
        doctor_models = self.doctor_repository.search(search_term)
        
        # Convert to domain entities
        return [
            Doctor(
                first_name=d.first_name,
                last_name=d.last_name,
                dob=d.dob,
                email=d.email,
                phone=d.phone,
                address=d.address,
                staff_id=d.staff_id,
                role=d.role,
                department=d.department,
                qualification=d.qualification,
                specialisation=d.specialisation,
                license_number=d.license_number,
                certifications=d.certifications,
                hire_date=d.hire_date,
                id=d.id
            ) for d in doctor_models
        ]
    
    def search_appointments(self, doctor_id=None, patient_id=None, date=None, status=None):
        """Search for appointments with various filters"""
        from domain.entities import Appointment
        from db.models import Appointment as AppointmentModel
        
        # Start with a base query
        query = self.appointment_repository.session.query(AppointmentModel)
        
        # Apply filters
        if doctor_id:
            query = query.filter(AppointmentModel.doctor_id == doctor_id)
        
        if patient_id:
            query = query.filter(AppointmentModel.patient_id == patient_id)
        
        if date:
            # If date is a string, convert it to datetime
            if isinstance(date, str):
                date = datetime.strptime(date, "%Y-%m-%d").date()
            
            # Filter appointments for the specified date
            query = query.filter(
                AppointmentModel.schedule_time >= datetime.combine(date, datetime.min.time()),
                AppointmentModel.schedule_time < datetime.combine(date, datetime.max.time())
            )
        
        if status:
            query = query.filter(AppointmentModel.status == status)
        
        # Execute the query
        appointment_models = query.all()
        
        # Convert to domain entities
        appointments = []
        for a in appointment_models:
            patient_model = self.patient_repository.get_by_id(a.patient_id)
            doctor_model = self.doctor_repository.get_by_id(a.doctor_id)
            
            appointments.append(Appointment(
                patient=patient_model,
                doctor=doctor_model,
                schedule_time=a.schedule_time,
                duration=a.duration,
                status=a.status,
                notes=a.notes,
                appointment_id=a.appointment_id
            ))
        
        return appointments
    
    def search_patient_medical_records(self, patient_id=None, diagnosis_term=None):
        """Search for medical records"""
        from domain.entities import PatientMedicalRecord
        from db.models import PatientMedicalRecord as MedicalRecordModel
        
        # Start with a base query
        query = self.medical_record_repository.session.query(MedicalRecordModel)
        
        # Apply filters
        if patient_id:
            query = query.filter(MedicalRecordModel.patient_id == patient_id)
        
        if diagnosis_term:
            query = query.filter(MedicalRecordModel.diagnosis.ilike(f"%{diagnosis_term}%"))
        
        # Execute the query
        record_models = query.all()
        
        # Convert to domain entities
        records = []
        for r in record_models:
            patient_model = self.patient_repository.get_by_id(r.patient_id)
            
            records.append(PatientMedicalRecord(
                patient=patient_model,
                diagnosis=r.diagnosis,
                treatment_plan=r.treatment_plan,
                notes=r.notes,
                date_created=r.date_created,
                record_id=r.record_id
            ))
        
        return records
    
    def filter_results(self, results, filter_criteria):
        """Apply additional filtering to search results"""
        filtered_results = []
        
        for item in results:
            matches_all_criteria = True
            
            for field, value in filter_criteria.items():
                if hasattr(item, field):
                    item_value = getattr(item, field)
                    
                    # Handle different types of comparisons
                    if isinstance(value, str) and isinstance(item_value, str):
                        if value.lower() not in item_value.lower():
                            matches_all_criteria = False
                            break
                    elif item_value != value:
                        matches_all_criteria = False
                        break
                else:
                    matches_all_criteria = False
                    break
            
            if matches_all_criteria:
                filtered_results.append(item)
        
        return filtered_results

class FileExportService:
    """Service for exporting data to various file formats"""
    
    def __init__(self, config):
        self.config = config
    
    def export_to_csv(self, data, output_file):
        """Export data to CSV format"""
        import csv
        import os
        
        # Ensure the output directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Check if data is a list of dictionaries
        if not data or not isinstance(data, list):
            raise ValueError("Data must be a non-empty list")
        
        # Get the fieldnames from the first item
        if hasattr(data[0], 'to_dict'):
            fieldnames = data[0].to_dict().keys()
            # Convert all items to dictionaries
            data = [item.to_dict() for item in data]
        elif isinstance(data[0], dict):
            fieldnames = data[0].keys()
        else:
            raise ValueError("Data items must be dictionaries or have a to_dict method")
        
        # Write to CSV
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        return output_file
    
    def export_to_pdf(self, data, output_file, title=None):
        """Export data to PDF format"""
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib import colors
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
            import os
            
            # Ensure the output directory exists
            output_dir = os.path.dirname(output_file)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Check if data is a list
            if not data or not isinstance(data, list):
                raise ValueError("Data must be a non-empty list")
            
            # Convert data to list of dictionaries if needed
            if hasattr(data[0], 'to_dict'):
                data_dicts = [item.to_dict() for item in data]
            elif isinstance(data[0], dict):
                data_dicts = data
            else:
                raise ValueError("Data items must be dictionaries or have a to_dict method")
            
            # Create the PDF document
            doc = SimpleDocTemplate(output_file, pagesize=letter)
            styles = getSampleStyleSheet()
            elements = []
            
            # Add title if provided
            if title:
                elements.append(Paragraph(title, styles['Title']))
                elements.append(Spacer(1, 12))
            
            # Get the fieldnames from the first item
            fieldnames = list(data_dicts[0].keys())
            
            # Create table data
            table_data = [fieldnames]  # Header row
            for item in data_dicts:
                row = [str(item.get(field, '')) for field in fieldnames]
                table_data.append(row)
            
            # Create the table
            table = Table(table_data)
            
            # Add style to the table
            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ])
            table.setStyle(style)
            
            elements.append(table)
            
            # Build the PDF
            doc.build(elements)
            
            return output_file
        except ImportError:
            raise ImportError("ReportLab is required for PDF export. Install it with 'pip install reportlab'")
    
    def generate_report(self, report_type, data, output_file, format_type="csv", title=None):
        """Generate a report based on the report type and format"""
        # Validate report type
        valid_report_types = ["patients", "doctors", "appointments", "medical_records"]
        if report_type not in valid_report_types:
            raise ValueError(f"Invalid report type. Must be one of: {', '.join(valid_report_types)}")
        
        # Validate format type
        valid_format_types = ["csv", "pdf"]
        if format_type not in valid_format_types:
            raise ValueError(f"Invalid format type. Must be one of: {', '.join(valid_format_types)}")
        
        # Generate the report
        if format_type == "csv":
            return self.export_to_csv(data, output_file)
        elif format_type == "pdf":
            return self.export_to_pdf(data, output_file, title=title or f"{report_type.capitalize()} Report")

