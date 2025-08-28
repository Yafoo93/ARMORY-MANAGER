import customtkinter as ctk
from src.gui.user_management import UserManagement
from src.gui.weapon_management import WeaponManagement
from src.database import SessionLocal
from src.models.weapon import Weapon
from src.models.booking import Booking

# Set appearance mode and default color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class ArmoryApp(ctk.CTk):
    def __init__(self, user):
        super().__init__()

        self.user = user  # Store the logged-in user

        self.title("Armory Management System")
        self.geometry("900x600")

        # Configure grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Create Navigation Frame (Sidebar)
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color="#333333")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(7, weight=1)

        # App Logo/Title
        self.logo_label = ctk.CTkLabel(self.sidebar, text="ARMORY SYSTEM", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Navigation Menu Label
        self.menu_label = ctk.CTkLabel(self.sidebar, text="NAVIGATION MENU", font=ctk.CTkFont(size=12, weight="bold"))
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
                text_color="white",
                hover_color="#1f538d",
                anchor="w",
                command=lambda k=key: self.show_frame(k)
            )
            button.grid(row=idx + 2, column=0, padx=20, pady=5, sticky="ew")
            self.menu_buttons[key] = button

        # Profile section
        self.profile_label = ctk.CTkLabel(
            self.sidebar,
            text=f"On Duty: {self.user.name}" if self.user and hasattr(self.user, "name") else "Not Signed In",
            font=ctk.CTkFont(size=12),
            anchor="w"
        )
        self.profile_label.grid(row=8, column=0, padx=20, pady=(5, 10))

        # Sign Out Button
        self.sign_out_button = ctk.CTkButton(
            self.sidebar,
            text="Sign Out",
            font=ctk.CTkFont(size=13),
            height=32,
            fg_color="#c75450",
            hover_color="#b44743",
            command=self.sign_out
        )
        self.sign_out_button.grid(row=9, column=0, padx=20, pady=(0, 10), sticky="ew")

        # Create Main Content Frame
        self.content_frame = ctk.CTkFrame(self, corner_radius=10)
        self.content_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # Show Default Dashboard
        self.show_dashboard()

    def show_frame(self, frame_name):
        """Switch between frames."""
        self.clear_content()

        if frame_name == "dashboard":
            self.show_dashboard()
        elif frame_name == "users":
            self.show_users()
        elif frame_name == "weapons":
            self.show_weapons()

    def show_dashboard(self):
        
        from datetime import datetime
        from zoneinfo import ZoneInfo
        from sqlalchemy import func
        """Displays the main dashboard with an overview and statistics."""
        self.clear_content()

        # Dashboard Title
        welcome_label = ctk.CTkLabel(self.content_frame, text="Welcome to Armory Management System",
                                     font=ctk.CTkFont(size=24, weight="bold"), text_color="white")
        welcome_label.pack(pady=(20, 10))

        # Quick Stats Grid
        stats_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        stats_frame.pack(fill="both", expand=True, padx=20, pady=20)
        stats_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Fetch Data from the Database
        session = SessionLocal()

        total_weapons = session.query(Weapon).count()
        booked_out = session.query(Booking).filter(Booking.status == "Booked Out").count()
        due_return = session.query(Booking).filter(Booking.status == "Due Return").count()
        start_date = datetime(2025, 3, 1, tzinfo=ZoneInfo("Africa/Accra"))

        recent_bookings = (
            session.query(Booking)
            .filter(Booking.requested_at >= start_date)
            .count()
        )
        total_ammunition = 5000 

        session.close()

        # Display Statistics
        self.create_stat_box(stats_frame, 0, 0, "Total Weapons in Stock", str(total_weapons), "#2fa572")  # Green
        self.create_stat_box(stats_frame, 0, 1, "Weapons Booked Out", str(booked_out), "#c75450")  # Red
        self.create_stat_box(stats_frame, 0, 2, "Weapons Due Return", str(due_return), "#e69138")  # Orange
        self.create_stat_box(stats_frame, 1, 0, "Recently Booked (24h)", str(recent_bookings), "#3d85c6")  # Blue
        self.create_stat_box(stats_frame, 1, 1, "Ammunition Count", str(total_ammunition), "#674ea7")  # Purple

    def create_stat_box(self, parent, row, column, title, value, color):
        """Helper function to create a stat box."""
        frame = ctk.CTkFrame(parent, fg_color=color, corner_radius=10)
        frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=14, weight="bold"), text_color="white").pack(pady=(10, 5))
        ctk.CTkLabel(frame, text=value, font=ctk.CTkFont(size=28, weight="bold"), text_color="white").pack(pady=(0, 10))

    def show_users(self):
        """Displays the User Management section."""
        self.clear_content()
        UserManagement(self.content_frame)

    def show_weapons(self):
        """Displays the Weapons Management section."""
        self.clear_content()
        WeaponManagement(self.content_frame)

    def clear_content(self):
        """Clears the content area before displaying new content."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def sign_out(self):
        """Handle sign-out functionality."""
        self.destroy()
        from src.gui.login import LoginApp
        app = LoginApp()
        app.mainloop()


def run_main_app(user):
    app = ArmoryApp(user)
    app.mainloop()
