"""
Tests for CLI command parser
"""
import unittest
import os
import sys

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cli.cmd_parser import parse_command

class TestCommandParser(unittest.TestCase):
    """Test cases for command parser"""
    
    def test_parse_simple_command(self):
        """Test parsing a simple command"""
        command = "patient list"
        entity, action, args_with_options = parse_command(command)
        
        self.assertEqual(entity, "patient")
        self.assertEqual(action, "list")
        self.assertEqual(args_with_options["args"], [])
        self.assertEqual(args_with_options["options"], {})
    
    def test_parse_command_with_args(self):
        """Test parsing a command with arguments"""
        command = 'patient add "John" "Doe" "01/15/1985" "john@example.com" "555-123-4567"'
        entity, action, args_with_options = parse_command(command)
        
        self.assertEqual(entity, "patient")
        self.assertEqual(action, "add")
        self.assertEqual(args_with_options["args"], ["John", "Doe", "01/15/1985", "john@example.com", "555-123-4567"])
        self.assertEqual(args_with_options["options"], {})
    
    def test_parse_command_with_options(self):
        """Test parsing a command with options"""
        command = 'appointment list --doctor="Smith" --date="2023-12-01"'
        entity, action, args_with_options = parse_command(command)
        
        self.assertEqual(entity, "appointment")
        self.assertEqual(action, "list")
        self.assertEqual(args_with_options["args"], [])
        self.assertEqual(args_with_options["options"], {"doctor": "Smith", "date": "2023-12-01"})
    
    def test_parse_command_with_args_and_options(self):
        """Test parsing a command with both arguments and options"""
        command = 'patient search "Doe" --limit=10 --offset=0'
        entity, action, args_with_options = parse_command(command)
        
        self.assertEqual(entity, "patient")
        self.assertEqual(action, "search")
        self.assertEqual(args_with_options["args"], ["Doe"])
        self.assertEqual(args_with_options["options"], {"limit": "10", "offset": "0"})
    
    def test_parse_command_with_boolean_option(self):
        """Test parsing a command with a boolean option"""
        command = 'report export --type="patients" --format="csv" --output="patients.csv" --include-inactive'
        entity, action, args_with_options = parse_command(command)
        
        self.assertEqual(entity, "report")
        self.assertEqual(action, "export")
        self.assertEqual(args_with_options["args"], [])
        self.assertEqual(args_with_options["options"]["include-inactive"], True)
    
    def test_parse_empty_command(self):
        """Test parsing an empty command"""
        command = ""
        entity, action, args_with_options = parse_command(command)
        
        self.assertIsNone(entity)
        self.assertIsNone(action)
        self.assertEqual(args_with_options, [])
    
    def test_parse_invalid_command(self):
        """Test parsing an invalid command"""
        command = "invalid command with no proper structure"
        entity, action, args_with_options = parse_command(command)
        
        self.assertEqual(entity, "invalid")
        self.assertEqual(action, "command")
        self.assertEqual(args_with_options["args"], ["with", "no", "proper", "structure"])

if __name__ == '__main__':
    unittest.main()

