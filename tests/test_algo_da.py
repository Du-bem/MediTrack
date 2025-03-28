"""
Tests for data analysis algorithms
"""
import unittest
import os
import sys
from datetime import datetime, timedelta

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.data_analysis import (
    analyze_patient_demographics, analyze_appointment_patterns,
    analyze_medical_conditions, predict_appointment_demand
)

class TestDataAnalysisAlgorithms(unittest.TestCase):
    """Test cases for data analysis algorithms"""
    
    def test_analyze_patient_demographics(self):
        """Test analyzing patient demographics"""
        # Create test data
        class Patient:
            def __init__(self, id, first_name, last_name, dob, gender=None, insurance_info=None, reg_date=None):
                self.id = id
                self.first_name = first_name
                self.last_name = last_name
                self.dob = dob
                self.gender = gender
                self.insurance_info = insurance_info
                self.reg_date = reg_date
        
        today = datetime.now().date()
        patients = [
            Patient(1, "John", "Doe", today - timedelta(days=365*5), "Male", "BlueCross Health", today - timedelta(days=30)),
            Patient(2, "Jane", "Smith", today - timedelta(days=365*15), "Female", "Aetna Insurance", today - timedelta(days=60)),
            Patient(3, "Bob", "Johnson", today - timedelta(days=365*35), "Male", "UnitedHealth Care", today - timedelta(days=90)),
            Patient(4, "Alice", "Williams", today - timedelta(days=365*70), "Female", "Medicare Plan", today - timedelta(days=120))
        ]
        
        # Test analyzing demographics
        results = analyze_patient_demographics(patients)
        
        # Verify results
        self.assertEqual(results["total_patients"], 4)
        
        # Verify age distribution
        self.assertEqual(results["age_distribution"]["0-18"]["count"], 2)
        self.assertEqual(results["age_distribution"]["19-35"]["count"], 0)
        self.assertEqual(results["age_distribution"]["36-50"]["count"], 1)
        self.assertEqual(results["age_distribution"]["51-65"]["count"], 0)
        self.assertEqual(results["age_distribution"]["66+"]["count"], 1)
        
        # Verify gender distribution
        self.assertEqual(results["gender_distribution"]["Male"]["count"], 2)
        self.assertEqual(results["gender_distribution"]["Female"]["count"], 2)
        
        # Verify insurance distribution
        self.assertEqual(len(results["insurance_distribution"]), 4)
        
        # Verify registration trends
        self.assertEqual(len(results["registration_trends"]), 4)
    
    def test_analyze_appointment_patterns(self):
        """Test analyzing appointment patterns"""
        # Create test data
        class Doctor:
            def __init__(self, id, name):
                self.id = id
                self.name = name
        
        class Appointment:
            def __init__(self, id, schedule_time, status, doctor):
                self.id = id
                self.schedule_time = schedule_time
                self.status = status
                self.doctor = doctor
        
        doctor1 = Doctor(1, "Dr. Smith")
        doctor2 = Doctor(2, "Dr. Johnson")
        
        base_time = datetime(2023, 1, 2, 9, 0)  # Monday, 9 AM
        appointments = [
            Appointment(1, base_time, "scheduled", doctor1),
            Appointment(2, base_time + timedelta(hours=1), "scheduled", doctor1),
            Appointment(3, base_time + timedelta(days=1), "completed", doctor2),
            Appointment(4, base_time + timedelta(days=2), "cancelled", doctor1),
            Appointment(5, base_time + timedelta(days=3), "no-show", doctor2)
        ]
        
        # Test analyzing patterns
        results = analyze_appointment_patterns(appointments)
        
        # Verify results
        self.assertEqual(results["total_appointments"], 5)
        
        # Verify day of week distribution
        self.assertEqual(results["days_of_week_distribution"]["Monday"], 2)
        self.assertEqual(results["days_of_week_distribution"]["Tuesday"], 1)
        self.assertEqual(results["days_of_week_distribution"]["Wednesday"], 1)
        self.assertEqual(results["days_of_week_distribution"]["Thursday"], 1)
        
        # Verify hour of day distribution
        self.assertEqual(results["hours_of_day_distribution"][9], 3)  # 3 appointments at 9 AM
        self.assertEqual(results["hours_of_day_distribution"][10], 2)  # 2 appointments at 10 AM
        
        # Verify status distribution
        self.assertEqual(results["status_distribution"]["scheduled"], 2)
        self.assertEqual(results["status_distribution"]["completed"], 1)
        self.assertEqual(results["status_distribution"]["cancelled"], 1)
        self.assertEqual(results["status_distribution"]["no-show"], 1)
        
        # Verify doctor workload
        self.assertEqual(results["top_doctors_by_workload"][1], 3)  # Doctor 1 has 3 appointments
        self.assertEqual(results["top_doctors_by_workload"][2], 2)  # Doctor 2 has 2 appointments
        
        # Verify rates
        self.assertEqual(results["cancellation_rate"], 20.0)  # 1 out of 5 appointments cancelled
        self.assertEqual(results["no_show_rate"], 20.0)  # 1 out of 5 appointments no-show
    
    def test_analyze_medical_conditions(self):
        """Test analyzing medical conditions"""
        # Create test data
        class LabTest:
            def __init__(self, test_name, is_abnormal):
                self.test_name = test_name
                self.is_abnormal = is_abnormal
        
        class MedicalRecord:
            def __init__(self, id, diagnosis, treatment_plan, lab_tests=None):
                self.id = id
                self.diagnosis = diagnosis
                self.treatment_plan = treatment_plan
                self.lab_tests = lab_tests or []
        
        records = [
            MedicalRecord(1, "Hypertension", "Medication, diet", [
                LabTest("Blood Pressure", True),
                LabTest("Cholesterol", False)
            ]),
            MedicalRecord(2, "Type 2 Diabetes", "Insulin, diet", [
                LabTest("Blood Sugar", True),
                LabTest("HbA1c", True)
            ]),
            MedicalRecord(3, "Hypertension, Obesity", "Medication, exercise", [
                LabTest("Blood Pressure", True),
                LabTest("BMI", True)
            ]),
            MedicalRecord(4, "Common Cold", "Rest, fluids", [
                LabTest("Throat Culture", False)
            ])
        ]
        
        # Test analyzing conditions
        results = analyze_medical_conditions(records)
        
        # Verify results
        self.assertEqual(results["total_records"], 4)
        
        # Verify top diagnoses
        self.assertEqual(results["top_diagnoses"]["Hypertension"], 2)
        self.assertEqual(results["top_diagnoses"]["Type 2 Diabetes"], 1)
        self.assertEqual(results["top_diagnoses"]["Obesity"], 1)
        self.assertEqual(results["top_diagnoses"]["Common Cold"], 1)
        
        # Verify top treatments
        self.assertEqual(results["top_treatments"]["Medication"], 2)
        self.assertEqual(results["top_treatments"]["diet"], 2)
        self.assertEqual(results["top_treatments"]["exercise"], 1)
        self.assertEqual(results["top_treatments"]["Rest"], 1)
        
        # Verify top abnormal tests
        self.assertEqual(results["top_abnormal_tests"]["Blood Pressure"], 2)
        self.assertEqual(results["top_abnormal_tests"]["Blood Sugar"], 1)
        self.assertEqual(results["top_abnormal_tests"]["HbA1c"], 1)
        self.assertEqual(results["top_abnormal_tests"]["BMI"], 1)
    
    def test_predict_appointment_demand(self):
        """Test predicting appointment demand"""
        # Create test data
        class Appointment:
            def __init__(self, id, schedule_time, status="scheduled"):
                self.id = id
                self.schedule_time = schedule_time
                self.status = status
        
        # Create appointments for 3 weeks
        base_date = datetime.now().date() - timedelta(days=21)
        appointments = []
        
        # Monday: 5 appointments each week
        for week in range(3):
            day = base_date + timedelta(days=week*7)
            for i in range(5):
                appointments.append(Appointment(len(appointments)+1, datetime.combine(day, datetime.min.time())))
        
        # Tuesday: 3 appointments each week
        for week in range(3):
            day = base_date + timedelta(days=week*7+1)
            for i in range(3):
                appointments.append(Appointment(len(appointments)+1, datetime.combine(day, datetime.min.time())))
        
        # Wednesday: 4 appointments each week
        for week in range(3):
            day = base_date + timedelta(days=week*7+2)
            for i in range(4):
                appointments.append(Appointment(len(appointments)+1, datetime.combine(day, datetime.min.time())))
        
        # Test predicting demand
        results = predict_appointment_demand(appointments, future_days=7)
        
        # Verify day of week averages
        self.assertEqual(results["day_of_week_averages"]["Monday"], 5.0)
        self.assertEqual(results["day_of_week_averages"]["Tuesday"], 3.0)
        self.assertEqual(results["day_of_week_averages"]["Wednesday"], 4.0)
        
        # Verify predicted demand
        self.assertEqual(len(results["predicted_demand"]), 7)
        
        # Get the day of week for the first prediction day
        first_day = datetime.now().date() + timedelta(days=1)
        day_of_week = first_day.strftime("%A")
        
        # Verify the prediction for that day
        if day_of_week == "Monday":
            self.assertEqual(results["predicted_demand"][first_day.strftime("%Y-%m-%d")], 5.0)
        elif day_of_week == "Tuesday":
            self.assertEqual(results["predicted_demand"][first_day.strftime("%Y-%m-%d")], 3.0)
        elif day_of_week == "Wednesday":
            self.assertEqual(results["predicted_demand"][first_day.strftime("%Y-%m-%d")], 4.0)

if __name__ == '__main__':
    unittest.main()

