import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from student_record_system import StudentRecordSystem, Student
import datetime

class CompleteDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("🎓 Student Management Dashboard with AVL Tree Visualization")
        self.root.geometry("1600x1000")
        self.root.configure(bg='#ffffff')
        
        self.system = StudentRecordSystem()
        
        # Settings
        self.settings = {
            'font_size': 10,
            'node_size': 30,
            'theme': 'light'
        }
        
        self.colors = {
            'bg': '#f8f9fa',
            'sidebar': '#2c3e50', 
            'content': '#ffffff',
            'card': '#ffffff',
            'primary': '#2c3e50',
            'accent': '#3498db',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'text': '#2c3e50',
            'node': '#3498db',
            'edge': '#2c3e50'
        }
        
        self.create_dashboard()
        
    def create_dashboard(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar
        sidebar = tk.Frame(main_frame, bg=self.colors['sidebar'], width=300)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        # Logo
        logo_frame = tk.Frame(sidebar, bg=self.colors['sidebar'])
        logo_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(logo_frame, text="🎓", font=('Arial', 30), 
                bg=self.colors['sidebar'], fg=self.colors['primary']).pack()
        tk.Label(logo_frame, text="STUDENT DASHBOARD", font=('Arial', 12, 'bold'),
                bg=self.colors['sidebar'], fg=self.colors['text']).pack()
        
        # Navigation
        nav_frame = tk.Frame(sidebar, bg=self.colors['sidebar'])
        nav_frame.pack(fill=tk.X, padx=20, pady=20)
        
        nav_buttons = [
            ("■ DASHBOARD", self.show_dashboard),
            ("■ TREE VIEW", self.show_tree_view),
            ("■ STUDENTS", self.show_students),
            ("■ AVL THEORY", self.show_theory),
            ("■ ANALYTICS", self.show_analytics),
            ("⚙️ SETTINGS", self.show_settings)
        ]
        
        for text, command in nav_buttons:
            btn = tk.Button(nav_frame, text=text, command=command,
                          font=('Consolas', 11, 'bold'), bg=self.colors['card'], 
                          fg=self.colors['text'], relief=tk.FLAT, pady=12, anchor='w')
            btn.pack(fill=tk.X, pady=2)
        
        # Content area
        self.content_frame = tk.Frame(main_frame, bg='#f8f9fa')
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Show dashboard by default
        self.show_dashboard()
        
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
    def show_dashboard(self):
        self.clear_content()
        
        # Header with welcome message
        header = tk.Frame(self.content_frame, bg='#ffffff')
        header.pack(fill=tk.X, padx=30, pady=20)
        
        welcome_frame = tk.Frame(header, bg='#3498db', relief=tk.FLAT)
        welcome_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(welcome_frame, text="🎓 Welcome to Student Management System", 
                font=('Segoe UI', 18, 'bold'), bg='#3498db', fg='#ffffff').pack(pady=15)
        tk.Label(welcome_frame, text="Manage students efficiently with AVL Tree data structure", 
                font=('Segoe UI', 11), bg='#3498db', fg='#ecf0f1').pack(pady=(0, 15))
        
        # Main content container
        main_container = tk.Frame(self.content_frame, bg='#ffffff')
        main_container.pack(fill=tk.BOTH, expand=True, padx=30)
        
        # Left column - Stats and Quick Actions
        left_column = tk.Frame(main_container, bg='#ffffff')
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        # Stats cards
        stats_frame = tk.Frame(left_column, bg='#ffffff')
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        students = []
        self.system.avl_tree.inorder(self.system.avl_tree.root, students)
        
        stats = [
            ("STUDENTS", len(students), '👥', '#3498db'),
            ("COURSES", len(set(s.course for s in students)) if students else 0, '📚', '#27ae60')
        ]
        
        for label, value, icon, color in stats:
            card = tk.Frame(stats_frame, bg=color, relief=tk.FLAT)
            card.pack(side=tk.LEFT, padx=(0, 15), pady=10)
            
            tk.Label(card, text=icon, font=('Segoe UI', 25), bg=color, fg='#ffffff').pack(pady=(15, 5))
            tk.Label(card, text=str(value), font=('Segoe UI', 24, 'bold'), bg=color, fg='#ffffff').pack()
            tk.Label(card, text=label, font=('Segoe UI', 10, 'bold'), bg=color, fg='#ffffff').pack(pady=(5, 15), padx=20)
        
        # Quick Actions Panel
        actions_frame = tk.LabelFrame(left_column, text="⚡ Quick Actions", 
                                     font=('Segoe UI', 12, 'bold'), bg='#ffffff', fg='#2c3e50')
        actions_frame.pack(fill=tk.X, pady=(0, 20))
        
        actions = [
            ("👥 Manage Students", self.show_students, '#3498db'),
            ("🌳 View Tree", self.show_tree_view, '#27ae60'),
            ("📊 Analytics", self.show_analytics, '#f39c12')
        ]
        
        for text, command, color in actions:
            btn = tk.Button(actions_frame, text=text, command=command, bg=color, fg='#ffffff',
                          font=('Segoe UI', 11, 'bold'), relief=tk.FLAT, pady=12, cursor='hand2')
            btn.pack(fill=tk.X, padx=15, pady=5)
        
        # System Status Panel
        status_frame = tk.LabelFrame(left_column, text="📊 System Status", 
                                    font=('Segoe UI', 12, 'bold'), bg='#ffffff', fg='#2c3e50')
        status_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tree health indicator
        health_frame = tk.Frame(status_frame, bg='#ffffff')
        health_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tree_balanced = self.is_balanced()
        health_color = '#27ae60' if tree_balanced else '#e74c3c'
        health_text = 'BALANCED' if tree_balanced else 'UNBALANCED'
        health_icon = '✅' if tree_balanced else '❌'
        
        tk.Label(health_frame, text=f"{health_icon} Tree Status: {health_text}", 
                font=('Segoe UI', 11, 'bold'), bg='#ffffff', fg=health_color).pack(anchor='w')
        
        # Performance metrics
        metrics = [
            (f"Tree Height: {self.system.avl_tree.get_height(self.system.avl_tree.root)}", '#34495e'),
            (f"Total Nodes: {len(students)}", '#34495e'),
            (f"Avg CGPA: {sum(s.cgpa for s in students)/len(students):.2f}" if students else "Avg CGPA: 0.00", '#34495e')
        ]
        
        for metric, color in metrics:
            tk.Label(status_frame, text=f"• {metric}", font=('Segoe UI', 10), 
                    bg='#ffffff', fg=color).pack(anchor='w', padx=15, pady=2)
        
        # Right column - Recent Activity and Preview
        right_column = tk.Frame(main_container, bg='#ffffff')
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(15, 0))
        
        # Recent Students Preview
        preview_frame = tk.LabelFrame(right_column, text="👥 Recent Students", 
                                     font=('Segoe UI', 12, 'bold'), bg='#ffffff', fg='#2c3e50')
        preview_frame.pack(fill=tk.X, pady=(0, 20))
        
        if students:
            recent_students = students[-3:] if len(students) >= 3 else students
            for student in recent_students:
                student_card = tk.Frame(preview_frame, bg='#ecf0f1', relief=tk.FLAT)
                student_card.pack(fill=tk.X, padx=15, pady=5)
                
                tk.Label(student_card, text=f"🎓 {student.name}", 
                        font=('Segoe UI', 10, 'bold'), bg='#ecf0f1', fg='#2c3e50').pack(anchor='w', padx=10, pady=5)
                tk.Label(student_card, text=f"Roll: {student.roll_number} | Course: {student.course} | CGPA: {student.cgpa}", 
                        font=('Segoe UI', 9), bg='#ecf0f1', fg='#7f8c8d').pack(anchor='w', padx=10, pady=(0, 5))
        else:
            tk.Label(preview_frame, text="No students added yet", 
                    font=('Segoe UI', 10), bg='#ffffff', fg='#7f8c8d').pack(padx=15, pady=10)
        
        # Feature Highlights
        features_frame = tk.LabelFrame(right_column, text="✨ Key Features", 
                                      font=('Segoe UI', 12, 'bold'), bg='#ffffff', fg='#2c3e50')
        features_frame.pack(fill=tk.BOTH, expand=True)
        
        features = [
            "🌳 Self-balancing AVL Tree structure",
            "⚡ O(log n) search, insert, delete operations", 
            "🔄 Automatic tree rotations (LL, RR, LR, RL)",
            "💾 Persistent JSON data storage",
            "📊 Real-time analytics and statistics",
            "🔍 Interactive tree visualization"
        ]
        
        for feature in features:
            feature_frame = tk.Frame(features_frame, bg='#ffffff')
            feature_frame.pack(fill=tk.X, padx=15, pady=3)
            tk.Label(feature_frame, text=feature, font=('Segoe UI', 10), 
                    bg='#ffffff', fg='#2c3e50').pack(anchor='w')
    
    def show_tree_view(self):
        self.clear_content()
        
        # Header
        header = tk.Frame(self.content_frame, bg=self.colors['content'])
        header.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(header, text="🌳 AVL TREE VISUALIZATION", font=('Consolas', 24, 'bold'),
                bg=self.colors['content'], fg=self.colors['primary']).pack(anchor='w')
        
        # Main content with tree and controls
        main_content = tk.Frame(self.content_frame, bg=self.colors['content'])
        main_content.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Left side - Tree canvas
        tree_frame = tk.Frame(main_content, bg=self.colors['card'], relief=tk.RAISED, bd=1)
        tree_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        tree_header = tk.Frame(tree_frame, bg=self.colors['card'])
        tree_header.pack(fill=tk.X, pady=10)
        
        tk.Label(tree_header, text="■ TREE STRUCTURE", font=('Consolas', 14, 'bold'),
                bg=self.colors['card'], fg=self.colors['primary']).pack(side=tk.LEFT, padx=20)
        
        tk.Button(tree_header, text="🔍 FULLSCREEN", command=self.open_fullscreen_tree,
                 bg=self.colors['success'], fg='black', font=('Consolas', 9, 'bold'),
                 relief=tk.FLAT, padx=10).pack(side=tk.RIGHT, padx=20)
        
        self.canvas = tk.Canvas(tree_frame, bg='#f8f9fa', height=600, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Bind canvas events for interactivity
        self.canvas.bind("<Button-1>", self.on_node_click)
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.selected_node = None
        
        # Right side - Controls and info
        control_frame = tk.Frame(main_content, bg=self.colors['card'], width=350, relief=tk.RAISED, bd=1)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y)
        control_frame.pack_propagate(False)
        
        # Student form
        form_frame = tk.Frame(control_frame, bg=self.colors['card'])
        form_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(form_frame, text="■ STUDENT OPERATIONS", font=('Consolas', 12, 'bold'),
                bg=self.colors['card'], fg=self.colors['primary']).pack(pady=(0, 10))
        
        # Input fields
        fields = [("Roll Number:", "roll_entry"), ("Name:", "name_entry"), 
                 ("Course:", "course_entry"), ("CGPA:", "cgpa_entry")]
        
        for label_text, attr in fields:
            tk.Label(form_frame, text=label_text, bg=self.colors['card'], 
                    fg=self.colors['text'], font=('Consolas', 9)).pack(anchor='w')
            entry = tk.Entry(form_frame, bg=self.colors['bg'], fg=self.colors['text'],
                           font=('Consolas', 9), relief=tk.FLAT, bd=3,
                           insertbackground='white')
            entry.pack(fill=tk.X, pady=(2, 8))
            setattr(self, attr, entry)
        
        # Buttons
        btn_frame = tk.Frame(form_frame, bg=self.colors['card'])
        btn_frame.pack(fill=tk.X, pady=10)
        
        buttons = [
            ("INSERT", self.insert_student, self.colors['success']),
            ("DELETE", self.delete_student, self.colors['danger']),
            ("SEARCH", self.search_student, self.colors['warning']),
            ("CLEAR", self.clear_fields, self.colors['accent'])
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(btn_frame, text=text, command=command, bg=color, fg='black',
                          font=('Consolas', 8, 'bold'), relief=tk.FLAT, pady=3)
            btn.pack(fill=tk.X, pady=1)
        
        # Tree info
        info_frame = tk.Frame(control_frame, bg=self.colors['card'])
        info_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        tk.Label(info_frame, text="■ TREE INFO", font=('Consolas', 12, 'bold'),
                bg=self.colors['card'], fg=self.colors['primary']).pack(pady=(0, 10))
        
        self.info_text = tk.Text(info_frame, height=8, bg=self.colors['bg'], 
                               fg=self.colors['text'], font=('Consolas', 8),
                               relief=tk.SOLID, bd=1)
        self.info_text.pack(fill=tk.BOTH, expand=True)
        
        # Operations log
        tk.Label(info_frame, text="■ OPERATIONS LOG", font=('Consolas', 10, 'bold'),
                bg=self.colors['card'], fg=self.colors['primary']).pack(pady=(10, 5))
        
        self.log_text = scrolledtext.ScrolledText(info_frame, height=6, bg=self.colors['bg'], 
                                                fg=self.colors['text'], font=('Consolas', 7),
                                                relief=tk.SOLID, bd=1)
        self.log_text.pack(fill=tk.X)
        
        # Draw initial tree
        self.draw_tree()
        self.update_tree_info()
        
    def draw_tree(self):
        self.canvas.delete("all")
        
        if not self.system.avl_tree.root:
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            self.canvas.create_text(canvas_width//2, canvas_height//2,
                                  text="🌱 EMPTY TREE\nInsert students to visualize",
                                  fill=self.colors['text'], font=('Consolas', 14, 'bold'),
                                  justify=tk.CENTER)
            return
        
        canvas_width = self.canvas.winfo_width()
        if canvas_width <= 1:
            self.root.after(100, self.draw_tree)
            return
        
        # Draw tree starting from root with better spacing
        self.draw_node(self.system.avl_tree.root, canvas_width//2, 80, canvas_width//3)
        
    def draw_node(self, node, x, y, x_offset):
        if not node:
            return
        
        node_radius = self.settings['node_size']
        
        # Draw edges with high contrast
        if node.left:
            child_x = x - x_offset
            child_y = y + 90
            self.canvas.create_line(x, y + node_radius, child_x, child_y - node_radius,
                                  fill='#2c3e50', width=5, smooth=True)
            self.draw_node(node.left, child_x, child_y, x_offset//2)
        
        if node.right:
            child_x = x + x_offset
            child_y = y + 90
            self.canvas.create_line(x, y + node_radius, child_x, child_y - node_radius,
                                  fill='#2c3e50', width=5, smooth=True)
            self.draw_node(node.right, child_x, child_y, x_offset//2)
        
        # Draw shadow
        self.canvas.create_oval(x - node_radius + 3, y - node_radius + 3,
                              x + node_radius + 3, y + node_radius + 3,
                              fill='#bdc3c7', outline='')
        
        # Draw main node circle
        self.canvas.create_oval(x - node_radius, y - node_radius,
                              x + node_radius, y + node_radius,
                              fill='#3498db', outline='#2c3e50', width=4)
        
        # Inner highlight
        self.canvas.create_oval(x - node_radius + 6, y - node_radius + 6,
                              x + node_radius - 6, y + node_radius - 6,
                              fill='#5dade2', outline='')
        
        # Roll number
        self.canvas.create_text(x, y - 5, text=str(node.student.roll_number),
                              fill='#ffffff', font=('Segoe UI', self.settings['font_size'] + 4, 'bold'))
        
        # Balance factor
        balance = self.system.avl_tree.get_balance(node)
        bf_color = '#27ae60' if abs(balance) <= 1 else '#e74c3c'
        
        self.canvas.create_rectangle(x - 18, y + 2, x + 18, y + 18,
                                   fill=bf_color, outline='', width=0)
        self.canvas.create_text(x, y + 10, text=f"BF:{balance}",
                              fill='#ffffff', font=('Segoe UI', self.settings['font_size'] - 1, 'bold'))
        
        # Height
        self.canvas.create_rectangle(x - 15, y + 38, x + 15, y + 54,
                                   fill='#34495e', outline='', width=0)
        self.canvas.create_text(x, y + 46, text=f"H:{node.height}",
                              fill='#ffffff', font=('Segoe UI', self.settings['font_size'] - 1, 'bold'))
        
        # Name
        name_text = node.student.name[:8]
        name_width = len(name_text) * 5
        self.canvas.create_rectangle(x - name_width, y + 60, 
                                   x + name_width, y + 76,
                                   fill='#ecf0f1', outline='#bdc3c7', width=2)
        self.canvas.create_text(x, y + 68, text=name_text,
                              fill='#2c3e50', font=('Segoe UI', self.settings['font_size'], 'bold'))
    
    def insert_student(self):
        try:
            roll = int(self.roll_entry.get())
            name = self.name_entry.get().strip()
            course = self.course_entry.get().strip()
            cgpa = float(self.cgpa_entry.get())
            
            if not name or not course:
                messagebox.showerror("Error", "Fill all fields!")
                return
            
            if cgpa < 0 or cgpa > 10.0:
                messagebox.showerror("Error", "CGPA must be between 0 and 10.0!")
                return
            
            student = Student(roll, name, course, cgpa)
            
            # Capture rotations
            import io, sys
            old_stdout = sys.stdout
            sys.stdout = captured = io.StringIO()
            
            self.system.avl_tree.root = self.system.avl_tree.insert(self.system.avl_tree.root, student)
            
            sys.stdout = old_stdout
            rotation_output = captured.getvalue()
            
            self.system.save_data()
            
            self.log_operation(f"✅ INSERTED: {roll} - {name}")
            if rotation_output:
                self.log_operation(f"🔄 {rotation_output.strip()}")
            
            self.clear_fields()
            self.draw_tree()
            self.update_tree_info()
            
        except ValueError:
            messagebox.showerror("Error", "Invalid data!")
    
    def delete_student(self):
        try:
            roll = int(self.roll_entry.get())
            
            # Capture rotations
            import io, sys
            old_stdout = sys.stdout
            sys.stdout = captured = io.StringIO()
            
            self.system.avl_tree.root = self.system.avl_tree.delete(self.system.avl_tree.root, roll)
            
            sys.stdout = old_stdout
            rotation_output = captured.getvalue()
            
            self.system.save_data()
            
            self.log_operation(f"❌ DELETED: {roll}")
            if rotation_output:
                self.log_operation(f"🔄 {rotation_output.strip()}")
            
            self.clear_fields()
            self.draw_tree()
            self.update_tree_info()
            
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
            else:
                self.log_operation(f"❌ NOT FOUND: {roll}")
                messagebox.showwarning("Not Found", "Student not found!")
                
        except ValueError:
            messagebox.showerror("Error", "Invalid roll number!")
    
    def clear_fields(self):
        for entry in [self.roll_entry, self.name_entry, self.course_entry, self.cgpa_entry]:
            entry.delete(0, tk.END)
    
    def log_operation(self, message):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
    
    def open_fullscreen_tree(self):
        # Create fullscreen window
        fullscreen_window = tk.Toplevel(self.root)
        fullscreen_window.title("🌳 AVL Tree - Fullscreen View")
        fullscreen_window.geometry("1400x900")
        fullscreen_window.configure(bg=self.colors['bg'])
        
        # Header with controls
        header_frame = tk.Frame(fullscreen_window, bg=self.colors['sidebar'], height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="🌳 AVL TREE VISUALIZATION - INTERACTIVE MODE", 
                font=('Consolas', 18, 'bold'), bg=self.colors['sidebar'], 
                fg=self.colors['primary']).pack(side=tk.LEFT, padx=20, pady=15)
        
        tk.Button(header_frame, text="❌ CLOSE", command=fullscreen_window.destroy,
                 bg=self.colors['danger'], fg='white', font=('Consolas', 10, 'bold'),
                 relief=tk.FLAT, padx=15).pack(side=tk.RIGHT, padx=20, pady=15)
        
        # Main canvas
        canvas_frame = tk.Frame(fullscreen_window, bg=self.colors['content'])
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        fullscreen_canvas = tk.Canvas(canvas_frame, bg=self.colors['content'])
        fullscreen_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Info panel
        info_panel = tk.Frame(fullscreen_window, bg=self.colors['sidebar'], height=100)
        info_panel.pack(fill=tk.X)
        info_panel.pack_propagate(False)
        
        self.fs_info_label = tk.Label(info_panel, text="Click on any node to see details", 
                                     font=('Consolas', 12), bg=self.colors['sidebar'], 
                                     fg=self.colors['text'])
        self.fs_info_label.pack(pady=20)
        
        # Bind events
        fullscreen_canvas.bind("<Button-1>", lambda e: self.on_fullscreen_click(e, fullscreen_canvas))
        fullscreen_canvas.bind("<Motion>", lambda e: self.on_fullscreen_hover(e, fullscreen_canvas))
        
        # Draw tree on fullscreen canvas
        self.draw_fullscreen_tree(fullscreen_canvas)
        
    def draw_fullscreen_tree(self, canvas):
        canvas.delete("all")
        
        if not self.system.avl_tree.root:
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()
            canvas.create_text(canvas_width//2, canvas_height//2,
                             text="🌱 EMPTY TREE\nInsert students to visualize",
                             fill=self.colors['text'], font=('Consolas', 20, 'bold'),
                             justify=tk.CENTER)
            return
        
        canvas.update()
        canvas_width = canvas.winfo_width()
        if canvas_width <= 1:
            canvas.after(100, lambda: self.draw_fullscreen_tree(canvas))
            return
        
        # Draw with larger spacing for fullscreen
        self.draw_fullscreen_node(canvas, self.system.avl_tree.root, 
                                canvas_width//2, 100, canvas_width//3)
        
    def draw_fullscreen_node(self, canvas, node, x, y, x_offset):
        if not node:
            return
        
        node_radius = self.settings['node_size'] + 10  # Larger nodes for fullscreen
        
        # Draw edges
        if node.left:
            child_x = x - x_offset
            child_y = y + 120
            canvas.create_line(x, y + node_radius, child_x, child_y - node_radius,
                             fill='#000000', width=4, smooth=True)
            self.draw_fullscreen_node(canvas, node.left, child_x, child_y, x_offset//2)
        
        if node.right:
            child_x = x + x_offset
            child_y = y + 120
            canvas.create_line(x, y + node_radius, child_x, child_y - node_radius,
                             fill='#000000', width=4, smooth=True)
            self.draw_fullscreen_node(canvas, node.right, child_x, child_y, x_offset//2)
        
        # Store node position for click detection
        node_id = f"node_{node.student.roll_number}"
        
        # Draw shadow
        canvas.create_oval(x - node_radius + 3, y - node_radius + 3,
                         x + node_radius + 3, y + node_radius + 3,
                         fill='#cccccc', outline='', tags=node_id)
        
        # Draw node
        canvas.create_oval(x - node_radius, y - node_radius,
                         x + node_radius, y + node_radius,
                         fill='#4169e1', outline='#000000', width=4, tags=node_id)
        
        # Inner circle
        canvas.create_oval(x - node_radius + 8, y - node_radius + 8,
                         x + node_radius - 8, y + node_radius - 8,
                         fill='#1e90ff', outline='', tags=node_id)
        
        # Roll number
        canvas.create_text(x, y - 8, text=str(node.student.roll_number),
                         fill='#ffffff', font=('Arial', self.settings['font_size'] + 6, 'bold'), tags=node_id)
        
        # Balance factor
        balance = self.system.avl_tree.get_balance(node)
        bf_color = '#008000' if abs(balance) <= 1 else '#dc143c'
        canvas.create_rectangle(x - 20, y + 5, x + 20, y + 20,
                              fill='#ffffff', outline=bf_color, width=2, tags=node_id)
        canvas.create_text(x, y + 12, text=f"BF:{balance}",
                         fill=bf_color, font=('Arial', self.settings['font_size'], 'bold'), tags=node_id)
        
        # Height
        canvas.create_rectangle(x - 15, y + 50, x + 15, y + 65,
                              fill='#ffffff', outline='#000000', width=2, tags=node_id)
        canvas.create_text(x, y + 57, text=f"H:{node.height}",
                         fill='#000000', font=('Arial', self.settings['font_size'], 'bold'), tags=node_id)
        
        # Name
        name_text = node.student.name[:10]
        canvas.create_rectangle(x - len(name_text)*5, y + 75, 
                              x + len(name_text)*5, y + 90,
                              fill='#f0f0f0', outline='#000000', width=2, tags=node_id)
        canvas.create_text(x, y + 82, text=name_text,
                         fill='#000000', font=('Arial', self.settings['font_size'] + 1, 'bold'), tags=node_id)
        
        # Store node data for interaction
        canvas.node_data = getattr(canvas, 'node_data', {})
        canvas.node_data[node_id] = {
            'student': node.student,
            'balance': balance,
            'height': node.height,
            'x': x, 'y': y, 'radius': node_radius
        }
    
    def on_fullscreen_click(self, event, canvas):
        # Find clicked node
        clicked_items = canvas.find_overlapping(event.x-5, event.y-5, event.x+5, event.y+5)
        
        for item in clicked_items:
            tags = canvas.gettags(item)
            for tag in tags:
                if tag.startswith('node_'):
                    node_data = canvas.node_data.get(tag)
                    if node_data:
                        student = node_data['student']
                        info_text = f"""SELECTED NODE: {student.roll_number}
                        
Student: {student.name}
Course: {student.course}
CGPA: {student.cgpa}
Balance Factor: {node_data['balance']}
Height: {node_data['height']}"""
                        self.fs_info_label.configure(text=info_text)
                        
                        # Highlight selected node
                        canvas.delete("highlight")
                        canvas.create_oval(node_data['x'] - node_data['radius'] - 5,
                                         node_data['y'] - node_data['radius'] - 5,
                                         node_data['x'] + node_data['radius'] + 5,
                                         node_data['y'] + node_data['radius'] + 5,
                                         outline='#ffff00', width=5, tags="highlight")
                    return
    
    def on_fullscreen_hover(self, event, canvas):
        # Change cursor on hover
        hovered_items = canvas.find_overlapping(event.x-5, event.y-5, event.x+5, event.y+5)
        
        for item in hovered_items:
            tags = canvas.gettags(item)
            for tag in tags:
                if tag.startswith('node_'):
                    canvas.configure(cursor="hand2")
                    return
        
        canvas.configure(cursor="")
    
    def on_node_click(self, event):
        # Handle node clicks in regular view
        clicked_items = self.canvas.find_overlapping(event.x-5, event.y-5, event.x+5, event.y+5)
        # Simple click handling for regular view
        pass
    
    def on_mouse_move(self, event):
        # Handle mouse movement in regular view
        pass
    
    def update_tree_info(self):
        students = []
        self.system.avl_tree.inorder(self.system.avl_tree.root, students)
        
        info = f"""TREE STATISTICS:

Nodes: {len(students)}
Height: {self.system.avl_tree.get_height(self.system.avl_tree.root)}
Balanced: {'✅' if self.is_balanced() else '❌'}

STUDENTS:
"""
        
        for student in students:
            info += f"{student.roll_number}: {student.name}\n"
        
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, info)
    
    def is_balanced(self):
        def check_balance(node):
            if not node:
                return True
            balance = self.system.avl_tree.get_balance(node)
            if abs(balance) > 1:
                return False
            return check_balance(node.left) and check_balance(node.right)
        return check_balance(self.system.avl_tree.root)
    
    def show_students(self):
        self.clear_content()
        
        header = tk.Frame(self.content_frame, bg=self.colors['content'])
        header.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(header, text="■ STUDENT RECORDS", font=('Consolas', self.settings['font_size'] + 14, 'bold'),
                bg=self.colors['content'], fg=self.colors['primary']).pack(anchor='w')
        
        # Modern table container
        table_container = tk.Frame(self.content_frame, bg='#f8f9fa')
        table_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        table_frame = tk.Frame(table_container, bg='#ffffff', relief=tk.FLAT, bd=0)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Shadow effect
        shadow = tk.Frame(table_container, bg='#bdc3c7', height=3)
        shadow.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Configure treeview style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Students.Treeview', 
                       background='#ffffff',
                       foreground='#2c3e50',
                       fieldbackground='#ffffff',
                       borderwidth=2,
                       relief='solid',
                       rowheight=35)
        style.configure('Students.Treeview.Heading',
                       background='#3498db',
                       foreground='#ffffff',
                       font=('Segoe UI', 13, 'bold'),
                       borderwidth=2,
                       relief='flat')
        style.map('Students.Treeview',
                 background=[('selected', '#3498db')],
                 foreground=[('selected', '#ffffff')])
        
        # Create treeview with scrollbars
        tree_container = tk.Frame(table_frame, bg=self.colors['card'])
        tree_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        columns = ("Roll No", "Student Name", "Course", "CGPA")
        tree = ttk.Treeview(tree_container, columns=columns, show="headings", 
                           style='Students.Treeview', height=20)
        
        # Configure columns with proper widths and separators
        tree.heading("Roll No", text="ROLL NUMBER")
        tree.heading("Student Name", text="STUDENT NAME")
        tree.heading("Course", text="COURSE")
        tree.heading("CGPA", text="CGPA")
        
        tree.column("Roll No", width=120, anchor='center', minwidth=100)
        tree.column("Student Name", width=200, anchor='w', minwidth=150)
        tree.column("Course", width=180, anchor='center', minwidth=120)
        tree.column("CGPA", width=100, anchor='center', minwidth=80)
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(tree_container, orient=tk.VERTICAL, command=tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_container, orient=tk.HORIZONTAL, command=tree.xview)
        tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout for tree and scrollbars
        tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)
        
        # Configure alternating row colors with high contrast
        tree.tag_configure('oddrow', background='#ecf0f1', foreground='#2c3e50')
        tree.tag_configure('evenrow', background='#ffffff', foreground='#2c3e50')
        
        # Populate table with alternating colors
        students = []
        self.system.avl_tree.inorder(self.system.avl_tree.root, students)
        
        for i, student in enumerate(students):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            tree.insert("", tk.END, values=(
                student.roll_number, student.name, student.course, student.cgpa
            ), tags=(tag,))
        
        # Modern summary cards
        summary_frame = tk.Frame(table_frame, bg='#ffffff')
        summary_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        total_card = tk.Frame(summary_frame, bg='#3498db', relief=tk.FLAT)
        total_card.pack(side=tk.LEFT, padx=(0, 10))
        tk.Label(total_card, text=f"📊 {len(students)}", 
                font=('Segoe UI', 14, 'bold'), bg='#3498db', 
                fg='#ffffff', padx=15, pady=8).pack()
        tk.Label(total_card, text="Total Students", 
                font=('Segoe UI', 8), bg='#3498db', 
                fg='#ffffff').pack(padx=15, pady=(0, 8))
        
        if students:
            avg_cgpa = sum(s.cgpa for s in students) / len(students)
            avg_card = tk.Frame(summary_frame, bg='#27ae60', relief=tk.FLAT)
            avg_card.pack(side=tk.RIGHT, padx=(10, 0))
            tk.Label(avg_card, text=f"🎯 {avg_cgpa:.2f}", 
                    font=('Segoe UI', 14, 'bold'), bg='#27ae60', 
                    fg='#ffffff', padx=15, pady=8).pack()
            tk.Label(avg_card, text="Average CGPA", 
                    font=('Segoe UI', 8), bg='#27ae60', 
                    fg='#ffffff').pack(padx=15, pady=(0, 8))
    
    def show_theory(self):
        self.clear_content()
        
        header = tk.Frame(self.content_frame, bg=self.colors['content'])
        header.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(header, text="■ AVL TREE THEORY", font=('Consolas', self.settings['font_size'] + 14, 'bold'),
                bg=self.colors['content'], fg=self.colors['primary']).pack(anchor='w')
        
        theory_text = scrolledtext.ScrolledText(self.content_frame, bg=self.colors['card'], 
                                              fg=self.colors['text'], font=('Consolas', 11))
        theory_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        theory_content = """
■ AVL TREE FUNDAMENTALS

DEFINITION:
• Self-balancing binary search tree
• Height difference between left and right subtrees ≤ 1
• Named after Adelson-Velsky and Landis (1962)

BALANCE FACTOR:
• BF = Height(Left Subtree) - Height(Right Subtree)
• Valid values: -1, 0, +1
• If |BF| > 1, rotation is required

ROTATIONS:
• LL Case → Right Rotation
• RR Case → Left Rotation  
• LR Case → Left-Right Rotation
• RL Case → Right-Left Rotation

TIME COMPLEXITY:
• Search: O(log n)
• Insert: O(log n)
• Delete: O(log n)
• Space: O(n)

ADVANTAGES:
• Guaranteed logarithmic operations
• Self-balancing property
• Efficient for frequent searches
• Maintains sorted order in in-order traversal

APPLICATIONS:
• Database indexing
• Memory management
• Expression parsing
• File systems
        """
        
        theory_text.insert(tk.END, theory_content)
        theory_text.config(state=tk.DISABLED)
    
    def show_analytics(self):
        self.clear_content()
        
        header = tk.Frame(self.content_frame, bg=self.colors['content'])
        header.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(header, text="■ SYSTEM ANALYTICS", font=('Consolas', self.settings['font_size'] + 14, 'bold'),
                bg=self.colors['content'], fg=self.colors['primary']).pack(anchor='w')
        
        students = []
        self.system.avl_tree.inorder(self.system.avl_tree.root, students)
        
        if students:
            # Course distribution
            courses = {}
            cgpa_ranges = {"3.5-4.0": 0, "3.0-3.5": 0, "2.5-3.0": 0, "Below 2.5": 0}
            
            for student in students:
                courses[student.course] = courses.get(student.course, 0) + 1
                
                if student.cgpa >= 3.5:
                    cgpa_ranges["3.5-4.0"] += 1
                elif student.cgpa >= 3.0:
                    cgpa_ranges["3.0-3.5"] += 1
                elif student.cgpa >= 2.5:
                    cgpa_ranges["2.5-3.0"] += 1
                else:
                    cgpa_ranges["Below 2.5"] += 1
            
            # Display analytics
            analytics_frame = tk.Frame(self.content_frame, bg=self.colors['card'])
            analytics_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            analytics_text = scrolledtext.ScrolledText(analytics_frame, bg=self.colors['bg'], 
                                                     fg=self.colors['text'], font=('Consolas', 12))
            analytics_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            analytics_content = f"""
■ COURSE DISTRIBUTION:
"""
            for course, count in courses.items():
                analytics_content += f"• {course}: {count} students\n"
            
            analytics_content += f"""
■ CGPA DISTRIBUTION:
"""
            for range_name, count in cgpa_ranges.items():
                analytics_content += f"• {range_name}: {count} students\n"
            
            analytics_content += f"""
■ TREE METRICS:
• Total Students: {len(students)}
• Tree Height: {self.system.avl_tree.get_height(self.system.avl_tree.root)}
• Average CGPA: {sum(s.cgpa for s in students)/len(students):.2f}
• Balanced: {'Yes' if self.is_balanced() else 'No'}
            """
            
            analytics_text.insert(tk.END, analytics_content)
            analytics_text.config(state=tk.DISABLED)
    
    def show_settings(self):
        self.clear_content()
        
        header = tk.Frame(self.content_frame, bg=self.colors['content'])
        header.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(header, text="⚙️ SETTINGS", font=('Consolas', self.settings['font_size'] + 14, 'bold'),
                bg=self.colors['content'], fg=self.colors['primary']).pack(anchor='w')
        
        # Settings panel
        settings_frame = tk.Frame(self.content_frame, bg=self.colors['card'], relief=tk.RAISED, bd=2)
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Font size setting
        font_frame = tk.Frame(settings_frame, bg=self.colors['card'])
        font_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(font_frame, text="Font Size:", font=('Consolas', 12, 'bold'),
                bg=self.colors['card'], fg=self.colors['text']).pack(side=tk.LEFT)
        
        font_var = tk.IntVar(value=self.settings['font_size'])
        font_scale = tk.Scale(font_frame, from_=8, to=20, orient=tk.HORIZONTAL,
                             variable=font_var, bg=self.colors['card'], fg=self.colors['text'],
                             command=lambda v: self.update_font_size(int(v)))
        font_scale.pack(side=tk.LEFT, padx=20)
        
        tk.Label(font_frame, text=f"Current: {self.settings['font_size']}", 
                font=('Consolas', 10), bg=self.colors['card'], fg=self.colors['text']).pack(side=tk.LEFT)
        
        # Node size setting
        node_frame = tk.Frame(settings_frame, bg=self.colors['card'])
        node_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(node_frame, text="Node Size:", font=('Consolas', 12, 'bold'),
                bg=self.colors['card'], fg=self.colors['text']).pack(side=tk.LEFT)
        
        node_var = tk.IntVar(value=self.settings['node_size'])
        node_scale = tk.Scale(node_frame, from_=20, to=50, orient=tk.HORIZONTAL,
                             variable=node_var, bg=self.colors['card'], fg=self.colors['text'],
                             command=lambda v: self.update_node_size(int(v)))
        node_scale.pack(side=tk.LEFT, padx=20)
        
        tk.Label(node_frame, text=f"Current: {self.settings['node_size']}", 
                font=('Consolas', 10), bg=self.colors['card'], fg=self.colors['text']).pack(side=tk.LEFT)
        
        # Apply button
        apply_frame = tk.Frame(settings_frame, bg=self.colors['card'])
        apply_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Button(apply_frame, text="✅ APPLY CHANGES", command=self.apply_settings,
                 bg=self.colors['success'], fg='white', font=('Consolas', 12, 'bold'),
                 relief=tk.FLAT, padx=20, pady=10).pack()
        
        # Reset button
        tk.Button(apply_frame, text="🔄 RESET TO DEFAULT", command=self.reset_settings,
                 bg=self.colors['warning'], fg='black', font=('Consolas', 12, 'bold'),
                 relief=tk.FLAT, padx=20, pady=10).pack(pady=10)
    
    def update_font_size(self, size):
        self.settings['font_size'] = size
    
    def update_node_size(self, size):
        self.settings['node_size'] = size
    
    def apply_settings(self):
        messagebox.showinfo("Settings", "Settings applied successfully! Go to Tree View to see changes.")
    
    def reset_settings(self):
        self.settings = {
            'font_size': 10,
            'node_size': 30,
            'theme': 'light'
        }
        messagebox.showinfo("Settings", "Settings reset to default!")
        self.show_settings()  # Refresh settings page

if __name__ == "__main__":
    root = tk.Tk()
    app = CompleteDashboard(root)
    root.mainloop()