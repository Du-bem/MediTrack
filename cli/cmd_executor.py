"""
Command executor for the CLI
Executes commands based on the parsed input
"""
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def execute_command(entity, action, args_with_options, config):
    """Execute a command based on entity, action, and arguments"""
    try:
        # Extract args and options
        args = args_with_options.get("args", [])
        options = args_with_options.get("options", {})
        
        # Create a session
        session = config["db_session"]()
        
        # Execute the appropriate command
        if entity == "patient":
            execute_patient_command(action, args, options, session)
        elif entity == "doctor":
            execute_doctor_command(action, args, options, session)
        elif entity == "appointment":
            execute_appointment_command(action, args, options, session)
        elif entity == "medicalrecord":
            execute_medical_record_command(action, args, options, session)
        elif entity == "prescription":
            execute_prescription_command(action, args, options, session)
        elif entity == "labtest":
            execute_lab_test_command(action, args, options, session)
        elif entity == "report":
            execute_report_command(action, args, options, session, config)
        else:
            print(f"Unknown entity: {entity}")
        
        # Close the session
        session.close()
    
    except Exception as e:
        logger.error(f"Error executing command: {e}")
        print(f"Error: {e}")

def execute_patient_command(action, args, options, session):
    """Execute patient-related commands"""
    from db.repository import PatientRepository
    from domain.services import PatientService
    
    patient_repo = PatientRepository(session)
    patient_service = PatientService(patient_repo)
    
    if action == "add":
        # Validate arguments
        if len(args) < 5:
            print("Error: Not enough arguments")
            print("Usage: patient add <firstName> <lastName> <dob> <email> <phone> [address] [insuranceInfo]")
            return
        
        # Extract arguments
        first_name = args[0]
        last_name = args[1]
        dob = args[2]
        email = args[3]
        phone = args[4]
        address = args[5] if len(args) > 5 else None
        insurance_info = args[6] if len(args) > 6 else None
        
        # Create the patient
        try:
            patient = patient_service.create_patient(
                first_name, last_name, dob, email, phone, address, insurance_info
            )
            print(f"Patient created successfully with ID: {patient.patient_id}")
        except Exception as e:
            print(f"Error creating patient: {e}")
    
    elif action == "search":
        # Validate arguments
        if len(args) < 1:
            print("Error: Search term required")
            print("Usage: patient search <searchTerm>")
            return
        
        # Extract arguments
        search_term = args[0]
        
        # Search for patients
        patients = patient_service.search_patients(search_term)
        
        if patients:
            print(f"Found {len(patients)} patients:")
            for patient in patients:
                print(f"ID: {patient.patient_id}, Name: {patient.get_full_name()}, DOB: {patient.dob}, Email: {patient.email}")
        else:
            print("No patients found matching the search term")
    
    elif action == "list":
        # Extract options
        limit = int(options.get("limit", 10))
        offset = int(options.get("offset", 0))
        
        # Get all patients
        patients = patient_repo.get_all(limit=limit, offset=offset)
        
        if patients:
            print(f"Listing {len(patients)} patients:")
            for patient in patients:
                print(f"ID: {patient.patient_id}, Name: {patient.first_name} {patient.last_name}, DOB: {patient.dob}, Email: {patient.email}")
        else:
            print("No patients found")
    
    elif action == "view":
        # Validate arguments
        if len(args) < 1:
            print("Error: Patient ID required")
            print("Usage: patient view <patientId>")
            return
        
        # Extract arguments
        patient_id = args[0]
        
        # Get the patient
        patient = patient_service.get_patient(patient_id)
        
        if patient:
            print(f"Patient Details:")
            print(f"ID: {patient.patient_id}")
            print(f"Name: {patient.get_full_name()}")
            print(f"DOB: {patient.dob} (Age: {patient.get_age()})")
            print(f"Email: {patient.email}")
            print(f"Phone: {patient.phone}")
            print(f"Address: {patient.address}")
            print(f"Insurance: {patient.insurance_info}")
            print(f"Registration Date: {patient.reg_date}")
        else:
            print(f"Patient not found with ID: {patient_id}")
    
    elif action == "update":
        # Validate arguments
        if len(args) < 3:
            print("Error: Not enough arguments")
            print("Usage: patient update <patientId> <field> <value>")
            return
        
        # Extract arguments
        patient_id = args[0]
        field = args[1]
        value = args[2]
        
        # Update the patient
        try:
            patient = patient_service.update_patient(patient_id, field, value)
            if patient:
                print(f"Patient updated successfully")
                print(f"ID: {patient.patient_id}, Name: {patient.get_full_name()}, {field}: {value}")
            else:
                print(f"Patient not found with ID: {patient_id}")
        except Exception as e:
            print(f"Error updating patient: {e}")
    
    else:
        print(f"Unknown action: {action}")

def execute_doctor_command(action, args, options, session):
    """Execute doctor-related commands"""
    from db.repository import DoctorRepository
    from domain.services import DoctorService
    
    doctor_repo = DoctorRepository(session)
    doctor_service = DoctorService(doctor_repo)
    
    if action == "add":
        # Validate arguments
        if len(args) < 7:
            print("Error: Not enough arguments")
            print("Usage: doctor add <firstName> <lastName> <dob> <email> <phone> <specialisation> <licenseNumber> [department] [certifications]")
            return
        
        # Extract arguments
        first_name = args[0]
        last_name = args[1]
        dob = args[2]
        email = args[3]
        phone = args[4]
        specialisation = args[5]
        license_number = args[6]
        department = args[7] if len(args) > 7 else "General"
        certifications = args[8] if len(args) > 8 else None
        
        # Create the doctor
        try:
            doctor = doctor_service.create_doctor(
                first_name, last_name, dob, email, phone, specialisation, 
                license_number, department, certifications
            )
            print(f"Doctor created successfully with ID: {doctor.staff_id}")
        except Exception as e:
            print(f"Error creating doctor: {e}")
    
    elif action == "search":
        # Validate arguments
        if len(args) < 1:
            print("Error: Search term required")
            print("Usage: doctor search <searchTerm>")
            return
        
        # Extract arguments
        search_term = args[0]
        
        # Search for doctors
        doctors = doctor_service.search_doctors(search_term)
        
        if doctors:
            print(f"Found {len(doctors)} doctors:")
            for doctor in doctors:
                print(f"ID: {doctor.staff_id}, Name: {doctor.get_full_name()}, Specialisation: {doctor.specialisation}")
        else:
            print("No doctors found matching the search term")
    
    elif action == "list":
        # Extract options
        department = options.get("department")
        specialisation = options.get("specialisation")
        
        # Get doctors based on filters
        if specialisation:
            doctors = doctor_service.get_doctors_by_specialisation(specialisation)
        else:
            doctors = doctor_repo.get_all()
        
        # Filter by department if specified
        if department and doctors:
            doctors = [d for d in doctors if d.department == department]
        
        if doctors:
            print(f"Listing {len(doctors)} doctors:")
            for doctor in doctors:
                print(f"ID: {doctor.staff_id}, Name: {doctor.first_name} {doctor.last_name}, Specialisation: {doctor.specialisation}, Department: {doctor.department}")
        else:
            print("No doctors found")
    
    else:
        print(f"Unknown action: {action}")

def execute_appointment_command(action, args, options, session):
    """Execute appointment-related commands"""
    from db.repository import AppointmentRepository, PatientRepository, DoctorRepository
    from domain.services import AppointmentService
    
    appointment_repo = AppointmentRepository(session)
    patient_repo = PatientRepository(session)
    doctor_repo = DoctorRepository(session)
    appointment_service = AppointmentService(appointment_repo, patient_repo, doctor_repo)
    
    if action == "add":
        # Validate arguments
        if len(args) < 4:
            print("Error: Not enough arguments")
            print("Usage: appointment add <patientId> <doctorId> <dateTime> <duration> [notes]")
            return
        
        # Extract arguments
        patient_id = int(args[0])
        doctor_id = int(args[1])
        schedule_time = args[2]
        duration = int(args[3])
        notes = args[4] if len(args) > 4 else None
        
        # Create the appointment
        try:
            appointment = appointment_service.create_appointment(
                patient_id, doctor_id, schedule_time, duration, notes
            )
            print(f"Appointment created successfully with ID: {appointment.appointment_id}")
            print(f"Patient: {appointment.patient.get_full_name()}")
            print(f"Doctor: {appointment.doctor.get_full_name()}")
            print(f"Time: {appointment.schedule_time}")
            print(f"Duration: {appointment.duration} minutes")
        except Exception as e:
            print(f"Error creating appointment: {e}")
    
    elif action == "list":
        # Extract options
        doctor_id = options.get("doctor")
        patient_id = options.get("patient")
        date = options.get("date")
        status = options.get("status")
        
        # Convert IDs to integers if provided
        if doctor_id:
            try:
                doctor_id = int(doctor_id)
            except ValueError:
                print("Error: doctor ID must be an integer")
                return
        
        if patient_id:
            try:
                patient_id = int(patient_id)
            except ValueError:
                print("Error: patient ID must be an integer")
                return
        
        # Get appointments based on filters
        from domain.services import SearchService
        search_service = SearchService(patient_repo, doctor_repo, appointment_repo, None)
        appointments = search_service.search_appointments(doctor_id, patient_id, date, status)
        
        if appointments:
            print(f"Listing {len(appointments)} appointments:")
            for appointment in appointments:
                print(f"ID: {appointment.appointment_id}, Patient: {appointment.patient.get_full_name()}, Doctor: {appointment.doctor.get_full_name()}, Time: {appointment.schedule_time}, Status: {appointment.status}")
        else:
            print("No appointments found")
    
    elif action == "reschedule":
        # Validate arguments
        if len(args) < 2:
            print("Error: Not enough arguments")
            print("Usage: appointment reschedule <appointmentId> <newDateTime>")
            return
        
        # Extract arguments
        appointment_id = int(args[0])
        new_schedule_time = args[1]
        
        # Reschedule the appointment
        try:
            appointment = appointment_service.reschedule_appointment(appointment_id, new_schedule_time)
            print(f"Appointment rescheduled successfully")
            print(f"ID: {appointment.appointment_id}")
            print(f"Patient: {appointment.patient.get_full_name()}")
            print(f"Doctor: {appointment.doctor.get_full_name()}")
            print(f"New Time: {appointment.schedule_time}")
            print(f"Status: {appointment.status}")
        except Exception as e:
            print(f"Error rescheduling appointment: {e}")
    
    elif action == "cancel":
        # Validate arguments
        if len(args) < 1:
            print("Error: Appointment ID required")
            print("Usage: appointment cancel <appointmentId> [reason]")
            return
        
        # Extract arguments
        appointment_id = int(args[0])
        
        # Cancel the appointment
        try:
            appointment = appointment_service.cancel_appointment(appointment_id)
            print(f"Appointment cancelled successfully")
            print(f"ID: {appointment.appointment_id}")
            print(f"Patient: {appointment.patient.get_full_name()}")
            print(f"Doctor: {appointment.doctor.get_full_name()}")
            print(f"Time: {appointment.schedule_time}")
            print(f"Status: {appointment.status}")
        except Exception as e:
            print(f"Error cancelling appointment: {e}")
    
    else:
        print(f"Unknown action: {action}")

def execute_medical_record_command(action, args, options, session):
    """Execute medical record-related commands"""
    from db.repository import MedicalRecordRepository, PatientRepository
    from domain.services import MedicalRecordService
    
    medical_record_repo = MedicalRecordRepository(session)
    patient_repo = PatientRepository(session)
    medical_record_service = MedicalRecordService(medical_record_repo, patient_repo)
    
    if action == "add":
        # Validate arguments
        if len(args) < 3:
            print("Error: Not enough arguments")
            print("Usage: medicalrecord add <patientId> <diagnosis> <treatmentPlan> [notes]")
            return
        
        # Extract arguments
        patient_id = int(args[0])
        diagnosis = args[1]
        treatment_plan = args[2]
        notes = args[3] if len(args) > 3 else None
        
        # Create the medical record
        try:
            record = medical_record_service.create_medical_record(
                patient_id, diagnosis, treatment_plan, notes
            )
            print(f"Medical record created successfully with ID: {record.record_id}")
            print(f"Patient: {record.patient.get_full_name()}")
            print(f"Diagnosis: {record.diagnosis}")
            print(f"Treatment Plan: {record.treatment_plan}")
        except Exception as e:
            print(f"Error creating medical record: {e}")
    
    elif action == "view":
        # Validate arguments
        if len(args) < 1:
            print("Error: Record ID required")
            print("Usage: medicalrecord view <recordId>")
            return
        
        # Extract arguments
        record_id = int(args[0])
        
        # Get the medical record
        record = medical_record_service.get_medical_record(record_id)
        
        if record:
            print(f"Medical Record Details:")
            print(f"ID: {record.record_id}")
            print(f"Patient: {record.patient.get_full_name()}")
            print(f"Date Created: {record.date_created}")
            print(f"Diagnosis: {record.diagnosis}")
            print(f"Treatment Plan: {record.treatment_plan}")
            print(f"Notes: {record.notes}")
        else:
            print(f"Medical record not found with ID: {record_id}")
    
    elif action == "list":
        # Validate arguments
        if len(args) < 1:
            print("Error: Patient ID required")
            print("Usage: medicalrecord list <patientId>")
            return
        
        # Extract arguments
        patient_id = int(args[0])
        
        # Get the medical records
        records = medical_record_service.get_medical_records_for_patient(patient_id)
        
        if records:
            print(f"Listing {len(records)} medical records for patient:")
            for record in records:
                print(f"ID: {record.record_id}, Date: {record.date_created}, Diagnosis: {record.diagnosis}")
        else:
            print("No medical records found")
    
    elif action == "update":
        # Validate arguments
        if len(args) < 3:
            print("Error: Not enough arguments")
            print("Usage: medicalrecord update <recordId> <field> <value>")
            return
        
        # Extract arguments
        record_id = int(args[0])
        field = args[1]
        value = args[2]
        
        # Update the medical record
        try:
            record = medical_record_service.update_medical_record(record_id, field, value)
            if record:
                print(f"Medical record updated successfully")
                print(f"ID: {record.record_id}, {field}: {value}")
            else:
                print(f"Medical record not found with ID: {record_id}")
        except Exception as e:
            print(f"Error updating medical record: {e}")
    
    else:
        print(f"Unknown action: {action}")

def execute_prescription_command(action, args, options, session):
    """Execute prescription-related commands"""
    from db.repository import PrescriptionRepository, MedicalRecordRepository
    from db.models import Prescription
    
    prescription_repo = PrescriptionRepository(session)
    medical_record_repo = MedicalRecordRepository(session)
    
    if action == "add":
        # Validate arguments
        if len(args) < 6:
            print("Error: Not enough arguments")
            print("Usage: prescription add <recordId> <medication> <dosage> <frequency> <startDate> <endDate> [instructions]")
            return
        
        # Extract arguments
        record_id = int(args[0])
        medication = args[1]
        dosage = args[2]
        frequency = args[3]
        start_date = args[4]
        end_date = args[5]
        instructions = args[6] if len(args) > 6 else None
        
        # Check if the medical record exists
        medical_record = medical_record_repo.get_by_id(record_id)
        if not medical_record:
            print(f"Medical record not found with ID: {record_id}")
            return
        
        # Create the prescription
        try:
            # Convert dates if they are strings
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            if isinstance(end_date, str):
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            
            prescription = Prescription(
                record_id=record_id,
                medication=medication,
                dosage=dosage,
                frequency=frequency,
                start_date=start_date,
                end_date=end_date,
                instructions=instructions
            )
            
            created_prescription = prescription_repo.create(prescription)
            print(f"Prescription created successfully with ID: {created_prescription.prescription_id}")
            print(f"Medication: {created_prescription.medication}")
            print(f"Dosage: {created_prescription.dosage}")
            print(f"Frequency: {created_prescription.frequency}")
        except Exception as e:
            print(f"Error creating prescription: {e}")
    
    elif action == "list":
        # Validate arguments
        if len(args) < 1:
            print("Error: Record ID required")
            print("Usage: prescription list <recordId>")
            return
        
        # Extract arguments
        record_id = int(args[0])
        
        # Get the prescriptions
        prescriptions = prescription_repo.get_by_record(record_id)
        
        if prescriptions:
            print(f"Listing {len(prescriptions)} prescriptions for medical record {record_id}:")
            for prescription in prescriptions:
                status = "Active" if prescription.is_active else "Inactive"
                print(f"ID: {prescription.prescription_id}, Medication: {prescription.medication}, Dosage: {prescription.dosage}, Status: {status}")
        else:
            print("No prescriptions found")
    
    elif action == "update":
        # Validate arguments
        if len(args) < 3:
            print("Error: Not enough arguments")
            print("Usage: prescription update <prescriptionId> <field> <value>")
            return
        
        # Extract arguments
        prescription_id = int(args[0])
        field = args[1]
        value = args[2]
        
        # Get the prescription
        prescription = prescription_repo.get_by_id(prescription_id)
        
        if not prescription:
            print(f"Prescription not found with ID: {prescription_id}")
            return
        
        # Update the field
        if hasattr(prescription, field):
            # Handle date fields
            if field in ['start_date', 'end_date'] and not isinstance(value, datetime):
                value = datetime.strptime(value, "%Y-%m-%d").date()
            # Handle boolean fields
            elif field == 'is_active':
                value = value.lower() in ['true', 'yes', '1']
                
            setattr(prescription, field, value)
            updated_prescription = prescription_repo.update(prescription)
            print(f"Prescription updated successfully")
            print(f"ID: {updated_prescription.prescription_id}, {field}: {value}")
        else:
            print(f"Invalid field: {field}")
    
    elif action == "refill":
        # Validate arguments
        if len(args) < 2:
            print("Error: Not enough arguments")
            print("Usage: prescription refill <prescriptionId> <newEndDate>")
            return
        
        # Extract arguments
        prescription_id = int(args[0])
        new_end_date = args[1]
        
        # Get the prescription
        prescription = prescription_repo.get_by_id(prescription_id)
        
        if not prescription:
            print(f"Prescription not found with ID: {prescription_id}")
            return
        
        # Refill the prescription
        try:
            # Convert date if it's a string
            if isinstance(new_end_date, str):
                new_end_date = datetime.strptime(new_end_date, "%Y-%m-%d").date()
            
            prescription.end_date = new_end_date
            prescription.is_active = True
            
            updated_prescription = prescription_repo.update(prescription)
            print(f"Prescription refilled successfully")
            print(f"ID: {updated_prescription.prescription_id}")
            print(f"Medication: {updated_prescription.medication}")
            print(f"New End Date: {updated_prescription.end_date}")
            print(f"Status: Active")
        except Exception as e:
            print(f"Error refilling prescription: {e}")
    
    else:
        print(f"Unknown action: {action}")

def execute_lab_test_command(action, args, options, session):
    """Execute lab test-related commands"""
    from db.repository import LabTestRepository, MedicalRecordRepository
    from db.models import LabTest
    
    lab_test_repo = LabTestRepository(session)
    medical_record_repo = MedicalRecordRepository(session)
    
    if action == "add":
        # Validate arguments
        if len(args) < 4:
            print("Error: Not enough arguments")
            print("Usage: labtest add <recordId> <testName> <testType> <orderedDate>")
            return
        
        # Extract arguments
        record_id = int(args[0])
        test_name = args[1]
        test_type = args[2]
        ordered_date = args[3]
        
        # Check if the medical record exists
        medical_record = medical_record_repo.get_by_id(record_id)
        if not medical_record:
            print(f"Medical record not found with ID: {record_id}")
            return
        
        # Create the lab test
        try:
            # Convert date if it's a string
            if isinstance(ordered_date, str):
                ordered_date = datetime.strptime(ordered_date, "%Y-%m-%d").date()
            
            lab_test = LabTest(
                record_id=record_id,
                test_name=test_name,
                test_type=test_type,
                ordered_date=ordered_date
            )
            
            created_lab_test = lab_test_repo.create(lab_test)
            print(f"Lab test created successfully with ID: {created_lab_test.test_id}")
            print(f"Test Name: {created_lab_test.test_name}")
            print(f"Test Type: {created_lab_test.test_type}")
            print(f"Ordered Date: {created_lab_test.ordered_date}")
        except Exception as e:
            print(f"Error creating lab test: {e}")
    
    elif action == "result":
        # Validate arguments
        if len(args) < 5:
            print("Error: Not enough arguments")
            print("Usage: labtest result <testId> <resultDate> <result> <referenceRange> <isAbnormal>")
            return
        
        # Extract arguments
        test_id = int(args[0])
        result_date = args[1]
        result = args[2]
        reference_range = args[3]
        is_abnormal = args[4].lower() in ['true', 'yes', '1']
        
        # Get the lab test
        lab_test = lab_test_repo.get_by_id(test_id)
        
        if not lab_test:
            print(f"Lab test not found with ID: {test_id}")
            return
        
        # Update the lab test with results
        try:
            # Convert date if it's a string
            if isinstance(result_date, str):
                result_date = datetime.strptime(result_date, "%Y-%m-%d").date()
            
            lab_test.result_date = result_date
            lab_test.result = result
            lab_test.reference_range = reference_range
            lab_test.is_abnormal = is_abnormal
            
            updated_lab_test = lab_test_repo.update(lab_test)
            print(f"Lab test results added successfully")
            print(f"ID: {updated_lab_test.test_id}")
            print(f"Test Name: {updated_lab_test.test_name}")
            print(f"Result: {updated_lab_test.result}")
            print(f"Abnormal: {'Yes' if updated_lab_test.is_abnormal else 'No'}")
        except Exception as e:
            print(f"Error adding lab test results: {e}")
    
    elif action == "list":
        # Validate arguments
        if len(args) < 1:
            print("Error: Record ID required")
            print("Usage: labtest list <recordId>")
            return
        
        # Extract arguments
        record_id = int(args[0])
        
        # Get the lab tests
        lab_tests = lab_test_repo.get_by_record(record_id)
        
        if lab_tests:
            print(f"Listing {len(lab_tests)} lab tests for medical record {record_id}:")
            for lab_test in lab_tests:
                result_status = "Results Available" if lab_test.result else "Pending"
                abnormal = "Abnormal" if lab_test.is_abnormal else "Normal"
                print(f"ID: {lab_test.test_id}, Test: {lab_test.test_name}, Type: {lab_test.test_type}, Status: {result_status}, {abnormal if lab_test.result else ''}")
        else:
            print("No lab tests found")
    
    else:
        print(f"Unknown action: {action}")

def execute_report_command(action, args, options, session, config):
    """Execute report-related commands"""
    if action != "export":
        print(f"Unknown action: {action}")
        return
    
    # Extract options
    report_type = options.get("type")
    format_type = options.get("format", "csv")
    output_file = options.get("output")
    filters = options.get("filters", "")
    
    if not report_type:
        print("Error: Report type required")
        print("Usage: report export --type=<entityType> --format=<formatType> --output=<fileName> [--filters=<filterString>]")
        return
    
    if not output_file:
        print("Error: Output file required")
        print("Usage: report export --type=<entityType> --format=<formatType> --output=<fileName> [--filters=<filterString>]")
        return
    
    # Prepare the output file path
    import os
    output_dir = config["export"]["default_directory"]
    output_path = os.path.join(output_dir, output_file)
    
    # Get the data based on report type
    data = []
    title = None
    
    if report_type == "patients":
        from db.repository import PatientRepository
        patient_repo = PatientRepository(session)
        patients = patient_repo.get_all()
        data = [p for p in patients]
        title = "Patient Report"
    
    elif report_type == "doctors":
        from db.repository import DoctorRepository
        doctor_repo = DoctorRepository(session)
        doctors = doctor_repo.get_all()
        data = [d for d in doctors]
        title = "Doctor Report"
    
    elif report_type == "appointments":
        from db.repository import AppointmentRepository
        appointment_repo = AppointmentRepository(session)
        appointments = appointment_repo.get_all()
        data = [a for a in appointments]
        title = "Appointment Report"
    
    elif report_type == "medical_records":
        from db.repository import MedicalRecordRepository
        medical_record_repo = MedicalRecordRepository(session)
        records = medical_record_repo.get_all()
        data = [r for r in records]
        title = "Medical Record Report"
    
    else:
        print(f"Unknown report type: {report_type}")
        return
    
    # Apply filters if provided
    if filters:
        # Parse filter string (format: field1=value1,field2=value2)
        filter_dict = {}
        filter_parts = filters.split(',')
        for part in filter_parts:
            if '=' in part:
                key, value = part.split('=', 1)
                filter_dict[key.strip()] = value.strip()
        
        # Apply filters
        filtered_data = []
        for item in data:
            matches_all = True
            for field, value in filter_dict.items():
                if hasattr(item, field):
                    item_value = str(getattr(item, field))
                    if value not in item_value:
                        matches_all = False
                        break
                else:
                    matches_all = False
                    break
            
            if matches_all:
                filtered_data.append(item)
        
        data = filtered_data
    
    # Generate the report
    if not data:
        print("No data found for the report")
        return
    
    try:
        from domain.services import FileExportService
        export_service = FileExportService(config)
        
        if format_type == "csv":
            export_service.export_to_csv(data, output_path)
            print(f"Report exported successfully to {output_path}")
        elif format_type == "pdf":
            export_service.export_to_pdf(data, output_path, title=title)
            print(f"Report exported successfully to {output_path}")
        else:
            print(f"Unsupported format type: {format_type}")
    except Exception as e:
        print(f"Error generating report: {e}")

