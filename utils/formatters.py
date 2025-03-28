"""
Formatting utilities for MediTrack
"""
from datetime import datetime, date
import json

def format_date(date_obj, format="%Y-%m-%d"):
    """Format a date object to string"""
    if isinstance(date_obj, date):
        return date_obj.strftime(format)
    return str(date_obj)

def format_datetime(datetime_obj, format="%Y-%m-%d %H:%M"):
    """Format a datetime object to string"""
    if isinstance(datetime_obj, datetime):
        return datetime_obj.strftime(format)
    return str(datetime_obj)

def format_phone(phone):
    """Format a phone number to a consistent format"""
    # Remove all non-digit characters
    digits = ''.join(filter(str.isdigit, phone))
    
    # Format based on length
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    else:
        return phone  # Return as is if we can't format it

def format_name(first_name, last_name, include_title=False, title=None):
    """Format a name with optional title"""
    if include_title and title:
        return f"{title} {first_name} {last_name}"
    return f"{first_name} {last_name}"

def format_address(address_parts):
    """Format address parts into a single string"""
    if isinstance(address_parts, dict):
        # If address is a dictionary with parts
        parts = []
        if 'street' in address_parts:
            parts.append(address_parts['street'])
        if 'city' in address_parts and 'state' in address_parts:
            parts.append(f"{address_parts['city']}, {address_parts['state']}")
        if 'zip' in address_parts:
            parts.append(address_parts['zip'])
        
        return ", ".join(parts)
    else:
        # If address is already a string
        return str(address_parts)

def format_currency(amount, currency="$"):
    """Format a number as currency"""
    return f"{currency}{amount:.2f}"

def format_percentage(value, decimal_places=1):
    """Format a number as percentage"""
    return f"{value:.{decimal_places}f}%"

def format_duration(minutes):
    """Format minutes into a human-readable duration"""
    if minutes < 60:
        return f"{minutes} minutes"
    else:
        hours = minutes // 60
        mins = minutes % 60
        if mins == 0:
            return f"{hours} hour{'s' if hours > 1 else ''}"
        else:
            return f"{hours} hour{'s' if hours > 1 else ''} {mins} minute{'s' if mins > 1 else ''}"

def format_table(data, headers=None, alignment=None):
    """Format data as a text table"""
    if not data:
        return "No data to display"
    
    # If data is a list of dictionaries, extract headers and rows
    if isinstance(data[0], dict):
        if not headers:
            headers = list(data[0].keys())
        rows = [[str(item.get(header, '')) for header in headers] for item in data]
    else:
        # Assume data is a list of lists
        rows = [[str(cell) for cell in row] for row in data]
        if not headers:
            headers = [f"Column {i+1}" for i in range(len(rows[0]))]
    
    # Determine column widths
    col_widths = [max(len(str(headers[i])), max(len(row[i]) for row in rows)) for i in range(len(headers))]
    
    # Set default alignment if not provided
    if not alignment:
        alignment = ['<'] * len(headers)  # Left-align by default
    
    # Create the header row
    header_row = ' | '.join(f"{headers[i]:{alignment[i]}{col_widths[i]}}" for i in range(len(headers)))
    separator = '-+-'.join('-' * width for width in col_widths)
    
    # Create the data rows
    data_rows = [' | '.join(f"{row[i]:{alignment[i]}{col_widths[i]}}" for i in range(len(row))) for row in rows]
    
    # Combine all parts
    table = [header_row, separator] + data_rows
    
    return '\n'.join(table)

def format_json(data, indent=2):
    """Format data as JSON string"""
    if hasattr(data, 'to_dict'):
        data = data.to_dict()
    return json.dumps(data, indent=indent, default=str)

