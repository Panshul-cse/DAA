import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from student_record_system import StudentRecordSystem, Student
import datetime

class AnimatedDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System - Professional Edition")
        self.root.geometry("1400x900")
        self.root.configure(bg='#000000')
        
        self.system = StudentRecordSystem()
        self.current_page = None
        self.animation_running = False
        
        self.setup_theme()
        self.create_dashboard()
        self.animate_startup()
        
    def setup_theme(self):
        self.colors = {
            'bg': '#000000',
            'sidebar': '#1a1a1a', 
            'content': '#0d0d0d',
            'card': '#262626',
            'primary': '#ffffff',
            'accent': '#404040',
            'success': '#00ff00',
            'warning': '#ffff00',
            'danger': '#ff0000',
            'text': '#e0e0e0',
            'muted': '#808080'
        }
        
    def create_dashboard(self):
        # Main container
        self.main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Animated sidebar
        self.sidebar = tk.Frame(self.main_frame, bg=self.colors['sidebar'], width=0)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        # Logo section
        self.logo_frame = tk.Frame(self.sidebar, bg=self.colors['sidebar'], height=120)
        self.logo_frame.pack(fill=tk.X)
        self.logo_frame.pack_propagate(False)
        
        self.logo_label = tk.Label(self.logo_frame, text="◆", font=('Arial', 40), 
                                  bg=self.colors['sidebar'], fg=self.colors['primary'])
        self.logo_label.pack(expand=True)
        
        self.title_label = tk.Label(self.logo_frame, text="STUDENT SYSTEM", 
                                   font=('Arial', 12, 'bold'),
                                   bg=self.colors['sidebar'], fg=self.colors['text'])
        self.title_label.pack()
        
        # Navigation
        self.nav_frame = tk.Frame(self.sidebar, bg=self.colors['sidebar'])
        self.nav_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=20)
        
        nav_items = [
            ("■ DASHBOARD", self.show_dashboard),
            ("■ STUDENTS", self.show_students),
            ("■ AVL THEORY", self.show_theory),
            ("■ SYSTEM INFO", self.show_system),
            ("■ ANALYTICS", self.show_analytics)
        ]
        
        self.nav_buttons = []
        for i, (text, command) in enumerate(nav_items):
            btn = tk.Button(self.nav_frame, text=text, command=lambda c=command: self.animate_page_change(c),
                          font=('Consolas', 11, 'bold'), bg=self.colors['sidebar'], 
                          fg=self.colors['muted'], relief=tk.FLAT, pady=15, anchor='w',
                          cursor='hand2', bd=0)
            btn.pack(fill=tk.X, pady=2)
            self.nav_buttons.append(btn)
            
            # Hover animations
            btn.bind("<Enter>", lambda e, b=btn: self.animate_button_hover(b, True))
            btn.bind("<Leave>", lambda e, b=btn: self.animate_button_hover(b, False))
        
        # Content area
        self.content_frame = tk.Frame(self.main_frame, bg=self.colors['content'])
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Loading screen
        self.create_loading_screen()
        
    def animate_startup(self):
        # Animate sidebar expansion
        target_width = 250
        current_width = 0
        
        def expand_sidebar():
            nonlocal current_width
            if current_width < target_width:
                current_width += 10
                self.sidebar.configure(width=current_width)
                self.root.after(20, expand_sidebar)
            else:
                self.animate_logo()
        
        expand_sidebar()
        
    def animate_logo(self):
        # Animate logo rotation
        symbols = ["◆", "◇", "◈", "◉", "●", "○", "◆"]
        current = 0
        
        def rotate_logo():
            nonlocal current
            if current < len(symbols):
                self.logo_label.configure(text=symbols[current])
                current += 1
                self.root.after(200, rotate_logo)
            else:
                self.show_dashboard()
        
        rotate_logo()
        
    def animate_button_hover(self, button, entering):
        if entering:
            button.configure(fg=self.colors['primary'], bg=self.colors['accent'])
            # Slide effect
            self.animate_button_slide(button, 5)
        else:
            button.configure(fg=self.colors['muted'], bg=self.colors['sidebar'])
            self.animate_button_slide(button, -5)
            
    def animate_button_slide(self, button, offset):
        current_padx = button.cget('padx') or 0
        target_padx = max(0, current_padx + offset)
        button.configure(padx=target_padx)
        
    def animate_page_change(self, page_func):
        if self.animation_running:
            return
            
        self.animation_running = True
        
        # Fade out current content
        self.fade_content(0.0, lambda: self.switch_page(page_func))
        
    def fade_content(self, alpha, callback=None):
        # Simulate fade by changing background colors
        fade_color = self.interpolate_color(self.colors['content'], self.colors['bg'], alpha)
        
        for widget in self.content_frame.winfo_children():
            try:
                widget.configure(bg=fade_color)
            except:
                pass
                
        if alpha < 1.0:
            self.root.after(30, lambda: self.fade_content(alpha + 0.1, callback))
        elif callback:
            callback()
            
    def interpolate_color(self, color1, color2, t):
        # Simple color interpolation
        return color1 if t < 0.5 else color2
        
    def switch_page(self, page_func):
        self.clear_content()
        page_func()
        self.fade_content_in()
        
    def fade_content_in(self):
        # Fade in new content
        self.root.after(100, lambda: self.set_content_colors())
        self.animation_running = False
        
    def set_content_colors(self):
        for widget in self.content_frame.winfo_children():
            try:
                widget.configure(bg=self.colors['content'])
            except:
                pass
                
    def create_loading_screen(self):
        loading_frame = tk.Frame(self.content_frame, bg=self.colors['content'])
        loading_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(loading_frame, text="◆ INITIALIZING SYSTEM ◆", 
                font=('Consolas', 24, 'bold'), bg=self.colors['content'], 
                fg=self.colors['primary']).pack(expand=True)
        
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
    def create_animated_card(self, parent, title, height=200):
        card = tk.Frame(parent, bg=self.colors['card'], relief=tk.RAISED, bd=1, height=height)
        card.pack(fill=tk.X, padx=20, pady=10)
        card.pack_propagate(False)
        
        # Animated header
        header = tk.Frame(card, bg=self.colors['card'], height=40)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title_label = tk.Label(header, text=f"■ {title}", font=('Consolas', 14, 'bold'),
                              bg=self.colors['card'], fg=self.colors['primary'])
        title_label.pack(pady=10, anchor='w', padx=20)
        
        # Content area
        content = tk.Frame(card, bg=self.colors['card'])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Hover animation
        def on_enter(e):
            card.configure(relief=tk.RAISED, bd=2)
            title_label.configure(fg=self.colors['success'])
            
        def on_leave(e):
            card.configure(relief=tk.RAISED, bd=1)
            title_label.configure(fg=self.colors['primary'])
            
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        
        return content
        
    def show_dashboard(self):
        self.clear_content()
        
        # Animated header
        header = tk.Frame(self.content_frame, bg=self.colors['content'], height=100)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title = tk.Label(header, text="■ SYSTEM DASHBOARD", font=('Consolas', 28, 'bold'),
                        bg=self.colors['content'], fg=self.colors['primary'])
        title.pack(expand=True)
        
        # Animated stats
        stats_frame = tk.Frame(self.content_frame, bg=self.colors['content'])
        stats_frame.pack(fill=tk.X, padx=20, pady=20)
        
        students = []
        self.system.avl_tree.inorder(self.system.avl_tree.root, students)
        
        stats = [
            ("STUDENTS", len(students)),
            ("COURSES", len(set(s.course for s in students)) if students else 0),
            ("AVG CGPA", f"{sum(s.cgpa for s in students)/len(students):.2f}" if students else "0.00"),
            ("TREE HEIGHT", self.get_tree_height())
        ]
        
        for i, (label, value) in enumerate(stats):
            self.animate_stat_card(stats_frame, label, value, i * 200)
            
    def animate_stat_card(self, parent, label, value, delay):
        def create_card():
            card = tk.Frame(parent, bg=self.colors['card'], width=200, height=120)
            card.pack(side=tk.LEFT, padx=15)
            card.pack_propagate(False)
            
            tk.Label(card, text=str(value), font=('Consolas', 32, 'bold'),
                    bg=self.colors['card'], fg=self.colors['success']).pack(expand=True)
            tk.Label(card, text=label, font=('Consolas', 10, 'bold'),
                    bg=self.colors['card'], fg=self.colors['text']).pack()
                    
            # Pulse animation
            self.animate_pulse(card)
            
        self.root.after(delay, create_card)
        
    def animate_pulse(self, widget):
        colors = [self.colors['card'], self.colors['accent']]
        current = 0
        
        def pulse():
            nonlocal current
            widget.configure(bg=colors[current % 2])
            current += 1
            if current < 6:  # Pulse 3 times
                self.root.after(300, pulse)
            else:
                widget.configure(bg=self.colors['card'])
                
        pulse()
        
    def show_students(self):
        self.clear_content()
        
        # Header
        header = tk.Frame(self.content_frame, bg=self.colors['content'])
        header.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(header, text="■ STUDENT MANAGEMENT", font=('Consolas', 24, 'bold'),
                bg=self.colors['content'], fg=self.colors['primary']).pack(anchor='w')
        
        # Form card
        form_content = self.create_animated_card(self.content_frame, "DATA INPUT", 180)
        self.create_student_form(form_content)
        
        # List card
        list_content = self.create_animated_card(self.content_frame, "STUDENT RECORDS", 300)
        self.create_student_list(list_content)
        
    def create_student_form(self, parent):
        # Input grid
        grid_frame = tk.Frame(parent, bg=self.colors['card'])
        grid_frame.pack(fill=tk.X)
        
        fields = [("ROLL:", "roll_entry"), ("NAME:", "name_entry"), 
                 ("COURSE:", "course_entry"), ("CGPA:", "cgpa_entry")]
        
        for i, (label, attr) in enumerate(fields):
            row = i // 2
            col = (i % 2) * 2
            
            tk.Label(grid_frame, text=label, font=('Consolas', 10, 'bold'),
                    bg=self.colors['card'], fg=self.colors['text']).grid(row=row, column=col, sticky='w', padx=5, pady=5)
            
            entry = tk.Entry(grid_frame, font=('Consolas', 10), bg=self.colors['bg'], 
                           fg=self.colors['primary'], relief=tk.FLAT, bd=3, width=15)
            entry.grid(row=row, column=col+1, padx=5, pady=5)
            setattr(self, attr, entry)
        
        # Buttons
        btn_frame = tk.Frame(parent, bg=self.colors['card'])
        btn_frame.pack(fill=tk.X, pady=10)
        
        buttons = [("ADD", self.add_student, self.colors['success']),
                  ("UPDATE", self.update_student, self.colors['warning']),
                  ("DELETE", self.delete_student, self.colors['danger']),
                  ("CLEAR", self.clear_fields, self.colors['muted'])]
        
        for text, cmd, color in buttons:
            btn = tk.Button(btn_frame, text=text, command=cmd, bg=color, fg='black',
                          font=('Consolas', 9, 'bold'), relief=tk.FLAT, padx=12, pady=5)
            btn.pack(side=tk.LEFT, padx=5)
            
            # Button animations
            btn.bind("<Enter>", lambda e, b=btn: b.configure(relief=tk.RAISED))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(relief=tk.FLAT))
    
    def create_student_list(self, parent):
        # Custom treeview styling
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Custom.Treeview', background=self.colors['bg'], 
                       foreground=self.colors['text'], fieldbackground=self.colors['bg'])
        style.configure('Custom.Treeview.Heading', background=self.colors['card'],
                       foreground=self.colors['primary'], font=('Consolas', 10, 'bold'))
        
        self.tree = ttk.Treeview(parent, columns=("Roll", "Name", "Course", "CGPA"), 
                               show="headings", style='Custom.Treeview')
        
        for col in ["Roll", "Name", "Course", "CGPA"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor='center')
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<ButtonRelease-1>", self.on_select)
        self.refresh_tree()
        
    def show_theory(self):
        self.clear_content()
        
        # Header
        header = tk.Frame(self.content_frame, bg=self.colors['content'])
        header.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(header, text="■ AVL TREE THEORY", font=('Consolas', 24, 'bold'),
                bg=self.colors['content'], fg=self.colors['primary']).pack(anchor='w')
        
        # Theory content with animations
        theory_sections = [
            ("DEFINITION", "Self-balancing binary search tree\nHeight difference ≤ 1 between subtrees"),
            ("BALANCE FACTOR", "BF = Height(Left) - Height(Right)\nValid range: {-1, 0, +1}"),
            ("ROTATIONS", "LL → Right Rotation\nRR → Left Rotation\nLR → Left-Right\nRL → Right-Left"),
            ("COMPLEXITY", "Search: O(log n)\nInsert: O(log n)\nDelete: O(log n)")
        ]
        
        for i, (title, content) in enumerate(theory_sections):
            self.animate_theory_card(title, content, i * 300)
            
    def animate_theory_card(self, title, content, delay):
        def create_card():
            card_content = self.create_animated_card(self.content_frame, title, 120)
            
            tk.Label(card_content, text=content, font=('Consolas', 11), justify=tk.LEFT,
                    bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w')
                    
        self.root.after(delay, create_card)
        
    def show_system(self):
        self.clear_content()
        
        # Header
        header = tk.Frame(self.content_frame, bg=self.colors['content'])
        header.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(header, text="■ SYSTEM ARCHITECTURE", font=('Consolas', 24, 'bold'),
                bg=self.colors['content'], fg=self.colors['primary']).pack(anchor='w')
        
        # System info
        info_content = self.create_animated_card(self.content_frame, "IMPLEMENTATION DETAILS", 400)
        
        info_text = scrolledtext.ScrolledText(info_content, bg=self.colors['bg'], 
                                            fg=self.colors['text'], font=('Consolas', 10))
        info_text.pack(fill=tk.BOTH, expand=True)
        
        system_info = """
■ CORE COMPONENTS

├── Student Class
│   ├── Properties: roll_number, name, course, cgpa
│   └── Methods: to_dict(), from_dict()

├── AVLNode Class  
│   ├── Properties: student, left, right, height
│   └── Purpose: Tree node structure

├── AVLTree Class
│   ├── insert(): O(log n) insertion with balancing
│   ├── delete(): O(log n) deletion with rebalancing
│   ├── search(): O(log n) lookup operation
│   └── rotations(): LL, RR, LR, RL rotations

└── StudentRecordSystem Class
    ├── File I/O operations (JSON)
    ├── Data persistence management
    └── System integration layer

■ OPERATION FLOW

INSERT → BST Insert → Update Heights → Check Balance → Rotate if needed → Save
DELETE → BST Delete → Update Heights → Check Balance → Rotate if needed → Save
SEARCH → Standard BST traversal → O(log n) guaranteed

■ FEATURES

• Real-time animations and transitions
• Professional black & white theme
• Comprehensive AVL theory section
• Advanced analytics and statistics
• Automatic data persistence
• Error handling and validation
        """
        
        info_text.insert(tk.END, system_info)
        info_text.config(state=tk.DISABLED)
        
    def show_analytics(self):
        self.clear_content()
        
        # Header
        header = tk.Frame(self.content_frame, bg=self.colors['content'])
        header.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(header, text="■ SYSTEM ANALYTICS", font=('Consolas', 24, 'bold'),
                bg=self.colors['content'], fg=self.colors['primary']).pack(anchor='w')
        
        # Analytics cards
        students = []
        self.system.avl_tree.inorder(self.system.avl_tree.root, students)
        
        if students:
            # Performance metrics
            metrics_content = self.create_animated_card(self.content_frame, "PERFORMANCE METRICS", 150)
            
            metrics = [
                ("Tree Height", self.get_tree_height()),
                ("Total Nodes", len(students)),
                ("Leaf Nodes", self.count_leaf_nodes()),
                ("Balance Factor", "Optimal")
            ]
            
            metrics_grid = tk.Frame(metrics_content, bg=self.colors['card'])
            metrics_grid.pack(fill=tk.X)
            
            for i, (label, value) in enumerate(metrics):
                row = i // 2
                col = (i % 2) * 2
                
                tk.Label(metrics_grid, text=f"{label}:", font=('Consolas', 10, 'bold'),
                        bg=self.colors['card'], fg=self.colors['text']).grid(row=row, column=col, sticky='w', padx=10, pady=5)
                tk.Label(metrics_grid, text=str(value), font=('Consolas', 10, 'bold'),
                        bg=self.colors['card'], fg=self.colors['success']).grid(row=row, column=col+1, sticky='w', padx=10, pady=5)
        
    # Helper methods
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
                messagebox.showerror("ERROR", "Please fill all fields!")
                return
                
            student = Student(roll, name, course, cgpa)
            self.system.avl_tree.root = self.system.avl_tree.insert(self.system.avl_tree.root, student)
            self.system.save_data()
            self.refresh_tree()
            self.clear_fields()
            messagebox.showinfo("SUCCESS", "Student added successfully!")
            
        except ValueError:
            messagebox.showerror("ERROR", "Invalid data format!")
    
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
                messagebox.showinfo("SUCCESS", "Student updated!")
            else:
                messagebox.showerror("ERROR", "Student not found!")
        except ValueError:
            messagebox.showerror("ERROR", "Invalid data format!")
    
    def delete_student(self):
        try:
            roll = int(self.roll_entry.get())
            if messagebox.askyesno("CONFIRM", f"Delete student {roll}?"):
                self.system.avl_tree.root = self.system.avl_tree.delete(self.system.avl_tree.root, roll)
                self.system.save_data()
                self.refresh_tree()
                self.clear_fields()
                messagebox.showinfo("SUCCESS", "Student deleted!")
        except ValueError:
            messagebox.showerror("ERROR", "Invalid roll number!")
    
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
    app = AnimatedDashboard(root)
    root.mainloop()