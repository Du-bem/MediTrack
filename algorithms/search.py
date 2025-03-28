"""
Search algorithms for MediTrack
"""
import re
from datetime import datetime, timedelta

def fuzzy_search(items, search_term, fields, threshold=0.6):
    """
    Perform a fuzzy search on a list of items
    
    Args:
        items: List of objects to search through
        search_term: The term to search for
        fields: List of field names to search in
        threshold: Similarity threshold (0-1)
        
    Returns:
        List of matching items sorted by relevance
    """
    import difflib
    
    if not search_term:
        return items
    
    search_term = search_term.lower()
    results = []
    
    for item in items:
        max_ratio = 0
        
        for field in fields:
            if hasattr(item, field):
                field_value = str(getattr(item, field)).lower()
                
                # Check for exact substring match first
                if search_term in field_value:
                    ratio = 1.0
                else:
                    # Use difflib for fuzzy matching
                    ratio = difflib.SequenceMatcher(None, search_term, field_value).ratio()
                
                max_ratio = max(max_ratio, ratio)
        
        if max_ratio >= threshold:
            results.append((item, max_ratio))
    
    # Sort by relevance (highest ratio first)
    results.sort(key=lambda x: x[1], reverse=True)
    
    # Return just the items
    return [item for item, ratio in results]

def binary_search(sorted_items, key, key_func=None):
    """
    Perform a binary search on a sorted list of items
    
    Args:
        sorted_items: Sorted list of items
        key: The key to search for
        key_func: Function to extract the key from an item (default: identity)
        
    Returns:
        The found item or None
    """
    if not sorted_items:
        return None
    
    if key_func is None:
        key_func = lambda x: x
    
    left = 0
    right = len(sorted_items) - 1
    
    while left <= right:
        mid = (left + right) // 2
        mid_key = key_func(sorted_items[mid])
        
        if mid_key == key:
            return sorted_items[mid]
        elif mid_key < key:
            left = mid + 1
        else:
            right = mid - 1
    
    return None

def search_by_regex(items, pattern, fields):
    """
    Search items using regular expressions
    
    Args:
        items: List of objects to search through
        pattern: Regular expression pattern
        fields: List of field names to search in
        
    Returns:
        List of matching items
    """
    try:
        regex = re.compile(pattern, re.IGNORECASE)
        results = []
        
        for item in items:
            for field in fields:
                if hasattr(item, field):
                    field_value = str(getattr(item, field))
                    
                    if regex.search(field_value):
                        results.append(item)
                        break  # Break to avoid adding the same item multiple times
        
        return results
    except re.error:
        # If the pattern is invalid, fall back to simple substring search
        return [item for item in items if any(
            hasattr(item, field) and pattern.lower() in str(getattr(item, field)).lower() 
            for field in fields
        )]

def search_appointments_by_date_range(appointments, start_date, end_date):
    """
    Search appointments within a date range
    
    Args:
        appointments: List of appointment objects
        start_date: Start date (inclusive)
        end_date: End date (inclusive)
        
    Returns:
        List of matching appointments
    """
    # Convert string dates to datetime if needed
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    
    # Ensure we're comparing dates, not datetimes
    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.max.time())
    
    return [
        appointment for appointment in appointments
        if start_datetime <= appointment.schedule_time <= end_datetime
    ]

def search_patients_by_age_range(patients, min_age, max_age):
    """
    Search patients within an age range
    
    Args:
        patients: List of patient objects
        min_age: Minimum age (inclusive)
        max_age: Maximum age (inclusive)
        
    Returns:
        List of matching patients
    """
    today = datetime.now().date()
    
    def calculate_age(dob):
        """Calculate age from date of birth"""
        age = today.year - dob.year
        if (today.month, today.day) < (dob.month, dob.day):
            age -= 1
        return age
    
    return [
        patient for patient in patients
        if min_age <= calculate_age(patient.dob) <= max_age
    ]

