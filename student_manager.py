"""
Student Management System - Manager Module
This module provides high-level operations and business logic.
"""

from typing import List, Dict, Optional, Tuple
from datetime import datetime
from student import Student
from database import StudentDatabase


class StudentManager:
    """
    High-level manager class for student operations.
    Provides business logic and validation for student management.
    """
    
    def __init__(self, db_file: str = "students.json"):
        """
        Initialize the Student Manager.
        
        Args:
            db_file (str): Path to the database file
        """
        self.db = StudentDatabase(db_file)
    
    def add_student(self, student_data: Dict) -> Tuple[bool, str]:
        """
        Add a new student with comprehensive validation.
        
        Args:
            student_data (Dict): Dictionary containing student information
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            # Create student object (this will validate the data)
            student = Student(
                student_id=student_data['student_id'],
                first_name=student_data['first_name'],
                last_name=student_data['last_name'],
                email=student_data['email'],
                phone=student_data['phone'],
                date_of_birth=student_data['date_of_birth'],
                address=student_data.get('address', ''),
                major=student_data.get('major', ''),
                gpa=float(student_data.get('gpa', 0.0))
            )
            
            # Check if student already exists
            existing_student = self.db.get_student(student.student_id)
            if existing_student:
                return False, f"Student with ID {student.student_id} already exists"
            
            # Add to database
            if self.db.add_student(student):
                return True, f"Student {student.get_full_name()} added successfully"
            else:
                return False, "Failed to add student to database"
                
        except ValueError as e:
            return False, f"Validation error: {str(e)}"
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"
    
    def get_student(self, student_id: str) -> Tuple[Optional[Student], str]:
        """
        Retrieve a student by ID.
        
        Args:
            student_id (str): Student ID to search for
            
        Returns:
            Tuple[Optional[Student], str]: (student_object, message)
        """
        try:
            student = self.db.get_student(student_id)
            if student:
                return student, "Student found"
            else:
                return None, f"Student with ID {student_id} not found"
        except Exception as e:
            return None, f"Error retrieving student: {str(e)}"
    
    def update_student(self, student_id: str, update_data: Dict) -> Tuple[bool, str]:
        """
        Update student information.
        
        Args:
            student_id (str): Student ID to update
            update_data (Dict): Dictionary containing fields to update
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            # Get existing student
            student = self.db.get_student(student_id)
            if not student:
                return False, f"Student with ID {student_id} not found"
            
            # Update student information
            student.update_info(**update_data)
            
            # Save to database
            if self.db.update_student(student):
                return True, f"Student {student.get_full_name()} updated successfully"
            else:
                return False, "Failed to update student in database"
                
        except ValueError as e:
            return False, f"Validation error: {str(e)}"
        except Exception as e:
            return False, f"Error updating student: {str(e)}"
    
    def delete_student(self, student_id: str) -> Tuple[bool, str]:
        """
        Delete a student from the system.
        
        Args:
            student_id (str): Student ID to delete
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            # Check if student exists
            student = self.db.get_student(student_id)
            if not student:
                return False, f"Student with ID {student_id} not found"
            
            # Delete from database
            if self.db.delete_student(student_id):
                return True, f"Student {student.get_full_name()} deleted successfully"
            else:
                return False, "Failed to delete student from database"
                
        except Exception as e:
            return False, f"Error deleting student: {str(e)}"
    
    def list_all_students(self) -> List[Student]:
        """
        Get all students from the database.
        
        Returns:
            List[Student]: List of all students
        """
        return self.db.get_all_students()
    
    def search_students(self, search_criteria: Dict) -> Tuple[List[Student], str]:
        """
        Search for students based on criteria.
        
        Args:
            search_criteria (Dict): Search criteria
            
        Returns:
            Tuple[List[Student], str]: (matching_students, message)
        """
        try:
            students = self.db.search_students(**search_criteria)
            if students:
                return students, f"Found {len(students)} matching student(s)"
            else:
                return [], "No students found matching the criteria"
        except Exception as e:
            return [], f"Error searching students: {str(e)}"
    
    def add_course_to_student(self, student_id: str, course_name: str) -> Tuple[bool, str]:
        """
        Add a course to a student's course list.
        
        Args:
            student_id (str): Student ID
            course_name (str): Course name to add
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            student = self.db.get_student(student_id)
            if not student:
                return False, f"Student with ID {student_id} not found"
            
            if student.add_course(course_name):
                if self.db.update_student(student):
                    return True, f"Course '{course_name}' added to {student.get_full_name()}"
                else:
                    return False, "Failed to save changes to database"
            else:
                return False, f"Course '{course_name}' already exists for this student"
                
        except ValueError as e:
            return False, f"Validation error: {str(e)}"
        except Exception as e:
            return False, f"Error adding course: {str(e)}"
    
    def remove_course_from_student(self, student_id: str, course_name: str) -> Tuple[bool, str]:
        """
        Remove a course from a student's course list.
        
        Args:
            student_id (str): Student ID
            course_name (str): Course name to remove
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            student = self.db.get_student(student_id)
            if not student:
                return False, f"Student with ID {student_id} not found"
            
            if student.remove_course(course_name):
                if self.db.update_student(student):
                    return True, f"Course '{course_name}' removed from {student.get_full_name()}"
                else:
                    return False, "Failed to save changes to database"
            else:
                return False, f"Course '{course_name}' not found for this student"
                
        except Exception as e:
            return False, f"Error removing course: {str(e)}"
    
    def add_grade_to_student(self, student_id: str, course_name: str, grade: float) -> Tuple[bool, str]:
        """
        Add a grade for a specific course to a student.
        
        Args:
            student_id (str): Student ID
            course_name (str): Course name
            grade (float): Grade value (0.0 - 4.0)
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            student = self.db.get_student(student_id)
            if not student:
                return False, f"Student with ID {student_id} not found"
            
            if student.add_grade(course_name, grade):
                if self.db.update_student(student):
                    return True, f"Grade {grade} added for course '{course_name}' to {student.get_full_name()}"
                else:
                    return False, "Failed to save changes to database"
            else:
                return False, "Failed to add grade"
                
        except ValueError as e:
            return False, f"Validation error: {str(e)}"
        except Exception as e:
            return False, f"Error adding grade: {str(e)}"
    
    def get_student_transcript(self, student_id: str) -> Tuple[Optional[Dict], str]:
        """
        Get a student's academic transcript.
        
        Args:
            student_id (str): Student ID
            
        Returns:
            Tuple[Optional[Dict], str]: (transcript_data, message)
        """
        try:
            student = self.db.get_student(student_id)
            if not student:
                return None, f"Student with ID {student_id} not found"
            
            transcript = {
                'student_info': {
                    'id': student.student_id,
                    'name': student.get_full_name(),
                    'major': student.major,
                    'enrollment_date': student.enrollment_date
                },
                'courses': student.courses,
                'grades': student.grades,
                'overall_gpa': student.gpa,
                'total_courses': len(student.courses),
                'completed_courses': len(student.grades)
            }
            
            return transcript, "Transcript generated successfully"
            
        except Exception as e:
            return None, f"Error generating transcript: {str(e)}"
    
    def get_statistics(self) -> Tuple[Dict, str]:
        """
        Get system statistics.
        
        Returns:
            Tuple[Dict, str]: (statistics, message)
        """
        try:
            stats = self.db.get_statistics()
            return stats, "Statistics generated successfully"
        except Exception as e:
            return {}, f"Error generating statistics: {str(e)}"
    
    def export_data(self, filename: str = None) -> Tuple[bool, str]:
        """
        Export student data to CSV.
        
        Args:
            filename (str): Output filename (optional)
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            if self.db.export_to_csv(filename):
                export_file = filename or f"students_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                return True, f"Data exported successfully to {export_file}"
            else:
                return False, "Failed to export data"
        except Exception as e:
            return False, f"Error exporting data: {str(e)}"
    
    def import_data(self, filename: str) -> Tuple[bool, str]:
        """
        Import student data from CSV.
        
        Args:
            filename (str): Input filename
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            successful, failed = self.db.import_from_csv(filename)
            if successful > 0:
                message = f"Import completed: {successful} students imported successfully"
                if failed > 0:
                    message += f", {failed} failed"
                return True, message
            else:
                return False, f"Import failed: {failed} records could not be imported"
        except Exception as e:
            return False, f"Error importing data: {str(e)}"
    
    def validate_student_data(self, student_data: Dict) -> Tuple[bool, List[str]]:
        """
        Validate student data without creating a student object.
        
        Args:
            student_data (Dict): Student data to validate
            
        Returns:
            Tuple[bool, List[str]]: (is_valid, list_of_errors)
        """
        errors = []
        
        # Required fields
        required_fields = ['student_id', 'first_name', 'last_name', 'email', 'phone', 'date_of_birth']
        for field in required_fields:
            if field not in student_data or not student_data[field]:
                errors.append(f"Missing required field: {field}")
        
        if errors:
            return False, errors
        
        try:
            # Try to create a temporary student object for validation
            Student(
                student_id=student_data['student_id'],
                first_name=student_data['first_name'],
                last_name=student_data['last_name'],
                email=student_data['email'],
                phone=student_data['phone'],
                date_of_birth=student_data['date_of_birth'],
                address=student_data.get('address', ''),
                major=student_data.get('major', ''),
                gpa=float(student_data.get('gpa', 0.0))
            )
            return True, []
        except ValueError as e:
            errors.append(str(e))
            return False, errors
    
    def get_students_by_major(self, major: str) -> List[Student]:
        """
        Get all students in a specific major.
        
        Args:
            major (str): Major to search for
            
        Returns:
            List[Student]: Students in the specified major
        """
        return self.db.search_students(major=major)
    
    def get_top_students(self, limit: int = 10) -> List[Student]:
        """
        Get top students by GPA.
        
        Args:
            limit (int): Number of top students to return
            
        Returns:
            List[Student]: Top students sorted by GPA
        """
        all_students = self.db.get_all_students()
        # Filter students with GPA > 0 and sort by GPA descending
        students_with_gpa = [s for s in all_students if s.gpa > 0]
        students_with_gpa.sort(key=lambda x: x.gpa, reverse=True)
        return students_with_gpa[:limit]
    
    def get_students_needing_attention(self) -> List[Student]:
        """
        Get students who might need academic attention (low GPA).
        
        Returns:
            List[Student]: Students with GPA below 2.0
        """
        return self.db.search_students(gpa_max=1.99)