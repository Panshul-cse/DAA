import json
import os

class Student:
    """Student record class"""
    def __init__(self, roll_number, name, course, cgpa):
        self.roll_number = roll_number
        self.name = name
        self.course = course
        self.cgpa = cgpa
    
    def to_dict(self):
        return {
            'roll_number': self.roll_number,
            'name': self.name,
            'course': self.course,
            'cgpa': self.cgpa
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(data['roll_number'], data['name'], data['course'], data['cgpa'])

class AVLNode:
    """AVL Tree Node"""
    def __init__(self, student):
        self.student = student
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    """AVL Tree implementation for student records"""
    
    def __init__(self):
        self.root = None
    
    def get_height(self, node):
        if not node:
            return 0
        return node.height
    
    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)
    
    def update_height(self, node):
        if node:
            node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
    
    def rotate_right(self, y):
        """LL Rotation"""
        print(f"Performing LL rotation on node {y.student.roll_number}")
        x = y.left
        T2 = x.right
        
        x.right = y
        y.left = T2
        
        self.update_height(y)
        self.update_height(x)
        
        return x
    
    def rotate_left(self, x):
        """RR Rotation"""
        print(f"Performing RR rotation on node {x.student.roll_number}")
        y = x.right
        T2 = y.left
        
        y.left = x
        x.right = T2
        
        self.update_height(x)
        self.update_height(y)
        
        return y
    
    def insert(self, root, student):
        # Standard BST insertion
        if not root:
            return AVLNode(student)
        
        if student.roll_number < root.student.roll_number:
            root.left = self.insert(root.left, student)
        elif student.roll_number > root.student.roll_number:
            root.right = self.insert(root.right, student)
        else:
            return root  # Duplicate roll numbers not allowed
        
        # Update height
        self.update_height(root)
        
        # Get balance factor
        balance = self.get_balance(root)
        
        # Left Left Case (LL)
        if balance > 1 and student.roll_number < root.left.student.roll_number:
            return self.rotate_right(root)
        
        # Right Right Case (RR)
        if balance < -1 and student.roll_number > root.right.student.roll_number:
            return self.rotate_left(root)
        
        # Left Right Case (LR)
        if balance > 1 and student.roll_number > root.left.student.roll_number:
            print(f"Performing LR rotation on node {root.student.roll_number}")
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)
        
        # Right Left Case (RL)
        if balance < -1 and student.roll_number < root.right.student.roll_number:
            print(f"Performing RL rotation on node {root.student.roll_number}")
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)
        
        return root
    
    def get_min_value_node(self, root):
        if root is None or root.left is None:
            return root
        return self.get_min_value_node(root.left)
    
    def delete(self, root, roll_number):
        if not root:
            return root
        
        if roll_number < root.student.roll_number:
            root.left = self.delete(root.left, roll_number)
        elif roll_number > root.student.roll_number:
            root.right = self.delete(root.right, roll_number)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left
            
            temp = self.get_min_value_node(root.right)
            root.student = temp.student
            root.right = self.delete(root.right, temp.student.roll_number)
        
        self.update_height(root)
        balance = self.get_balance(root)
        
        # Left Left Case
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.rotate_right(root)
        
        # Left Right Case
        if balance > 1 and self.get_balance(root.left) < 0:
            print(f"Performing LR rotation on node {root.student.roll_number}")
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)
        
        # Right Right Case
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.rotate_left(root)
        
        # Right Left Case
        if balance < -1 and self.get_balance(root.right) > 0:
            print(f"Performing RL rotation on node {root.student.roll_number}")
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)
        
        return root
    
    def search(self, root, roll_number):
        if root is None or root.student.roll_number == roll_number:
            return root
        
        if roll_number < root.student.roll_number:
            return self.search(root.left, roll_number)
        
        return self.search(root.right, roll_number)
    
    def inorder(self, root, result):
        if root:
            self.inorder(root.left, result)
            result.append(root.student)
            self.inorder(root.right, result)

class StudentRecordSystem:
    """Main system class"""
    
    def __init__(self, filename="students.json"):
        self.avl_tree = AVLTree()
        self.filename = filename
        self.load_data()
    
    def load_data(self):
        """Load student data from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    data = json.load(file)
                    for student_data in data:
                        student = Student.from_dict(student_data)
                        self.avl_tree.root = self.avl_tree.insert(self.avl_tree.root, student)
                print(f"Loaded {len(data)} records from {self.filename}")
            except Exception as e:
                print(f"Error loading data: {e}")
        else:
            print("No existing data file found. Starting fresh.")
    
    def save_data(self):
        """Save all student data to JSON file"""
        students = []
        self.avl_tree.inorder(self.avl_tree.root, students)
        
        student_dicts = [student.to_dict() for student in students]
        
        try:
            with open(self.filename, 'w') as file:
                json.dump(student_dicts, file, indent=2)
            print("Data saved successfully!")
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def add_student(self):
        """Add a new student"""
        try:
            roll_number = int(input("Enter Roll Number: "))
            
            # Check if student already exists
            if self.avl_tree.search(self.avl_tree.root, roll_number):
                print("Student with this roll number already exists!")
                return
            
            name = input("Enter Name: ")
            course = input("Enter Course: ")
            cgpa = float(input("Enter CGPA: "))
            
            student = Student(roll_number, name, course, cgpa)
            print(f"\nInserting student {roll_number}...")
            self.avl_tree.root = self.avl_tree.insert(self.avl_tree.root, student)
            self.save_data()
            print("Student added successfully!")
            
        except ValueError:
            print("Invalid input! Please enter correct data types.")
    
    def search_student(self):
        """Search for a student"""
        try:
            roll_number = int(input("Enter Roll Number to search: "))
            node = self.avl_tree.search(self.avl_tree.root, roll_number)
            
            if node:
                s = node.student
                print(f"\nStudent Found:")
                print(f"Roll Number: {s.roll_number}")
                print(f"Name: {s.name}")
                print(f"Course: {s.course}")
                print(f"CGPA: {s.cgpa}")
            else:
                print("Student not found!")
        except ValueError:
            print("Invalid roll number!")
    
    def delete_student(self):
        """Delete a student"""
        try:
            roll_number = int(input("Enter Roll Number to delete: "))
            
            if not self.avl_tree.search(self.avl_tree.root, roll_number):
                print("Student not found!")
                return
            
            print(f"\nDeleting student {roll_number}...")
            self.avl_tree.root = self.avl_tree.delete(self.avl_tree.root, roll_number)
            self.save_data()
            print("Student deleted successfully!")
            
        except ValueError:
            print("Invalid roll number!")
    
    def edit_student(self):
        """Edit student details"""
        try:
            roll_number = int(input("Enter Roll Number to edit: "))
            node = self.avl_tree.search(self.avl_tree.root, roll_number)
            
            if not node:
                print("Student not found!")
                return
            
            student = node.student
            print(f"\nCurrent details:")
            print(f"Name: {student.name}")
            print(f"Course: {student.course}")
            print(f"CGPA: {student.cgpa}")
            
            name = input(f"Enter new Name (current: {student.name}): ") or student.name
            course = input(f"Enter new Course (current: {student.course}): ") or student.course
            cgpa_input = input(f"Enter new CGPA (current: {student.cgpa}): ")
            cgpa = float(cgpa_input) if cgpa_input else student.cgpa
            
            student.name = name
            student.course = course
            student.cgpa = cgpa
            
            self.save_data()
            print("Student details updated successfully!")
            
        except ValueError:
            print("Invalid input!")
    
    def display_all_students(self):
        """Display all students in sorted order"""
        students = []
        self.avl_tree.inorder(self.avl_tree.root, students)
        
        if not students:
            print("No students found!")
            return
        
        print(f"\n{'Roll No':<10} {'Name':<20} {'Course':<15} {'CGPA':<6}")
        print("-" * 55)
        for student in students:
            print(f"{student.roll_number:<10} {student.name:<20} {student.course:<15} {student.cgpa:<6}")
    
    def run(self):
        """Main menu loop"""
        while True:
            print("\n" + "="*50)
            print("STUDENT RECORD MANAGEMENT SYSTEM")
            print("="*50)
            print("1. Add Student")
            print("2. Search Student")
            print("3. Delete Student")
            print("4. Edit Student")
            print("5. Display All Students")
            print("6. Exit")
            print("-"*50)
            
            try:
                choice = int(input("Enter your choice (1-6): "))
                
                if choice == 1:
                    self.add_student()
                elif choice == 2:
                    self.search_student()
                elif choice == 3:
                    self.delete_student()
                elif choice == 4:
                    self.edit_student()
                elif choice == 5:
                    self.display_all_students()
                elif choice == 6:
                    print("Thank you for using Student Record Management System!")
                    break
                else:
                    print("Invalid choice! Please enter 1-6.")
                    
            except ValueError:
                print("Invalid input! Please enter a number.")

if __name__ == "__main__":
    system = StudentRecordSystem()
    system.run()