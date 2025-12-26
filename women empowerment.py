import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
from datetime import datetime
import sqlite3
import os
import json

class WomenEmpowermentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🌸 Women Empowerment Platform")
        self.root.geometry("1400x800")
        self.root.configure(bg='#f0f8ff')
        
        self.current_role = "Learner"
        self.registered_workshops = []  # Track registered workshops
        self.user_profile = {
            "age": 25,
            "location": "Urban",
            "business_type": "None",
            "education": "Graduate",
            "income_level": "Medium"
        }
        self.chat_history = []
        self.current_user = None
        self.users = {}  # Simple user storage
        
        # Initialize database
        self.init_database()
        
        self.setup_front_page()
    
    def init_database(self):
        """Initialize SQLite database and create tables"""
        self.conn = sqlite3.connect('women_empowerment.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        # Drop and recreate tables to ensure correct schema
        self.cursor.execute('DROP TABLE IF EXISTS users')
        self.cursor.execute('DROP TABLE IF EXISTS workshops')
        self.cursor.execute('DROP TABLE IF EXISTS job_applications')
        self.cursor.execute('DROP TABLE IF EXISTS user_profile')
        
        # Create users table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                name TEXT NOT NULL,
                phone TEXT,
                age INTEGER,
                location TEXT,
                education TEXT,
                role TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create workshops table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS workshops (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_email TEXT NOT NULL,
                workshop_title TEXT NOT NULL,
                workshop_date TEXT NOT NULL,
                workshop_time TEXT NOT NULL,
                registration_data TEXT,
                registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_email) REFERENCES users (email)
            )
        ''')
        
        # Create job_applications table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS job_applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_email TEXT NOT NULL,
                job_title TEXT NOT NULL,
                company TEXT NOT NULL,
                application_data TEXT,
                application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'Pending',
                FOREIGN KEY (user_email) REFERENCES users (email)
            )
        ''')
        
        # Create user_profile table for additional user information
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_profile (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_email TEXT UNIQUE NOT NULL,
                age INTEGER,
                location TEXT,
                business_type TEXT,
                education TEXT,
                income_level TEXT,
                FOREIGN KEY (user_email) REFERENCES users (email)
            )
        ''')
        
        self.conn.commit()
    
    def setup_front_page(self):
        self.clear_screen()
        
        # Main container with gradient effect
        main_frame = tk.Frame(self.root, bg='#f0f8ff')
        main_frame.pack(fill='both', expand=True)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#e75480', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="🌸 Women Empowerment Platform", 
                font=('Arial', 24, 'bold'), bg='#e75480', fg='white').pack(pady=20)
        
        # Hero Section
        hero_frame = tk.Frame(main_frame, bg='#fff0f5', padx=50, pady=50)
        hero_frame.pack(fill='both', expand=True)
        
        # Left side - Welcome message
        left_frame = tk.Frame(hero_frame, bg='#fff0f5')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 20))
        
        tk.Label(left_frame, text="Empower Your Journey", 
                font=('Arial', 36, 'bold'), bg='#fff0f5', fg='#e75480').pack(pady=(50, 20))
        
        tk.Label(left_frame, text="Join thousands of women transforming their lives through education, entrepreneurship, and community support.", 
                font=('Arial', 16), bg='#fff0f5', fg='#555555', wraplength=500).pack(pady=10)
        
        # Features highlights
        features = [
            "🎓 Learn new skills with certified courses",
            "💼 Start and grow your business",
            "🛍️ Sell products in our marketplace",
            "👥 Connect with mentors and peers",
            "🏛️ Access government schemes",
            "📊 Track your progress with analytics"
        ]
        
        for feature in features:
            tk.Label(left_frame, text=feature, font=('Arial', 14), 
                    bg='#fff0f5', fg='#333333', anchor='w').pack(fill='x', pady=5)
        
        # Right side - Login/Signup
        right_frame = tk.Frame(hero_frame, bg='white', relief='raised', bd=2, padx=30, pady=30)
        right_frame.pack(side='right', fill='y', padx=(20, 0))
        
        tk.Label(right_frame, text="Welcome!", 
                font=('Arial', 20, 'bold'), bg='white', fg='#e75480').pack(pady=20)
        
        # Login Form
        login_frame = tk.Frame(right_frame, bg='white')
        login_frame.pack(fill='x', pady=10)
        
        tk.Label(login_frame, text="Email", font=('Arial', 12), bg='white').pack(anchor='w')
        self.login_email = tk.Entry(login_frame, font=('Arial', 12), width=25)
        self.login_email.pack(fill='x', pady=(5, 15))
        
        tk.Label(login_frame, text="Password", font=('Arial', 12), bg='white').pack(anchor='w')
        self.login_password = tk.Entry(login_frame, font=('Arial', 12), width=25, show='*')
        self.login_password.pack(fill='x', pady=(5, 15))
        
        login_btn = tk.Button(login_frame, text="Sign In", 
                             font=('Arial', 14, 'bold'), bg='#e75480', fg='white',
                             padx=30, pady=10, command=self.sign_in)
        login_btn.pack(pady=10)
        
        # Separator
        separator = tk.Frame(right_frame, height=2, bg='#e0e0e0')
        separator.pack(fill='x', pady=20)
        
        # Sign Up Section
        tk.Label(right_frame, text="New Here? Join Us!", 
                font=('Arial', 18, 'bold'), bg='white', fg='#e75480').pack(pady=10)
        
        signup_btn = tk.Button(right_frame, text="Sign Up",
                              font=('Arial', 12, 'bold'), bg='#4ecdc4', fg='white',
                              padx=20, pady=8, command=self.show_signup_form)
        signup_btn.pack(pady=10)
        
        # Quick stats at bottom
        stats_frame = tk.Frame(main_frame, bg='#f8f0f5', height=80)
        stats_frame.pack(fill='none', side='bottom')
        stats_frame.pack_propagate(False)
        
        stats_data = [
            ("10,000+", "Women Empowered"),
            ("500+", "Courses Available"),
            ("2,000+", "Successful Businesses"),
            ("50+", "Government Schemes")
        ]
        
        for value, label in stats_data:
            stat = tk.Frame(stats_frame, bg='#f8f0f5')
            stat.pack(side='left', expand=True, fill='both')
            tk.Label(stat, text=value, font=('Arial', 16, 'bold'), 
                    bg='#f8f0f5', fg='#e75480').pack()
            tk.Label(stat, text=label, font=('Arial', 10), 
                    bg='#f8f0f5', fg='#666666').pack()

    def show_signup_form(self):
        signup_window = tk.Toplevel(self.root)
        signup_window.title("Sign Up - Create Your Account")
        signup_window.geometry("500x650")
        signup_window.configure(bg='#f0f8ff')
        signup_window.resizable(False, False)
        
        # Center the window
        signup_window.transient(self.root)
        signup_window.grab_set()
        
        # Main container for signup form
        main_container = tk.Frame(signup_window, bg='#f0f8ff')
        main_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        tk.Label(main_container, text="Sign Up - Join Our Community",
                font=('Arial', 20, 'bold'), bg='#f0f8ff', fg='#e75480').pack(pady=20)
        
        # Create a canvas and scrollbar for the form
        canvas = tk.Canvas(main_container, bg='#f0f8ff', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f8ff')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        form_frame = tk.Frame(scrollable_frame, bg='white', padx=30, pady=30)
        form_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Form fields
        fields = [
            ("Full Name", "text"),
            ("Email", "text"),
            ("Phone", "text"),
            ("Password", "password"),
            ("Confirm Password", "password"),
            ("Age", "number"),
            ("Location", "combo"),
            ("Education Level", "combo")
        ]
        
        self.signup_entries = {}
        
        for field, field_type in fields:
            frame = tk.Frame(form_frame, bg='white')
            frame.pack(fill='x', pady=8)
            
            tk.Label(frame, text=field, font=('Arial', 11), bg='white', width=15, anchor='w').pack(side='left')
            
            if field_type == "combo":
                if field == "Location":
                    values = ["Urban", "Rural", "Semi-Urban"]
                else:
                    values = ["10th", "12th", "Diploma", "Graduate", "Post Graduate"]
                
                entry = ttk.Combobox(frame, values=values, width=27)
                entry.set(values[0])
            else:
                if field_type == "password":
                    show_char = '*'
                else:
                    show_char = ''
                entry = tk.Entry(frame, width=30, show=show_char)
            
            entry.pack(side='left', padx=10, fill='x', expand=True)
            self.signup_entries[field] = entry
        
        # Role selection
        role_frame = tk.Frame(form_frame, bg='white')
        role_frame.pack(fill='x', pady=15)
        
        tk.Label(role_frame, text="I want to:", font=('Arial', 11), bg='white').pack(anchor='w')
        
        self.role_var = tk.StringVar(value="Learner")
        roles = [
            ("🎓 Learn new skills", "Learner"),
            ("💼 Start/grow my business", "Entrepreneur"),
            ("👩‍🏫 Mentor others", "Mentor")
        ]
        
        for text, value in roles:
            tk.Radiobutton(role_frame, text=text, variable=self.role_var, 
                          value=value, bg='white').pack(anchor='w', pady=2)
        
        def create_account():
            # Validate form
            if not all(entry.get().strip() for field, entry in self.signup_entries.items() 
                      if field not in ["Confirm Password"]):
                messagebox.showerror("Error", "Please fill in all fields")
                return
            
            if self.signup_entries["Password"].get() != self.signup_entries["Confirm Password"].get():
                messagebox.showerror("Error", "Passwords do not match")
                return
            
            email = self.signup_entries["Email"].get()
            
            # Check if email already exists in database
            self.cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            if self.cursor.fetchone():
                messagebox.showerror("Error", "Email already registered")
                return
            
            # Save user to database
            try:
                self.cursor.execute('''
                    INSERT INTO users (email, password, name, phone, age, location, education, role)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    email,
                    self.signup_entries["Password"].get(),
                    self.signup_entries["Full Name"].get(),
                    self.signup_entries["Phone"].get(),
                    int(self.signup_entries["Age"].get()),
                    self.signup_entries["Location"].get(),
                    self.signup_entries["Education Level"].get(),
                    self.role_var.get()
                ))
                
                # Also save to user_profile table
                self.cursor.execute('''
                    INSERT INTO user_profile (user_email, age, location, education)
                    VALUES (?, ?, ?, ?)
                ''', (
                    email,
                    int(self.signup_entries["Age"].get()),
                    self.signup_entries["Location"].get(),
                    self.signup_entries["Education Level"].get()
                ))
                
                self.conn.commit()
                
                # Update local variables
                self.current_user = email
                self.current_role = self.role_var.get()
                
                # Update in-memory users dictionary
                self.users[email] = {
                    "password": self.signup_entries["Password"].get(),
                    "name": self.signup_entries["Full Name"].get(),
                    "phone": self.signup_entries["Phone"].get(),
                    "age": self.signup_entries["Age"].get(),
                    "location": self.signup_entries["Location"].get(),
                    "education": self.signup_entries["Education Level"].get(),
                    "role": self.role_var.get(),
                    "email": email
                }
                
                messagebox.showinfo("Success", "Account created successfully! Welcome to our community!")
                signup_window.destroy()
                self.show_role_selection()
                
            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to create account: {str(e)}")
                self.conn.rollback()
        
        # Button frame to ensure proper placement
        button_frame = tk.Frame(main_container, bg='#f0f8ff')
        button_frame.pack(fill='x', pady=10)
        
        tk.Button(button_frame, text="Sign Up", bg='#e75480', fg='white',
                 font=('Arial', 14, 'bold'), command=create_account, 
                 padx=30, pady=10).pack(pady=10)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Update scrollregion after everything is packed
        signup_window.update()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def sign_in(self):
        email = self.login_email.get()
        password = self.login_password.get()
        
        if not email or not password:
            messagebox.showerror("Error", "Please enter both email and password")
            return
        
        # Check credentials in database
        self.cursor.execute('''
            SELECT * FROM users WHERE email = ? AND password = ?
        ''', (email, password))
        
        user_data = self.cursor.fetchone()
        
        if user_data:
            # Get column names
            columns = [description[0] for description in self.cursor.description]
            user_dict = dict(zip(columns, user_data))
            
            self.current_user = email
            self.current_role = user_dict['role']
            
            # Update in-memory users dictionary
            self.users[email] = user_dict
            
            # Load user profile data
            self.cursor.execute('SELECT * FROM user_profile WHERE user_email = ?', (email,))
            profile_data = self.cursor.fetchone()
            if profile_data:
                profile_columns = [description[0] for description in self.cursor.description]
                profile_dict = dict(zip(profile_columns, profile_data))
                self.user_profile.update({
                    "age": profile_dict.get('age', 25),
                    "location": profile_dict.get('location', 'Urban'),
                    "business_type": profile_dict.get('business_type', 'None'),
                    "education": profile_dict.get('education', 'Graduate'),
                    "income_level": profile_dict.get('income_level', 'Medium')
                })
            
            # Load registered workshops
            self.load_registered_workshops()
            
            messagebox.showinfo("Success", f"Welcome back, {user_dict['name']}!")
            self.show_role_selection()
        else:
            messagebox.showerror("Error", "Invalid email or password")

    def load_registered_workshops(self):
        """Load user's registered workshops from database"""
        if not self.current_user:
            return
        
        self.registered_workshops = []
        self.cursor.execute('''
            SELECT workshop_title, workshop_date, workshop_time, registration_data, registration_date 
            FROM workshops WHERE user_email = ?
        ''', (self.current_user,))
        
        workshops = self.cursor.fetchall()
        for workshop in workshops:
            self.registered_workshops.append({
                'title': workshop[0],
                'date': workshop[1],
                'time': workshop[2],
                'registration_data': workshop[3],
                'registration_date': workshop[4]
            })

    def show_role_selection(self):
        self.clear_screen()
        
        tk.Label(self.root, text="Select Your Role", 
                font=('Arial', 24, 'bold'), bg='#f0f8ff', fg='#e75480').pack(pady=20)
        
        # Display user info if logged in
        if self.current_user:
            user_info = self.users[self.current_user]
            welcome_text = f"Welcome, {user_info['name']}! ({user_info['email']})"
            tk.Label(self.root, text=welcome_text, 
                    font=('Arial', 14), bg='#f0f8ff', fg='#666666').pack(pady=5)
        
        roles_frame = tk.Frame(self.root, bg='#f0f8ff')
        roles_frame.pack(expand=True, fill='both', padx=100, pady=50)
        
        roles = [
            ("🎓 Learner", "Learn new skills and courses", "#f06bff"),
            ("💼 Entrepreneur", "Start and grow your business", "#4ecdb6"),
            ("👩‍🏫 Mentor", "Guide and teach others", "#45b7d1"),
            ("⚙️ Admin", "Manage platform operations", "#96ceb4")
        ]
        
        for i, (role, description, color) in enumerate(roles):
            role_frame = tk.Frame(roles_frame, bg=color, relief='raised', bd=2)
            role_frame.grid(row=i//2, column=i%2, padx=20, pady=20, sticky='nsew')
            
            tk.Label(role_frame, text=role, font=('Arial', 18, 'bold'), 
                    bg=color, fg='white').pack(pady=20)
            tk.Label(role_frame, text=description, font=('Arial', 12), 
                    bg=color, fg='white', wraplength=200).pack(pady=10)
            
            tk.Button(role_frame, text="Select Role", 
                     font=('Arial', 11, 'bold'),
                     bg='white', fg=color,
                     command=lambda r=role: self.set_role_and_continue(r)).pack(pady=20)
            
            roles_frame.grid_columnconfigure(i%2, weight=1)
            roles_frame.grid_rowconfigure(i//2, weight=1)
        
        # Add logout button if user is logged in
        if self.current_user:
            logout_frame = tk.Frame(self.root, bg='#f0f8ff')
            logout_frame.pack(pady=20)
            
            tk.Button(logout_frame, text="🚪 Logout", 
                     font=('Arial', 10), bg='#6c757d', fg='white',
                     command=self.logout).pack()

    def logout(self):
        self.current_user = None
        self.current_role = "Learner"
        self.registered_workshops = []
        messagebox.showinfo("Logged Out", "You have been successfully logged out.")
        self.setup_front_page()

    def set_role_and_continue(self, role):
        role_clean = role.replace("🎓 ", "").replace("💼 ", "").replace("👩‍🏫 ", "").replace("⚙️ ", "")
        self.current_role = role_clean
        
        # Update user role in database if logged in
        if self.current_user:
            try:
                self.cursor.execute('''
                    UPDATE users SET role = ? WHERE email = ?
                ''', (role_clean, self.current_user))
                self.conn.commit()
                
                # Update local users dictionary
                if self.current_user in self.users:
                    self.users[self.current_user]["role"] = role_clean
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update role: {str(e)}")
        
        self.show_main_dashboard()

    def show_main_dashboard(self):
        self.clear_screen()
        
        # Header with user info
        header = tk.Frame(self.root, bg='#e75480', height=100)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        header_content = tk.Frame(header, bg='#e75480')
        header_content.pack(fill='both', padx=20, pady=10)
        
        # Left side - Welcome message
        left_header = tk.Frame(header_content, bg='#e75480')
        left_header.pack(side='left')
        
        if self.current_user:
            user_name = self.users[self.current_user]["name"]
            welcome_text = f"🌸 Welcome, {user_name}! | Role: {self.current_role}"
        else:
            welcome_text = f"🌸 Welcome! Role: {self.current_role}"
            
        tk.Label(left_header, text=welcome_text, 
                font=('Arial', 20, 'bold'), bg='#e75480', fg='white').pack(anchor='w')
        
        # Right side - User controls
        right_header = tk.Frame(header_content, bg='#e75480')
        right_header.pack(side='right')
        
        if self.current_user:
            tk.Button(right_header, text="👤 Profile", font=('Arial', 10),
                     bg='white', fg='#e75480', command=self.show_user_profile).pack(side='left', padx=5)
            tk.Button(right_header, text="🚪 Logout", font=('Arial', 10),
                     bg='white', fg='#e75480', command=self.logout).pack(side='left', padx=5)
        else:
            tk.Button(right_header, text="🔐 Login", font=('Arial', 10),
                     bg='white', fg='#e75480', command=self.setup_front_page).pack(side='left', padx=5)
        
        # Navigation
        nav_frame = tk.Frame(self.root, bg='#f8f0f5')
        nav_frame.pack(fill='x', pady=10)
        
        modules = [
            "🏠 Dashboard", "🎓 Learning", "🛍️ E-Commerce", "📅 Workshops",
            "💼 Jobs", "🏛️ Schemes", "👥 Community", "📊 Analytics"
        ]
        
        for module in modules:
            tk.Button(nav_frame, text=module, font=('Arial', 10),
                     bg='#e75480', fg='white', padx=15, pady=8,
                     command=lambda m=module: self.show_module(m)).pack(side='left', padx=5)
        
        # Main Content
        self.content_frame = tk.Frame(self.root, bg='#f0f8ff')
        self.content_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        self.show_dashboard()

    def show_user_profile(self):
        if not self.current_user:
            messagebox.showinfo("Login Required", "Please login to view your profile")
            self.setup_front_page()
            return
        
        profile_window = tk.Toplevel(self.root)
        profile_window.title("My Profile")
        profile_window.geometry("500x500")
        profile_window.configure(bg='#f0f8ff')
        
        # Get user data from database
        self.cursor.execute('SELECT * FROM users WHERE email = ?', (self.current_user,))
        user_data = self.cursor.fetchone()
        columns = [description[0] for description in self.cursor.description]
        user_dict = dict(zip(columns, user_data))
        
        tk.Label(profile_window, text="👤 My Profile", 
                font=('Arial', 20, 'bold'), bg='#f0f8ff', fg='#e75480').pack(pady=20)
        
        profile_frame = tk.Frame(profile_window, bg='white', padx=30, pady=30)
        profile_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        # Display user information
        info_fields = [
            ("Name", user_dict["name"]),
            ("Email", self.current_user),
            ("Phone", user_dict.get("phone", "Not provided")),
            ("Age", str(user_dict.get("age", "Not provided"))),
            ("Location", user_dict.get("location", "Not provided")),
            ("Education", user_dict.get("education", "Not provided")),
            ("Role", user_dict.get("role", "Learner"))
        ]
        
        for field, value in info_fields:
            frame = tk.Frame(profile_frame, bg='white')
            frame.pack(fill='x', pady=8)
            
            tk.Label(frame, text=field, font=('Arial', 11, 'bold'), 
                    bg='white', width=12, anchor='w').pack(side='left')
            tk.Label(frame, text=value, font=('Arial', 11), 
                    bg='white').pack(side='left', padx=10)
        
        # Edit profile button
        tk.Button(profile_window, text="Edit Profile", bg='#e75480', fg='white',
                 font=('Arial', 12, 'bold'), command=lambda: self.edit_user_profile(profile_window)).pack(pady=20)

    def edit_user_profile(self, parent_window):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Profile")
        edit_window.geometry("500x600")
        edit_window.configure(bg='#f0f8ff')
        
        # Get current user data
        self.cursor.execute('SELECT * FROM users WHERE email = ?', (self.current_user,))
        user_data = self.cursor.fetchone()
        columns = [description[0] for description in self.cursor.description]
        user_dict = dict(zip(columns, user_data))
        
        tk.Label(edit_window, text="Edit Your Profile", 
                font=('Arial', 20, 'bold'), bg='#f0f8ff', fg='#e75480').pack(pady=20)
        
        form_frame = tk.Frame(edit_window, bg='white', padx=30, pady=30)
        form_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        # Editable fields
        fields = [
            ("Full Name", "text", user_dict["name"]),
            ("Phone", "text", user_dict.get("phone", "")),
            ("Age", "number", str(user_dict.get("age", ""))),
            ("Location", "combo", user_dict.get("location", "Urban")),
            ("Education Level", "combo", user_dict.get("education", "Graduate"))
        ]
        
        edit_entries = {}
        
        for field, field_type, current_value in fields:
            frame = tk.Frame(form_frame, bg='white')
            frame.pack(fill='x', pady=8)
            
            tk.Label(frame, text=field, font=('Arial', 11), bg='white', width=15, anchor='w').pack(side='left')
            
            if field_type == "combo":
                if field == "Location":
                    values = ["Urban", "Rural", "Semi-Urban"]
                else:
                    values = ["10th", "12th", "Diploma", "Graduate", "Post Graduate"]
                
                entry = ttk.Combobox(frame, values=values, width=27)
                entry.set(current_value)
            else:
                entry = tk.Entry(frame, width=30)
                entry.insert(0, current_value)
            
            entry.pack(side='left', padx=10, fill='x', expand=True)
            edit_entries[field] = entry
        
        def save_profile():
            try:
                # Update user data in database
                self.cursor.execute('''
                    UPDATE users 
                    SET name = ?, phone = ?, age = ?, location = ?, education = ?
                    WHERE email = ?
                ''', (
                    edit_entries["Full Name"].get(),
                    edit_entries["Phone"].get(),
                    int(edit_entries["Age"].get()),
                    edit_entries["Location"].get(),
                    edit_entries["Education Level"].get(),
                    self.current_user
                ))
                
                # Update user_profile table
                self.cursor.execute('''
                    INSERT OR REPLACE INTO user_profile (user_email, age, location, education)
                    VALUES (?, ?, ?, ?)
                ''', (
                    self.current_user,
                    int(edit_entries["Age"].get()),
                    edit_entries["Location"].get(),
                    edit_entries["Education Level"].get()
                ))
                
                self.conn.commit()
                
                # Update local variables
                if self.current_user in self.users:
                    self.users[self.current_user].update({
                        "name": edit_entries["Full Name"].get(),
                        "phone": edit_entries["Phone"].get(),
                        "age": edit_entries["Age"].get(),
                        "location": edit_entries["Location"].get(),
                        "education": edit_entries["Education Level"].get()
                    })
                
                messagebox.showinfo("Success", "Profile updated successfully!")
                edit_window.destroy()
                parent_window.destroy()
                self.show_user_profile()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update profile: {str(e)}")
                self.conn.rollback()
        
        tk.Button(edit_window, text="Save Changes", bg='#28a745', fg='white',
                 font=('Arial', 12, 'bold'), command=save_profile).pack(pady=20)

    def show_module(self, module_name):
        self.clear_content()
        
        if module_name == "🏠 Dashboard":
            self.show_dashboard()
        elif module_name == "🎓 Learning":
            self.show_learning()
        elif module_name == "🛍️ E-Commerce":
            self.show_ecommerce()
        elif module_name == "📅 Workshops":
            self.show_workshops()
        elif module_name == "💼 Jobs":
            self.show_jobs()
        elif module_name == "🏛️ Schemes":
            self.show_schemes()
        elif module_name == "👥 Community":
            self.show_community()
        elif module_name == "📊 Analytics":
            self.show_analytics()

    def show_dashboard(self):
        tk.Label(self.content_frame, text="🏠 Personal Dashboard", 
                font=('Arial', 24, 'bold'), bg='#f0f8ff').pack(pady=20)
        
        # Display user-specific welcome if logged in
        if self.current_user:
            user_name = self.users[self.current_user]["name"]
            welcome_msg = f"Hello, {user_name}! Here's your personalized dashboard."
            tk.Label(self.content_frame, text=welcome_msg, 
                    font=('Arial', 14), bg='#f0f8ff', fg='#666666').pack(pady=5)
        
        # Quick Stats
        stats_frame = tk.Frame(self.content_frame, bg='#f0f8ff')
        stats_frame.pack(fill='x', pady=20)
        
        # Get workshop count from database
        workshop_count = len(self.registered_workshops)
        
        stats_data = [
            ("Courses Enrolled", "5", "#6b7cff"),
            ("Products Listed", "12", "#4ebccd"),
            ("Workshops", f"{workshop_count}", "#45b7d1"),
            ("Mentorship Sessions", "8", "#ce9696")
        ]
        
        for i, (title, value, color) in enumerate(stats_data):
            stat_card = tk.Frame(stats_frame, bg=color, relief='raised', bd=2)
            stat_card.pack(side='left', expand=True, fill='both', padx=10)
            
            tk.Label(stat_card, text=value, font=('Arial', 24, 'bold'), 
                    bg=color, fg='white').pack(pady=10)
            tk.Label(stat_card, text=title, font=('Arial', 12), 
                    bg=color, fg='white').pack(pady=5)
        
        # Recent Activity
        activity_frame = tk.Frame(self.content_frame, bg='#f0f8ff')
        activity_frame.pack(fill='both', expand=True, pady=20)
        
        tk.Label(activity_frame, text="Recent Activity", 
                font=('Arial', 18, 'bold'), bg='#f0f8ff').pack(pady=10)
        
        activities = [
            "✅ Completed Digital Marketing course",
            "🛍️ Listed new product: Handmade Jewelry",
            "📅 Registered for Entrepreneurship Workshop" if self.registered_workshops else "📅 No workshop registrations yet",
            "💼 Applied for Marketing Internship",
            "👥 Joined Community Discussion"
        ]
        
        for activity in activities:
            tk.Label(activity_frame, text=activity, font=('Arial', 11),
                    bg='white', relief='raised', bd=1).pack(fill='x', pady=2, padx=50)

    def show_learning(self):
        tk.Label(self.content_frame, text="🎓 Learning Center", 
                font=('Arial', 24, 'bold'), bg='#f0f8ff').pack(pady=20)
        
        # Courses List
        courses = [
            {"name": "Digital Marketing", "instructor": "Dr. Smith", "progress": 75, "status": "In Progress"},
            {"name": "Entrepreneurship Fundamentals", "instructor": "Ms. Johnson", "progress": 30, "status": "Started"},
            {"name": "Financial Literacy", "instructor": "Mrs. Davis", "progress": 100, "status": "Completed"},
            {"name": "Web Development", "instructor": "Tech Academy", "progress": 0, "status": "Not Started"}
        ]
        
        for course in courses:
            course_frame = tk.Frame(self.content_frame, bg='white', relief='raised', bd=1)
            course_frame.pack(fill='x', pady=5, padx=50)
            
            # Course info
            info_frame = tk.Frame(course_frame, bg='white')
            info_frame.pack(fill='x', padx=10, pady=10)
            
            tk.Label(info_frame, text=course["name"], font=('Arial', 14, 'bold'), 
                    bg='white').pack(anchor='w')
            tk.Label(info_frame, text=f"Instructor: {course['instructor']} | Status: {course['status']}", 
                    bg='white').pack(anchor='w')
            
            # Progress bar (simulated with label)
            progress_frame = tk.Frame(course_frame, bg='white')
            progress_frame.pack(fill='x', padx=10, pady=5)
            
            tk.Label(progress_frame, text="Progress:", bg='white').pack(side='left')
            progress_text = f"{course['progress']}%"
            tk.Label(progress_frame, text=progress_text, font=('Arial', 10, 'bold'),
                    bg='#4ecdc4' if course['progress'] == 100 else '#ff6b6b', 
                    fg='white', width=4).pack(side='left', padx=5)
            
            # Action buttons
            btn_frame = tk.Frame(course_frame, bg='white')
            btn_frame.pack(anchor='e', padx=10, pady=5)
            
            if course['progress'] < 100:
                tk.Button(btn_frame, text="Continue", bg='#45b7d1', fg='white',
                         command=lambda c=course: self.continue_course(c)).pack(side='left', padx=2)
            tk.Button(btn_frame, text="Take Exam", bg='#96ceb4', fg='white',
                     command=lambda c=course: self.take_exam(c)).pack(side='left', padx=2)
            if course['progress'] == 100:
                tk.Button(btn_frame, text="Get Certificate", bg='#ff6b6b', fg='white',
                         command=lambda c=course: self.get_certificate(c)).pack(side='left', padx=2)

    def continue_course(self, course):
        messagebox.showinfo("Continue Course", f"Continuing with: {course['name']}")

    def take_exam(self, course):
        messagebox.showinfo("Take Exam", f"Starting exam for: {course['name']}")

    def get_certificate(self, course):
        messagebox.showinfo("Certificate", f"Generating certificate for: {course['name']}\n\nCertificate successfully generated and downloaded!")

    def show_ecommerce(self):
        tk.Label(self.content_frame, text="🛍️ E-Commerce Marketplace", 
                font=('Arial', 24, 'bold'), bg='#f0f8ff').pack(pady=20)
        
        # Create tabs
        tab_control = ttk.Notebook(self.content_frame)
        
        # Browse Products Tab
        browse_tab = ttk.Frame(tab_control)
        tab_control.add(browse_tab, text='Browse Products')
        
        # My Products Tab
        my_products_tab = ttk.Frame(tab_control)
        tab_control.add(my_products_tab, text='My Products')
        
        tab_control.pack(expand=1, fill='both', padx=20, pady=10)
        
        # Browse Products Content
        products = [
            {
                "name": "Handmade Jewelry Set", 
                "price": "$25", 
                "stock": "15 available", 
                "rating": "4.41", 
                "seller": "CraftyWomen"
            },
            {
                "name": "Organic Lavender Soaps", 
                "price": "$12", 
                "stock": "23 available", 
                "rating": "4.43", 
                "seller": "NaturalBeauty"
            },
            {
                "name": "Embroidery Wall Art", 
                "price": "$45", 
                "stock": "8 available", 
                "rating": "4.47", 
                "seller": "ArtisanHands"
            }
        ]
        
        for product in products:
            product_frame = tk.Frame(browse_tab, bg='white', relief='raised', bd=1)
            product_frame.pack(fill='x', pady=10, padx=20)
            
            # Product name
            name_frame = tk.Frame(product_frame, bg='white')
            name_frame.pack(fill='x', padx=15, pady=5)
            tk.Label(name_frame, text=product["name"], font=('Arial', 14, 'bold'), 
                    bg='white').pack(anchor='w')
            
            # Product details
            details_frame = tk.Frame(product_frame, bg='white')
            details_frame.pack(fill='x', padx=15, pady=5)
            
            # Left side - Rating and seller
            left_frame = tk.Frame(details_frame, bg='white')
            left_frame.pack(side='left', fill='x', expand=True)
            
            tk.Label(left_frame, text=f"⭐{product['rating']} | Seller: {product['seller']}", 
                    font=('Arial', 10), bg='white').pack(anchor='w')
            
            # Right side - Price and stock
            right_frame = tk.Frame(details_frame, bg='white')
            right_frame.pack(side='right')
            
            tk.Label(right_frame, text=product["price"], font=('Arial', 16, 'bold'), 
                    bg='white', fg='#e75480').pack(anchor='e')
            tk.Label(right_frame, text=product["stock"], font=('Arial', 10), 
                    bg='white', fg='#666666').pack(anchor='e')
            
            # Add to Cart button
            btn_frame = tk.Frame(product_frame, bg='white')
            btn_frame.pack(fill='x', padx=15, pady=10)
            
            add_cart_btn = tk.Button(btn_frame, text="Add to Cart", 
                                   bg='#28a745', fg='white', font=('Arial', 11, 'bold'),
                                   padx=20, pady=8,
                                   command=lambda p=product: self.add_to_cart(p))
            add_cart_btn.pack(anchor='e')

    def add_to_cart(self, product):
        """Handle adding product to cart with proper functionality"""
        # Show add to cart confirmation
        result = messagebox.askyesno(
            "Add to Cart", 
            f"Add '{product['name']}' to your cart?\n\n"
            f"Price: {product['price']}\n"
            f"Seller: {product['seller']}\n"
            f"Rating: ⭐{product['rating']}"
        )
        
        if result:
            # Simulate adding to cart
            messagebox.showinfo(
                "Added to Cart", 
                f"✅ '{product['name']}' has been added to your cart!\n\n"
                f"Price: {product['price']}\n"
                f"You can view your cart and proceed to checkout."
            )

    def show_workshops(self):
        tk.Label(self.content_frame, text="📅 Workshops & Events", 
                font=('Arial', 24, 'bold'), bg='#f0f8ff').pack(pady=20)
        
        # Show registered workshops first
        if self.registered_workshops:
            tk.Label(self.content_frame, text="🎯 Your Registered Workshops", 
                    font=('Arial', 18, 'bold'), bg='#f0f8ff', fg='#e75480').pack(pady=10)
            
            for workshop in self.registered_workshops:
                workshop_frame = tk.Frame(self.content_frame, bg='#d4edda', relief='raised', bd=1)
                workshop_frame.pack(fill='x', pady=5, padx=50)
                
                tk.Label(workshop_frame, text=f"✅ {workshop['title']}", 
                        font=('Arial', 12, 'bold'), bg='#d4edda').pack(anchor='w', padx=10, pady=5)
                tk.Label(workshop_frame, text=f"📅 {workshop['date']} ⏰ {workshop['time']} - REGISTERED", 
                        font=('Arial', 10), bg='#d4edda').pack(anchor='w', padx=10)
                
                tk.Button(workshop_frame, text="View Details", bg='#17a2b8', fg='white',
                         command=lambda w=workshop: self.view_workshop_details(w)).pack(anchor='e', padx=10, pady=5)
        
        # Available workshops
        tk.Label(self.content_frame, text="📋 Available Workshops", 
                font=('Arial', 18, 'bold'), bg='#f0f8ff').pack(pady=20)
        
        workshops = [
            {"title": "Entrepreneurship Masterclass", "date": "2024-01-15", "time": "2:00 PM", "seats": "12/50", "description": "Learn how to start and grow your business"},
            {"title": "Digital Marketing Workshop", "date": "2024-01-20", "time": "10:00 AM", "seats": "35/50", "description": "Master digital marketing strategies"},
            {"title": "Financial Planning Session", "date": "2024-01-25", "time": "3:30 PM", "seats": "8/30", "description": "Plan your financial future"}
        ]
        
        for workshop in workshops:
            # Check if already registered
            is_registered = any(w['title'] == workshop['title'] for w in self.registered_workshops)
            
            workshop_frame = tk.Frame(self.content_frame, bg='white', relief='raised', bd=1)
            workshop_frame.pack(fill='x', pady=8, padx=50)
            
            tk.Label(workshop_frame, text=workshop["title"], font=('Arial', 14, 'bold'), 
                    bg='white').pack(anchor='w', padx=10, pady=5)
            tk.Label(workshop_frame, text=workshop["description"], font=('Arial', 10), 
                    bg='white', wraplength=600).pack(anchor='w', padx=10)
            
            details_frame = tk.Frame(workshop_frame, bg='white')
            details_frame.pack(fill='x', padx=10, pady=5)
            
            tk.Label(details_frame, text=f"📅 {workshop['date']} ⏰ {workshop['time']}", 
                    bg='white').pack(side='left')
            tk.Label(details_frame, text=f"🎟️ Seats: {workshop['seats']}", 
                    bg='white').pack(side='right')
            
            btn_frame = tk.Frame(workshop_frame, bg='white')
            btn_frame.pack(anchor='e', padx=10, pady=5)
            
            if is_registered:
                tk.Button(btn_frame, text="Already Registered", bg='#6c757d', fg='white',
                         state='disabled').pack(side='left', padx=2)
            else:
                tk.Button(btn_frame, text="Register Now", bg='#e75480', fg='white',
                         font=('Arial', 10, 'bold'),
                         command=lambda w=workshop: self.register_for_workshop(w)).pack(side='left', padx=2)
            
            tk.Button(btn_frame, text="View Details", bg='#17a2b8', fg='white',
                     command=lambda w=workshop: self.view_workshop_details(w)).pack(side='left', padx=2)

    def register_for_workshop(self, workshop):
        # Check if already registered
        if any(w['title'] == workshop['title'] for w in self.registered_workshops):
            messagebox.showinfo("Already Registered", f"You are already registered for: {workshop['title']}")
            return
        
        # Show registration form
        self.show_registration_form(workshop)

    def show_registration_form(self, workshop):
        registration_window = tk.Toplevel(self.root)
        registration_window.title(f"Register for {workshop['title']}")
        registration_window.geometry("500x400")
        registration_window.configure(bg='#f0f8ff')
        
        tk.Label(registration_window, text=f"Register for: {workshop['title']}", 
                font=('Arial', 16, 'bold'), bg='#f0f8ff').pack(pady=20)
        
        tk.Label(registration_window, text=f"Date: {workshop['date']} | Time: {workshop['time']}", 
                font=('Arial', 12), bg='#f0f8ff').pack(pady=5)
        
        # Registration form
        form_frame = tk.Frame(registration_window, bg='white', padx=20, pady=20)
        form_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        # Form fields
        fields = ["Full Name", "Email", "Phone", "Organization", "Special Requirements"]
        entries = {}
        
        for field in fields:
            frame = tk.Frame(form_frame, bg='white')
            frame.pack(fill='x', pady=8)
            
            tk.Label(frame, text=field, font=('Arial', 11), bg='white', width=15, anchor='w').pack(side='left')
            
            if field == "Special Requirements":
                entry = tk.Text(frame, height=3, width=30)
            else:
                entry = tk.Entry(frame, width=30)
            entry.pack(side='left', padx=10, fill='x', expand=True)
            entries[field] = entry
        
        # Pre-fill with user data if available
        if self.current_user and self.current_user in self.users:
            user_data = self.users[self.current_user]
            entries["Full Name"].insert(0, user_data.get("name", ""))
            entries["Email"].insert(0, self.current_user)
            entries["Phone"].insert(0, user_data.get("phone", ""))
        
        def submit_registration():
            # Get form data
            registration_data = {}
            for field, entry in entries.items():
                if field == "Special Requirements":
                    registration_data[field] = entry.get("1.0", tk.END).strip()
                else:
                    registration_data[field] = entry.get().strip()
            
            # Validate required fields
            if not registration_data["Full Name"] or not registration_data["Email"]:
                messagebox.showerror("Error", "Please fill in required fields (Name and Email)")
                return
            
            # Save to database
            try:
                self.cursor.execute('''
                    INSERT INTO workshops (user_email, workshop_title, workshop_date, workshop_time, registration_data)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    self.current_user,
                    workshop['title'],
                    workshop['date'],
                    workshop['time'],
                    str(registration_data)
                ))
                
                self.conn.commit()
                
                # Add to registered workshops
                workshop_copy = workshop.copy()
                workshop_copy['registration_data'] = registration_data
                workshop_copy['registration_date'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                self.registered_workshops.append(workshop_copy)
                
                messagebox.showinfo("Registration Successful", 
                                  f"Successfully registered for: {workshop['title']}\n\n"
                                  f"Date: {workshop['date']}\n"
                                  f"Time: {workshop['time']}\n"
                                  f"Confirmation sent to: {registration_data['Email']}\n\n"
                                  "You will receive reminder emails and SMS before the event!")
                
                registration_window.destroy()
                self.show_workshops()  # Refresh the workshops view
                
            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to register: {str(e)}")
                self.conn.rollback()
        
        tk.Button(registration_window, text="Submit Registration", bg='#28a745', fg='white',
                 font=('Arial', 12, 'bold'), command=submit_registration).pack(pady=20)

    def view_workshop_details(self, workshop):
        details_text = f"""
Workshop Details:
───────────────
Title: {workshop['title']}
Date: {workshop['date']}
Time: {workshop['time']}
Seats: {workshop['seats']}
Description: {workshop.get('description', 'No description available')}

"""
        
        if 'registration_data' in workshop:
            details_text += f"""
Your Registration:
────────────────
Name: {workshop['registration_data']['Full Name']}
Email: {workshop['registration_data']['Email']}
Registered on: {workshop['registration_date']}
"""
        
        messagebox.showinfo("Workshop Details", details_text)

    def show_jobs(self):
        tk.Label(self.content_frame, text="💼 Jobs & Mentorship", 
                font=('Arial', 24, 'bold'), bg='#f0f8ff').pack(pady=20)
        
        # Job listings
        jobs = [
            {"title": "Marketing Intern", "company": "TextSolutions Inc", "location": "Remote", "type": "Internship"},
            {"title": "Business Development", "company": "StartUp Ventures", "location": "Mumbai", "type": "Full-time"},
            {"title": "Content Writer", "company": "Digital Media Co", "location": "Remote", "type": "Freelance"}
        ]
        
        for job in jobs:
            job_frame = tk.Frame(self.content_frame, bg='white', relief='raised', bd=1)
            job_frame.pack(fill='x', pady=8, padx=50)
            
            # Job header
            header_frame = tk.Frame(job_frame, bg='white')
            header_frame.pack(fill='x', padx=10, pady=5)
            
            tk.Label(header_frame, text=job["title"], font=('Arial', 14, 'bold'), 
                    bg='white').pack(anchor='w')
            
            # Job details
            details_frame = tk.Frame(job_frame, bg='white')
            details_frame.pack(fill='x', padx=10, pady=2)
            
            tk.Label(details_frame, text=f"{job['company']} | {job['location']} | {job['type']}", 
                    font=('Arial', 10), bg='white', fg='#666666').pack(anchor='w')
            
            # Buttons frame
            btn_frame = tk.Frame(job_frame, bg='white')
            btn_frame.pack(fill='x', padx=10, pady=10)
            
            # Apply with Profile button
            apply_btn = tk.Button(btn_frame, text="Apply with Profile", 
                                bg='#45b7d1', fg='white', font=('Arial', 10, 'bold'),
                                padx=15, pady=5,
                                command=lambda j=job: self.apply_for_job(j))
            apply_btn.pack(side='left', padx=5)
            
            # Book Mentorship button
            mentor_btn = tk.Button(btn_frame, text="Book Mentorship", 
                                 bg='#96ceb4', fg='white', font=('Arial', 10, 'bold'),
                                 padx=15, pady=5,
                                 command=lambda j=job: self.book_mentorship(j))
            mentor_btn.pack(side='left', padx=5)

    def apply_for_job(self, job):
        """Handle job application with database storage"""
        if not self.current_user:
            messagebox.showinfo("Login Required", "Please login to apply for jobs")
            return
        
        application_window = tk.Toplevel(self.root)
        application_window.title(f"Apply for {job['title']}")
        application_window.geometry("500x400")
        application_window.configure(bg='#f0f8ff')
        
        tk.Label(application_window, text=f"Apply for: {job['title']}", 
                font=('Arial', 16, 'bold'), bg='#f0f8ff').pack(pady=20)
        
        tk.Label(application_window, text=f"Company: {job['company']} | Location: {job['location']}", 
                font=('Arial', 12), bg='#f0f8ff').pack(pady=5)
        
        # Application form
        form_frame = tk.Frame(application_window, bg='white', padx=20, pady=20)
        form_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        # Form fields
        fields = ["Full Name", "Email", "Phone", "Current Position", "Years of Experience", "Cover Letter"]
        entries = {}
        
        for field in fields:
            frame = tk.Frame(form_frame, bg='white')
            frame.pack(fill='x', pady=8)
            
            tk.Label(frame, text=field, font=('Arial', 11), bg='white', width=20, anchor='w').pack(side='left')
            
            if field == "Cover Letter":
                entry = tk.Text(frame, height=4, width=30)
            else:
                entry = tk.Entry(frame, width=30)
            entry.pack(side='left', padx=10, fill='x', expand=True)
            entries[field] = entry
        
        # Pre-fill with user data
        if self.current_user in self.users:
            user_data = self.users[self.current_user]
            entries["Full Name"].insert(0, user_data.get("name", ""))
            entries["Email"].insert(0, self.current_user)
            entries["Phone"].insert(0, user_data.get("phone", ""))
        
        def submit_application():
            application_data = {}
            for field, entry in entries.items():
                if field == "Cover Letter":
                    application_data[field] = entry.get("1.0", tk.END).strip()
                else:
                    application_data[field] = entry.get().strip()
            
            # Validate required fields
            required_fields = ["Full Name", "Email", "Phone"]
            for field in required_fields:
                if not application_data[field]:
                    messagebox.showerror("Error", f"Please fill in {field}")
                    return
            
            # Save to database
            try:
                self.cursor.execute('''
                    INSERT INTO job_applications (user_email, job_title, company, application_data)
                    VALUES (?, ?, ?, ?)
                ''', (
                    self.current_user,
                    job['title'],
                    job['company'],
                    str(application_data)
                ))
                
                self.conn.commit()
                
                messagebox.showinfo("Application Submitted", 
                                  f"Application for {job['title']} at {job['company']} submitted successfully!\n\n"
                                  f"Application ID: JOB{random.randint(1000, 9999)}\n"
                                  f"Status: Under Review\n"
                                  f"Expected response time: 5-7 working days\n\n"
                                  "You will receive updates on your registered email.")
                
                application_window.destroy()
                
            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to submit application: {str(e)}")
                self.conn.rollback()
        
        tk.Button(application_window, text="Submit Application", bg='#28a745', fg='white',
                 font=('Arial', 12, 'bold'), command=submit_application).pack(pady=20)

    def book_mentorship(self, job):
        """Handle mentorship booking"""
        mentorship_window = tk.Toplevel(self.root)
        mentorship_window.title(f"Book Mentorship - {job['title']}")
        mentorship_window.geometry("500x450")
        mentorship_window.configure(bg='#f0f8ff')
        
        tk.Label(mentorship_window, text=f"Book Mentorship Session", 
                font=('Arial', 16, 'bold'), bg='#f0f8ff').pack(pady=20)
        
        tk.Label(mentorship_window, text=f"For: {job['title']} at {job['company']}", 
                font=('Arial', 12), bg='#f0f8ff').pack(pady=5)
        
        # Mentorship form
        form_frame = tk.Frame(mentorship_window, bg='white', padx=20, pady=20)
        form_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        # Available mentors
        tk.Label(form_frame, text="Available Mentors:", font=('Arial', 12, 'bold'), 
                bg='white').pack(anchor='w', pady=(0, 10))
        
        mentors = [
            {"name": "Sarah Johnson", "role": "Senior Marketing Manager", "experience": "8 years"},
            {"name": "Priya Sharma", "role": "Business Development Head", "experience": "10 years"},
            {"name": "Maria Garcia", "role": "Content Strategy Director", "experience": "7 years"}
        ]
        
        mentor_var = tk.StringVar(value=mentors[0]["name"])
        for mentor in mentors:
            frame = tk.Frame(form_frame, bg='white')
            frame.pack(fill='x', pady=5)
            
            rb = tk.Radiobutton(frame, text=f"{mentor['name']} - {mentor['role']} ({mentor['experience']})", 
                              variable=mentor_var, value=mentor['name'], bg='white')
            rb.pack(anchor='w')
        
        # Date and time
        tk.Label(form_frame, text="Preferred Date & Time:", font=('Arial', 12, 'bold'), 
                bg='white').pack(anchor='w', pady=(20, 10))
        
        date_frame = tk.Frame(form_frame, bg='white')
        date_frame.pack(fill='x', pady=5)
        
        tk.Label(date_frame, text="Date:", bg='white', width=10).pack(side='left')
        date_entry = tk.Entry(date_frame, width=15)
        date_entry.pack(side='left', padx=5)
        date_entry.insert(0, "YYYY-MM-DD")
        
        tk.Label(date_frame, text="Time:", bg='white', width=10).pack(side='left', padx=(20,0))
        time_entry = tk.Entry(date_frame, width=10)
        time_entry.pack(side='left', padx=5)
        time_entry.insert(0, "HH:MM")
        
        # Discussion topics
        tk.Label(form_frame, text="Discussion Topics:", font=('Arial', 12, 'bold'), 
                bg='white').pack(anchor='w', pady=(20, 10))
        
        topics_text = tk.Text(form_frame, height=3, width=50)
        topics_text.pack(fill='x', pady=5)
        topics_text.insert("1.0", "What would you like to discuss with the mentor?")
        
        def book_session():
            selected_mentor = mentor_var.get()
            date = date_entry.get()
            time = time_entry.get()
            topics = topics_text.get("1.0", tk.END).strip()
            
            if not date or not time or topics == "What would you like to discuss with the mentor?":
                messagebox.showerror("Error", "Please fill in all fields")
                return
            
            messagebox.showinfo("Mentorship Booked", 
                              f"Mentorship session booked successfully!\n\n"
                              f"Mentor: {selected_mentor}\n"
                              f"Date: {date}\n"
                              f"Time: {time}\n"
                              f"Job Role: {job['title']}\n\n"
                              "You will receive a confirmation email with meeting details.")
            
            mentorship_window.destroy()
        
        tk.Button(mentorship_window, text="Book Session", bg='#e75480', fg='white',
                 font=('Arial', 12, 'bold'), command=book_session).pack(pady=20)

    def show_schemes(self):
        tk.Label(self.content_frame, text="🏛️ Government Schemes", 
                font=('Arial', 24, 'bold'), bg='#f0f8ff').pack(pady=20)
        
        schemes = [
            {
                "name": "Women Entrepreneurship Scheme", 
                "eligibility": "Rural Women, Age 18-45, Annual Income < ₹5L", 
                "benefit": "₹50,000 subsidy + Business training",
                "criteria": {"location": "Rural", "age_min": 18, "age_max": 45, "income_max": 500000}
            },
            {
                "name": "Skill Development Grant", 
                "eligibility": "Age 18-35, Education: 10th pass or above", 
                "benefit": "Free training + ₹5,000 monthly stipend",
                "criteria": {"age_min": 18, "age_max": 35, "education_min": "10th"}
            },
            {
                "name": "Small Business Loan", 
                "eligibility": "Existing entrepreneurs, Business > 1 year", 
                "benefit": "Low interest loan up to ₹10L",
                "criteria": {"business_experience": 1, "existing_business": True}
            },
            {
                "name": "Higher Education Scholarship", 
                "eligibility": "Girl students, Family Income < ₹3L", 
                "benefit": "Full tuition fee + ₹10,000 monthly",
                "criteria": {"gender": "Female", "age_max": 25, "income_max": 300000, "student_status": True}
            }
        ]
        
        # Profile setup button
        profile_btn_frame = tk.Frame(self.content_frame, bg='#f0f8ff')
        profile_btn_frame.pack(pady=10)
        
        tk.Button(profile_btn_frame, text="📝 Setup Your Profile for Better Recommendations", 
                 bg='#e75480', fg='white', font=('Arial', 12, 'bold'),
                 command=self.setup_user_profile).pack(pady=5)
        
        for scheme in schemes:
            scheme_frame = tk.Frame(self.content_frame, bg='white', relief='raised', bd=1)
            scheme_frame.pack(fill='x', pady=8, padx=50)
            
            tk.Label(scheme_frame, text=scheme["name"], font=('Arial', 14, 'bold'), 
                    bg='white').pack(anchor='w', padx=10, pady=5)
            tk.Label(scheme_frame, text=f"✅ Eligibility: {scheme['eligibility']}", 
                    bg='white', wraplength=800).pack(anchor='w', padx=10)
            tk.Label(scheme_frame, text=f"💰 Benefit: {scheme['benefit']}", 
                    bg='white', wraplength=800).pack(anchor='w', padx=10)
            
            btn_frame = tk.Frame(scheme_frame, bg='white')
            btn_frame.pack(anchor='e', padx=10, pady=5)
            
            tk.Button(btn_frame, text="Check Eligibility", bg='#ff6b6b', fg='white',
                     command=lambda s=scheme: self.check_eligibility(s)).pack(side='left', padx=2)
            tk.Button(btn_frame, text="Apply Now", bg='#28a745', fg='white',
                     command=lambda s=scheme: self.apply_for_scheme(s)).pack(side='left', padx=2)

    def setup_user_profile(self):
        profile_window = tk.Toplevel(self.root)
        profile_window.title("Setup Your Profile")
        profile_window.geometry("500x500")
        profile_window.configure(bg='#f0f8ff')
        
        tk.Label(profile_window, text="Setup Your Profile for Scheme Recommendations", 
                font=('Arial', 16, 'bold'), bg='#f0f8ff').pack(pady=20)
        
        form_frame = tk.Frame(profile_window, bg='white', padx=20, pady=20)
        form_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        # Age
        tk.Label(form_frame, text="Age:", bg='white').pack(anchor='w')
        age_var = tk.StringVar(value=str(self.user_profile["age"]))
        age_spinbox = tk.Spinbox(form_frame, from_=18, to=65, textvariable=age_var, width=10)
        age_spinbox.pack(anchor='w', pady=5)
        
        # Location
        tk.Label(form_frame, text="Location:", bg='white').pack(anchor='w', pady=(10,0))
        location_var = tk.StringVar(value=self.user_profile["location"])
        location_combo = ttk.Combobox(form_frame, textvariable=location_var, 
                                     values=["Urban", "Rural", "Semi-Urban"])
        location_combo.pack(anchor='w', pady=5)
        
        # Business Type
        tk.Label(form_frame, text="Business Type:", bg='white').pack(anchor='w', pady=(10,0))
        business_var = tk.StringVar(value=self.user_profile["business_type"])
        business_combo = ttk.Combobox(form_frame, textvariable=business_var,
                                     values=["None", "Small Business", "Startup", "Home-based", "Service"])
        business_combo.pack(anchor='w', pady=5)
        
        # Education
        tk.Label(form_frame, text="Education:", bg='white').pack(anchor='w', pady=(10,0))
        education_var = tk.StringVar(value=self.user_profile["education"])
        education_combo = ttk.Combobox(form_frame, textvariable=education_var,
                                      values=["10th", "12th", "Diploma", "Graduate", "Post Graduate"])
        education_combo.pack(anchor='w', pady=5)
        
        # Income Level
        tk.Label(form_frame, text="Income Level:", bg='white').pack(anchor='w', pady=(10,0))
        income_var = tk.StringVar(value=self.user_profile["income_level"])
        income_combo = ttk.Combobox(form_frame, textvariable=income_var,
                                   values=["Low (< ₹3L)", "Medium (₹3L-₹8L)", "High (> ₹8L)"])
        income_combo.pack(anchor='w', pady=5)
        
        def save_profile():
            try:
                self.user_profile = {
                    "age": int(age_var.get()),
                    "location": location_var.get(),
                    "business_type": business_var.get(),
                    "education": education_var.get(),
                    "income_level": income_var.get()
                }
                
                # Save to database if user is logged in
                if self.current_user:
                    self.cursor.execute('''
                        INSERT OR REPLACE INTO user_profile 
                        (user_email, age, location, business_type, education, income_level)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        self.current_user,
                        int(age_var.get()),
                        location_var.get(),
                        business_var.get(),
                        education_var.get(),
                        income_var.get()
                    ))
                    self.conn.commit()
                
                messagebox.showinfo("Success", "Profile updated successfully!\nYou'll get better scheme recommendations now.")
                profile_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid age")
        
        tk.Button(profile_window, text="Save Profile", bg='#28a745', fg='white',
                 font=('Arial', 12, 'bold'), command=save_profile).pack(pady=20)

    def check_eligibility(self, scheme):
        eligibility_result = self.calculate_eligibility(scheme)
        
        result_text = f"Eligibility Check for: {scheme['name']}\n"
        result_text += "=" * 40 + "\n\n"
        
        if eligibility_result["eligible"]:
            result_text += "✅ CONGRATULATIONS! You are ELIGIBLE for this scheme!\n\n"
            result_text += f"Benefits: {scheme['benefit']}\n\n"
            result_text += "Next Steps:\n"
            result_text += "• Click 'Apply Now' to submit your application\n"
            result_text += "• Prepare required documents\n"
            result_text += "• Application will be processed within 15 days\n"
        else:
            result_text += "❌ Sorry, you are NOT ELIGIBLE for this scheme.\n\n"
            result_text += f"Reasons:\n"
            for reason in eligibility_result["reasons"]:
                result_text += f"• {reason}\n"
            result_text += f"\nEligibility Criteria: {scheme['eligibility']}"
        
        messagebox.showinfo("Eligibility Result", result_text)

    def calculate_eligibility(self, scheme):
        criteria = scheme.get("criteria", {})
        reasons = []
        eligible = True
        
        # Check age criteria
        if "age_min" in criteria and self.user_profile["age"] < criteria["age_min"]:
            reasons.append(f"Minimum age required: {criteria['age_min']} years")
            eligible = False
        if "age_max" in criteria and self.user_profile["age"] > criteria["age_max"]:
            reasons.append(f"Maximum age allowed: {criteria['age_max']} years")
            eligible = False
        
        # Check location criteria
        if "location" in criteria and self.user_profile["location"] != criteria["location"]:
            reasons.append(f"Required location: {criteria['location']}")
            eligible = False
        
        # Check income criteria
        if "income_max" in criteria:
            income_map = {"Low (< ₹3L)": 300000, "Medium (₹3L-₹8L)": 500000, "High (> ₹8L)": 1000000}
            user_income = income_map.get(self.user_profile["income_level"], 500000)
            if user_income > criteria["income_max"]:
                reasons.append(f"Maximum annual income allowed: ₹{criteria['income_max']:,}")
                eligible = False
        
        # Check business experience
        if criteria.get("existing_business") and self.user_profile["business_type"] == "None":
            reasons.append("Existing business required")
            eligible = False
        
        return {"eligible": eligible, "reasons": reasons}

    def apply_for_scheme(self, scheme):
        eligibility = self.calculate_eligibility(scheme)
        
        if not eligibility["eligible"]:
            messagebox.showerror("Not Eligible", 
                               f"You are not eligible for {scheme['name']}.\n\n"
                               "Please check eligibility criteria first.")
            return
        
        # Show application form
        application_window = tk.Toplevel(self.root)
        application_window.title(f"Apply for {scheme['name']}")
        application_window.geometry("500x400")
        application_window.configure(bg='#f0f8ff')
        
        tk.Label(application_window, text=f"Apply for: {scheme['name']}", 
                font=('Arial', 16, 'bold'), bg='#f0f8ff').pack(pady=20)
        
        form_frame = tk.Frame(application_window, bg='white', padx=20, pady=20)
        form_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        # Application form fields
        fields = ["Full Name", "Aadhar Number", "Bank Account Number", "IFSC Code", "Additional Information"]
        entries = {}
        
        for field in fields:
            frame = tk.Frame(form_frame, bg='white')
            frame.pack(fill='x', pady=8)
            
            tk.Label(frame, text=field, font=('Arial', 11), bg='white', width=20, anchor='w').pack(side='left')
            
            if field == "Additional Information":
                entry = tk.Text(frame, height=3, width=30)
            else:
                entry = tk.Entry(frame, width=30)
            entry.pack(side='left', padx=10, fill='x', expand=True)
            entries[field] = entry
        
        # Pre-fill with user data if available
        if self.current_user and self.current_user in self.users:
            user_data = self.users[self.current_user]
            entries["Full Name"].insert(0, user_data.get("name", ""))
        
        def submit_application():
            application_data = {}
            for field, entry in entries.items():
                if field == "Additional Information":
                    application_data[field] = entry.get("1.0", tk.END).strip()
                else:
                    application_data[field] = entry.get().strip()
            
            # Validate required fields
            required_fields = ["Full Name", "Aadhar Number", "Bank Account Number", "IFSC Code"]
            for field in required_fields:
                if not application_data[field]:
                    messagebox.showerror("Error", f"Please fill in {field}")
                    return
            
            messagebox.showinfo("Application Submitted", 
                              f"Application for {scheme['name']} submitted successfully!\n\n"
                              f"Application ID: WEP{random.randint(1000, 9999)}\n"
                              f"Status: Under Review\n"
                              f"Expected processing time: 15 working days\n\n"
                              "You will receive updates on your registered email.")
            
            application_window.destroy()
        
        tk.Button(application_window, text="Submit Application", bg='#28a745', fg='white',
                 font=('Arial', 12, 'bold'), command=submit_application).pack(pady=20)

    def show_community(self):
        tk.Label(self.content_frame, text="👥 Community & Support", 
                font=('Arial', 24, 'bold'), bg='#f0f8ff').pack(pady=20)
        
        # Create tabs for different community features
        tab_control = ttk.Notebook(self.content_frame)
        
        # Community Chat Tab
        chat_tab = ttk.Frame(tab_control)
        tab_control.add(chat_tab, text='💬 Community Chat')
        
        # AI Chatbot Tab
        chatbot_tab = ttk.Frame(tab_control)
        tab_control.add(chatbot_tab, text='🤖 AI Assistant')
        
        # Support Resources Tab
        support_tab = ttk.Frame(tab_control)
        tab_control.add(support_tab, text='🆘 Support Resources')
        
        tab_control.pack(expand=1, fill='both', padx=20, pady=10)
        
        # Setup each tab
        self.setup_community_chat(chat_tab)
        self.setup_ai_chatbot(chatbot_tab)
        self.setup_support_resources(support_tab)

    def setup_community_chat(self, parent):
        # Community chat implementation
        chat_frame = tk.Frame(parent, bg='white', relief='sunken', bd=1)
        chat_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Chat display
        self.community_chat_display = scrolledtext.ScrolledText(chat_frame, height=15, width=60, bg='#f8f9fa')
        self.community_chat_display.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Pre-populate with sample messages
        sample_messages = [
            "Welcome to the Women Empowerment Community! 👋",
            "Share your success stories and support each other! 💪",
            "Need help? Ask our community or use the safety helpline! 🆘"
        ]
        
        for msg in sample_messages:
            self.community_chat_display.insert(tk.END, f"System: {msg}\n\n")
        
        # Message input
        input_frame = tk.Frame(chat_frame, bg='white')
        input_frame.pack(fill='x', padx=5, pady=5)
        
        self.community_message_entry = tk.Entry(input_frame, width=50)
        self.community_message_entry.pack(side='left', padx=5)
        self.community_message_entry.insert(0, "Type your message here...")
        self.community_message_entry.bind('<FocusIn>', lambda e: self.community_message_entry.delete(0, tk.END) if self.community_message_entry.get() == "Type your message here..." else None)
        
        tk.Button(input_frame, text="Send", bg='#e75480', fg='white',
                 command=self.send_community_message).pack(side='left', padx=5)

    def send_community_message(self):
        message = self.community_message_entry.get()
        if message and message != "Type your message here...":
            self.community_chat_display.insert(tk.END, f"You: {message}\n\n")
            self.community_chat_display.see(tk.END)
            self.community_message_entry.delete(0, tk.END)
            
            # Simulate community responses
            responses = [
                "That's a great question! I faced similar challenges when starting my business.",
                "Thank you for sharing your experience! This is really helpful for others.",
                "Has anyone else encountered this situation? How did you handle it?",
                "I recommend checking the learning section for courses on this topic.",
                "Wonderful achievement! Your success inspires all of us. 🎉"
            ]
            
            # Simulate delayed response
            self.root.after(2000, lambda: self.add_community_response(random.choice(responses)))

    def add_community_response(self, response):
        self.community_chat_display.insert(tk.END, f"Community Member: {response}\n\n")
        self.community_chat_display.see(tk.END)

    def setup_ai_chatbot(self, parent):
        # AI Chatbot implementation
        chatbot_frame = tk.Frame(parent, bg='white', relief='sunken', bd=1)
        chatbot_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Welcome message
        welcome_label = tk.Label(chatbot_frame, 
                               text="🤖 Women Empowerment AI Assistant\nI'm here to help you with courses, business, schemes, and more!",
                               font=('Arial', 12, 'bold'), bg='#e8f4f8', fg='#2c3e50')
        welcome_label.pack(fill='x', padx=5, pady=10)
        
        # Chat display
        self.chatbot_display = scrolledtext.ScrolledText(chatbot_frame, height=15, width=60, bg='#f8f9fa')
        self.chatbot_display.pack(fill='both', expand=True, padx=5, pady=5)
        self.chatbot_display.insert(tk.END, "AI Assistant: Hello! I'm your Women Empowerment Assistant. How can I help you today?\n\n")
        self.chatbot_display.config(state=tk.DISABLED)
        
        # Quick action buttons
        quick_actions_frame = tk.Frame(chatbot_frame, bg='white')
        quick_actions_frame.pack(fill='x', padx=5, pady=5)
        
        quick_actions = [
            ("🎓 Course Help", "I need help with courses and learning"),
            ("💼 Business", "I want business and entrepreneurship advice"),
            ("🏛️ Schemes", "Help me with government schemes"),
            ("🛍️ E-commerce", "I need help with selling products")
        ]
        
        for action, message in quick_actions:
            tk.Button(quick_actions_frame, text=action, font=('Arial', 8),
                     bg='#45b7d1', fg='white', width=15,
                     command=lambda m=message: self.ask_ai_question(m)).pack(side='left', padx=2)
        
        # Message input
        input_frame = tk.Frame(chatbot_frame, bg='white')
        input_frame.pack(fill='x', padx=5, pady=5)
        
        self.chatbot_message_entry = tk.Entry(input_frame, width=50)
        self.chatbot_message_entry.pack(side='left', padx=5)
        self.chatbot_message_entry.insert(0, "Ask me anything about women empowerment...")
        self.chatbot_message_entry.bind('<FocusIn>', lambda e: self.chatbot_message_entry.delete(0, tk.END) if self.chatbot_message_entry.get() == "Ask me anything about women empowerment..." else None)
        self.chatbot_message_entry.bind('<Return>', lambda e: self.ask_ai_question())
        
        tk.Button(input_frame, text="Send", bg='#e75480', fg='white',
                 command=lambda: self.ask_ai_question()).pack(side='left', padx=5)

    def ask_ai_question(self, predefined_message=None):
        if predefined_message:
            question = predefined_message
        else:
            question = self.chatbot_message_entry.get()
            
        if question and question != "Ask me anything about women empowerment...":
            # Enable display for writing
            self.chatbot_display.config(state=tk.NORMAL)
            self.chatbot_display.insert(tk.END, f"You: {question}\n\n")
            self.chatbot_display.see(tk.END)
            
            if predefined_message is None:
                self.chatbot_message_entry.delete(0, tk.END)
            
            # Show typing indicator
            self.chatbot_display.insert(tk.END, "AI Assistant: 🤔 Thinking...\n\n")
            self.chatbot_display.see(tk.END)
            self.chatbot_display.config(state=tk.DISABLED)
            
            # Simulate AI processing and response
            self.root.after(1500, lambda: self.generate_ai_response(question))

    def generate_ai_response(self, question):
        # Enable display for writing
        self.chatbot_display.config(state=tk.NORMAL)
        
        # Remove "Thinking..." message
        self.chatbot_display.delete("end-2l", "end-1l")
        
        # Generate AI response based on question
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['course', 'learn', 'study', 'education']):
            response = self.get_course_advice(question)
        elif any(word in question_lower for word in ['business', 'entrepreneur', 'startup', 'sell']):
            response = self.get_business_advice(question)
        elif any(word in question_lower for word in ['scheme', 'government', 'subsidy', 'loan']):
            response = self.get_scheme_advice(question)
        elif any(word in question_lower for word in ['product', 'e-commerce', 'market', 'price']):
            response = self.get_ecommerce_advice(question)
        elif any(word in question_lower for word in ['job', 'career', 'mentorship', 'intern']):
            response = self.get_career_advice(question)
        elif any(word in question_lower for word in ['help', 'support', 'problem', 'issue']):
            response = self.get_general_help(question)
        else:
            response = self.get_general_response(question)
        
        self.chatbot_display.insert(tk.END, f"AI Assistant: {response}\n\n")
        self.chatbot_display.see(tk.END)
        self.chatbot_display.config(state=tk.DISABLED)

    def get_course_advice(self, question):
        courses_advice = {
            'digital marketing': "I recommend our Digital Marketing course! It covers SEO, social media marketing, and digital advertising. Perfect for business growth!",
            'entrepreneurship': "Our Entrepreneurship Fundamentals course is excellent! It teaches business planning, funding, and market analysis.",
            'financial': "The Financial Literacy course will help you manage money, investments, and business finances effectively.",
            'web development': "Web Development course is great for tech skills! Learn HTML, CSS, and JavaScript to build websites.",
            'default': "Based on your interests, I recommend checking our Learning Center. We have courses in Digital Marketing, Entrepreneurship, Financial Literacy, and Web Development that might interest you!"
        }
        
        for key in courses_advice:
            if key in question.lower():
                return courses_advice[key]
        return courses_advice['default']

    def get_business_advice(self, question):
        business_advice = [
            "Start with market research to understand your target audience and competition.",
            "Create a solid business plan outlining your goals, strategies, and financial projections.",
            "Leverage digital marketing to reach more customers - social media is powerful!",
            "Consider starting small and scaling gradually to manage risks effectively.",
            "Network with other women entrepreneurs for support and collaboration opportunities.",
            "Use our E-commerce platform to sell your products with low startup costs."
        ]
        return random.choice(business_advice)

    def get_scheme_advice(self, question):
        scheme_advice = [
            "Check the Government Schemes section to see which schemes you're eligible for based on your profile.",
            "The Women Entrepreneurship Scheme offers ₹50,000 subsidy for rural women entrepreneurs.",
            "Skill Development Grant provides free training with monthly stipend for age 18-35.",
            "Small Business Loan offers low-interest loans up to ₹10L for existing businesses.",
            "Setup your profile first for personalized scheme recommendations!"
        ]
        return random.choice(scheme_advice)

    def get_ecommerce_advice(self, question):
        ecommerce_advice = [
            "Take clear, high-quality photos of your products from multiple angles.",
            "Write detailed product descriptions highlighting benefits and features.",
            "Price competitively but don't undervalue your work and time.",
            "Offer excellent customer service to build trust and repeat business.",
            "Use social media to promote your products and drive traffic to your store.",
            "Consider packaging and shipping as part of your customer experience."
        ]
        return random.choice(ecommerce_advice)

    def get_career_advice(self, question):
        career_advice = [
            "Update your skills regularly through our learning courses to stay competitive.",
            "Network professionally and build connections in your industry.",
            "Consider mentorship - experienced guidance can accelerate your career growth.",
            "Look for internships or freelance work to gain practical experience.",
            "Build a strong professional profile highlighting your achievements and skills.",
            "Don't be afraid to negotiate your worth - research market salaries for your role."
        ]
        return random.choice(career_advice)

    def get_general_help(self, question):
        general_help = [
            "I'm here to help! You can ask me about courses, business advice, government schemes, or anything else related to women empowerment.",
            "Feel free to explore different sections of our platform - we have resources for learning, business, schemes, and community support.",
            "If you need immediate help, use the Emergency Helpline button for urgent assistance.",
            "Remember, you're not alone! Our community is here to support your journey to empowerment.",
            "Take one step at a time. Every small achievement brings you closer to your goals! 💪"
        ]
        return random.choice(general_help)

    def get_general_response(self, question):
        general_responses = [
            "That's an interesting question! Our platform offers various resources to support women in education, business, and personal growth.",
            "I understand you're looking for information. We have courses, business tools, government schemes, and a supportive community here.",
            "Great question! Let me connect you with the right resources. What specific area are you most interested in?",
            "I'd be happy to help! Our women empowerment platform focuses on education, entrepreneurship, and community support.",
            "Thanks for asking! We're here to help women achieve their goals through learning opportunities, business support, and financial schemes."
        ]
        return random.choice(general_responses)

    def setup_support_resources(self, parent):
        # Support resources implementation
        resources_frame = tk.Frame(parent, bg='#f0f8ff')
        resources_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Emergency contacts
        tk.Label(resources_frame, text="🆘 Emergency Contacts - Available 24/7", 
                font=('Arial', 16, 'bold'), bg='#f0f8ff').pack(pady=10)
        
        emergencies = [
            {"service": "National Women Helpline", "number": "181", "hours": "24/7"},
            {"service": "Police Emergency", "number": "100", "hours": "24/7"},
            {"service": "Ambulance", "number": "102", "hours": "24/7"},
            {"service": "Mental Health Crisis", "number": "080-46110007", "hours": "24/7"},
            {"service": "Domestic Violence", "number": "181", "hours": "24/7"}
        ]
        
        for emergency in emergencies:
            emergency_frame = tk.Frame(resources_frame, bg='#ffe6e6', relief='raised', bd=1)
            emergency_frame.pack(fill='x', pady=5, padx=20)
            
            tk.Label(emergency_frame, text=emergency["service"], font=('Arial', 12, 'bold'), 
                    bg='#ffe6e6').pack(anchor='w', padx=10, pady=5)
            tk.Label(emergency_frame, text=f"📞 {emergency['number']} | ⏰ {emergency['hours']}", 
                    font=('Arial', 11), bg='#ffe6e6').pack(anchor='w', padx=10)
        
        # Support groups
        tk.Label(resources_frame, text="👥 Support Groups", 
                font=('Arial', 16, 'bold'), bg='#f0f8ff').pack(pady=(20,10))
        
        groups = [
            {"name": "Women Entrepreneurs Network", "focus": "Business support and networking"},
            {"name": "Career Growth Community", "focus": "Professional development and job opportunities"},
            {"name": "Mental Wellness Circle", "focus": "Emotional support and self-care"},
            {"name": "Single Mothers Support", "focus": "Childcare and financial planning"}
        ]
        
        for group in groups:
            group_frame = tk.Frame(resources_frame, bg='#e8f4f8', relief='raised', bd=1)
            group_frame.pack(fill='x', pady=5, padx=20)
            
            tk.Label(group_frame, text=group["name"], font=('Arial', 11, 'bold'), 
                    bg='#e8f4f8').pack(anchor='w', padx=10, pady=5)
            tk.Label(group_frame, text=f"💬 {group['focus']}", 
                    bg='#e8f4f8').pack(anchor='w', padx=10)

    def show_analytics(self):
        tk.Label(self.content_frame, text="📊 Analytics Dashboard", 
                font=('Arial', 24, 'bold'), bg='#f0f8ff').pack(pady=20)
        
        # Get data from database for analytics
        workshop_count = len(self.registered_workshops)
        
        # Get job applications count from database
        job_applications_count = 0
        if self.current_user:
            self.cursor.execute('SELECT COUNT(*) FROM job_applications WHERE user_email = ?', (self.current_user,))
            job_applications_count = self.cursor.fetchone()[0]
        
        analytics_data = [
            ("Total Courses Completed", "3", "#ff6b6b"),
            ("Products Sold This Month", "8", "#4ecdc4"),
            ("Workshops Attended", f"{workshop_count}", "#45b7d1"),
            ("Job Applications", f"{job_applications_count}", "#96ceb4"),
            ("Community Posts", "15", "#ff9ff3"),
            ("Certificates Earned", "4", "#f368e0")
        ]
        
        analytics_frame = tk.Frame(self.content_frame, bg='#f0f8ff')
        analytics_frame.pack(fill='both', expand=True, padx=50, pady=20)
        
        for i, (title, value, color) in enumerate(analytics_data):
            row = i // 3
            col = i % 3
            
            metric_frame = tk.Frame(analytics_frame, bg=color, relief='raised', bd=2)
            metric_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            
            tk.Label(metric_frame, text=value, font=('Arial', 20, 'bold'), 
                    bg=color, fg='white').pack(pady=10)
            tk.Label(metric_frame, text=title, font=('Arial', 11), 
                    bg=color, fg='white', wraplength=150).pack(pady=5)
            
            analytics_frame.grid_columnconfigure(col, weight=1)
            analytics_frame.grid_rowconfigure(row, weight=1)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def __del__(self):
        """Close database connection when object is destroyed"""
        if hasattr(self, 'conn'):
            self.conn.close()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = WomenEmpowermentGUI(root)
    root.mainloop()