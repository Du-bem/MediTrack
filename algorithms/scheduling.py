"""
Scheduling algorithms for MediTrack
"""
from datetime import datetime, timedelta

def find_available_slots(appointments, start_time, end_time, duration, interval=30):
    """
    Find available time slots within a time range
    
    Args:
        appointments: List of existing appointments
        start_time: Start of the time range
        end_time: End of the time range
        duration: Duration of the appointment in minutes
        interval: Interval between slots in minutes
        
    Returns:
        List of available time slots
    """
    # Convert string times to datetime if needed
    if isinstance(start_time, str):
        start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
    if isinstance(end_time, str):
        end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M")
    
    # Generate all possible time slots
    all_slots = []
    current_time = start_time
    
    while current_time + timedelta(minutes=duration) <= end_time:
        all_slots.append(current_time)
        current_time += timedelta(minutes=interval)
    
    # Filter out slots that conflict with existing appointments
    available_slots = []
    
    for slot in all_slots:
        slot_end = slot + timedelta(minutes=duration)
        is_available = True
        
        for appointment in appointments:
            # Skip cancelled appointments
            if hasattr(appointment, 'status') and appointment.status == "cancelled":
                continue
            
            # Get appointment times
            appt_start = appointment.schedule_time
            appt_end = appt_start + timedelta(minutes=appointment.duration)
            
            # Check for overlap
            if (slot < appt_end and slot_end > appt_start):
                is_available = False
                break
        
        if is_available:
            available_slots.append(slot)
    
    return available_slots

def optimize_doctor_schedule(doctor, appointments, date):
    """
    Optimize a doctor's schedule for a specific date
    
    Args:
        doctor: Doctor object
        appointments: List of appointments for the doctor
        date: The date to optimize
        
    Returns:
        Optimized list of appointments
    """
    # Filter appointments for the specified date
    if isinstance(date, str):
        date = datetime.strptime(date, "%Y-%m-%d").date()
    
    date_appointments = [
        a for a in appointments 
        if a.schedule_time.date() == date and a.status != "cancelled"
    ]
    
    # Sort appointments by time
    date_appointments.sort(key=lambda a: a.schedule_time)
    
    # Identify gaps and potential optimizations
    optimized_appointments = []
    
    for i in range(len(date_appointments)):
        current_appt = date_appointments[i]
        optimized_appointments.append(current_appt)
        
        # If not the last appointment, check for large gaps
        if i < len(date_appointments) - 1:
            next_appt = date_appointments[i + 1]
            current_end = current_appt.schedule_time + timedelta(minutes=current_appt.duration)
            gap = (next_appt.schedule_time - current_end).total_seconds() / 60
            
            # If gap is larger than 30 minutes, suggest optimization
            if gap > 30:
                # This is where you would implement logic to suggest moving appointments
                # For now, we'll just flag it
                current_appt.optimization_note = f"Large gap of {gap} minutes before next appointment"
    
    return optimized_appointments

def detect_scheduling_conflicts(appointments):
    """
    Detect conflicts in a list of appointments
    
    Args:
        appointments: List of appointment objects
        
    Returns:
        List of conflicting appointment pairs
    """
    conflicts = []
    
    # Sort appointments by time
    sorted_appointments = sorted(appointments, key=lambda a: a.schedule_time)
    
    # Check for overlaps
    for i in range(len(sorted_appointments)):
        appt1 = sorted_appointments[i]
        
        # Skip cancelled appointments
        if appt1.status == "cancelled":
            continue
        
        appt1_end = appt1.schedule_time + timedelta(minutes=appt1.duration)
        
        for j in range(i + 1, len(sorted_appointments)):
            appt2 = sorted_appointments[j]
            
            # Skip cancelled appointments
            if appt2.status == "cancelled":
                continue
            
            # If appt2 starts after appt1 ends, no need to check further
            if appt2.schedule_time >= appt1_end:
                break
            
            # If we're here, there's a conflict
            conflicts.append((appt1, appt2))
    
    return conflicts

def suggest_appointment_slots(doctor_availability, patient_preferences, duration=30):
    """
    Suggest appointment slots based on doctor availability and patient preferences
    
    Args:
        doctor_availability: List of available time slots for the doctor
        patient_preferences: Dictionary of patient preferences
        duration: Duration of the appointment in minutes
        
    Returns:
        List of suggested time slots
    """
    suggested_slots = []
    
    # Extract patient preferences
    preferred_days = patient_preferences.get('preferred_days', [])
    preferred_times = patient_preferences.get('preferred_times', [])
    
    # Filter available slots based on patient preferences
    for slot in doctor_availability:
        slot_day = slot.strftime("%A")
        slot_hour = slot.hour
        
        # Check if slot matches patient preferences
        day_match = not preferred_days or slot_day in preferred_days
        time_match = not preferred_times or any(start <= slot_hour < end for start, end in preferred_times)
        
        if day_match and time_match:
            suggested_slots.append(slot)
    
    # If no slots match preferences, return all available slots
    if not suggested_slots and doctor_availability:
        return doctor_availability
    
    return suggested_slots

