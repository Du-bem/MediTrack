"""
Export utilities for MediTrack
"""
import csv
import json
import os
import logging

logger = logging.getLogger(__name__)

def export_to_csv(data, filename, headers=None):
    """
    Export data to CSV file
    
    Args:
        data: List of dictionaries or objects with to_dict method
        filename: Output filename
        headers: Optional list of column headers
    
    Returns:
        Path to the exported file
    """
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
        
        # Convert objects to dictionaries if needed
        if data and hasattr(data[0], 'to_dict'):
            data = [item.to_dict() for item in data]
        
        # Determine headers if not provided
        if not headers and data:
            headers = list(data[0].keys())
        
        # Write to CSV
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
        
        logger.info(f"Data exported to CSV: {filename}")
        return filename
    
    except Exception as e:
        logger.error(f"Error exporting to CSV: {e}")
        raise

def export_to_json(data, filename, indent=2):
    """
    Export data to JSON file
    
    Args:
        data: Data to export
        filename: Output filename
        indent: JSON indentation level
    
    Returns:
        Path to the exported file
    """
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
        
        # Convert objects to dictionaries if needed
        if isinstance(data, list) and data and hasattr(data[0], 'to_dict'):
            data = [item.to_dict() for item in data]
        elif hasattr(data, 'to_dict'):
            data = data.to_dict()
        
        # Write to JSON
        with open(filename, 'w') as jsonfile:
            json.dump(data, jsonfile, indent=indent, default=str)
        
        logger.info(f"Data exported to JSON: {filename}")
        return filename
    
    except Exception as e:
        logger.error(f"Error exporting to JSON: {e}")
        raise

def export_to_pdf(data, filename, title=None, headers=None):
    """
    Export data to PDF file
    
    Args:
        data: List of dictionaries or objects with to_dict method
        filename: Output filename
        title: Optional title for the PDF
        headers: Optional list of column headers
    
    Returns:
        Path to the exported file
    """
    try:
        # Check if ReportLab is installed
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib import colors
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
        except ImportError:
            logger.error("ReportLab is required for PDF export. Install it with 'pip install reportlab'")
            raise ImportError("ReportLab is required for PDF export")
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
        
        # Convert objects to dictionaries if needed
        if data and hasattr(data[0], 'to_dict'):
            data = [item.to_dict() for item in data]
        
        # Determine headers if not provided
        if not headers and data:
            headers = list(data[0].keys())
        
        # Create the PDF document
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []
        
        # Add title if provided
        if title:
            elements.append(Paragraph(title, styles['Title']))
            elements.append(Spacer(1, 12))
        
        # Create table data
        table_data = [headers]  # Header row
        for item in data:
            row = [str(item.get(field, '')) for field in headers]
            table_data.append(row)
        
        # Create the table
        table = Table(table_data)
        
        # Add style to the table
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])
        table.setStyle(style)
        
        elements.append(table)
        
        # Build the PDF
        doc.build(elements)
        
        logger.info(f"Data exported to PDF: {filename}")
        return filename
    
    except Exception as e:
        logger.error(f"Error exporting to PDF: {e}")
        raise

def export_report(data, filename, format_type="csv", title=None, headers=None):
    """
    Export data to a report file in the specified format
    
    Args:
        data: Data to export
        filename: Output filename
        format_type: Format type (csv, json, pdf)
        title: Optional title for the report
        headers: Optional list of column headers
    
    Returns:
        Path to the exported file
    """
    # Determine the export function based on format type
    if format_type.lower() == "csv":
        return export_to_csv(data, filename, headers)
    elif format_type.lower() == "json":
        return export_to_json(data, filename)
    elif format_type.lower() == "pdf":
        return export_to_pdf(data, filename, title, headers)
    else:
        raise ValueError(f"Unsupported format type: {format_type}")

