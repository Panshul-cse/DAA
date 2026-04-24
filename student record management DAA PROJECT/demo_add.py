from student_record_system import StudentRecordSystem, Student

# Create system instance
system = StudentRecordSystem()

# Add a new student
print("Adding new student...")
student = Student(201, "John Doe", "Computer Science", 3.75)
print(f"Inserting student {student.roll_number} ({student.name})")
system.avl_tree.root = system.avl_tree.insert(system.avl_tree.root, student)
system.save_data()
print("Student added successfully!")

# Display all students
print("\nAll students:")
system.display_all_students()