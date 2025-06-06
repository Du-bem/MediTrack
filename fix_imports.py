"""
Helper module to fix import issues
Add this to the beginning of scripts that have import problems
"""
import os
import sys

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

