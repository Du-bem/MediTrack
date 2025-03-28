MediTrack is a comprehensive healthcare management system designed to streamline patient care, appointment scheduling, medical record management, and clinical workflows. Built with a focus on security, efficiency, and user experience, MediTrack helps healthcare providers deliver better patient care.

[

](https://opensource.org/licenses/MIT)
[

](https://www.python.org/downloads/)
[

](https://www.postgresql.org/)

## 🌟 Features

- **Patient Management**: Register, update, and search patient information
- **Doctor Management**: Manage healthcare providers, specializations, and schedules
- **Appointment Scheduling**: Book, reschedule, and cancel appointments with conflict detection
- **Medical Records**: Create and maintain comprehensive patient medical histories
- **Prescription Management**: Issue, refill, and track patient prescriptions
- **Lab Test Management**: Order tests, record results, and flag abnormal findings
- **Reporting**: Generate customizable reports in various formats (CSV, PDF)
- **Command-Line Interface**: Intuitive CLI for all system operations


## 🛠️ Technology Stack

- **Backend**: Python 3.13
- **Database**: PostgreSQL 17
- **ORM**: SQLAlchemy
- **Testing**: Python unittest framework
- **Documentation**: Markdown, docstrings


## 📋 Prerequisites

- Python 3.8 or higher
- PostgreSQL 13 or higher
- pip (Python package manager)
- Git


## 🚀 Installation

### 1. Clone the repository

```shellscript
git clone https://github.com/yourusername/meditrack.git
cd meditrack
```

### 2. Create and activate a virtual environment

```shellscript
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```shellscript
pip install -r requirements.txt
```

### 4. Set up PostgreSQL database

```shellscript
# Run the PostgreSQL setup script
python setup_postgres.py

# Or manually set up the database
psql -U postgres
CREATE DATABASE meditrack_db;
CREATE USER meditrack_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE meditrack_db TO meditrack_user;
\q
```

### 5. Initialize the database

```shellscript
python db/init_db.py
```

### 6. Configure environment variables (optional)

Create a `.env` file in the project root:

```plaintext
DB_URL=postgresql://meditrack_user:your_secure_password@localhost/meditrack_db
LOG_LEVEL=INFO
EXPORT_DIR=./exports
```

## 🖥️ Usage

### Starting the application

```shellscript
python main.py
```

### Command-Line Interface

MediTrack provides a comprehensive CLI for all operations:

```plaintext
# Patient Management
patient add <firstName> <lastName> <dob> <email> <phone> [address] [insuranceInfo]
patient search <searchTerm>
patient update <patientId> <field> <value>
patient list [--limit=<n>] [--offset=<n>]
patient view <patientId>

# Doctor Management
doctor add <firstName> <lastName> <dob> <email> <phone> <specialisation> <licenseNumber>
doctor search <searchTerm>
doctor list [--department=<dept>] [--specialisation=<spec>]

# Appointment Management
appointment add <patientId> <doctorId> <dateTime> <duration> [notes]
appointment list [--doctor=<doctorId>] [--patient=<patientId>] [--date=<date>] [--status=<status>]
appointment update <appointmentId> <field> <value>
appointment cancel <appointmentId> [reason]
appointment reschedule <appointmentId> <newDateTime>

# Medical Record Management
medicalrecord add <patientId> <diagnosis> <treatmentPlan> [notes]
medicalrecord view <recordId>
medicalrecord list <patientId>
medicalrecord update <recordId> <field> <value>

# Prescription Management
prescription add <recordId> <medication> <dosage> <frequency> <startDate> <endDate> [instructions]
prescription list <recordId>
prescription update <prescriptionId> <field> <value>
prescription refill <prescriptionId> <newEndDate>

# Lab Test Management
labtest add <recordId> <testName> <testType> <orderedDate>
labtest result <testId> <resultDate> <result> <referenceRange> <isAbnormal>
labtest list <recordId>

# Reporting
report export --type=<entityType> --format=<formatType> --output=<fileName> [--filters=<filterString>]
```

### Examples

```shellscript
# Add a new patient
python main.py patient add "John" "Doe" "1985-05-15" "john.doe@example.com" "555-123-4567" "123 Main St" "BlueCross #BC987654321"

# Search for patients
python main.py patient search "Doe"

# Schedule an appointment
python main.py appointment add 1 2 "2023-12-15 10:00" 30 "Initial consultation"

# View medical records
python main.py medicalrecord list 1

# Generate a report
python main.py report export --type=patients --format=csv --output=patients.csv
```

## 📁 Project Structure

```plaintext
meditrack/
├── main.py                  # Main entry point
├── config.py                # Configuration settings
├── setup_postgres.py        # PostgreSQL setup script
├── requirements.txt         # Dependencies
├── db/
│   ├── init_db.py           # Database initialization
│   ├── models.py            # SQLAlchemy models
│   └── repository.py        # Data access layer
├── domain/
│   ├── entities.py          # Domain entities
│   └── services.py          # Business logic
├── cli/
│   ├── command_parser.py    # CLI command parsing
│   └── command_executor.py  # CLI command execution
├── algorithms/
│   ├── search.py            # Search algorithms
│   ├── scheduling.py        # Scheduling algorithms
│   └── data_analysis.py     # Data analysis algorithms
├── utils/
│   ├── validators.py        # Validation utilities
│   ├── formatters.py        # Formatting utilities
│   ├── export.py            # Export utilities
│   └── logging_config.py    # Logging configuration
└── tests/                   # Unit tests
    ├── test_db_models.py
    ├── test_db_repository.py
    ├── test_domain_entities.py
    ├── test_domain_services.py
    ├── test_algorithms_search.py
    ├── test_algorithms_scheduling.py
    ├── test_algorithms_data_analysis.py
    ├── test_cli_command_parser.py
    ├── test_utils_validators.py
    ├── test_utils_formatters.py
    ├── test_utils_export.py
    └── run_all_tests.py
```

## 🧪 Testing

MediTrack includes a comprehensive test suite covering all major components:

```shellscript
# Run all tests
python tests/run_all_tests.py

# Run specific test modules
python -m unittest tests/test_db_models.py
python -m unittest tests/test_domain_services.py
```

## 📊 Database Schema





MediTrack uses a relational database with the following key tables:

- **persons**: Base table for all individuals
- **patients**: Patient information
- **staff**: Staff information
- **doctors**: Doctor information
- **patient_medical_records**: Medical records
- **prescriptions**: Prescription information
- **lab_tests**: Laboratory test information
- **appointments**: Appointment scheduling
