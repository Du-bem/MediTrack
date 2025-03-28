"""
Tests for scheduling algorithms
"""
import unittest
import os
import sys
from datetime import datetime, timedelta

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.scheduling import (
    find_available_slots, optimize_doctor_schedule,
    detect_scheduling_conflicts, suggest_appointment_slots
)

class TestSchedulingAlgorithms(unittest.TestCase):
    """Test cases for scheduling algorithms"""
    
    def test_find_available_slots(self):
        """Test finding available time slots"""
        # Create test data
        class Appointment:
            def __init__(self, schedule_time, duration, status="scheduled"):
                self.schedule_time = schedule_time
                self.duration = duration
                self.status = status
        
        base_time = datetime(2023, 1, 1, 9, 0)  # 9 AM
        appointments = [
            Appointment(base_time + timedelta(hours=1), 30),  # 10:00 - 10:30
            Appointment(base_time + timedelta(hours=3), 60),  # 12:00 - 13:00
            Appointment(base_time + timedelta(hours=5), 30, "cancelled")  # 14:00 - 14:30 (cancelled)
        ]
        
        # Test finding slots
        start_time = base_time
        end_time = base_time + timedelta(hours=8)  # 9 AM to 5 PM
        slots = find_available_slots(appointments, start_time, end_time, 30, 30)
        
        # Expected available slots:
        # 9:00, 9:30, 10:30, 11:00, 11:30, 13:00, 13:30, 14:00, 14:30, 15:00, 15:30, 16:00, 16:30
        self.assertEqual(len(slots), 13)
        
        # Verify first and last slots
        self.assertEqual(slots[0], base_time)  # 9:00
        self.assertEqual(slots[-1], base_time + timedelta(hours=7, minutes=30))  # 16:30
        
        # Verify slots don't conflict with appointments
        self.assertNotIn(base_time + timedelta(hours=1), slots)  # 10:00
        self.assertNotIn(base_time + timedelta(hours=3), slots)  # 12:00
        self.assertNotIn(base_time + timedelta(hours=3, minutes=30), slots)  # 12:30
    
    def test_optimize_doctor_schedule(self):
        """Test optimizing a doctor's schedule"""
        # Create test data
        class Doctor:
            def __init__(self, id, name):
                self.id = id
                self.name = name
        
        class Appointment:
            def __init__(self, id, schedule_time, duration, status="scheduled"):
                self.id = id
                self.schedule_time = schedule_time
                self.duration = duration
                self.status = status
                self.optimization_note = None
        
        doctor = Doctor(1, "Dr. Smith")
        base_time = datetime(2023, 1, 1, 9, 0)  # 9 AM
        appointments = [
            Appointment(1, base_time, 30),  # 9:00 - 9:30
            Appointment(2, base_time + timedelta(hours=1), 30),  # 10:00 - 10:30
            Appointment(3, base_time + timedelta(hours=3), 60),  # 12:00 - 13:00
            Appointment(4, base_time + timedelta(hours=6), 30),  # 15:00 - 15:30
            Appointment(5, base_time + timedelta(hours=7), 30, "cancelled")  # 16:00 - 16:30 (cancelled)
        ]
        
        # Test optimizing schedule
        optimized = optimize_doctor_schedule(doctor, appointments, base_time.date())
        
        # Verify the number of appointments
        self.assertEqual(len(optimized), 4)  # Excluding cancelled appointment
        
        # Verify optimization notes for large gaps
        self.assertIsNotNone(optimized[1].optimization_note)  # Gap between 10:30 and 12:00
        self.assertIsNotNone(optimized[2].optimization_note)  # Gap between 13:00 and 15:00
    
    def test_detect_scheduling_conflicts(self):
        """Test detecting scheduling conflicts"""
        # Create test data
        class Appointment:
            def __init__(self, id, schedule_time, duration, status="scheduled"):
                self.id = id
                self.schedule_time = schedule_time
                self.duration = duration
                self.status = status
        
        base_time = datetime(2023, 1, 1, 9, 0)  # 9 AM
        appointments = [
            Appointment(1, base_time, 30),  # 9:00 - 9:30
            Appointment(2, base_time + timedelta(minutes=15), 30),  # 9:15 - 9:45 (conflict with #1)
            Appointment(3, base_time + timedelta(hours=1), 60),  # 10:00 - 11:00
            Appointment(4, base_time + timedelta(hours=2), 30),  # 11:00 - 11:30
            Appointment(5, base_time + timedelta(hours=2), 30, "cancelled")  # 11:00 - 11:30 (cancelled)
        ]
        
        # Test detecting conflicts
        conflicts = detect_scheduling_conflicts(appointments)
        
        # Verify conflicts
        self.assertEqual(len(conflicts), 1)
        self.assertEqual(conflicts[0][0].id, 1)
        self.assertEqual(conflicts[0][1].id, 2)
    
    def test_suggest_appointment_slots(self):
        """Test suggesting appointment slots based on preferences"""
        # Create test data
        base_time = datetime(2023, 1, 2, 9, 0)  # Monday, 9 AM
        doctor_availability = [
            base_time,  # Monday, 9 AM
            base_time + timedelta(hours=1),  # Monday, 10 AM
            base_time + timedelta(hours=2),  # Monday, 11 AM
            base_time + timedelta(days=1, hours=2),  # Tuesday, 11 AM
            base_time + timedelta(days=1, hours=3),  # Tuesday, 12 PM
            base_time + timedelta(days=2, hours=1),  # Wednesday, 10 AM
            base_time + timedelta(days=2, hours=2),  # Wednesday, 11 AM
        ]
        
        # Patient prefers mornings on Monday and Wednesday
        patient_preferences = {
            "preferred_days": ["Monday", "Wednesday"],
            "preferred_times": [(9, 12)]  # 9 AM to 12 PM
        }
        
        # Test suggesting slots
        suggested = suggest_appointment_slots(doctor_availability, patient_preferences)
        
        # Verify suggested slots
        self.assertEqual(len(suggested), 4)
        self.assertEqual(suggested[0], base_time)  # Monday, 9 AM
        self.assertEqual(suggested[1], base_time + timedelta(hours=1))  # Monday, 10 AM
        self.assertEqual(suggested[2], base_time + timedelta(hours=2))  # Monday, 11 AM
        self.assertEqual(suggested[3], base_time + timedelta(days=2, hours=1))  # Wednesday, 10 AM
        
        # Test with no matching preferences
        patient_preferences = {
            "preferred_days": ["Friday"],
            "preferred_times": [(15, 17)]  # 3 PM to 5 PM
        }
        
        suggested = suggest_appointment_slots(doctor_availability, patient_preferences)
        
        # Should return all available slots when no preferences match
        self.assertEqual(len(suggested), 7)

if __name__ == '__main__':
    unittest.main()

