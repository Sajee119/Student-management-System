"""
Student Management System - Database Module
This module handles data persistence for the student management system.
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime
from student import Student


class StudentDatabase:
    """
    Handles data persistence for students using JSON files.
    """
    
    def __init__(self, db_file: str = "students.json"):
        """
        Initialize the database.
        
        Args:
            db_file (str): Path to the JSON database file
        """
        self.db_file = db_file
        self.backup_dir = "backups"
        self._ensure_database_exists()
        self._ensure_backup_dir()
    
    def _ensure_database_exists(self) -> None:
        """Create the database file if it doesn't exist."""
        if not os.path.exists(self.db_file):
            with open(self.db_file, 'w') as f:
                json.dump([], f)
    
    def _ensure_backup_dir(self) -> None:
        """Create backup directory if it doesn't exist."""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
    
    def _load_data(self) -> List[Dict]:
        """
        Load data from the JSON file.
        
        Returns:
            List[Dict]: List of student dictionaries
        """
        try:
            with open(self.db_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading database: {e}")
            return []
    
    def _save_data(self, data: List[Dict]) -> bool:
        """
        Save data to the JSON file.
        
        Args:
            data (List[Dict]): List of student dictionaries to save
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create backup before saving
            self._create_backup()
            
            with open(self.db_file, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving database: {e}")
            return False
    
    def _create_backup(self) -> None:
        """Create a backup of the current database."""
        if os.path.exists(self.db_file):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(self.backup_dir, f"students_backup_{timestamp}.json")
            try:
                with open(self.db_file, 'r') as src, open(backup_file, 'w') as dst:
                    dst.write(src.read())
            except Exception as e:
                print(f"Warning: Could not create backup: {e}")
    
    def add_student(self, student: Student) -> bool:
        """
        Add a student to the database.
        
        Args:
            student (Student): Student object to add
            
        Returns:
            bool: True if successful, False if student ID already exists
        """
        data = self._load_data()
        
        # Check if student ID already exists
        for existing_student in data:
            if existing_student['student_id'] == student.student_id:
                return False
        
        # Add the new student
        data.append(student.to_dict())
        return self._save_data(data)
    
    def get_student(self, student_id: str) -> Optional[Student]:
        """
        Retrieve a student by ID.
        
        Args:
            student_id (str): Student ID to search for
            
        Returns:
            Optional[Student]: Student object if found, None otherwise
        """
        data = self._load_data()
        
        for student_data in data:
            if student_data['student_id'] == student_id.upper():
                return Student.from_dict(student_data)
        
        return None
    
    def get_all_students(self) -> List[Student]:
        """
        Retrieve all students from the database.
        
        Returns:
            List[Student]: List of all Student objects
        """
        data = self._load_data()
        students = []
        
        for student_data in data:
            try:
                students.append(Student.from_dict(student_data))
            except Exception as e:
                print(f"Error loading student {student_data.get('student_id', 'Unknown')}: {e}")
        
        return students
    
    def update_student(self, student: Student) -> bool:
        """
        Update an existing student in the database.
        
        Args:
            student (Student): Student object with updated information
            
        Returns:
            bool: True if successful, False if student not found
        """
        data = self._load_data()
        
        for i, existing_student in enumerate(data):
            if existing_student['student_id'] == student.student_id:
                data[i] = student.to_dict()
                return self._save_data(data)
        
        return False
    
    def delete_student(self, student_id: str) -> bool:
        """
        Delete a student from the database.
        
        Args:
            student_id (str): Student ID to delete
            
        Returns:
            bool: True if successful, False if student not found
        """
        data = self._load_data()
        
        for i, student_data in enumerate(data):
            if student_data['student_id'] == student_id.upper():
                del data[i]
                return self._save_data(data)
        
        return False
    
    def search_students(self, **criteria) -> List[Student]:
        """
        Search for students based on various criteria.
        
        Args:
            **criteria: Search criteria (e.g., major='Computer Science', gpa_min=3.0)
            
        Returns:
            List[Student]: List of matching Student objects
        """
        all_students = self.get_all_students()
        matching_students = []
        
        for student in all_students:
            match = True
            
            for key, value in criteria.items():
                if key == 'name':
                    # Search in full name (case insensitive)
                    if value.lower() not in student.get_full_name().lower():
                        match = False
                        break
                elif key == 'major':
                    if value.lower() not in student.major.lower():
                        match = False
                        break
                elif key == 'email':
                    if value.lower() not in student.email.lower():
                        match = False
                        break
                elif key == 'gpa_min':
                    if student.gpa < float(value):
                        match = False
                        break
                elif key == 'gpa_max':
                    if student.gpa > float(value):
                        match = False
                        break
                elif key == 'age_min':
                    if student.get_age() < int(value):
                        match = False
                        break
                elif key == 'age_max':
                    if student.get_age() > int(value):
                        match = False
                        break
                elif hasattr(student, key):
                    student_value = getattr(student, key)
                    if isinstance(student_value, str) and isinstance(value, str):
                        if value.lower() not in student_value.lower():
                            match = False
                            break
                    elif student_value != value:
                        match = False
                        break
            
            if match:
                matching_students.append(student)
        
        return matching_students
    
    def get_statistics(self) -> Dict:
        """
        Get database statistics.
        
        Returns:
            Dict: Statistics about the student database
        """
        students = self.get_all_students()
        
        if not students:
            return {
                'total_students': 0,
                'average_gpa': 0.0,
                'majors': {},
                'age_distribution': {}
            }
        
        # Calculate statistics
        total_students = len(students)
        total_gpa = sum(student.gpa for student in students if student.gpa > 0)
        students_with_gpa = len([s for s in students if s.gpa > 0])
        average_gpa = total_gpa / students_with_gpa if students_with_gpa > 0 else 0.0
        
        # Major distribution
        majors = {}
        for student in students:
            major = student.major or 'Undeclared'
            majors[major] = majors.get(major, 0) + 1
        
        # Age distribution
        age_ranges = {'18-20': 0, '21-25': 0, '26-30': 0, '30+': 0}
        for student in students:
            age = student.get_age()
            if 18 <= age <= 20:
                age_ranges['18-20'] += 1
            elif 21 <= age <= 25:
                age_ranges['21-25'] += 1
            elif 26 <= age <= 30:
                age_ranges['26-30'] += 1
            else:
                age_ranges['30+'] += 1
        
        return {
            'total_students': total_students,
            'average_gpa': round(average_gpa, 2),
            'majors': majors,
            'age_distribution': age_ranges
        }
    
    def export_to_csv(self, filename: str = None) -> bool:
        """
        Export student data to CSV file.
        
        Args:
            filename (str): CSV filename (optional)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"students_export_{timestamp}.csv"
        
        try:
            import csv
            students = self.get_all_students()
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                if not students:
                    return True
                
                fieldnames = [
                    'student_id', 'first_name', 'last_name', 'email', 'phone',
                    'date_of_birth', 'address', 'major', 'gpa', 'enrollment_date',
                    'courses', 'age'
                ]
                
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for student in students:
                    row = student.to_dict()
                    row['courses'] = ', '.join(student.courses)
                    row['age'] = student.get_age()
                    # Remove grades field as it's not in fieldnames
                    if 'grades' in row:
                        del row['grades']
                    writer.writerow(row)
            
            return True
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False
    
    def import_from_csv(self, filename: str) -> tuple[int, int]:
        """
        Import student data from CSV file.
        
        Args:
            filename (str): CSV filename to import from
            
        Returns:
            tuple[int, int]: (successful_imports, failed_imports)
        """
        try:
            import csv
            successful = 0
            failed = 0
            
            with open(filename, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row in reader:
                    try:
                        # Parse courses
                        courses = [course.strip() for course in row.get('courses', '').split(',') if course.strip()]
                        
                        # Create student object
                        student = Student(
                            student_id=row['student_id'],
                            first_name=row['first_name'],
                            last_name=row['last_name'],
                            email=row['email'],
                            phone=row['phone'],
                            date_of_birth=row['date_of_birth'],
                            address=row.get('address', ''),
                            major=row.get('major', ''),
                            gpa=float(row.get('gpa', 0.0))
                        )
                        
                        # Add courses
                        for course in courses:
                            student.add_course(course)
                        
                        # Set enrollment date if provided
                        if 'enrollment_date' in row and row['enrollment_date']:
                            student.enrollment_date = row['enrollment_date']
                        
                        # Add to database
                        if self.add_student(student):
                            successful += 1
                        else:
                            failed += 1
                            print(f"Failed to add student {student.student_id} (may already exist)")
                    
                    except Exception as e:
                        failed += 1
                        print(f"Error importing row: {e}")
            
            return successful, failed
        
        except Exception as e:
            print(f"Error importing from CSV: {e}")
            return 0, 0