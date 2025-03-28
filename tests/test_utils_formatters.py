"""
Tests for formatting utilities
"""
import unittest
import os
import sys
from datetime import datetime, date

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.formatters import (
    format_date, format_datetime, format_phone, format_name,
    format_address, format_currency, format_percentage,
    format_duration, format_table, format_json
)

class TestFormatters(unittest.TestCase):
    """Test cases for formatters"""
    
    def test_format_date(self):
        """Test date formatting"""
        # Test with date object
        test_date = date(2023, 1, 15)
        self.assertEqual(format_date(test_date), "2023-01-15")
        self.assertEqual(format_date(test_date, format="%m/%d/%Y"), "01/15/2023")
        
        # Test with datetime object
        test_datetime = datetime(2023, 1, 15, 12, 30)
        self.assertEqual(format_date(test_datetime), "2023-01-15")
        
        # Test with string
        self.assertEqual(format_date("2023-01-15"), "2023-01-15")
    
    def test_format_datetime(self):
        """Test datetime formatting"""
        # Test with datetime object
        test_datetime = datetime(2023, 1, 15, 12, 30)
        self.assertEqual(format_datetime(test_datetime), "2023-01-15 12:30")
        self.assertEqual(format_datetime(test_datetime, format="%m/%d/%Y %I:%M %p"), "01/15/2023 12:30 PM")
        
        # Test with string
        self.assertEqual(format_datetime("2023-01-15 12:30"), "2023-01-15 12:30")
    
    def test_format_phone(self):
        """Test phone formatting"""
        # Test with 10-digit number
        self.assertEqual(format_phone("5551234567"), "(555) 123-4567")
        
        # Test with formatted number
        self.assertEqual(format_phone("555-123-4567"), "(555) 123-4567")
        
        # Test with country code
        self.assertEqual(format_phone("15551234567"), "+1 (555) 123-4567")
        
        # Test with non-standard format
        self.assertEqual(format_phone("12345"), "12345")  # Returns as is
    
    def test_format_name(self):
        """Test name formatting"""
        # Test without title
        self.assertEqual(format_name("John", "Doe"), "John Doe")
        
        # Test with title
        self.assertEqual(format_name("John", "Doe", include_title=True, title="Dr."), "Dr. John Doe")
        
        # Test with title flag but no title
        self.assertEqual(format_name("John", "Doe", include_title=True), "John Doe")
    
    def test_format_address(self):
        """Test address formatting"""
        # Test with dictionary
        address_dict = {
            "street": "123 Main St",
            "city": "Anytown",
            "state": "CA",
            "zip": "12345"
        }
        self.assertEqual(format_address(address_dict), "123 Main St, Anytown, CA, 12345")
        
        # Test with string
        self.assertEqual(format_address("123 Main St, Anytown, CA 12345"), "123 Main St, Anytown, CA 12345")
    
    def test_format_currency(self):
        """Test currency formatting"""
        # Test with integer
        self.assertEqual(format_currency(100), "$100.00")
        
        # Test with float
        self.assertEqual(format_currency(99.99), "$99.99")
        
        # Test with different currency symbol
        self.assertEqual(format_currency(100, currency="€"), "€100.00")
    
    def test_format_percentage(self):
        """Test percentage formatting"""
        # Test with integer
        self.assertEqual(format_percentage(75), "75.0%")
        
        # Test with float
        self.assertEqual(format_percentage(75.5), "75.5%")
        
        # Test with different decimal places
        self.assertEqual(format_percentage(75.5, decimal_places=2), "75.50%")
        self.assertEqual(format_percentage(75.5, decimal_places=0), "76%")
    
    def test_format_duration(self):
        """Test duration formatting"""
        # Test with minutes less than an hour
        self.assertEqual(format_duration(30), "30 minutes")
        
        # Test with exactly one hour
        self.assertEqual(format_duration(60), "1 hour")
        
        # Test with multiple hours
        self.assertEqual(format_duration(120), "2 hours")
        
        # Test with hours and minutes
        self.assertEqual(format_duration(90), "1 hour 30 minutes")
        self.assertEqual(format_duration(150), "2 hours 30 minutes")
    
    def test_format_table(self):
        """Test table formatting"""
        # Test with list of dictionaries
        data = [
            {"id": 1, "name": "John", "age": 30},
            {"id": 2, "name": "Jane", "age": 25},
            {"id": 3, "name": "Bob", "age": 40}
        ]
        
        table = format_table(data)
        
        # Check that the table contains all the data
        self.assertIn("id", table)
        self.assertIn("name", table)
        self.assertIn("age", table)
        self.assertIn("John", table)
        self.assertIn("Jane", table)
        self.assertIn("Bob", table)
        self.assertIn("30", table)
        self.assertIn("25", table)
        self.assertIn("40", table)
        
        # Test with list of lists and custom headers
        data = [
            [1, "John", 30],
            [2, "Jane", 25],
            [3, "Bob", 40]
        ]
        
        headers = ["ID", "Name", "Age"]
        
        table = format_table(data, headers=headers)
        
        # Check that the table contains all the data
        self.assertIn("ID", table)
        self.assertIn("Name", table)
        self.assertIn("Age", table)
        self.assertIn("John", table)
        self.assertIn("Jane", table)
        self.assertIn("Bob", table)
        self.assertIn("30", table)
        self.assertIn("25", table)
        self.assertIn("40", table)
    
    def test_format_json(self):
        """Test JSON formatting"""
        # Test with dictionary
        data = {
            "id": 1,
            "name": "John",
            "age": 30,
            "address": {
                "street": "123 Main St",
                "city": "Anytown"
            }
        }
        
        json_str = format_json(data)
        
        # Check that the JSON string contains all the data
        self.assertIn('"id": 1', json_str)
        self.assertIn('"name": "John"', json_str)
        self.assertIn('"age": 30', json_str)
        self.assertIn('"street": "123 Main St"', json_str)
        self.assertIn('"city": "Anytown"', json_str)
        
        # Test with object that has to_dict method
        class Person:
            def __init__(self, id, name, age):
                self.id = id
                self.name = name
                self.age = age
            
            def to_dict(self):
                return {
                    "id": self.id,
                    "name": self.name,
                    "age": self.age
                }
        
        person = Person(1, "John", 30)
        json_str = format_json(person)
        
        # Check that the JSON string contains all the data
        self.assertIn('"id": 1', json_str)
        self.assertIn('"name": "John"', json_str)
        self.assertIn('"age": 30', json_str)

if __name__ == '__main__':
    unittest.main()

