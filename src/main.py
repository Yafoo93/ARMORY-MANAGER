import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from src.gui.user_management import UserManagement


class ArmoryApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="superhero")  # Beautiful dark theme

        self.title("Armory Management System")
        self.geometry("900x600")
        self.resizable(False, False)

        # Navigation Panel (Sidebar)
        sidebar = ttk.Frame(self, padding=10, style="primary.TFrame")
        sidebar.pack(side=LEFT, fill=Y)

        ttk.Label(sidebar, text="MENU", font="Arial 12 bold", foreground="white", background="#333").pack(pady=10)

        # Buttons for different sections
        self.add_menu_button(sidebar, "Manage Users", self.show_users)
        self.add_menu_button(sidebar, "Manage Weapons", self.show_weapons)
        self.add_menu_button(sidebar, "Manage Ammunition", self.show_ammunition)
        self.add_menu_button(sidebar, "Booking & Return", self.show_records)
        self.add_menu_button(sidebar, "Duty Points", self.show_duty_points)

        # Content Area (Right Side)
        self.content_frame = ttk.Frame(self, padding=10)
        self.content_frame.pack(side=RIGHT, fill=BOTH, expand=True)

        # Show the default dashboard
        self.show_dashboard()

    def add_menu_button(self, parent, text, command):
        """Reusable function to add buttons to the sidebar."""
        btn = ttk.Button(parent, text=text, bootstyle="info-outline", command=command)
        btn.pack(fill=X, pady=5)

    def show_dashboard(self):
        """Displays the main dashboard with an overview."""
        self.clear_content()
        ttk.Label(self.content_frame, text="Welcome to Armory Management System",
                  font="Arial 16 bold").pack(pady=20)
        ttk.Label(self.content_frame, text="Select an option from the menu to get started.",
                  font="Arial 12").pack()

    def show_users(self):
        """Displays the User Management section."""
        self.clear_content()
        ttk.Label(self.content_frame, text="Manage Users", font="Arial 14 bold").pack(pady=10)
        
        self.clear_content()
        UserManagement(self.content_frame)

        add_user_btn = ttk.Button(self.content_frame, text="Add New User", bootstyle="success")
        add_user_btn.pack(pady=5)

    def show_weapons(self):
        """Displays the Weapons Management section."""
        self.clear_content()
        ttk.Label(self.content_frame, text="Manage Weapons", font="Arial 14 bold").pack(pady=10)

        add_weapon_btn = ttk.Button(self.content_frame, text="Add New Weapon", bootstyle="success")
        add_weapon_btn.pack(pady=5)

    def show_ammunition(self):
        """Displays the Ammunition Management section."""
        self.clear_content()
        ttk.Label(self.content_frame, text="Manage Ammunition", font="Arial 14 bold").pack(pady=10)

    def show_records(self):
        """Displays the Booking & Return section."""
        self.clear_content()
        ttk.Label(self.content_frame, text="Weapon Booking & Return", font="Arial 14 bold").pack(pady=10)

    def show_duty_points(self):
        """Displays the Duty Points section."""
        self.clear_content()
        ttk.Label(self.content_frame, text="Manage Duty Points", font="Arial 14 bold").pack(pady=10)

    def clear_content(self):
        """Removes all widgets from the content area before displaying a new section."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = ArmoryApp()
    app.mainloop()
