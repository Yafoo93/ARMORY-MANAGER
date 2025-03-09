import customtkinter as ctk
from src.gui.user_management import UserManagement
from src.gui.weapon_management import WeaponManagement

# Set appearance mode and default color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class ArmoryApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Armory Management System")
        self.geometry("900x600")
        
        # Configure grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Create Navigation Frame (Sidebar)
        self.sidebar = ctk.CTkFrame(
            self, 
            width=250, 
            corner_radius=0,
            fg_color="#333333"  # Dark gray background
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(7, weight=1)  # Push menu items to the top
        
        # App Logo/Title
        self.logo_label = ctk.CTkLabel(
            self.sidebar, 
            text="ARMORY SYSTEM",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Navigation Menu Label
        self.menu_label = ctk.CTkLabel(
            self.sidebar,
            text="NAVIGATION MENU",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.menu_label.grid(row=1, column=0, padx=20, pady=(20, 10))

        # Menu Buttons
        self.menu_buttons = {}
        menu_items = {
            "dashboard": "Dashboard",
            "users": "Manage Users",
            "weapons": "Manage Weapons",
            "ammunition": "Manage Ammunition",
            "records": "Booking & Return",
            "duty_points": "Duty Points"
        }
        
        for idx, (key, text) in enumerate(menu_items.items()):
            button = ctk.CTkButton(
                self.sidebar,
                text=text,
                font=ctk.CTkFont(size=14),
                height=40,
                corner_radius=8,
                fg_color="transparent",
                text_color="white",  # White text
                hover_color="#1f538d",  # Dark blue hover
                anchor="w",
                command=lambda k=key: self.show_frame(k)
            )
            if key == "duty_points":
                # Minimal padding for duty points button
                button.grid(row=idx + 2, column=0, padx=20, pady=(0, 20), sticky="ew")
            elif key == "records":
                # Reduced bottom padding for the button above duty points
                button.grid(row=idx + 2, column=0, padx=20, pady=(5, 0), sticky="ew")
            else:
                # Normal padding for other buttons
                button.grid(row=idx + 2, column=0, padx=20, pady=5, sticky="ew")
            self.menu_buttons[key] = button

        # Add a separator line
        self.separator = ctk.CTkFrame(
            self.sidebar,
            height=2,
            fg_color="#666666"  # Light gray line
        )
        self.separator.grid(row=7, column=0, sticky="ew", padx=20, pady=10)
        
        # Profile section frame
        self.profile_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )
        self.profile_frame.grid(row=8, column=0, sticky="ew", padx=20, pady=(5, 10))
        
        # Profile icon (using a simple circle symbol)
        self.profile_icon = ctk.CTkLabel(
            self.profile_frame,
            text="👤",  # Unicode user icon
            font=ctk.CTkFont(size=20),
            width=30
        )
        self.profile_icon.pack(side="left", padx=(0, 10))
        
        # Profile status/name label
        self.profile_label = ctk.CTkLabel(
            self.profile_frame,
            text="Not Signed In",
            font=ctk.CTkFont(size=12),
            anchor="w"
        )
        self.profile_label.pack(side="left", fill="x", expand=True)
        
        # Sign In/Out button
        self.sign_in_button = ctk.CTkButton(
            self.sidebar,
            text="Sign In",
            font=ctk.CTkFont(size=13),
            height=32,
            fg_color="#2fa572",  # Green color
            hover_color="#2a8c61",
            command=self.toggle_sign_in
        )
        self.sign_in_button.grid(row=9, column=0, padx=20, pady=(0, 10), sticky="ew")
        
        # Version label (move to last row)
        self.version_label = ctk.CTkLabel(
            self.sidebar,
            text="v1.0.0",
            font=ctk.CTkFont(size=12)
        )
        self.version_label.grid(row=10, column=0, padx=20, pady=(0, 20))
        
        # Add signed-in state variable
        self.is_signed_in = False
        self.current_armorer = None

        # Create Main Content Frame
        self.content_frame = ctk.CTkFrame(self, corner_radius=10)
        self.content_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        # Show default dashboard
        self.show_dashboard()
        
        # Set default active button
        self.set_active_button("dashboard")

    def set_active_button(self, active_key):
        """Update button colors to show which page is active"""
        for key, button in self.menu_buttons.items():
            if key == active_key:
                button.configure(
                    fg_color="#1f538d",  # Dark blue for active
                    text_color="white"
                )
            else:
                button.configure(
                    fg_color="transparent",
                    text_color="white"
                )

    def show_frame(self, frame_name):
        """Generic function to show different frames"""
        self.clear_content()
        self.set_active_button(frame_name)
        
        if frame_name == "dashboard":
            self.show_dashboard()
        elif frame_name == "users":
            self.show_users()
        elif frame_name == "weapons":
            self.show_weapons()
        elif frame_name == "ammunition":
            self.show_ammunition()
        elif frame_name == "records":
            self.show_records()
        elif frame_name == "duty_points":
            self.show_duty_points()

    def show_dashboard(self):
        """Displays the main dashboard with an overview."""
        # Welcome Frame
        welcome_frame = ctk.CTkFrame(self.content_frame)
        welcome_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Welcome message
        welcome_label = ctk.CTkLabel(
            welcome_frame,
            text="Welcome to Armory Management System",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        )
        welcome_label.pack(pady=(40, 20))
        
        # Quick Stats Grid
        stats_frame = ctk.CTkFrame(welcome_frame, fg_color="transparent")
        stats_frame.pack(fill="x", padx=40, pady=20)
        stats_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # First row of stats
        self.create_stat_box(stats_frame, 0, 0, "Total Weapons in Stock", "120", "#2fa572")  # Green
        self.create_stat_box(stats_frame, 0, 1, "Weapons Booked Out", "30", "#c75450")  # Red
        self.create_stat_box(stats_frame, 0, 2, "Weapons Due Return", "15", "#e69138")  # Orange

        # Second row of stats
        self.create_stat_box(stats_frame, 1, 0, "Recently Booked (24h)", "8", "#3d85c6")  # Blue
        self.create_stat_box(stats_frame, 1, 1, "Ammunition Count", "5000", "#674ea7")  # Purple
        
        # Add a refresh button
        refresh_btn = ctk.CTkButton(
            welcome_frame,
            text="Refresh Stats",
            font=ctk.CTkFont(size=14),
            width=120,
            height=32,
            fg_color="#1f538d",
            hover_color="#1a4572",
            command=self.refresh_dashboard_stats
        )
        refresh_btn.pack(pady=20)

    def create_stat_box(self, parent, row, column, title, value, color):
        """Helper function to create statistics boxes with custom colors"""
        frame = ctk.CTkFrame(
            parent,
            fg_color=color,
            corner_radius=10
        )
        frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(
            frame,
            text=title,
            font=ctk.CTkFont(size=14),
            text_color="white"
        ).pack(pady=(15, 5))
        
        ctk.CTkLabel(
            frame,
            text=value,
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="white"
        ).pack(pady=(0, 15))

    def refresh_dashboard_stats(self):
        """Refresh dashboard statistics from the database"""
        # TODO: Implement actual database queries to get real-time stats
        self.show_dashboard()

    def show_users(self):
        """Displays the User Management section."""
        UserManagement(self.content_frame)

    def show_weapons(self):
        """Displays the Weapons Management section."""
        WeaponManagement(self.content_frame)

    def show_ammunition(self):
        """Displays the Ammunition Management section."""
        label = ctk.CTkLabel(
            self.content_frame,
            text="Ammunition Management",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        label.pack(pady=20)

    def show_records(self):
        """Displays the Booking & Return section."""
        label = ctk.CTkLabel(
            self.content_frame,
            text="Booking & Return Management",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        label.pack(pady=20)

    def show_duty_points(self):
        """Displays the Duty Points section."""
        label = ctk.CTkLabel(
            self.content_frame,
            text="Duty Points Management",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        label.pack(pady=20)

    def clear_content(self):
        """Removes all widgets from the content area."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def toggle_sign_in(self):
        """Handle sign in/out functionality"""
        if not self.is_signed_in:
            # Create a simple dialog for sign in
            dialog = ctk.CTkInputDialog(
                text="Enter Service Number:",
                title="Sign In"
            )
            service_number = dialog.get_input()
            
            if service_number:
                # Here you would normally verify against database
                # For now, we'll just use the input as the name
                self.is_signed_in = True
                self.current_armorer = f"Armorer {service_number}"
                self.profile_label.configure(text=f"On Duty: {self.current_armorer}")
                self.sign_in_button.configure(
                    text="Sign Out",
                    fg_color="#c75450",  # Red color
                    hover_color="#b44743"
                )
        else:
            # Confirm before signing out
            confirm = ctk.CTkMessageBox(
                self,
                title="Confirm Sign Out",
                message="Are you sure you want to sign out?",
                icon="warning",
                option_1="Cancel",
                option_2="Sign Out"
            )
            
            if confirm.get() == "Sign Out":
                self.is_signed_in = False
                self.current_armorer = None
                self.profile_label.configure(text="Not Signed In")
                self.sign_in_button.configure(
                    text="Sign In",
                    fg_color="#2fa572",  # Green color
                    hover_color="#2a8c61"
                )

if __name__ == "__main__":
    app = ArmoryApp()
    app.mainloop()
