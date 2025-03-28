"""
Tests for export utilities
"""
import unittest
import os
import sys
import tempfile
import json
import csv

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.export import export_to_csv, export_to_json, export_report

class TestExport(unittest.TestCase):
    """Test cases for export utilities"""
    
    def setUp(self):
        """Set up test environment"""
        # Create a temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()
    
    def tearDown(self):
        """Clean up after tests"""
        # Remove the temporary directory
        self.temp_dir.cleanup()
    
    def test_export_to_csv(self):
        """Test exporting data to CSV"""
        # Create test data
        data = [
            {"id": 1, "name": "John", "age": 30},
            {"id": 2, "name": "Jane", "age": 25},
            {"id": 3, "name": "Bob", "age": 40}
        ]
        
        # Export to CSV
        filename = os.path.join(self.temp_dir.name, "test.csv")
        result = export_to_csv(data, filename)
        
        # Check that the file was created
        self.assertTrue(os.path.exists(filename))
        
        # Check that the function returned the correct filename
        self.assertEqual(result, filename)
        
        # Read the CSV file and check its contents
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            
            # Check that all rows were written
            self.assertEqual(len(rows), 3)
            
            # Check that the data is correct
            self.assertEqual(int(rows[0]["id"]), 1)
            self.assertEqual(rows[0]["name"], "John")
            self.assertEqual(int(rows[0]["age"]), 30)
            
            self.assertEqual(int(rows[1]["id"]), 2)
            self.assertEqual(rows[1]["name"], "Jane")
            self.assertEqual(int(rows[1]["age"]), 25)
            
            self.assertEqual(int(rows[2]["id"]), 3)
            self.assertEqual(rows[2]["name"], "Bob")
            self.assertEqual(int(rows[2]["age"]), 40)
    
    def test_export_to_json(self):
        """Test exporting data to JSON"""
        # Create test data
        data = {
            "patients": [
                {"id": 1, "name": "John", "age": 30},
                {"id": 2, "name": "Jane", "age": 25},
                {"id": 3, "name": "Bob", "age": 40}
            ],
            "total": 3
        }
        
        # Export to JSON
        filename = os.path.join(self.temp_dir.name, "test.json")
        result = export_to_json(data, filename)
        
        # Check that the file was created
        self.assertTrue(os.path.exists(filename))
        
        # Check that the function returned the correct filename
        self.assertEqual(result, filename)
        
        # Read the JSON file and check its contents
        with open(filename, 'r') as jsonfile:
            loaded_data = json.load(jsonfile)
            
            # Check that the data is correct
            self.assertEqual(loaded_data["total"], 3)
            self.assertEqual(len(loaded_data["patients"]), 3)
            self.assertEqual(loaded_data["patients"][0]["id"], 1)
            self.assertEqual(loaded_data["patients"][0]["name"], "John")
            self.assertEqual(loaded_data["patients"][0]["age"], 30)
    
    def test_export_report(self):
        """Test exporting a report"""
        # Create test data
        data = [
            {"id": 1, "name": "John", "age": 30},
            {"id": 2, "name": "Jane", "age": 25},
            {"id": 3, "name": "Bob", "age": 40}
        ]
        
        # Export to CSV
        csv_filename = os.path.join(self.temp_dir.name, "report.csv")
        result = export_report(data, csv_filename, format_type="csv")
        
        # Check that the file was created
        self.assertTrue(os.path.exists(csv_filename))
        
        # Export to JSON
        json_filename = os.path.join(self.temp_dir.name, "report.json")
        result = export_report(data, json_filename, format_type="json")
        
        # Check that the file was created
        self.assertTrue(os.path.exists(json_filename))
        
        # Test with invalid format
        with self.assertRaises(ValueError):
            export_report(data, "invalid.xyz", format_type="xyz")

if __name__ == '__main__':
    unittest.main()

