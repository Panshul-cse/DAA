import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from student_record_system import StudentRecordSystem, Student
import datetime

class ModernStudentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎓 Student Record Management System - AVL Tree")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Configure modern style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Custom colors
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#3498db', 
            'success': '#27ae60',
            'danger': '#e74c3c',
            'warning': '#f39c12',
            'light': '#ecf0f1',
            'dark': '#34495e'
        }
        
        self.configure_styles()
        self.system = StudentRecordSystem()
        self.create_widgets()
        self.refresh_display()
    
    def configure_styles(self):
        self.style.configure('Title.TLabel', font=('Segoe UI', 24, 'bold'), 
                           foreground=self.colors['primary'], background='#f0f0f0')
        self.style.configure('Heading.TLabel', font=('Segoe UI', 12, 'bold'), 
                           foreground=self.colors['dark'])
        self.style.configure('Custom.Treeview', font=('Segoe UI', 10),
                           rowheight=25, fieldbackground='white')
        self.style.configure('Custom.Treeview.Heading', font=('Segoe UI', 11, 'bold'),
                           background=self.colors['secondary'], foreground='white')
    
    def create_widgets(self):
        # Main container
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header frame
        header_frame = tk.Frame(main_container, bg='#f0f0f0', height=80)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Title with icon
        title_label = ttk.Label(header_frame, text="🎓 Student Record Management System", 
                               style='Title.TLabel')
        title_label.pack(pady=20)
        
        subtitle_label = ttk.Label(header_frame, text="AVL Tree Implementation with Auto-Balancing", 
                                 font=('Segoe UI', 12), foreground=self.colors['secondary'])
        subtitle_label.pack()
        
        # Main content frame
        content_frame = tk.Frame(main_container, bg='#f0f0f0')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel for input
        left_panel = tk.Frame(content_frame, bg='white', relief=tk.RAISED, bd=1)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Input frame
        input_frame = tk.Frame(left_panel, bg='white', padx=20, pady=20)
        input_frame.pack(fill=tk.BOTH, expand=True)
        
        # Input header
        input_header = ttk.Label(input_frame, text="📝 Student Information", 
                               style='Heading.TLabel')
        input_header.pack(pady=(0, 20))
        
        # Input fields
        fields = [
            ("🆔 Roll Number:", "roll_entry"),
            ("👤 Name:", "name_entry"), 
            ("📚 Course:", "course_entry"),
            ("📊 CGPA:", "cgpa_entry")
        ]
        
        for label_text, entry_name in fields:
            field_frame = tk.Frame(input_frame, bg='white')
            field_frame.pack(fill=tk.X, pady=10)
            
            label = tk.Label(field_frame, text=label_text, font=('Segoe UI', 11, 'bold'),
                           bg='white', fg=self.colors['dark'])
            label.pack(anchor=tk.W)
            
            entry = tk.Entry(field_frame, font=('Segoe UI', 11), relief=tk.FLAT, 
                           bd=5, bg='#f8f9fa', width=25)
            entry.pack(fill=tk.X, pady=(5, 0))
            setattr(self, entry_name, entry)
        
        # Buttons
        button_frame = tk.Frame(input_frame, bg='white')
        button_frame.pack(fill=tk.X, pady=20)
        
        buttons = [
            ("➕ Add Student", self.add_student, self.colors['success']),
            ("🔍 Search", self.search_student, self.colors['secondary']),
            ("✏️ Update", self.update_student, self.colors['warning']),
            ("🗑️ Delete", self.delete_student, self.colors['danger']),
            ("🧹 Clear", self.clear_fields, self.colors['dark'])
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(button_frame, text=text, command=command,
                          font=('Segoe UI', 10, 'bold'), bg=color, fg='white',
                          relief=tk.FLAT, padx=15, pady=8, cursor='hand2')
            btn.pack(fill=tk.X, pady=3)
            
            # Hover effects
            def on_enter(e, btn=btn, color=color):
                btn.configure(bg=self.lighten_color(color))
            def on_leave(e, btn=btn, color=color):
                btn.configure(bg=color)
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
        
        # Right panel for display
        right_panel = tk.Frame(content_frame, bg='white', relief=tk.RAISED, bd=1)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Display frame
        display_frame = tk.Frame(right_panel, bg='white', padx=20, pady=20)
        display_frame.pack(fill=tk.BOTH, expand=True)
        
        # Display header
        display_header = ttk.Label(display_frame, text="📋 Student Records", 
                                 style='Heading.TLabel')
        display_header.pack(pady=(0, 15))
        
        # Treeview
        tree_frame = tk.Frame(display_frame, bg='white')
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("Roll No", "Name", "Course", "CGPA")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", 
                               style='Custom.Treeview', height=20)
        
        # Configure columns
        column_configs = [
            ("Roll No", "🆔 Roll No", 120),
            ("Name", "👤 Name", 200), 
            ("Course", "📚 Course", 180),
            ("CGPA", "📊 CGPA", 100)
        ]
        
        for col, heading, width in column_configs:
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=width, anchor=tk.CENTER)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        self.tree.bind("<ButtonRelease-1>", self.on_select)
        
        # Row colors
        self.tree.tag_configure('oddrow', background='#f8f9fa')
        self.tree.tag_configure('evenrow', background='white')
        
        # Operations log
        log_container = tk.Frame(main_container, bg='white', relief=tk.RAISED, bd=1)
        log_container.pack(fill=tk.X, pady=(10, 0))
        
        log_frame = tk.Frame(log_container, bg='white', padx=20, pady=15)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        log_header = ttk.Label(log_frame, text="🔄 AVL Tree Operations Log", 
                             style='Heading.TLabel')
        log_header.pack(pady=(0, 10))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=6, width=80,
                                                font=('Consolas', 10), bg='#2c3e50', 
                                                fg='#ecf0f1', insertbackground='white')
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Welcome message
        self.log_operation("🎓 Welcome to Student Record Management System!")
        self.log_operation("🌳 AVL Tree operations will be displayed here...")
    
    def lighten_color(self, color):
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        lighter_rgb = tuple(min(255, int(c * 1.2)) for c in rgb)
        return f"#{lighter_rgb[0]:02x}{lighter_rgb[1]:02x}{lighter_rgb[2]:02x}"
    
    def log_operation(self, message):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, formatted_message)
        self.log_text.see(tk.END)
    
    def add_student(self):
        try:
            roll_number = int(self.roll_entry.get())
            name = self.name_entry.get().strip()
            course = self.course_entry.get().strip()
            cgpa = float(self.cgpa_entry.get())
            
            if not name or not course:
                messagebox.showerror("❌ Error", "Please fill all fields!")
                return
            
            if self.system.avl_tree.search(self.system.avl_tree.root, roll_number):
                messagebox.showerror("❌ Error", "Student with this roll number already exists!")
                return
            
            student = Student(roll_number, name, course, cgpa)
            self.log_operation(f"Adding student {roll_number} ({name})...")
            
            # Capture rotations
            import io, sys
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
            messagebox.showinfo("✅ Success", "Student added successfully!")
            
        except ValueError:
            messagebox.showerror("❌ Error", "Please enter valid data!")
    
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
                messagebox.showinfo("✅ Found", f"Student found: {student.name}")
            else:
                messagebox.showwarning("⚠️ Not Found", "Student not found!")
                self.log_operation(f"Student {roll_number} not found")
                
        except ValueError:
            messagebox.showerror("❌ Error", "Please enter a valid roll number!")
    
    def update_student(self):
        try:
            roll_number = int(self.roll_entry.get())
            node = self.system.avl_tree.search(self.system.avl_tree.root, roll_number)
            
            if not node:
                messagebox.showerror("❌ Error", "Student not found!")
                return
            
            name = self.name_entry.get().strip()
            course = self.course_entry.get().strip()
            cgpa = float(self.cgpa_entry.get())
            
            if not name or not course:
                messagebox.showerror("❌ Error", "Please fill all fields!")
                return
            
            student = node.student
            student.name = name
            student.course = course
            student.cgpa = cgpa
            
            self.system.save_data()
            self.log_operation(f"Updated student {roll_number}")
            self.refresh_display()
            messagebox.showinfo("✅ Success", "Student updated successfully!")
            
        except ValueError:
            messagebox.showerror("❌ Error", "Please enter valid data!")
    
    def delete_student(self):
        try:
            roll_number = int(self.roll_entry.get())
            
            if not self.system.avl_tree.search(self.system.avl_tree.root, roll_number):
                messagebox.showerror("❌ Error", "Student not found!")
                return
            
            result = messagebox.askyesno("🗑️ Confirm Delete", f"Delete student {roll_number}?")
            if result:
                self.log_operation(f"Deleting student {roll_number}...")
                
                # Capture rotations
                import io, sys
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
                messagebox.showinfo("✅ Success", "Student deleted successfully!")
                
        except ValueError:
            messagebox.showerror("❌ Error", "Please enter a valid roll number!")
    
    def clear_fields(self):
        self.roll_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.course_entry.delete(0, tk.END)
        self.cgpa_entry.delete(0, tk.END)
    
    def refresh_display(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        students = []
        self.system.avl_tree.inorder(self.system.avl_tree.root, students)
        
        for i, student in enumerate(students):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert("", tk.END, values=(
                student.roll_number, student.name, student.course, student.cgpa
            ), tags=(tag,))
        
        if students:
            self.log_operation(f"📊 Displaying {len(students)} student records")
    
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
    app = ModernStudentGUI(root)
    root.mainloop()