import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from student_record_system import StudentRecordSystem, Student
import datetime

class DashboardGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎓 Student Management Dashboard - AVL Tree System")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1e1e2e')
        
        self.system = StudentRecordSystem()
        self.setup_styles()
        self.create_dashboard()
        
    def setup_styles(self):
        self.colors = {
            'bg': '#1e1e2e',
            'sidebar': '#313244', 
            'content': '#181825',
            'card': '#45475a',
            'primary': '#89b4fa',
            'success': '#a6e3a1',
            'warning': '#f9e2af',
            'danger': '#f38ba8',
            'text': '#cdd6f4',
            'accent': '#b4befe'
        }
        
    def create_dashboard(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar
        sidebar = tk.Frame(main_frame, bg=self.colors['sidebar'], width=250)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        # Logo/Title
        title_frame = tk.Frame(sidebar, bg=self.colors['sidebar'])
        title_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(title_frame, text="🎓", font=('Arial', 30), 
                bg=self.colors['sidebar'], fg=self.colors['primary']).pack()
        tk.Label(title_frame, text="Student Dashboard", font=('Segoe UI', 14, 'bold'),
                bg=self.colors['sidebar'], fg=self.colors['text']).pack()
        
        # Navigation buttons
        nav_frame = tk.Frame(sidebar, bg=self.colors['sidebar'])
        nav_frame.pack(fill=tk.X, padx=20, pady=20)
        
        nav_buttons = [
            ("📊 Dashboard", self.show_dashboard),
            ("👥 Students", self.show_students),
            ("🌳 AVL Theory", self.show_avl_theory),
            ("⚙️ Implementation", self.show_implementation),
            ("📈 Analytics", self.show_analytics)
        ]
        
        self.nav_buttons = []
        for text, command in nav_buttons:
            btn = tk.Button(nav_frame, text=text, command=command,
                          font=('Segoe UI', 11), bg=self.colors['card'], fg=self.colors['text'],
                          relief=tk.FLAT, pady=12, anchor='w', cursor='hand2')
            btn.pack(fill=tk.X, pady=2)
            self.nav_buttons.append(btn)
            
        # Content area
        self.content_frame = tk.Frame(main_frame, bg=self.colors['content'])
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Show dashboard by default
        self.show_dashboard()
        
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
    def create_card(self, parent, title, content_func):
        card = tk.Frame(parent, bg=self.colors['card'], relief=tk.RAISED, bd=1)
        card.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Card header
        header = tk.Frame(card, bg=self.colors['card'])
        header.pack(fill=tk.X, padx=15, pady=(15, 5))
        
        tk.Label(header, text=title, font=('Segoe UI', 14, 'bold'),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w')
        
        # Card content
        content = tk.Frame(card, bg=self.colors['card'])
        content.pack(fill=tk.BOTH, expand=True, padx=15, pady=(5, 15))
        
        content_func(content)
        return card
        
    def show_dashboard(self):
        self.clear_content()
        
        # Header
        header = tk.Frame(self.content_frame, bg=self.colors['content'])
        header.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(header, text="📊 Dashboard Overview", font=('Segoe UI', 20, 'bold'),
                bg=self.colors['content'], fg=self.colors['text']).pack(anchor='w')
        
        # Stats cards
        stats_frame = tk.Frame(self.content_frame, bg=self.colors['content'])
        stats_frame.pack(fill=tk.X, padx=20)
        
        students = []
        self.system.avl_tree.inorder(self.system.avl_tree.root, students)
        
        stats = [
            ("👥 Total Students", len(students), self.colors['primary']),
            ("📚 Courses", len(set(s.course for s in students)), self.colors['success']),
            ("📊 Avg CGPA", f"{sum(s.cgpa for s in students)/len(students):.2f}" if students else "0.00", self.colors['warning']),
            ("🌳 Tree Height", self.get_tree_height(), self.colors['danger'])
        ]
        
        for i, (title, value, color) in enumerate(stats):
            stat_card = tk.Frame(stats_frame, bg=color, width=200, height=100)
            stat_card.pack(side=tk.LEFT, padx=10, pady=10)
            stat_card.pack_propagate(False)
            
            tk.Label(stat_card, text=str(value), font=('Segoe UI', 24, 'bold'),
                    bg=color, fg='white').pack(expand=True)
            tk.Label(stat_card, text=title, font=('Segoe UI', 10),
                    bg=color, fg='white').pack()
                    
    def show_students(self):
        self.clear_content()
        
        # Header
        header = tk.Frame(self.content_frame, bg=self.colors['content'])
        header.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(header, text="👥 Student Management", font=('Segoe UI', 20, 'bold'),
                bg=self.colors['content'], fg=self.colors['text']).pack(anchor='w')
        
        # Main content
        main_content = tk.Frame(self.content_frame, bg=self.colors['content'])
        main_content.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Input form
        self.create_card(main_content, "📝 Add/Edit Student", self.create_student_form)
        
        # Student list
        self.create_card(main_content, "📋 Student Records", self.create_student_list)
        
        # Operations log
        self.create_card(main_content, "🔄 AVL Operations Log", self.create_operations_log)
        
    def create_student_form(self, parent):
        form_frame = tk.Frame(parent, bg=self.colors['card'])
        form_frame.pack(fill=tk.X)
        
        # Input fields
        fields = [("Roll Number:", "roll_entry"), ("Name:", "name_entry"), 
                 ("Course:", "course_entry"), ("CGPA:", "cgpa_entry")]
        
        for i, (label, attr) in enumerate(fields):
            row = tk.Frame(form_frame, bg=self.colors['card'])
            row.pack(fill=tk.X, pady=5)
            
            tk.Label(row, text=label, font=('Segoe UI', 10), width=12,
                    bg=self.colors['card'], fg=self.colors['text'], anchor='w').pack(side=tk.LEFT)
            
            entry = tk.Entry(row, font=('Segoe UI', 10), bg=self.colors['bg'], 
                           fg=self.colors['text'], relief=tk.FLAT, bd=5)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
            setattr(self, attr, entry)
        
        # Buttons
        btn_frame = tk.Frame(form_frame, bg=self.colors['card'])
        btn_frame.pack(fill=tk.X, pady=10)
        
        buttons = [("Add", self.add_student, self.colors['success']),
                  ("Update", self.update_student, self.colors['warning']),
                  ("Delete", self.delete_student, self.colors['danger']),
                  ("Clear", self.clear_fields, self.colors['primary'])]
        
        for text, cmd, color in buttons:
            tk.Button(btn_frame, text=text, command=cmd, bg=color, fg='white',
                     font=('Segoe UI', 9, 'bold'), relief=tk.FLAT, padx=15).pack(side=tk.LEFT, padx=5)
    
    def create_student_list(self, parent):
        # Treeview
        self.tree = ttk.Treeview(parent, columns=("Roll", "Name", "Course", "CGPA"), 
                               show="headings", height=15)
        
        for col in ["Roll", "Name", "Course", "CGPA"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<ButtonRelease-1>", self.on_select)
        self.refresh_tree()
        
    def create_operations_log(self, parent):
        self.log_text = scrolledtext.ScrolledText(parent, height=8, bg=self.colors['bg'],
                                                fg=self.colors['text'], font=('Consolas', 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
    def show_avl_theory(self):
        self.clear_content()
        
        # Header
        header = tk.Frame(self.content_frame, bg=self.colors['content'])
        header.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(header, text="🌳 AVL Tree Theory", font=('Segoe UI', 20, 'bold'),
                bg=self.colors['content'], fg=self.colors['text']).pack(anchor='w')
        
        # Scrollable content
        canvas = tk.Canvas(self.content_frame, bg=self.colors['content'])
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['content'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Theory content
        theory_sections = [
            ("📖 What is an AVL Tree?", 
             "An AVL tree is a self-balancing binary search tree where the heights of the two child subtrees of any node differ by at most one. Named after Adelson-Velsky and Landis."),
            
            ("⚖️ Balance Factor",
             "Balance Factor = Height(Left Subtree) - Height(Right Subtree)\nValid values: -1, 0, +1\nIf |BF| > 1, rotation is needed."),
            
            ("🔄 Rotations",
             "Four types of rotations:\n• LL Rotation (Right Rotation)\n• RR Rotation (Left Rotation)\n• LR Rotation (Left-Right)\n• RL Rotation (Right-Left)"),
            
            ("⏱️ Time Complexity",
             "• Search: O(log n)\n• Insert: O(log n)\n• Delete: O(log n)\n• Space: O(n)"),
            
            ("✅ Advantages",
             "• Guaranteed O(log n) operations\n• Self-balancing\n• Efficient for frequent searches\n• Maintains sorted order")
        ]
        
        for title, content in theory_sections:
            self.create_theory_card(scrollable_frame, title, content)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20)
        scrollbar.pack(side="right", fill="y")
        
    def create_theory_card(self, parent, title, content):
        card = tk.Frame(parent, bg=self.colors['card'], relief=tk.RAISED, bd=1)
        card.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(card, text=title, font=('Segoe UI', 14, 'bold'),
                bg=self.colors['card'], fg=self.colors['primary']).pack(anchor='w', padx=15, pady=(15, 5))
        
        tk.Label(card, text=content, font=('Segoe UI', 11), justify=tk.LEFT,
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', padx=15, pady=(5, 15))
    
    def show_implementation(self):
        self.clear_content()
        
        # Header
        header = tk.Frame(self.content_frame, bg=self.colors['content'])
        header.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(header, text="⚙️ Project Implementation", font=('Segoe UI', 20, 'bold'),
                bg=self.colors['content'], fg=self.colors['text']).pack(anchor='w')
        
        # Implementation details
        impl_text = scrolledtext.ScrolledText(self.content_frame, bg=self.colors['card'], 
                                            fg=self.colors['text'], font=('Consolas', 10))
        impl_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        implementation_details = """
🏗️ PROJECT ARCHITECTURE

📁 File Structure:
├── student_record_system.py    # Core AVL implementation
├── dashboard_gui.py           # Modern GUI interface  
├── students.json             # Data persistence
└── README.md                # Documentation

🔧 Core Classes:

1️⃣ Student Class:
   • Stores: roll_number, name, course, cgpa
   • Methods: to_dict(), from_dict()
   • Purpose: Data model for student records

2️⃣ AVLNode Class:
   • Properties: student, left, right, height
   • Purpose: Tree node structure

3️⃣ AVLTree Class:
   • insert(): Adds student with auto-balancing
   • delete(): Removes student with rebalancing  
   • search(): O(log n) student lookup
   • rotations(): LL, RR, LR, RL rotations
   • height management and balance factor calculation

4️⃣ StudentRecordSystem Class:
   • File I/O operations (JSON persistence)
   • Integration between AVL tree and storage
   • Data loading/saving automation

🔄 AVL Operations Flow:

INSERT:
1. Standard BST insertion
2. Update heights bottom-up
3. Calculate balance factors
4. Perform rotations if needed
5. Save to JSON

DELETE:
1. Standard BST deletion
2. Update heights bottom-up  
3. Check balance factors
4. Perform rotations if needed
5. Save to JSON

🎯 Key Features:
• Real-time rotation visualization
• Automatic data persistence
• Modern dashboard interface
• Educational AVL theory section
• Analytics and statistics
• Error handling and validation

💾 Data Persistence:
• JSON format for portability
• Automatic save after operations
• Load existing data on startup
• Backup and recovery support
        """
        
        impl_text.insert(tk.END, implementation_details)
        impl_text.config(state=tk.DISABLED)
        
    def show_analytics(self):
        self.clear_content()
        
        # Header
        header = tk.Frame(self.content_frame, bg=self.colors['content'])
        header.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(header, text="📈 Analytics & Statistics", font=('Segoe UI', 20, 'bold'),
                bg=self.colors['content'], fg=self.colors['text']).pack(anchor='w')
        
        # Analytics content
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
            analytics_frame = tk.Frame(self.content_frame, bg=self.colors['content'])
            analytics_frame.pack(fill=tk.BOTH, expand=True, padx=20)
            
            # Course distribution
            self.create_analytics_card(analytics_frame, "📚 Course Distribution", courses)
            
            # CGPA distribution  
            self.create_analytics_card(analytics_frame, "📊 CGPA Distribution", cgpa_ranges)
            
            # Tree statistics
            tree_stats = {
                "Tree Height": self.get_tree_height(),
                "Total Nodes": len(students),
                "Leaf Nodes": self.count_leaf_nodes(),
                "Internal Nodes": len(students) - self.count_leaf_nodes()
            }
            self.create_analytics_card(analytics_frame, "🌳 Tree Statistics", tree_stats)
        
    def create_analytics_card(self, parent, title, data):
        card = tk.Frame(parent, bg=self.colors['card'])
        card.pack(fill=tk.X, pady=10)
        
        tk.Label(card, text=title, font=('Segoe UI', 14, 'bold'),
                bg=self.colors['card'], fg=self.colors['primary']).pack(pady=10)
        
        for key, value in data.items():
            row = tk.Frame(card, bg=self.colors['card'])
            row.pack(fill=tk.X, padx=20, pady=2)
            
            tk.Label(row, text=f"{key}:", font=('Segoe UI', 10),
                    bg=self.colors['card'], fg=self.colors['text']).pack(side=tk.LEFT)
            tk.Label(row, text=str(value), font=('Segoe UI', 10, 'bold'),
                    bg=self.colors['card'], fg=self.colors['accent']).pack(side=tk.RIGHT)
    
    def get_tree_height(self):
        return self.system.avl_tree.get_height(self.system.avl_tree.root)
    
    def count_leaf_nodes(self):
        def count_leaves(node):
            if not node:
                return 0
            if not node.left and not node.right:
                return 1
            return count_leaves(node.left) + count_leaves(node.right)
        return count_leaves(self.system.avl_tree.root)
    
    def add_student(self):
        try:
            roll = int(self.roll_entry.get())
            name = self.name_entry.get().strip()
            course = self.course_entry.get().strip()
            cgpa = float(self.cgpa_entry.get())
            
            if not name or not course:
                messagebox.showerror("Error", "Please fill all fields!")
                return
                
            student = Student(roll, name, course, cgpa)
            self.system.avl_tree.root = self.system.avl_tree.insert(self.system.avl_tree.root, student)
            self.system.save_data()
            self.refresh_tree()
            self.clear_fields()
            messagebox.showinfo("Success", "Student added!")
            
        except ValueError:
            messagebox.showerror("Error", "Invalid data!")
    
    def update_student(self):
        try:
            roll = int(self.roll_entry.get())
            node = self.system.avl_tree.search(self.system.avl_tree.root, roll)
            
            if node:
                node.student.name = self.name_entry.get().strip()
                node.student.course = self.course_entry.get().strip()
                node.student.cgpa = float(self.cgpa_entry.get())
                self.system.save_data()
                self.refresh_tree()
                messagebox.showinfo("Success", "Student updated!")
            else:
                messagebox.showerror("Error", "Student not found!")
        except ValueError:
            messagebox.showerror("Error", "Invalid data!")
    
    def delete_student(self):
        try:
            roll = int(self.roll_entry.get())
            self.system.avl_tree.root = self.system.avl_tree.delete(self.system.avl_tree.root, roll)
            self.system.save_data()
            self.refresh_tree()
            self.clear_fields()
            messagebox.showinfo("Success", "Student deleted!")
        except ValueError:
            messagebox.showerror("Error", "Invalid roll number!")
    
    def clear_fields(self):
        for entry in [self.roll_entry, self.name_entry, self.course_entry, self.cgpa_entry]:
            entry.delete(0, tk.END)
    
    def refresh_tree(self):
        if hasattr(self, 'tree'):
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            students = []
            self.system.avl_tree.inorder(self.system.avl_tree.root, students)
            
            for student in students:
                self.tree.insert("", tk.END, values=(
                    student.roll_number, student.name, student.course, student.cgpa
                ))
    
    def on_select(self, event):
        if hasattr(self, 'tree'):
            selection = self.tree.selection()
            if selection:
                values = self.tree.item(selection[0])['values']
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
    app = DashboardGUI(root)
    root.mainloop()