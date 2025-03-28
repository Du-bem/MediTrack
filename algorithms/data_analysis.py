"""
Data analysis algorithms for MediTrack
"""
from datetime import datetime, timedelta
from collections import Counter, defaultdict

def analyze_patient_demographics(patients):
    """
    Analyze patient demographics
    
    Args:
        patients: List of patient objects
        
    Returns:
        Dictionary with demographic analysis
    """
    if not patients:
        return {"error": "No patients to analyze"}
    
    today = datetime.now().date()
    
    # Age distribution
    age_groups = {
        "0-18": 0,
        "19-35": 0,
        "36-50": 0,
        "51-65": 0,
        "66+": 0
    }
    
    # Gender distribution (assuming gender is stored in the patient object)
    genders = Counter()
    
    # Insurance distribution
    insurance_types = Counter()
    
    # Registration trends
    reg_months = Counter()
    
    for patient in patients:
        # Calculate age
        age = today.year - patient.dob.year - ((today.month, today.day) < (patient.dob.month, patient.dob.day))
        
        # Update age groups
        if age <= 18:
            age_groups["0-18"] += 1
        elif age <= 35:
            age_groups["19-35"] += 1
        elif age <= 50:
            age_groups["36-50"] += 1
        elif age <= 65:
            age_groups["51-65"] += 1
        else:
            age_groups["66+"] += 1
        
        # Update gender counter if gender attribute exists
        if hasattr(patient, 'gender'):
            genders[patient.gender] += 1
        
        # Update insurance counter
        if hasattr(patient, 'insurance_info') and patient.insurance_info:
            # Extract insurance type from insurance_info
            insurance_type = patient.insurance_info.split()[0] if patient.insurance_info else "None"
            insurance_types[insurance_type] += 1
        
        # Update registration trends
        if hasattr(patient, 'reg_date'):
            reg_month = patient.reg_date.strftime("%Y-%m")
            reg_months[reg_month] += 1
    
    # Calculate percentages
    total_patients = len(patients)
    age_distribution = {group: {"count": count, "percentage": (count / total_patients) * 100} 
                        for group, count in age_groups.items()}
    
    gender_distribution = {gender: {"count": count, "percentage": (count / total_patients) * 100} 
                          for gender, count in genders.items()}
    
    insurance_distribution = {ins: {"count": count, "percentage": (count / total_patients) * 100} 
                             for ins, count in insurance_types.items()}
    
    # Sort registration trends by month
    sorted_reg_months = dict(sorted(reg_months.items()))
    
    return {
        "total_patients": total_patients,
        "age_distribution": age_distribution,
        "gender_distribution": gender_distribution,
        "insurance_distribution": insurance_distribution,
        "registration_trends": sorted_reg_months
    }

def analyze_appointment_patterns(appointments):
    """
    Analyze appointment patterns
    
    Args:
        appointments: List of appointment objects
        
    Returns:
        Dictionary with appointment analysis
    """
    if not appointments:
        return {"error": "No appointments to analyze"}
    
    # Day of week distribution
    days_of_week = Counter()
    
    # Hour of day distribution
    hours_of_day = Counter()
    
    # Status distribution
    status_counts = Counter()
    
    # Doctor workload
    doctor_appointments = defaultdict(int)
    
    # Cancellation rate
    total_appointments = len(appointments)
    cancelled_appointments = 0
    
    # No-show rate (if status includes "no-show")
    no_show_appointments = 0
    
    for appointment in appointments:
        # Day of week
        day_of_week = appointment.schedule_time.strftime("%A")
        days_of_week[day_of_week] += 1
        
        # Hour of day
        hour = appointment.schedule_time.hour
        hours_of_day[hour] += 1
        
        # Status
        status_counts[appointment.status] += 1
        
        # Doctor workload
        if hasattr(appointment, 'doctor') and hasattr(appointment.doctor, 'id'):
            doctor_id = appointment.doctor.id
            doctor_appointments[doctor_id] += 1
        
        # Cancellation count
        if appointment.status == "cancelled":
            cancelled_appointments += 1
        
        # No-show count
        if appointment.status == "no-show":
            no_show_appointments += 1
    
    # Calculate rates
    cancellation_rate = (cancelled_appointments / total_appointments) * 100 if total_appointments > 0 else 0
    no_show_rate = (no_show_appointments / total_appointments) * 100 if total_appointments > 0 else 0
    
    # Sort distributions
    days_sorted = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    days_of_week_sorted = {day: days_of_week[day] for day in days_sorted}
    
    hours_of_day_sorted = dict(sorted(hours_of_day.items()))
    
    # Get top doctors by workload
    top_doctors = dict(sorted(doctor_appointments.items(), key=lambda x: x[1], reverse=True)[:5])
    
    return {
        "total_appointments": total_appointments,
        "days_of_week_distribution": days_of_week_sorted,
        "hours_of_day_distribution": hours_of_day_sorted,
        "status_distribution": dict(status_counts),
        "top_doctors_by_workload": top_doctors,
        "cancellation_rate": cancellation_rate,
        "no_show_rate": no_show_rate
    }

def analyze_medical_conditions(medical_records):
    """
    Analyze medical conditions from medical records
    
    Args:
        medical_records: List of medical record objects
        
    Returns:
        Dictionary with medical condition analysis
    """
    if not medical_records:
        return {"error": "No medical records to analyze"}
    
    # Common diagnoses
    diagnoses = Counter()
    
    # Common treatments
    treatments = Counter()
    
    # Abnormal lab tests
    abnormal_tests = Counter()
    
    for record in medical_records:
        # Extract diagnoses (assuming diagnoses are comma-separated)
        if hasattr(record, 'diagnosis'):
            for diagnosis in record.diagnosis.split(','):
                diagnoses[diagnosis.strip()] += 1
        
        # Extract treatments (assuming treatments are comma-separated)
        if hasattr(record, 'treatment_plan'):
            for treatment in record.treatment_plan.split(','):
                treatments[treatment.strip()] += 1
        
        # Count abnormal lab tests
        if hasattr(record, 'lab_tests'):
            for test in record.lab_tests:
                if test.is_abnormal:
                    abnormal_tests[test.test_name] += 1
    
    # Get top diagnoses, treatments, and abnormal tests
    top_diagnoses = dict(diagnoses.most_common(10))
    top_treatments = dict(treatments.most_common(10))
    top_abnormal_tests = dict(abnormal_tests.most_common(10))
    
    return {
        "total_records": len(medical_records),
        "top_diagnoses": top_diagnoses,
        "top_treatments": top_treatments,
        "top_abnormal_tests": top_abnormal_tests
    }

def predict_appointment_demand(appointments, future_days=30):
    """
    Predict appointment demand for future days based on historical data
    
    Args:
        appointments: List of historical appointment objects
        future_days: Number of days to predict
        
    Returns:
        Dictionary with predicted demand by day
    """
    if not appointments:
        return {"error": "No appointments to analyze"}
    
    # Group appointments by day of week
    day_of_week_counts = defaultdict(list)
    
    # Group appointments by date to get daily counts
    daily_counts = Counter()
    
    for appointment in appointments:
        # Skip cancelled appointments
        if appointment.status == "cancelled":
            continue
        
        appt_date = appointment.schedule_time.date()
        day_of_week = appointment.schedule_time.strftime("%A")
        
        # Add to daily counts
        daily_counts[appt_date] += 1
        
        # Add to day of week counts
        day_of_week_counts[day_of_week].append(daily_counts[appt_date])
    
    # Calculate average appointments per day of week
    day_of_week_averages = {}
    for day, counts in day_of_week_counts.items():
        day_of_week_averages[day] = sum(counts) / len(counts) if counts else 0
    
    # Predict future demand
    today = datetime.now().date()
    future_demand = {}
    
    for i in range(1, future_days + 1):
        future_date = today + timedelta(days=i)
        day_of_week = future_date.strftime("%A")
        
        # Use the average for this day of week
        predicted_demand = day_of_week_averages.get(day_of_week, 0)
        future_demand[future_date.strftime("%Y-%m-%d")] = round(predicted_demand, 1)
    
    return {
        "day_of_week_averages": day_of_week_averages,
        "predicted_demand": future_demand
    }

