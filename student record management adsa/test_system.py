from student_record_system import StudentRecordSystem, Student

def test_system():
    """Test the Student Record Management System"""
    print("Testing Student Record Management System with AVL Tree")
    print("="*60)
    
    # Create system instance
    system = StudentRecordSystem("test_students.json")
    
    # Test data
    test_students = [
        Student(101, "Alice Johnson", "Computer Science", 3.8),
        Student(105, "Bob Smith", "Mathematics", 3.6),
        Student(103, "Charlie Brown", "Physics", 3.9),
        Student(107, "Diana Prince", "Chemistry", 3.7),
        Student(102, "Eve Wilson", "Biology", 3.5)
    ]
    
    print("\n1. Adding test students (watch for rotations):")
    print("-" * 50)
    for student in test_students:
        print(f"\nAdding student {student.roll_number} ({student.name})")
        system.avl_tree.root = system.avl_tree.insert(system.avl_tree.root, student)
    
    # Save data
    system.save_data()
    
    print("\n2. Displaying all students (in-order traversal):")
    print("-" * 50)
    system.display_all_students()
    
    print("\n3. Searching for student 103:")
    print("-" * 50)
    node = system.avl_tree.search(system.avl_tree.root, 103)
    if node:
        s = node.student
        print(f"Found: {s.name} - {s.course} - CGPA: {s.cgpa}")
    
    print("\n4. Deleting student 105 (watch for rotations):")
    print("-" * 50)
    system.avl_tree.root = system.avl_tree.delete(system.avl_tree.root, 105)
    system.save_data()
    
    print("\n5. Final student list:")
    print("-" * 50)
    system.display_all_students()

if __name__ == "__main__":
    test_system()