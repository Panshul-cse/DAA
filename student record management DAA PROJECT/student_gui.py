import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from student_record_system import StudentRecordSystem, Student

class StudentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Record Management System - AVL Tree")
        self.root.geometry("800x600")
        
        self.system = StudentRecordSystem()
        
        self.create_widgets()
        self.refresh_display()
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Student Record Management System", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Input frame
        input_frame = ttk.LabelFrame(main_frame, text="Student Information", padding="10")
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Input fields
        ttk.Label(input_frame, text="Roll Number:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.roll_entry = ttk.Entry(input_frame, width=20)
        self.roll_entry.grid(row=0, column=1, pady=5, padx=(10, 0))
        
        ttk.Label(input_frame, text="Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(input_frame, width=20)
        self.name_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        ttk.Label(input_frame, text="Course:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.course_entry = ttk.Entry(input_frame, width=20)
        self.course_entry.grid(row=2, column=1, pady=5, padx=(10, 0))
        
        ttk.Label(input_frame, text="CGPA:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.cgpa_entry = ttk.Entry(input_frame, width=20)
        self.cgpa_entry.grid(row=3, column=1, pady=5, padx=(10, 0))
        
        # Buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Add Student", command=self.add_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Search", command=self.search_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Update", command=self.update_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete", command=self.delete_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_fields).pack(side=tk.LEFT, padx=5)
        
        # Display frame
        display_frame = ttk.LabelFrame(main_frame, text="Student Records", padding="10")
        display_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Treeview for displaying students
        columns = ("Roll No", "Name", "Course", "CGPA")
        self.tree = ttk.Treeview(display_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(display_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.tree.bind("<ButtonRelease-1>", self.on_select)
        
        # Operations log
        log_frame = ttk.LabelFrame(main_frame, text="AVL Tree Operations Log", padding="10")
        log_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        display_frame.columnconfigure(0, weight=1)
        display_frame.rowconfigure(0, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
    
    def log_operation(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
    
    def add_student(self):
        try:
            roll_number = int(self.roll_entry.get())
            name = self.name_entry.get().strip()
            course = self.course_entry.get().strip()
            cgpa = float(self.cgpa_entry.get())
            
            if not name or not course:
                messagebox.showerror("Error", "Please fill all fields!")
                return
            
            if self.system.avl_tree.search(self.system.avl_tree.root, roll_number):
                messagebox.showerror("Error", "Student with this roll number already exists!")
                return
            
            student = Student(roll_number, name, course, cgpa)
            self.log_operation(f"Adding student {roll_number} ({name})...")
            
            # Capture rotation messages
            import io
            import sys
            old_stdout = sys.stdout
            sys.stdout = captured_output = io.StringIO()
            
            self.system.avl_tree.root = self.system.avl_tree.insert(self.system.avl_tree.root, student)
            
            sys.stdout = old_stdout
            rotation_output = captured_output.getvalue()
            
            if rotation_output:
                self.log_operation(rotation_output.strip())
            
            self.system.save_data()
            self.log_operation("Student added successfully!")
            
            self.clear_fields()
            self.refresh_display()
            messagebox.showinfo("Success", "Student added successfully!")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid data!")
    
    def search_student(self):
        try:
            roll_number = int(self.roll_entry.get())
            node = self.system.avl_tree.search(self.system.avl_tree.root, roll_number)
            
            if node:
                student = node.student
                self.name_entry.delete(0, tk.END)
                self.name_entry.insert(0, student.name)
                self.course_entry.delete(0, tk.END)
                self.course_entry.insert(0, student.course)
                self.cgpa_entry.delete(0, tk.END)
                self.cgpa_entry.insert(0, str(student.cgpa))
                
                self.log_operation(f"Found student: {student.name}")
                messagebox.showinfo("Found", f"Student found: {student.name}")
            else:
                messagebox.showwarning("Not Found", "Student not found!")
                self.log_operation(f"Student {roll_number} not found")
                
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid roll number!")
    
    def update_student(self):
        try:
            roll_number = int(self.roll_entry.get())
            node = self.system.avl_tree.search(self.system.avl_tree.root, roll_number)
            
            if not node:
                messagebox.showerror("Error", "Student not found!")
                return
            
            name = self.name_entry.get().strip()
            course = self.course_entry.get().strip()
            cgpa = float(self.cgpa_entry.get())
            
            if not name or not course:
                messagebox.showerror("Error", "Please fill all fields!")
                return
            
            student = node.student
            student.name = name
            student.course = course
            student.cgpa = cgpa
            
            self.system.save_data()
            self.log_operation(f"Updated student {roll_number}")
            self.refresh_display()
            messagebox.showinfo("Success", "Student updated successfully!")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid data!")
    
    def delete_student(self):
        try:
            roll_number = int(self.roll_entry.get())
            
            if not self.system.avl_tree.search(self.system.avl_tree.root, roll_number):
                messagebox.showerror("Error", "Student not found!")
                return
            
            result = messagebox.askyesno("Confirm", f"Delete student {roll_number}?")
            if result:
                self.log_operation(f"Deleting student {roll_number}...")
                
                # Capture rotation messages
                import io
                import sys
                old_stdout = sys.stdout
                sys.stdout = captured_output = io.StringIO()
                
                self.system.avl_tree.root = self.system.avl_tree.delete(self.system.avl_tree.root, roll_number)
                
                sys.stdout = old_stdout
                rotation_output = captured_output.getvalue()
                
                if rotation_output:
                    self.log_operation(rotation_output.strip())
                
                self.system.save_data()
                self.log_operation("Student deleted successfully!")
                
                self.clear_fields()
                self.refresh_display()
                messagebox.showinfo("Success", "Student deleted successfully!")
                
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid roll number!")
    
    def clear_fields(self):
        self.roll_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.course_entry.delete(0, tk.END)
        self.cgpa_entry.delete(0, tk.END)
    
    def refresh_display(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get all students
        students = []
        self.system.avl_tree.inorder(self.system.avl_tree.root, students)
        
        # Insert students into treeview
        for student in students:
            self.tree.insert("", tk.END, values=(
                student.roll_number, student.name, student.course, student.cgpa
            ))
    
    def on_select(self, event):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            
            self.roll_entry.delete(0, tk.END)
            self.roll_entry.insert(0, str(values[0]))
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, values[1])
            self.course_entry.delete(0, tk.END)
            self.course_entry.insert(0, values[2])
            self.cgpa_entry.delete(0, tk.END)
            self.cgpa_entry.insert(0, str(values[3]))

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentGUI(root)
    root.mainloop()