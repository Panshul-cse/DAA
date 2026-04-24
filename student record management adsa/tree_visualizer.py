import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from student_record_system import StudentRecordSystem, Student
import math

class TreeVisualizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🌳 AVL Tree Visualizer - Student Management System")
        self.root.geometry("1600x1000")
        self.root.configure(bg='#1a1a1a')
        
        self.system = StudentRecordSystem()
        self.colors = {
            'bg': '#1a1a1a',
            'sidebar': '#2d2d2d', 
            'content': '#0f0f0f',
            'card': '#333333',
            'primary': '#00ff88',
            'secondary': '#0088ff',
            'text': '#ffffff',
            'node': '#4a90e2',
            'node_text': '#ffffff',
            'edge': '#666666'
        }
        
        self.create_interface()
        
    def create_interface(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left sidebar for controls
        sidebar = tk.Frame(main_frame, bg=self.colors['sidebar'], width=350)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        # Title
        title_frame = tk.Frame(sidebar, bg=self.colors['sidebar'])
        title_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(title_frame, text="🌳 AVL TREE", font=('Arial', 20, 'bold'),
                bg=self.colors['sidebar'], fg=self.colors['primary']).pack()
        tk.Label(title_frame, text="VISUALIZER", font=('Arial', 16, 'bold'),
                bg=self.colors['sidebar'], fg=self.colors['text']).pack()
        
        # Student form
        form_frame = tk.LabelFrame(sidebar, text="Student Operations", 
                                  bg=self.colors['sidebar'], fg=self.colors['text'],
                                  font=('Arial', 12, 'bold'), padx=10, pady=10)
        form_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Input fields
        fields = [("Roll Number:", "roll_entry"), ("Name:", "name_entry"), 
                 ("Course:", "course_entry"), ("CGPA:", "cgpa_entry")]
        
        for label_text, attr in fields:
            tk.Label(form_frame, text=label_text, bg=self.colors['sidebar'], 
                    fg=self.colors['text'], font=('Arial', 10)).pack(anchor='w')
            entry = tk.Entry(form_frame, bg=self.colors['card'], fg=self.colors['text'],
                           font=('Arial', 10), relief=tk.FLAT, bd=3)
            entry.pack(fill=tk.X, pady=(2, 8))
            setattr(self, attr, entry)
        
        # Buttons
        btn_frame = tk.Frame(form_frame, bg=self.colors['sidebar'])
        btn_frame.pack(fill=tk.X, pady=10)
        
        buttons = [
            ("➕ INSERT", self.insert_student, self.colors['primary']),
            ("🗑️ DELETE", self.delete_student, '#ff4444'),
            ("🔍 SEARCH", self.search_student, self.colors['secondary']),
            ("🧹 CLEAR", self.clear_fields, '#888888')
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(btn_frame, text=text, command=command, bg=color, fg='black',
                          font=('Arial', 9, 'bold'), relief=tk.FLAT, pady=5)
            btn.pack(fill=tk.X, pady=2)
        
        # Tree info
        info_frame = tk.LabelFrame(sidebar, text="Tree Information", 
                                  bg=self.colors['sidebar'], fg=self.colors['text'],
                                  font=('Arial', 12, 'bold'), padx=10, pady=10)
        info_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.info_text = tk.Text(info_frame, height=8, bg=self.colors['card'], 
                               fg=self.colors['text'], font=('Consolas', 9))
        self.info_text.pack(fill=tk.BOTH, expand=True)
        
        # Operations log
        log_frame = tk.LabelFrame(sidebar, text="Operations Log", 
                                 bg=self.colors['sidebar'], fg=self.colors['text'],
                                 font=('Arial', 12, 'bold'), padx=10, pady=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, bg=self.colors['card'], 
                                                fg=self.colors['text'], font=('Consolas', 8))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Right side - Tree visualization
        viz_frame = tk.Frame(main_frame, bg=self.colors['content'])
        viz_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Canvas for tree drawing
        canvas_frame = tk.Frame(viz_frame, bg=self.colors['content'])
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.canvas = tk.Canvas(canvas_frame, bg=self.colors['content'], 
                              highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Initial display
        self.update_display()
        
    def draw_tree(self):
        self.canvas.delete("all")
        
        if not self.system.avl_tree.root:
            # Draw empty tree message
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            self.canvas.create_text(canvas_width//2, canvas_height//2,
                                  text="🌱 EMPTY TREE\nInsert students to see visualization",
                                  fill=self.colors['text'], font=('Arial', 16, 'bold'),
                                  justify=tk.CENTER)
            return
        
        # Calculate tree dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            self.root.after(100, self.draw_tree)
            return
        
        # Draw the tree
        self.draw_node(self.system.avl_tree.root, canvas_width//2, 80, 
                      canvas_width//4, 0)
        
    def draw_node(self, node, x, y, x_offset, level):
        if not node:
            return
        
        node_radius = 25
        
        # Draw edges to children first (so they appear behind nodes)
        if node.left:
            child_x = x - x_offset
            child_y = y + 80
            self.canvas.create_line(x, y + node_radius, child_x, child_y - node_radius,
                                  fill=self.colors['edge'], width=2)
            self.draw_node(node.left, child_x, child_y, x_offset//2, level + 1)
        
        if node.right:
            child_x = x + x_offset
            child_y = y + 80
            self.canvas.create_line(x, y + node_radius, child_x, child_y - node_radius,
                                  fill=self.colors['edge'], width=2)
            self.draw_node(node.right, child_x, child_y, x_offset//2, level + 1)
        
        # Draw the node
        self.canvas.create_oval(x - node_radius, y - node_radius,
                              x + node_radius, y + node_radius,
                              fill=self.colors['node'], outline=self.colors['primary'], width=2)
        
        # Draw node text (roll number)
        self.canvas.create_text(x, y - 5, text=str(node.student.roll_number),
                              fill=self.colors['node_text'], font=('Arial', 10, 'bold'))
        
        # Draw balance factor
        balance = self.system.avl_tree.get_balance(node)
        bf_color = self.colors['primary'] if abs(balance) <= 1 else '#ff4444'
        self.canvas.create_text(x, y + 8, text=f"BF:{balance}",
                              fill=bf_color, font=('Arial', 8))
        
        # Draw height
        self.canvas.create_text(x, y + 35, text=f"H:{node.height}",
                              fill=self.colors['text'], font=('Arial', 8))
        
        # Draw student name below node
        self.canvas.create_text(x, y + 50, text=node.student.name[:8],
                              fill=self.colors['text'], font=('Arial', 8))
    
    def insert_student(self):
        try:
            roll = int(self.roll_entry.get())
            name = self.name_entry.get().strip()
            course = self.course_entry.get().strip()
            cgpa = float(self.cgpa_entry.get())
            
            if not name or not course:
                messagebox.showerror("Error", "Please fill all fields!")
                return
            
            if self.system.avl_tree.search(self.system.avl_tree.root, roll):
                messagebox.showerror("Error", "Student already exists!")
                return
            
            student = Student(roll, name, course, cgpa)
            
            # Capture rotation output
            import io, sys
            old_stdout = sys.stdout
            sys.stdout = captured = io.StringIO()
            
            self.system.avl_tree.root = self.system.avl_tree.insert(self.system.avl_tree.root, student)
            
            sys.stdout = old_stdout
            rotation_output = captured.getvalue()
            
            self.system.save_data()
            
            # Log operation
            self.log_operation(f"✅ INSERTED: {roll} - {name}")
            if rotation_output:
                self.log_operation(f"🔄 {rotation_output.strip()}")
            
            self.clear_fields()
            self.update_display()
            
        except ValueError:
            messagebox.showerror("Error", "Invalid input data!")
    
    def delete_student(self):
        try:
            roll = int(self.roll_entry.get())
            
            if not self.system.avl_tree.search(self.system.avl_tree.root, roll):
                messagebox.showerror("Error", "Student not found!")
                return
            
            # Capture rotation output
            import io, sys
            old_stdout = sys.stdout
            sys.stdout = captured = io.StringIO()
            
            self.system.avl_tree.root = self.system.avl_tree.delete(self.system.avl_tree.root, roll)
            
            sys.stdout = old_stdout
            rotation_output = captured.getvalue()
            
            self.system.save_data()
            
            # Log operation
            self.log_operation(f"❌ DELETED: {roll}")
            if rotation_output:
                self.log_operation(f"🔄 {rotation_output.strip()}")
            
            self.clear_fields()
            self.update_display()
            
        except ValueError:
            messagebox.showerror("Error", "Invalid roll number!")
    
    def search_student(self):
        try:
            roll = int(self.roll_entry.get())
            node = self.system.avl_tree.search(self.system.avl_tree.root, roll)
            
            if node:
                student = node.student
                self.name_entry.delete(0, tk.END)
                self.name_entry.insert(0, student.name)
                self.course_entry.delete(0, tk.END)
                self.course_entry.insert(0, student.course)
                self.cgpa_entry.delete(0, tk.END)
                self.cgpa_entry.insert(0, str(student.cgpa))
                
                self.log_operation(f"🔍 FOUND: {roll} - {student.name}")
                messagebox.showinfo("Found", f"Student: {student.name}\nCourse: {student.course}\nCGPA: {student.cgpa}")
            else:
                self.log_operation(f"❌ NOT FOUND: {roll}")
                messagebox.showwarning("Not Found", "Student not found!")
                
        except ValueError:
            messagebox.showerror("Error", "Invalid roll number!")
    
    def clear_fields(self):
        for entry in [self.roll_entry, self.name_entry, self.course_entry, self.cgpa_entry]:
            entry.delete(0, tk.END)
    
    def log_operation(self, message):
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
    
    def update_tree_info(self):
        students = []
        self.system.avl_tree.inorder(self.system.avl_tree.root, students)
        
        info = f"""
🌳 TREE STATISTICS

📊 Total Nodes: {len(students)}
📏 Tree Height: {self.system.avl_tree.get_height(self.system.avl_tree.root)}
🍃 Leaf Nodes: {self.count_leaf_nodes()}
⚖️ Balanced: {'✅ Yes' if self.is_balanced() else '❌ No'}

📚 COURSES:
"""
        
        if students:
            courses = {}
            for student in students:
                courses[student.course] = courses.get(student.course, 0) + 1
            
            for course, count in courses.items():
                info += f"• {course}: {count}\n"
            
            avg_cgpa = sum(s.cgpa for s in students) / len(students)
            info += f"\n📊 Average CGPA: {avg_cgpa:.2f}"
        else:
            info += "No students in system"
        
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, info)
    
    def count_leaf_nodes(self):
        def count_leaves(node):
            if not node:
                return 0
            if not node.left and not node.right:
                return 1
            return count_leaves(node.left) + count_leaves(node.right)
        return count_leaves(self.system.avl_tree.root)
    
    def is_balanced(self):
        def check_balance(node):
            if not node:
                return True
            balance = self.system.avl_tree.get_balance(node)
            if abs(balance) > 1:
                return False
            return check_balance(node.left) and check_balance(node.right)
        return check_balance(self.system.avl_tree.root)
    
    def update_display(self):
        self.root.after(100, self.draw_tree)  # Small delay to ensure canvas is ready
        self.update_tree_info()

if __name__ == "__main__":
    root = tk.Tk()
    app = TreeVisualizerGUI(root)
    root.mainloop()