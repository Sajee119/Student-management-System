"""
Student Management System - Student Class
This module defines the Student class with all necessary attributes and methods.
"""

from datetime import datetime
from typing import Dict, List, Optional
import re


class Student:
    """
    Represents a student with personal and academic information.
    """
    
    def __init__(self, student_id: str, first_name: str, last_name: str, 
                 email: str, phone: str, date_of_birth: str, 
                 address: str = "", major: str = "", gpa: float = 0.0):
        """
        Initialize a Student object.
        
        Args:
            student_id (str): Unique identifier for the student
            first_name (str): Student's first name
            last_name (str): Student's last name
            email (str): Student's email address
            phone (str): Student's phone number
            date_of_birth (str): Date of birth in YYYY-MM-DD format
            address (str): Student's address (optional)
            major (str): Student's major/field of study (optional)
            gpa (float): Student's GPA (optional, default 0.0)
        """
        self.student_id = self._validate_student_id(student_id)
        self.first_name = self._validate_name(first_name, "First name")
        self.last_name = self._validate_name(last_name, "Last name")
        self.email = self._validate_email(email)
        self.phone = self._validate_phone(phone)
        self.date_of_birth = self._validate_date(date_of_birth)
        self.address = address
        self.major = major
        self.gpa = self._validate_gpa(gpa)
        self.enrollment_date = datetime.now().strftime("%Y-%m-%d")
        self.courses: List[str] = []
        self.grades: Dict[str, float] = {}
    
    def _validate_student_id(self, student_id: str) -> str:
        """Validate student ID format."""
        if not student_id or not isinstance(student_id, str):
            raise ValueError("Student ID must be a non-empty string")
        if len(student_id) < 3:
            raise ValueError("Student ID must be at least 3 characters long")
        return student_id.strip().upper()
    
    def _validate_name(self, name: str, field_name: str) -> str:
        """Validate name fields."""
        if not name or not isinstance(name, str):
            raise ValueError(f"{field_name} must be a non-empty string")
        if not name.strip():
            raise ValueError(f"{field_name} cannot be empty or just whitespace")
        return name.strip().title()
    
    def _validate_email(self, email: str) -> str:
        """Validate email format."""
        if not email or not isinstance(email, str):
            raise ValueError("Email must be a non-empty string")
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format")
        return email.strip().lower()
    
    def _validate_phone(self, phone: str) -> str:
        """Validate phone number format."""
        if not phone or not isinstance(phone, str):
            raise ValueError("Phone number must be a non-empty string")
        
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', phone)
        if len(digits_only) < 10:
            raise ValueError("Phone number must contain at least 10 digits")
        return phone.strip()
    
    def _validate_date(self, date_str: str) -> str:
        """Validate date format (YYYY-MM-DD)."""
        if not date_str or not isinstance(date_str, str):
            raise ValueError("Date must be a non-empty string")
        
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")
    
    def _validate_gpa(self, gpa: float) -> float:
        """Validate GPA value."""
        if not isinstance(gpa, (int, float)):
            raise ValueError("GPA must be a number")
        if gpa < 0.0 or gpa > 4.0:
            raise ValueError("GPA must be between 0.0 and 4.0")
        return float(gpa)
    
    def add_course(self, course_name: str) -> bool:
        """
        Add a course to the student's course list.
        
        Args:
            course_name (str): Name of the course to add
            
        Returns:
            bool: True if course was added, False if already exists
        """
        if not course_name or not isinstance(course_name, str):
            raise ValueError("Course name must be a non-empty string")
        
        course_name = course_name.strip()
        if course_name not in self.courses:
            self.courses.append(course_name)
            return True
        return False
    
    def remove_course(self, course_name: str) -> bool:
        """
        Remove a course from the student's course list.
        
        Args:
            course_name (str): Name of the course to remove
            
        Returns:
            bool: True if course was removed, False if not found
        """
        if course_name in self.courses:
            self.courses.remove(course_name)
            # Also remove the grade if it exists
            if course_name in self.grades:
                del self.grades[course_name]
            return True
        return False
    
    def add_grade(self, course_name: str, grade: float) -> bool:
        """
        Add a grade for a specific course.
        
        Args:
            course_name (str): Name of the course
            grade (float): Grade value (0.0 - 4.0)
            
        Returns:
            bool: True if grade was added successfully
        """
        if course_name not in self.courses:
            raise ValueError(f"Course '{course_name}' not found in student's course list")
        
        if not isinstance(grade, (int, float)):
            raise ValueError("Grade must be a number")
        if grade < 0.0 or grade > 4.0:
            raise ValueError("Grade must be between 0.0 and 4.0")
        
        self.grades[course_name] = float(grade)
        self._update_gpa()
        return True
    
    def _update_gpa(self) -> None:
        """Update the student's overall GPA based on course grades."""
        if self.grades:
            self.gpa = sum(self.grades.values()) / len(self.grades)
        else:
            self.gpa = 0.0
    
    def get_full_name(self) -> str:
        """Return the student's full name."""
        return f"{self.first_name} {self.last_name}"
    
    def get_age(self) -> int:
        """Calculate and return the student's age."""
        birth_date = datetime.strptime(self.date_of_birth, "%Y-%m-%d")
        today = datetime.now()
        age = today.year - birth_date.year
        if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
            age -= 1
        return age
    
    def to_dict(self) -> Dict:
        """Convert student object to dictionary for serialization."""
        return {
            'student_id': self.student_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'date_of_birth': self.date_of_birth,
            'address': self.address,
            'major': self.major,
            'gpa': self.gpa,
            'enrollment_date': self.enrollment_date,
            'courses': self.courses,
            'grades': self.grades
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Student':
        """Create a Student object from a dictionary."""
        student = cls(
            student_id=data['student_id'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone=data['phone'],
            date_of_birth=data['date_of_birth'],
            address=data.get('address', ''),
            major=data.get('major', ''),
            gpa=data.get('gpa', 0.0)
        )
        student.enrollment_date = data.get('enrollment_date', student.enrollment_date)
        student.courses = data.get('courses', [])
        student.grades = data.get('grades', {})
        return student
    
    def update_info(self, **kwargs) -> None:
        """
        Update student information.
        
        Args:
            **kwargs: Keyword arguments for fields to update
        """
        updatable_fields = {
            'first_name': self._validate_name,
            'last_name': self._validate_name,
            'email': self._validate_email,
            'phone': self._validate_phone,
            'address': str,
            'major': str,
        }
        
        for field, value in kwargs.items():
            if field in updatable_fields:
                if field in ['first_name', 'last_name']:
                    setattr(self, field, updatable_fields[field](value, field.replace('_', ' ').title()))
                elif field in ['email', 'phone']:
                    setattr(self, field, updatable_fields[field](value))
                else:
                    setattr(self, field, str(value).strip())
    
    def __str__(self) -> str:
        """String representation of the student."""
        return f"Student(ID: {self.student_id}, Name: {self.get_full_name()}, Major: {self.major}, GPA: {self.gpa:.2f})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the student."""
        return (f"Student(student_id='{self.student_id}', "
                f"name='{self.get_full_name()}', "
                f"email='{self.email}', "
                f"major='{self.major}', "
                f"gpa={self.gpa:.2f})")