#!/usr/bin/env python3
"""
MediTrack - Healthcare Management System
Main entry point for the CLI application
"""
import sys
import logging
from config import setup_logging, load_config
from cli.cmd_parser import parse_command
from cli.cmd_executor import execute_command

def main():
    """Main entry point for the MediTrack CLI application"""
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting MediTrack Healthcare Management System")
    
    # Load configuration
    config = load_config()
    
    # Check if running in interactive mode or with command line arguments
    if len(sys.argv) > 1:
        # Command provided as command line arguments
        command_string = " ".join(sys.argv[1:])
        try:
            entity, action, args = parse_command(command_string)
            if entity and action:
                execute_command(entity, action, args, config)
            else:
                print("Invalid command format. Type 'help' for available commands.")
        except Exception as e:
            logger.error(f"Error executing command: {e}")
            print(f"Error: {e}")
    else:
        # Interactive mode
        print("Welcome to MediTrack Healthcare Management System")
        print("Type 'help' for available commands or 'exit' to quit")
        
        while True:
            try:
                command_string = input("MediTrack> ").strip()
                
                if command_string.lower() == "exit":
                    print("Exiting MediTrack. Goodbye!")
                    break
                elif command_string.lower() == "help":
                    show_help()
                elif command_string:
                    entity, action, args = parse_command(command_string)
                    if entity and action:
                        execute_command(entity, action, args, config)
                    else:
                        print("Invalid command format. Type 'help' for available commands.")
            except KeyboardInterrupt:
                print("\nExiting MediTrack. Goodbye!")
                break
            except Exception as e:
                logger.error(f"Error: {e}")
                print(f"Error: {e}")

def show_help():
    """Display help information for available commands"""
    print("\nAvailable Commands:")
    print("------------------")
    print("patient add <firstName> <lastName> <dob> <email> <phone> [address] [insuranceInfo]")
    print("patient search <searchTerm>")
    print("patient update <patientId> <field> <value>")
    print("patient list [--limit=<n>] [--offset=<n>]")
    print("patient view <patientId>")
    
    print("\ndoctor add <firstName> <lastName> <dob> <email> <phone> <specialisation> <licenseNumber>")
    print("doctor search <searchTerm>")
    print("doctor list [--department=<dept>] [--specialisation=<spec>]")
    
    print("\nappointment add <patientId> <doctorId> <dateTime> <duration> [notes]")
    print("appointment list [--doctor=<doctorId>] [--patient=<patientId>] [--date=<date>] [--status=<status>]")
    print("appointment update <appointmentId> <field> <value>")
    print("appointment cancel <appointmentId> [reason]")
    print("appointment reschedule <appointmentId> <newDateTime>")
    
    print("\nmedicalrecord add <patientId> <diagnosis> <treatmentPlan> [notes]")
    print("medicalrecord view <recordId>")
    print("medicalrecord list <patientId>")
    print("medicalrecord update <recordId> <field> <value>")
    
    print("\nprescription add <recordId> <medication> <dosage> <frequency> <startDate> <endDate> [instructions]")
    print("prescription list <recordId>")
    print("prescription update <prescriptionId> <field> <value>")
    print("prescription refill <prescriptionId> <newEndDate>")
    
    print("\nlabtest add <recordId> <testName> <testType> <orderedDate>")
    print("labtest result <testId> <resultDate> <result> <referenceRange> <isAbnormal>")
    print("labtest list <recordId>")
    
    print("\nreport export --type=<entityType> --format=<formatType> --output=<fileName> [--filters=<filterString>]")
    print("\nexit - Exit the application")
    print("help - Display this help message")

if __name__ == "__main__":
    main()

