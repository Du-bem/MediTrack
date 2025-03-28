"""
Tests for search algorithms
"""
import unittest
import os
import sys
from datetime import datetime, timedelta

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.search import (
    fuzzy_search, binary_search, search_by_regex,
    search_appointments_by_date_range, search_patients_by_age_range
)

class TestSearchAlgorithms(unittest.TestCase):
    """Test cases for search algorithms"""
    
    def test_fuzzy_search(self):
        """Test fuzzy search algorithm"""
        # Create test data
        class Person:
            def __init__(self, name, email):
                self.name = name
                self.email = email
        
        people = [
            Person("John Doe", "john.doe@example.com"),
            Person("Jane Smith", "jane.smith@example.com"),
            Person("John Smith", "john.smith@example.com"),
            Person("Jane Doe", "jane.doe@example.com")
        ]
        
        # Test exact match
        results = fuzzy_search(people, "John Doe", ["name"])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "John Doe")
        
        # Test partial match
        results = fuzzy_search(people, "John", ["name"])
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].name, "John Doe")
        self.assertEqual(results[1].name, "John Smith")
        
        # Test fuzzy match
        results = fuzzy_search(people, "Jon", ["name"], threshold=0.5)
        self.assertEqual(len(results), 2)
        
        # Test multiple fields
        results = fuzzy_search(people, "john.smith", ["name", "email"])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "John Smith")
    
    def test_binary_search(self):
        """Test binary search algorithm"""
        # Create sorted test data
        numbers = [1, 3, 5, 7, 9, 11, 13, 15]
        
        # Test finding an existing item
        result = binary_search(numbers, 7)
        self.assertEqual(result, 7)
        
        # Test finding a non-existing item
        result = binary_search(numbers, 8)
        self.assertIsNone(result)
        
        # Test with custom key function
        class Person:
            def __init__(self, id, name):
                self.id = id
                self.name = name
        
        people = [
            Person(1, "Alice"),
            Person(2, "Bob"),
            Person(3, "Charlie"),
            Person(4, "David"),
            Person(5, "Eve")
        ]
        
        result = binary_search(people, 3, key_func=lambda p: p.id)
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "Charlie")
        
        result = binary_search(people, 6, key_func=lambda p: p.id)
        self.assertIsNone(result)
    
    def test_search_by_regex(self):
        """Test regex search algorithm"""
        # Create test data
        class Person:
            def __init__(self, name, email, phone):
                self.name = name
                self.email = email
                self.phone = phone
        
        people = [
            Person("John Doe", "john.doe@example.com", "555-123-4567"),
            Person("Jane Smith", "jane.smith@example.com", "555-987-6543"),
            Person("John Smith", "john.smith@example.com", "555-456-7890"),
            Person("Jane Doe", "jane.doe@example.com", "555-654-3210")
        ]
        
        # Test simple pattern
        results = search_by_regex(people, "John", ["name"])
        self.assertEqual(len(results), 2)
        
        # Test email pattern
        results = search_by_regex(people, r"john\.[a-z]+@example\.com", ["email"])
        self.assertEqual(len(results), 2)
        
        # Test phone pattern
        results = search_by_regex(people, r"555-\d{3}-\d{4}", ["phone"])
        self.assertEqual(len(results), 4)
        
        # Test specific phone pattern
        results = search_by_regex(people, r"555-123-\d{4}", ["phone"])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "John Doe")
    
    def test_search_appointments_by_date_range(self):
        """Test appointment date range search"""
        # Create test data
        class Appointment:
            def __init__(self, id, schedule_time):
                self.id = id
                self.schedule_time = schedule_time
        
        base_date = datetime(2023, 1, 1)
        appointments = [
            Appointment(1, base_date),
            Appointment(2, base_date + timedelta(days=1)),
            Appointment(3, base_date + timedelta(days=2)),
            Appointment(4, base_date + timedelta(days=3)),
            Appointment(5, base_date + timedelta(days=4))
        ]
        
        # Test exact date range
        results = search_appointments_by_date_range(
            appointments, 
            base_date.date(), 
            base_date.date()
        )
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, 1)
        
        # Test date range spanning multiple days
        results = search_appointments_by_date_range(
            appointments, 
            base_date.date(), 
            (base_date + timedelta(days=2)).date()
        )
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0].id, 1)
        self.assertEqual(results[1].id, 2)
        self.assertEqual(results[2].id, 3)
        
        # Test date range with no appointments
        results = search_appointments_by_date_range(
            appointments, 
            (base_date - timedelta(days=2)).date(), 
            (base_date - timedelta(days=1)).date()
        )
        self.assertEqual(len(results), 0)
    
    def test_search_patients_by_age_range(self):
        """Test patient age range search"""
        # Create test data
        class Patient:
            def __init__(self, id, name, dob):
                self.id = id
                self.name = name
                self.dob = dob
        
        today = datetime.now().date()
        patients = [
            Patient(1, "Child", today - timedelta(days=365*5)),  # 5 years old
            Patient(2, "Teen", today - timedelta(days=365*15)),  # 15 years old
            Patient(3, "Adult", today - timedelta(days=365*35)),  # 35 years old
            Patient(4, "Senior", today - timedelta(days=365*70))  # 70 years old
        ]
        
        # Test specific age range
        results = search_patients_by_age_range(patients, 10, 20)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Teen")
        
        # Test broader age range
        results = search_patients_by_age_range(patients, 0, 18)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].name, "Child")
        self.assertEqual(results[1].name, "Teen")
        
        # Test adult age range
        results = search_patients_by_age_range(patients, 18, 65)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Adult")
        
        # Test senior age range
        results = search_patients_by_age_range(patients, 65, 100)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Senior")

if __name__ == '__main__':
    unittest.main()

