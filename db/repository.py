"""
Repository pattern implementation for database access
"""
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

class BaseRepository:
    """Base repository with common CRUD operations"""
    
    def __init__(self, session: Session, model_class):
        self.session = session
        self.model_class = model_class
    
    def get_by_id(self, id):
        """Get entity by ID"""
        return self.session.query(self.model_class).get(id)
    
    def get_all(self, limit=None, offset=None):
        """Get all entities with optional pagination"""
        query = self.session.query(self.model_class)
        
        if offset is not None:
            query = query.offset(offset)
        
        if limit is not None:
            query = query.limit(limit)
            
        return query.all()
    
    def create(self, entity):
        """Create a new entity"""
        try:
            self.session.add(entity)
            self.session.commit()
            return entity
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error creating entity: {e}")
            raise
    
    def update(self, entity):
        """Update an existing entity"""
        try:
            self.session.merge(entity)
            self.session.commit()
            return entity
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating entity: {e}")
            raise
    
    def delete(self, entity):
        """Delete an entity"""
        try:
            self.session.delete(entity)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error deleting entity: {e}")
            raise
    
    def delete_by_id(self, id):
        """Delete entity by ID"""
        entity = self.get_by_id(id)
        if entity:
            return self.delete(entity)
        return False

class PatientRepository(BaseRepository):
    """Repository for Patient entity"""
    
    def __init__(self, session):
        from db.models import Patient
        super().__init__(session, Patient)
    
    def search(self, search_term):
        """Search patients by name, email, or patient ID"""
        from db.models import Patient
        search_pattern = f"%{search_term}%"
        
        return self.session.query(Patient).filter(
            (Patient.first_name.ilike(search_pattern)) |
            (Patient.last_name.ilike(search_pattern)) |
            (Patient.email.ilike(search_pattern)) |
            (Patient.patient_id.ilike(search_pattern))
        ).all()
    
    def get_by_patient_id(self, patient_id):
        """Get patient by patient_id field"""
        from db.models import Patient
        return self.session.query(Patient).filter(Patient.patient_id == patient_id).first()

class DoctorRepository(BaseRepository):
    """Repository for Doctor entity"""
    
    def __init__(self, session):
        from db.models import Doctor
        super().__init__(session, Doctor)
    
    def search(self, search_term):
        """Search doctors by name, email, specialisation, or license number"""
        from db.models import Doctor
        search_pattern = f"%{search_term}%"
        
        return self.session.query(Doctor).filter(
            (Doctor.first_name.ilike(search_pattern)) |
            (Doctor.last_name.ilike(search_pattern)) |
            (Doctor.email.ilike(search_pattern)) |
            (Doctor.specialisation.ilike(search_pattern)) |
            (Doctor.license_number.ilike(search_pattern))
        ).all()
    
    def get_by_specialisation(self, specialisation):
        """Get doctors by specialisation"""
        from db.models import Doctor
        return self.session.query(Doctor).filter(Doctor.specialisation == specialisation).all()
    
    def get_by_department(self, department):
        """Get doctors by department"""
        from db.models import Doctor
        return self.session.query(Doctor).filter(Doctor.department == department).all()

class AppointmentRepository(BaseRepository):
    """Repository for Appointment entity"""
    
    def __init__(self, session):
        from db.models import Appointment
        super().__init__(session, Appointment)
    
    def get_by_doctor(self, doctor_id, date=None):
        """Get appointments for a specific doctor, optionally filtered by date"""
        from db.models import Appointment
        from datetime import datetime
        
        query = self.session.query(Appointment).filter(Appointment.doctor_id == doctor_id)
        
        if date:
            # If date is a string, convert it to datetime
            if isinstance(date, str):
                date = datetime.strptime(date, "%Y-%m-%d").date()
            
            # Filter appointments for the specified date
            query = query.filter(
                Appointment.schedule_time >= datetime.combine(date, datetime.min.time()),
                Appointment.schedule_time < datetime.combine(date, datetime.max.time())
            )
        
        return query.all()
    
    def get_by_patient(self, patient_id, date=None):
        """Get appointments for a specific patient, optionally filtered by date"""
        from db.models import Appointment
        from datetime import datetime
        
        query = self.session.query(Appointment).filter(Appointment.patient_id == patient_id)
        
        if date:
            # If date is a string, convert it to datetime
            if isinstance(date, str):
                date = datetime.strptime(date, "%Y-%m-%d").date()
            
            # Filter appointments for the specified date
            query = query.filter(
                Appointment.schedule_time >= datetime.combine(date, datetime.min.time()),
                Appointment.schedule_time < datetime.combine(date, datetime.max.time())
            )
        
        return query.all()
    
    def get_by_date_range(self, start_date, end_date):
        """Get appointments within a date range"""
        from db.models import Appointment
        from datetime import datetime
        
        # Convert string dates to datetime if needed
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        
        return self.session.query(Appointment).filter(
            Appointment.schedule_time >= datetime.combine(start_date, datetime.min.time()),
            Appointment.schedule_time < datetime.combine(end_date, datetime.max.time())
        ).all()

class MedicalRecordRepository(BaseRepository):
    """Repository for PatientMedicalRecord entity"""
    
    def __init__(self, session):
        from db.models import PatientMedicalRecord
        super().__init__(session, PatientMedicalRecord)
    
    def get_by_patient(self, patient_id):
        """Get all medical records for a patient"""
        from db.models import PatientMedicalRecord
        return self.session.query(PatientMedicalRecord).filter(
            PatientMedicalRecord.patient_id == patient_id
        ).all()
    
    def search_by_diagnosis(self, diagnosis_term):
        """Search medical records by diagnosis"""
        from db.models import PatientMedicalRecord
        search_pattern = f"%{diagnosis_term}%"
        
        return self.session.query(PatientMedicalRecord).filter(
            PatientMedicalRecord.diagnosis.ilike(search_pattern)
        ).all()

class PrescriptionRepository(BaseRepository):
    """Repository for Prescription entity"""
    
    def __init__(self, session):
        from db.models import Prescription
        super().__init__(session, Prescription)
    
    def get_by_record(self, record_id):
        """Get all prescriptions for a medical record"""
        from db.models import Prescription
        return self.session.query(Prescription).filter(
            Prescription.record_id == record_id
        ).all()
    
    def get_active_prescriptions(self, record_id):
        """Get active prescriptions for a medical record"""
        from db.models import Prescription
        return self.session.query(Prescription).filter(
            Prescription.record_id == record_id,
            Prescription.is_active == True
        ).all()

class LabTestRepository(BaseRepository):
    """Repository for LabTest entity"""
    
    def __init__(self, session):
        from db.models import LabTest
        super().__init__(session, LabTest)
    
    def get_by_record(self, record_id):
        """Get all lab tests for a medical record"""
        from db.models import LabTest
        return self.session.query(LabTest).filter(
            LabTest.record_id == record_id
        ).all()
    
    def get_abnormal_tests(self, record_id=None):
        """Get abnormal lab tests, optionally filtered by record"""
        from db.models import LabTest
        
        query = self.session.query(LabTest).filter(LabTest.is_abnormal == True)
        
        if record_id:
            query = query.filter(LabTest.record_id == record_id)
            
        return query.all()

