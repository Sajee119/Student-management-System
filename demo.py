#!/usr/bin/env python3
"""
Student Management System - Demo Script
This script demonstrates the key features of the Student Management System.
"""

from student_manager import StudentManager
from student import Student

def main():
    """Demonstrate the Student Management System functionality."""
    print("=" * 60)
    print("    STUDENT MANAGEMENT SYSTEM - DEMO")
    print("=" * 60)
    print()
    
    # Initialize the system
    print("1. Initializing Student Management System...")
    manager = StudentManager("demo_students.json")
    print("✓ System initialized successfully!")
    print()
    
    # Add sample students
    print("2. Adding sample students...")
    
    sample_students = [
        {
            'student_id': 'STU001',
            'first_name': 'Alice',
            'last_name': 'Johnson',
            'email': 'alice.johnson@university.edu',
            'phone': '(555) 123-4567',
            'date_of_birth': '2001-03-15',
            'address': '123 Campus Drive',
            'major': 'Computer Science',
            'gpa': 3.8
        },
        {
            'student_id': 'STU002',
            'first_name': 'Bob',
            'last_name': 'Smith',
            'email': 'bob.smith@university.edu',
            'phone': '(555) 234-5678',
            'date_of_birth': '2000-07-22',
            'address': '456 University Ave',
            'major': 'Mathematics',
            'gpa': 3.6
        },
        {
            'student_id': 'STU003',
            'first_name': 'Carol',
            'last_name': 'Davis',
            'email': 'carol.davis@university.edu',
            'phone': '(555) 345-6789',
            'date_of_birth': '2002-01-10',
            'address': '789 College Street',
            'major': 'Physics',
            'gpa': 3.9
        }
    ]
    
    for student_data in sample_students:
        success, message = manager.add_student(student_data)
        if success:
            print(f"✓ {message}")
        else:
            print(f"✗ {message}")
    print()
    
    # Add courses to students
    print("3. Adding courses to students...")
    courses_data = [
        ('STU001', ['Data Structures', 'Algorithms', 'Database Systems']),
        ('STU002', ['Calculus I', 'Linear Algebra', 'Statistics']),
        ('STU003', ['Classical Mechanics', 'Quantum Physics', 'Thermodynamics'])
    ]
    
    for student_id, courses in courses_data:
        for course in courses:
            success, message = manager.add_course_to_student(student_id, course)
            if success:
                print(f"✓ {message}")
    print()
    
    # Add grades
    print("4. Adding grades to students...")
    grades_data = [
        ('STU001', 'Data Structures', 3.7),
        ('STU001', 'Algorithms', 3.8),
        ('STU001', 'Database Systems', 3.9),
        ('STU002', 'Calculus I', 3.5),
        ('STU002', 'Linear Algebra', 3.7),
        ('STU002', 'Statistics', 3.6),
        ('STU003', 'Classical Mechanics', 4.0),
        ('STU003', 'Quantum Physics', 3.8),
        ('STU003', 'Thermodynamics', 3.9)
    ]
    
    for student_id, course, grade in grades_data:
        success, message = manager.add_grade_to_student(student_id, course, grade)
        if success:
            print(f"✓ Grade {grade} added for {course} to student {student_id}")
    print()
    
    # Display all students
    print("5. Listing all students:")
    students = manager.list_all_students()
    print("-" * 80)
    print(f"{'ID':<8} {'Name':<20} {'Major':<18} {'GPA':<6} {'Age':<4} {'Email':<25}")
    print("-" * 80)
    for student in students:
        print(f"{student.student_id:<8} {student.get_full_name():<20} "
              f"{student.major:<18} {student.gpa:<6.2f} {student.get_age():<4} {student.email:<25}")
    print()
    
    # Search demonstration
    print("6. Search demonstrations:")
    
    # Search by major
    print("   a) Students in Computer Science:")
    cs_students, message = manager.search_students({'major': 'Computer Science'})
    for student in cs_students:
        print(f"      - {student.get_full_name()} (GPA: {student.gpa:.2f})")
    
    # Search by GPA range
    print("   b) Students with GPA above 3.7:")
    high_gpa_students, message = manager.search_students({'gpa_min': 3.7})
    for student in high_gpa_students:
        print(f"      - {student.get_full_name()} (GPA: {student.gpa:.2f})")
    print()
    
    # Display transcript
    print("7. Sample student transcript:")
    transcript, message = manager.get_student_transcript('STU001')
    if transcript:
        info = transcript['student_info']
        print(f"   Student: {info['name']} (ID: {info['id']})")
        print(f"   Major: {info['major']}")
        print(f"   Overall GPA: {transcript['overall_gpa']:.2f}")
        print(f"   Courses and Grades:")
        for course, grade in transcript['grades'].items():
            print(f"      - {course}: {grade:.2f}")
    print()
    
    # System statistics
    print("8. System statistics:")
    stats, message = manager.get_statistics()
    if stats:
        print(f"   Total Students: {stats['total_students']}")
        print(f"   Average GPA: {stats['average_gpa']:.2f}")
        print(f"   Major Distribution:")
        for major, count in stats['majors'].items():
            print(f"      - {major}: {count} students")
        print(f"   Age Distribution:")
        for age_range, count in stats['age_distribution'].items():
            print(f"      - {age_range}: {count} students")
    print()
    
    # Top students
    print("9. Top students by GPA:")
    top_students = manager.get_top_students(3)
    for i, student in enumerate(top_students, 1):
        print(f"   {i}. {student.get_full_name()} - GPA: {student.gpa:.2f} ({student.major})")
    print()
    
    # Export demonstration
    print("10. Data export demonstration:")
    success, message = manager.export_data("demo_export.csv")
    if success:
        print(f"✓ {message}")
    else:
        print(f"✗ {message}")
    print()
    
    print("=" * 60)
    print("    DEMO COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print()
    print("Features demonstrated:")
    print("✓ Student registration with validation")
    print("✓ Course enrollment management")
    print("✓ Grade recording and GPA calculation")
    print("✓ Student listing and search functionality")
    print("✓ Academic transcript generation")
    print("✓ System statistics and analytics")
    print("✓ Data export capabilities")
    print()
    print("To run the full interactive system, execute: python3 cli.py")
    print()

if __name__ == "__main__":
    main()