#!/usr/bin/env python3
"""
Student Management System - Command Line Interface
This module provides a user-friendly CLI for the student management system.
"""

import os
import sys
from typing import Dict, List
from datetime import datetime
from student_manager import StudentManager
from student import Student


class StudentManagementCLI:
    """
    Command Line Interface for the Student Management System.
    """
    
    def __init__(self):
        """Initialize the CLI with a StudentManager instance."""
        self.manager = StudentManager()
        self.running = True
    
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Print the application header."""
        print("=" * 60)
        print("          STUDENT MANAGEMENT SYSTEM")
        print("=" * 60)
        print()
    
    def print_menu(self):
        """Print the main menu options."""
        print("MAIN MENU:")
        print("-" * 30)
        print("1.  Add New Student")
        print("2.  View Student Details")
        print("3.  Update Student Information")
        print("4.  Delete Student")
        print("5.  List All Students")
        print("6.  Search Students")
        print("7.  Add Course to Student")
        print("8.  Remove Course from Student")
        print("9.  Add Grade to Student")
        print("10. View Student Transcript")
        print("11. View System Statistics")
        print("12. Export Data to CSV")
        print("13. Import Data from CSV")
        print("14. View Top Students")
        print("15. View Students Needing Attention")
        print("0.  Exit")
        print("-" * 30)
    
    def get_input(self, prompt: str, required: bool = True) -> str:
        """
        Get user input with validation.
        
        Args:
            prompt (str): Input prompt message
            required (bool): Whether input is required
            
        Returns:
            str: User input
        """
        while True:
            value = input(prompt).strip()
            if value or not required:
                return value
            print("This field is required. Please enter a value.")
    
    def get_float_input(self, prompt: str, min_val: float = None, max_val: float = None) -> float:
        """
        Get float input with validation.
        
        Args:
            prompt (str): Input prompt message
            min_val (float): Minimum allowed value
            max_val (float): Maximum allowed value
            
        Returns:
            float: Validated float value
        """
        while True:
            try:
                value = float(input(prompt).strip())
                if min_val is not None and value < min_val:
                    print(f"Value must be at least {min_val}")
                    continue
                if max_val is not None and value > max_val:
                    print(f"Value must be at most {max_val}")
                    continue
                return value
            except ValueError:
                print("Please enter a valid number.")
    
    def get_date_input(self, prompt: str) -> str:
        """
        Get date input with validation.
        
        Args:
            prompt (str): Input prompt message
            
        Returns:
            str: Validated date string in YYYY-MM-DD format
        """
        while True:
            date_str = input(prompt).strip()
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                return date_str
            except ValueError:
                print("Please enter date in YYYY-MM-DD format (e.g., 2000-01-15)")
    
    def pause(self):
        """Pause execution and wait for user input."""
        input("\nPress Enter to continue...")
    
    def add_student(self):
        """Add a new student to the system."""
        print("\nADD NEW STUDENT")
        print("-" * 20)
        
        try:
            student_data = {
                'student_id': self.get_input("Student ID: "),
                'first_name': self.get_input("First Name: "),
                'last_name': self.get_input("Last Name: "),
                'email': self.get_input("Email: "),
                'phone': self.get_input("Phone: "),
                'date_of_birth': self.get_date_input("Date of Birth (YYYY-MM-DD): "),
                'address': self.get_input("Address (optional): ", required=False),
                'major': self.get_input("Major (optional): ", required=False),
            }
            
            # Ask for GPA
            gpa_input = input("GPA (0.0-4.0, optional): ").strip()
            if gpa_input:
                student_data['gpa'] = float(gpa_input)
            else:
                student_data['gpa'] = 0.0
            
            success, message = self.manager.add_student(student_data)
            
            if success:
                print(f"\n✓ {message}")
            else:
                print(f"\n✗ {message}")
                
        except Exception as e:
            print(f"\n✗ Error: {str(e)}")
    
    def view_student(self):
        """View details of a specific student."""
        print("\nVIEW STUDENT DETAILS")
        print("-" * 20)
        
        student_id = self.get_input("Enter Student ID: ")
        student, message = self.manager.get_student(student_id)
        
        if student:
            print(f"\n{message}")
            print("-" * 40)
            print(f"Student ID: {student.student_id}")
            print(f"Name: {student.get_full_name()}")
            print(f"Email: {student.email}")
            print(f"Phone: {student.phone}")
            print(f"Date of Birth: {student.date_of_birth}")
            print(f"Age: {student.get_age()}")
            print(f"Address: {student.address or 'Not provided'}")
            print(f"Major: {student.major or 'Undeclared'}")
            print(f"GPA: {student.gpa:.2f}")
            print(f"Enrollment Date: {student.enrollment_date}")
            
            if student.courses:
                print(f"Courses: {', '.join(student.courses)}")
            else:
                print("Courses: None enrolled")
                
            if student.grades:
                print("Grades:")
                for course, grade in student.grades.items():
                    print(f"  - {course}: {grade:.2f}")
            else:
                print("Grades: No grades recorded")
        else:
            print(f"\n✗ {message}")
    
    def update_student(self):
        """Update student information."""
        print("\nUPDATE STUDENT INFORMATION")
        print("-" * 30)
        
        student_id = self.get_input("Enter Student ID: ")
        student, message = self.manager.get_student(student_id)
        
        if not student:
            print(f"\n✗ {message}")
            return
        
        print(f"\nCurrent information for {student.get_full_name()}:")
        print(f"Email: {student.email}")
        print(f"Phone: {student.phone}")
        print(f"Address: {student.address or 'Not provided'}")
        print(f"Major: {student.major or 'Undeclared'}")
        
        print("\nEnter new values (leave blank to keep current value):")
        
        update_data = {}
        
        new_email = input(f"Email ({student.email}): ").strip()
        if new_email:
            update_data['email'] = new_email
        
        new_phone = input(f"Phone ({student.phone}): ").strip()
        if new_phone:
            update_data['phone'] = new_phone
        
        new_address = input(f"Address ({student.address or 'Not provided'}): ").strip()
        if new_address:
            update_data['address'] = new_address
        
        new_major = input(f"Major ({student.major or 'Undeclared'}): ").strip()
        if new_major:
            update_data['major'] = new_major
        
        if update_data:
            success, message = self.manager.update_student(student_id, update_data)
            if success:
                print(f"\n✓ {message}")
            else:
                print(f"\n✗ {message}")
        else:
            print("\nNo changes made.")
    
    def delete_student(self):
        """Delete a student from the system."""
        print("\nDELETE STUDENT")
        print("-" * 15)
        
        student_id = self.get_input("Enter Student ID: ")
        student, message = self.manager.get_student(student_id)
        
        if not student:
            print(f"\n✗ {message}")
            return
        
        print(f"\nStudent to delete: {student.get_full_name()} (ID: {student.student_id})")
        confirm = input("Are you sure you want to delete this student? (yes/no): ").strip().lower()
        
        if confirm in ['yes', 'y']:
            success, message = self.manager.delete_student(student_id)
            if success:
                print(f"\n✓ {message}")
            else:
                print(f"\n✗ {message}")
        else:
            print("\nDeletion cancelled.")
    
    def list_all_students(self):
        """List all students in the system."""
        print("\nALL STUDENTS")
        print("-" * 15)
        
        students = self.manager.list_all_students()
        
        if not students:
            print("No students found in the system.")
            return
        
        print(f"\nTotal students: {len(students)}")
        print("-" * 80)
        print(f"{'ID':<10} {'Name':<25} {'Major':<20} {'GPA':<6} {'Email':<20}")
        print("-" * 80)
        
        for student in students:
            print(f"{student.student_id:<10} {student.get_full_name():<25} "
                  f"{student.major or 'Undeclared':<20} {student.gpa:<6.2f} {student.email:<20}")
    
    def search_students(self):
        """Search for students based on criteria."""
        print("\nSEARCH STUDENTS")
        print("-" * 15)
        
        print("Search options:")
        print("1. By name")
        print("2. By major")
        print("3. By GPA range")
        print("4. By age range")
        
        choice = input("Select search option (1-4): ").strip()
        
        search_criteria = {}
        
        if choice == '1':
            name = self.get_input("Enter name (partial match): ")
            search_criteria['name'] = name
        elif choice == '2':
            major = self.get_input("Enter major (partial match): ")
            search_criteria['major'] = major
        elif choice == '3':
            min_gpa = input("Minimum GPA (optional): ").strip()
            max_gpa = input("Maximum GPA (optional): ").strip()
            if min_gpa:
                search_criteria['gpa_min'] = float(min_gpa)
            if max_gpa:
                search_criteria['gpa_max'] = float(max_gpa)
        elif choice == '4':
            min_age = input("Minimum age (optional): ").strip()
            max_age = input("Maximum age (optional): ").strip()
            if min_age:
                search_criteria['age_min'] = int(min_age)
            if max_age:
                search_criteria['age_max'] = int(max_age)
        else:
            print("Invalid choice.")
            return
        
        students, message = self.manager.search_students(search_criteria)
        
        print(f"\n{message}")
        
        if students:
            print("-" * 80)
            print(f"{'ID':<10} {'Name':<25} {'Major':<20} {'GPA':<6} {'Age':<4}")
            print("-" * 80)
            
            for student in students:
                print(f"{student.student_id:<10} {student.get_full_name():<25} "
                      f"{student.major or 'Undeclared':<20} {student.gpa:<6.2f} {student.get_age():<4}")
    
    def add_course_to_student(self):
        """Add a course to a student's course list."""
        print("\nADD COURSE TO STUDENT")
        print("-" * 22)
        
        student_id = self.get_input("Enter Student ID: ")
        course_name = self.get_input("Enter Course Name: ")
        
        success, message = self.manager.add_course_to_student(student_id, course_name)
        
        if success:
            print(f"\n✓ {message}")
        else:
            print(f"\n✗ {message}")
    
    def remove_course_from_student(self):
        """Remove a course from a student's course list."""
        print("\nREMOVE COURSE FROM STUDENT")
        print("-" * 27)
        
        student_id = self.get_input("Enter Student ID: ")
        student, _ = self.manager.get_student(student_id)
        
        if not student:
            print(f"\n✗ Student with ID {student_id} not found")
            return
        
        if not student.courses:
            print("\nThis student has no courses enrolled.")
            return
        
        print(f"\nCurrent courses for {student.get_full_name()}:")
        for i, course in enumerate(student.courses, 1):
            print(f"{i}. {course}")
        
        course_name = self.get_input("Enter Course Name to remove: ")
        
        success, message = self.manager.remove_course_from_student(student_id, course_name)
        
        if success:
            print(f"\n✓ {message}")
        else:
            print(f"\n✗ {message}")
    
    def add_grade_to_student(self):
        """Add a grade for a specific course to a student."""
        print("\nADD GRADE TO STUDENT")
        print("-" * 20)
        
        student_id = self.get_input("Enter Student ID: ")
        student, _ = self.manager.get_student(student_id)
        
        if not student:
            print(f"\n✗ Student with ID {student_id} not found")
            return
        
        if not student.courses:
            print("\nThis student has no courses enrolled. Please add courses first.")
            return
        
        print(f"\nCourses for {student.get_full_name()}:")
        for i, course in enumerate(student.courses, 1):
            grade_info = f" (Current grade: {student.grades[course]:.2f})" if course in student.grades else ""
            print(f"{i}. {course}{grade_info}")
        
        course_name = self.get_input("Enter Course Name: ")
        grade = self.get_float_input("Enter Grade (0.0-4.0): ", 0.0, 4.0)
        
        success, message = self.manager.add_grade_to_student(student_id, course_name, grade)
        
        if success:
            print(f"\n✓ {message}")
        else:
            print(f"\n✗ {message}")
    
    def view_student_transcript(self):
        """View a student's academic transcript."""
        print("\nSTUDENT TRANSCRIPT")
        print("-" * 18)
        
        student_id = self.get_input("Enter Student ID: ")
        transcript, message = self.manager.get_student_transcript(student_id)
        
        if transcript:
            info = transcript['student_info']
            print(f"\n{message}")
            print("=" * 50)
            print(f"Student ID: {info['id']}")
            print(f"Name: {info['name']}")
            print(f"Major: {info['major'] or 'Undeclared'}")
            print(f"Enrollment Date: {info['enrollment_date']}")
            print("=" * 50)
            
            print(f"\nAcademic Summary:")
            print(f"Total Courses Enrolled: {transcript['total_courses']}")
            print(f"Courses with Grades: {transcript['completed_courses']}")
            print(f"Overall GPA: {transcript['overall_gpa']:.2f}")
            
            if transcript['courses']:
                print(f"\nCourses:")
                for course in transcript['courses']:
                    grade_info = f" - Grade: {transcript['grades'][course]:.2f}" if course in transcript['grades'] else " - No grade"
                    print(f"  • {course}{grade_info}")
            else:
                print("\nNo courses enrolled.")
        else:
            print(f"\n✗ {message}")
    
    def view_statistics(self):
        """View system statistics."""
        print("\nSYSTEM STATISTICS")
        print("-" * 17)
        
        stats, message = self.manager.get_statistics()
        
        if stats:
            print(f"\n{message}")
            print("-" * 40)
            print(f"Total Students: {stats['total_students']}")
            print(f"Average GPA: {stats['average_gpa']:.2f}")
            
            print(f"\nMajor Distribution:")
            for major, count in stats['majors'].items():
                print(f"  • {major}: {count} students")
            
            print(f"\nAge Distribution:")
            for age_range, count in stats['age_distribution'].items():
                print(f"  • {age_range}: {count} students")
        else:
            print(f"\n✗ {message}")
    
    def export_data(self):
        """Export student data to CSV."""
        print("\nEXPORT DATA TO CSV")
        print("-" * 18)
        
        filename = input("Enter filename (optional, press Enter for auto-generated): ").strip()
        if not filename:
            filename = None
        
        success, message = self.manager.export_data(filename)
        
        if success:
            print(f"\n✓ {message}")
        else:
            print(f"\n✗ {message}")
    
    def import_data(self):
        """Import student data from CSV."""
        print("\nIMPORT DATA FROM CSV")
        print("-" * 20)
        
        filename = self.get_input("Enter CSV filename: ")
        
        if not os.path.exists(filename):
            print(f"\n✗ File '{filename}' not found.")
            return
        
        print(f"\nImporting data from '{filename}'...")
        success, message = self.manager.import_data(filename)
        
        if success:
            print(f"\n✓ {message}")
        else:
            print(f"\n✗ {message}")
    
    def view_top_students(self):
        """View top students by GPA."""
        print("\nTOP STUDENTS BY GPA")
        print("-" * 19)
        
        limit = input("Enter number of top students to show (default 10): ").strip()
        limit = int(limit) if limit.isdigit() else 10
        
        top_students = self.manager.get_top_students(limit)
        
        if top_students:
            print(f"\nTop {len(top_students)} students:")
            print("-" * 70)
            print(f"{'Rank':<5} {'ID':<10} {'Name':<25} {'Major':<20} {'GPA':<6}")
            print("-" * 70)
            
            for i, student in enumerate(top_students, 1):
                print(f"{i:<5} {student.student_id:<10} {student.get_full_name():<25} "
                      f"{student.major or 'Undeclared':<20} {student.gpa:<6.2f}")
        else:
            print("\nNo students with GPA records found.")
    
    def view_students_needing_attention(self):
        """View students who might need academic attention."""
        print("\nSTUDENTS NEEDING ATTENTION")
        print("-" * 26)
        
        students = self.manager.get_students_needing_attention()
        
        if students:
            print(f"\nStudents with GPA below 2.0 ({len(students)} found):")
            print("-" * 70)
            print(f"{'ID':<10} {'Name':<25} {'Major':<20} {'GPA':<6}")
            print("-" * 70)
            
            for student in students:
                print(f"{student.student_id:<10} {student.get_full_name():<25} "
                      f"{student.major or 'Undeclared':<20} {student.gpa:<6.2f}")
        else:
            print("\nNo students found with GPA below 2.0.")
    
    def run(self):
        """Run the main CLI loop."""
        while self.running:
            self.clear_screen()
            self.print_header()
            self.print_menu()
            
            try:
                choice = input("\nEnter your choice (0-15): ").strip()
                
                if choice == '0':
                    self.running = False
                    print("\nThank you for using Student Management System!")
                elif choice == '1':
                    self.add_student()
                elif choice == '2':
                    self.view_student()
                elif choice == '3':
                    self.update_student()
                elif choice == '4':
                    self.delete_student()
                elif choice == '5':
                    self.list_all_students()
                elif choice == '6':
                    self.search_students()
                elif choice == '7':
                    self.add_course_to_student()
                elif choice == '8':
                    self.remove_course_from_student()
                elif choice == '9':
                    self.add_grade_to_student()
                elif choice == '10':
                    self.view_student_transcript()
                elif choice == '11':
                    self.view_statistics()
                elif choice == '12':
                    self.export_data()
                elif choice == '13':
                    self.import_data()
                elif choice == '14':
                    self.view_top_students()
                elif choice == '15':
                    self.view_students_needing_attention()
                else:
                    print("\n✗ Invalid choice. Please select a number between 0-15.")
                
                if self.running and choice != '0':
                    self.pause()
                    
            except KeyboardInterrupt:
                print("\n\nExiting...")
                self.running = False
            except Exception as e:
                print(f"\n✗ An error occurred: {str(e)}")
                self.pause()


def main():
    """Main function to run the CLI application."""
    try:
        cli = StudentManagementCLI()
        cli.run()
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()