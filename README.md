# Student Management System

A comprehensive, fully-functional Student Management System built in Python with a command-line interface. This system provides complete CRUD operations for managing student records, courses, grades, and academic data.

## Features

### Core Functionality
- **Student Management**: Add, view, update, and delete student records
- **Course Management**: Assign and remove courses from students
- **Grade Management**: Record and track student grades with automatic GPA calculation
- **Search & Filter**: Advanced search capabilities by name, major, GPA, age, etc.
- **Academic Reports**: Generate student transcripts and system statistics

### Data Management
- **JSON Database**: Persistent data storage with automatic backup system
- **CSV Import/Export**: Bulk data operations with CSV file support
- **Data Validation**: Comprehensive input validation and error handling
- **Backup System**: Automatic backups before data modifications

### User Interface
- **Interactive CLI**: User-friendly command-line interface
- **Menu-Driven**: Intuitive menu system with clear navigation
- **Input Validation**: Real-time validation with helpful error messages
- **Cross-Platform**: Works on Windows, macOS, and Linux

## System Architecture

The system follows a modular architecture with clear separation of concerns:

```
├── student.py          # Student class with validation and methods
├── database.py         # Data persistence and database operations
├── student_manager.py  # Business logic and high-level operations
├── cli.py             # Command-line interface and user interaction
├── requirements.txt   # Python dependencies (uses only standard library)
└── README.md         # Documentation
```

## Installation

### Prerequisites
- Python 3.7 or higher
- No external dependencies required (uses only Python standard library)

### Setup
1. Clone or download the project files
2. Navigate to the project directory
3. Run the application:
   ```bash
   python cli.py
   ```

## Usage

### Starting the Application
```bash
python cli.py
```

### Main Menu Options
1. **Add New Student** - Register a new student with personal and academic information
2. **View Student Details** - Display complete student profile including courses and grades
3. **Update Student Information** - Modify student contact and academic information
4. **Delete Student** - Remove a student from the system (with confirmation)
5. **List All Students** - Display summary of all registered students
6. **Search Students** - Find students by various criteria (name, major, GPA, age)
7. **Add Course to Student** - Enroll a student in a new course
8. **Remove Course from Student** - Remove a course from student's enrollment
9. **Add Grade to Student** - Record a grade for a specific course
10. **View Student Transcript** - Generate detailed academic transcript
11. **View System Statistics** - Display system-wide statistics and analytics
12. **Export Data to CSV** - Export all student data to CSV file
13. **Import Data from CSV** - Import student data from CSV file
14. **View Top Students** - Display highest-performing students by GPA
15. **View Students Needing Attention** - Show students with low GPA (< 2.0)

### Data Fields

#### Student Information
- **Student ID**: Unique identifier (required, minimum 3 characters)
- **Name**: First and last name (required)
- **Email**: Valid email address (required)
- **Phone**: Contact number (required, minimum 10 digits)
- **Date of Birth**: YYYY-MM-DD format (required)
- **Address**: Physical address (optional)
- **Major**: Field of study (optional)
- **GPA**: Grade Point Average 0.0-4.0 (calculated automatically from grades)

#### Academic Information
- **Courses**: List of enrolled courses
- **Grades**: Course-specific grades (0.0-4.0 scale)
- **Enrollment Date**: Automatically recorded
- **Overall GPA**: Calculated from all course grades

## Data Storage

### Database File
- **Format**: JSON
- **Location**: `students.json` (created automatically)
- **Backup**: Automatic backups in `backups/` directory

### Backup System
- Automatic backup before any data modification
- Timestamped backup files
- Backup directory created automatically

### CSV Import/Export
- **Export**: All student data with calculated fields (age, GPA)
- **Import**: Bulk student registration from CSV files
- **Format**: Standard CSV with headers

## Data Validation

### Input Validation
- **Student ID**: Non-empty, minimum 3 characters, automatically uppercase
- **Names**: Non-empty, properly capitalized
- **Email**: Valid email format using regex validation
- **Phone**: Minimum 10 digits, flexible formatting
- **Date**: YYYY-MM-DD format with date validation
- **GPA**: Numeric range 0.0-4.0

### Business Logic Validation
- **Unique Student IDs**: Prevents duplicate registrations
- **Course Prerequisites**: Must be enrolled in course before adding grades
- **Data Integrity**: Consistent data across all operations

## Error Handling

### Comprehensive Error Management
- **Input Validation Errors**: Clear messages for invalid input
- **File System Errors**: Graceful handling of file operations
- **Data Corruption**: Recovery mechanisms for corrupted data
- **User Errors**: Helpful guidance for common mistakes

### User-Friendly Messages
- Success indicators (✓)
- Error indicators (✗)
- Clear, actionable error messages
- Confirmation prompts for destructive operations

## Advanced Features

### Search Capabilities
- **Name Search**: Partial matching, case-insensitive
- **Major Filter**: Find students by field of study
- **GPA Range**: Filter by minimum/maximum GPA
- **Age Range**: Filter by student age
- **Combined Criteria**: Multiple search parameters

### Analytics & Reports
- **System Statistics**: Total students, average GPA, major distribution
- **Age Demographics**: Student age distribution analysis
- **Academic Performance**: Top performers and at-risk students
- **Transcript Generation**: Detailed academic records

### Data Management
- **Bulk Operations**: CSV import/export for large datasets
- **Data Migration**: Easy transfer between systems
- **Backup & Recovery**: Automatic data protection
- **Data Integrity**: Validation and consistency checks

## Technical Details

### Architecture Patterns
- **MVC Pattern**: Clear separation of data, logic, and presentation
- **Single Responsibility**: Each class has a focused purpose
- **Type Safety**: Comprehensive type hints throughout
- **Error Handling**: Robust exception management

### Code Quality
- **Documentation**: Comprehensive docstrings and comments
- **Validation**: Input validation at multiple levels
- **Testing**: Built-in validation and error handling
- **Maintainability**: Clean, readable, modular code

### Performance
- **Efficient Search**: Optimized search algorithms
- **Memory Management**: Efficient data structures
- **File I/O**: Optimized database operations
- **Scalability**: Handles large student populations

## Example Usage

### Adding a Student
```
Student ID: STU001
First Name: John
Last Name: Doe
Email: john.doe@university.edu
Phone: (555) 123-4567
Date of Birth: 2000-05-15
Address: 123 University Ave
Major: Computer Science
GPA: 3.75
```

### CSV Import Format
```csv
student_id,first_name,last_name,email,phone,date_of_birth,address,major,gpa,courses
STU001,John,Doe,john.doe@email.com,5551234567,2000-05-15,123 Main St,Computer Science,3.75,"Math 101, CS 101"
```

## Troubleshooting

### Common Issues
1. **Permission Errors**: Ensure write permissions in the directory
2. **File Not Found**: Check file paths and existence
3. **Invalid Data**: Review CSV format for imports
4. **Memory Issues**: For very large datasets, consider batch processing

### Support
- Check error messages for specific guidance
- Verify input formats match requirements
- Ensure Python version compatibility (3.7+)
- Review file permissions and disk space

## Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make changes with proper testing
4. Submit a pull request

### Code Standards
- Follow PEP 8 style guidelines
- Add comprehensive docstrings
- Include type hints
- Handle errors gracefully
- Write clear, readable code

## License

This project is open source and available under the MIT License.

## Version History

- **v1.0.0**: Initial release with full functionality
  - Complete CRUD operations
  - Advanced search and filtering
  - CSV import/export
  - Comprehensive validation
  - User-friendly CLI interface

---

**Student Management System** - A complete solution for educational institution student record management.
