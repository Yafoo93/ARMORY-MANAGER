import tkinter as tk
from tkinter import TclError, messagebox

import customtkinter as ctk
from sqlalchemy import text

from src.crud.crud_user import create_user, delete_user, get_all_users, update_user
from src.database import SessionLocal
from src.gui.fingerprint_enroll import FingerprintEnroll

# Set appearance mode and default color theme
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class UserManagement(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=10)
        self.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Create main content frame with proper background color
        self.content_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        self.parent = parent  # Store the parent reference for modal dialogs
        self.db = SessionLocal()  # Database session

        # Create a canvas with scrollbar for the main content - Add background color
        self.canvas = ctk.CTkCanvas(
            self.content_frame,
            highlightthickness=0,
            bg="#2b2b2b",  # Dark background to match theme
        )
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add vertical scrollbar to canvas
        self.scrollbar = ctk.CTkScrollbar(
            self.content_frame, orientation="vertical", command=self.canvas.yview
        )
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        # Create a main container inside the canvas with proper background
        self.main_container = ctk.CTkFrame(
            self.canvas, corner_radius=15, fg_color="#2b2b2b"  # Match canvas background
        )
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.main_container, anchor="nw"
        )

        # Configure the canvas window to expand with the main container
        self.main_container.bind("<Configure>", self.configure_canvas_window)

        # Header with title
        self.header_frame = ctk.CTkFrame(
            self.main_container, corner_radius=0, fg_color="transparent"
        )
        self.header_frame.pack(fill=tk.X, pady=(0, 20))

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Officer Management",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        self.title_label.pack(pady=10)

        # Search and filter frame
        self.search_frame = ctk.CTkFrame(self.main_container, height=50, corner_radius=10)
        self.search_frame.pack(fill=tk.X, pady=(0, 20))

        self.search_entry = ctk.CTkEntry(
            self.search_frame, placeholder_text="Search by name or service number..."
        )
        self.search_entry.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)

        self.search_button = ctk.CTkButton(
            self.search_frame, text="Search", width=100, command=self.search_users
        )
        self.search_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.refresh_button = ctk.CTkButton(
            self.search_frame,
            text="Refresh",
            width=100,
            fg_color="#4CAF50",
            hover_color="#388E3C",
            command=self.load_users,
        )
        self.refresh_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Create a frame for the treeview and scrollbar
        self.tree_frame = ctk.CTkFrame(
            self.main_container,
            corner_radius=10,
            fg_color="#2b2b2b",  # Match main container background
        )
        self.tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # Configure Treeview style
        self.style = tk.ttk.Style()

        # Configure the main Treeview style
        self.style.configure(
            "Treeview",
            background="#2b2b2b",
            foreground="white",
            fieldbackground="#2b2b2b",
            rowheight=30,
            borderwidth=0,
            font=("TkDefaultFont", 10),
        )

        # Configure the Treeview headers with specific colors
        self.style.configure(
            "Treeview.Heading",
            background="#1f6aa5",
            foreground="#000000",
            relief="flat",
            font=("TkDefaultFont", 20, "bold"),
            borderwidth=0,
        )

        # Remove the borders
        self.style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])

        # Important: Add specific mapping for the header background and text color
        self.style.map(
            "Treeview.Heading",
            background=[("active", "#1f6aa5"), ("pressed", "#1f6aa5")],
            foreground=[
                ("active", "#000000"),
                ("pressed", "#000000"),
            ],  # Keep text black in all states
            relief=[("pressed", "flat"), ("!pressed", "flat")],
        )

        # Configure selection colors
        self.style.map(
            "Treeview",
            background=[("selected", "#1f6aa5")],
            foreground=[("selected", "white")],
        )

        # Create scrollbars with matching colors
        self.tree_scroll_y = ctk.CTkScrollbar(
            self.tree_frame,
            orientation="vertical",
            fg_color="#2b2b2b",
            button_color="#1f6aa5",
            button_hover_color="#2980b9",
        )
        self.tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree_scroll_x = ctk.CTkScrollbar(
            self.tree_frame,
            orientation="horizontal",
            fg_color="#2b2b2b",
            button_color="#1f6aa5",
            button_hover_color="#2980b9",
        )
        self.tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Create Treeview with scrollbars
        self.tree = tk.ttk.Treeview(
            self.tree_frame,
            columns=("ID", "Name", "Service No", "Telephone", "Unit"),
            show="headings",
            yscrollcommand=self.tree_scroll_y.set,
            xscrollcommand=self.tree_scroll_x.set,
        )

        # Configure scrollbars
        self.tree_scroll_y.configure(command=self.tree.yview)
        self.tree_scroll_x.configure(command=self.tree.xview)

        # Configure headings and columns
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Service No", text="Service No")
        self.tree.heading("Telephone", text="Telephone")
        self.tree.heading("Unit", text="Unit")

        self.tree.column("ID", width=50, anchor="center", minwidth=50)
        self.tree.column("Name", width=150, minwidth=100)
        self.tree.column("Service No", width=100, anchor="center", minwidth=100)
        self.tree.column("Telephone", width=120, anchor="center", minwidth=100)
        self.tree.column("Unit", width=100, anchor="center", minwidth=100)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # After creating the Treeview, add this line:
        self.tree.tag_configure("oddrow", background="#333333")

        # Load initial data
        self.load_users()

        # Action buttons frame
        self.button_frame = ctk.CTkFrame(
            self.main_container, corner_radius=10, fg_color="transparent"
        )
        self.button_frame.pack(fill=tk.X, pady=(0, 10))

        # Grid layout for buttons
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.columnconfigure(2, weight=1)
        self.button_frame.columnconfigure(3, weight=1)

        # Modern buttons with icons
        self.add_button = ctk.CTkButton(
            self.button_frame,
            text="Add Officer",
            fg_color="#4CAF50",  # Green
            hover_color="#388E3C",
            height=40,
            corner_radius=8,
            command=self.add_user,
        )
        self.add_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.edit_button = ctk.CTkButton(
            self.button_frame,
            text="Edit Officer",
            fg_color="#2196F3",  # Blue
            hover_color="#1976D2",
            height=40,
            corner_radius=8,
            command=self.edit_user,
        )
        self.edit_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.delete_button = ctk.CTkButton(
            self.button_frame,
            text="Delete Officer",
            fg_color="#F44336",  # Red
            hover_color="#D32F2F",
            height=40,
            corner_radius=8,
            command=self.delete_user,
        )
        self.delete_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        # Enroll Fingerprint button
        self.enroll_button = ctk.CTkButton(
            self.button_frame,
            text="Enroll Fingerprint",
            fg_color="#9C27B0",  # Purple
            hover_color="#7B1FA2",
            height=40,
            corner_radius=8,
            command=self.open_fingerprint_enroll,
        )
        self.enroll_button.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

        # Add event binding for double-click edit
        self.tree.bind("<Double-1>", lambda event: self.edit_user())

        self.canvas.bind("<MouseWheel>", self._on_mousewheel)

        # Add unbind method for cleanup
        self.bind("<Destroy>", self._on_destroy)

        # Flag to track if a dialog is open
        self.dialog_open = False

    def configure_canvas_window(self, event):
        """Configure the canvas window to adjust to the size of the content"""
        # Update the scrollregion to encompass the inner frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        # Set the canvas window width to match the width of the canvas
        self.canvas.itemconfig(self.canvas_window, width=self.canvas.winfo_width())

    def _on_mousewheel(self, event):
        """Handle mousewheel scrolling"""
        try:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except tk.TclError:
            pass  # Ignore errors if widget is destroyed

    def _on_destroy(self, event):
        """Clean up bindings when widget is destroyed"""
        if event.widget == self:
            self.canvas.unbind("<MouseWheel>")
            self.canvas.unbind_all("<MouseWheel>")

    def load_users(self):
        """Load users into the table."""
        # Clear existing data
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Get all users from database
        users = get_all_users(self.db)

        # Insert users into treeview with sequential index and alternating colors
        for index, user in enumerate(users, start=1):
            # Use index instead of user.id for display, but keep user.id in the values
            tags = ("oddrow",) if index % 2 else ()
            self.tree.insert(
                "",
                "end",
                values=(
                    index,
                    user.name,
                    user.service_number,
                    user.telephone,
                    user.unit,
                ),
                tags=tags,
            )

    def search_users(self):
        """Search for users based on search entry."""
        search_text = self.search_entry.get().strip().lower()

        # If search field is empty, reload all users
        if not search_text:
            self.load_users()
            return

        # Clear existing data
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Get all users and filter
        users = get_all_users(self.db)
        for index, user in enumerate(users, start=1):
            if (
                search_text in user.name.lower()
                or search_text in user.service_number.lower()
                or search_text in user.telephone.lower()
                or search_text in user.role.lower()
            ):  # Search in role instead of unit

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        index,
                        user.name,
                        user.service_number,
                        user.telephone,
                        user.unit,
                    ),
                )

    def add_user(self):
        """Open a dialog to add a new user."""
        # Check if a dialog is already open
        if self.dialog_open:
            return

        self.dialog_open = True
        dialog = AddUserDialog(self.winfo_toplevel(), self)
        self.parent.wait_window(dialog)  # Wait for dialog to close
        self.dialog_open = False

    def open_fingerprint_enroll(self):
        selected_user_id = self.get_selected_user_id()
        if selected_user_id:
            FingerprintEnroll(self, selected_user_id)
        else:
            messagebox.showwarning(title="Warning", message="Select a user first!", icon="warning")

    def get_selected_user_id(self):
        """Return the actual database user.id for the selected row, or None."""
        selected_item = self.tree.selection()
        if not selected_item:
            return None
        try:
            display_values = self.tree.item(selected_item)["values"]
            display_index = int(display_values[0])  # 1-based index used in the table
            users = get_all_users(self.db)
            # Convert table index back to the user's primary key
            return users[display_index - 1].id if 0 < display_index <= len(users) else None
        except Exception:
            return None

    def edit_user(self):
        """Open a dialog to edit a selected user."""
        # Check if a dialog is already open
        if self.dialog_open:
            return

        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an officer to edit!")
            return

        user_data = self.tree.item(selected_item)["values"]
        self.dialog_open = True
        dialog = EditUserDialog(self.parent, self, user_data)  # Use parent window instead of self
        self.parent.wait_window(dialog)  # Wait for dialog to close
        self.dialog_open = False

    def delete_user(self):
        """Delete the selected user."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an officer to delete!")
            return

        # Get the actual user ID from the database (it's stored in the tree item values)
        display_values = self.tree.item(selected_item)["values"]
        # Find the corresponding user in the database
        users = get_all_users(self.db)
        user_id = users[display_values[0] - 1].id  # Convert display index back to user ID

        # Create a custom confirmation dialog
        confirm_dialog = CTkMessageBox(
            self.parent,
            title="Confirm Deletion",
            message=(
                "Are you sure you want to delete this officer? "
                "This will also delete all associated fingerprint records."
            ),
            icon="warning",
            option_1="Cancel",
            option_2="Delete",
        )

        if confirm_dialog.get() == "Delete":
            try:
                # First, delete associated fingerprints using text()
                self.db.execute(
                    text("DELETE FROM fingerprints WHERE user_id = :user_id"),
                    {"user_id": user_id},
                )

                # Then delete the user
                delete_user(self.db, user_id)

                # Commit any pending changes
                self.db.commit()

                self.load_users()  # This will refresh the list with new sequential numbers
                messagebox.showinfo(
                    "Success", "Officer and associated records deleted successfully!"
                )

            except Exception as e:
                # If anything goes wrong, rollback the transaction
                self.db.rollback()
                messagebox.showerror("Error", f"Failed to delete officer: {str(e)}")


class AddUserDialog(ctk.CTkToplevel):
    """Dialog for adding a new officer or armorer."""

    def __init__(self, master, controller, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.controller = controller
        self.title("Add Officer")
        self.geometry("400x450")
        self.resizable(False, False)
        self.transient(self.master)
        self.grab_set()

        # Store the controller reference to refresh data
        self.controller = controller

        # Update canvas background
        self.canvas = ctk.CTkCanvas(self, highlightthickness=0, bg="#2b2b2b")  # Dark background
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self._wheel_bind_id = self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.bind("<Destroy>", self._on_destroy)

        # Create main frame with proper background
        self.main_frame = ctk.CTkFrame(
            self.canvas, corner_radius=15, fg_color="#2b2b2b"  # Match canvas background
        )
        self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")

        # Bind the configure event to update the scroll region
        self.main_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Add New Officer",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.title_label.pack(pady=(20, 30))

        # Form fields
        self.create_form_field("Name:", "name_entry", "Enter full name")
        self.create_form_field("Service No:", "service_entry", "Enter service number")
        self.create_form_field("Telephone:", "phone_entry", "Enter telephone number")
        self.create_form_field("Unit:", "unit_entry", "Enter unit/department")

        # Role selection
        self.role_label = ctk.CTkLabel(self.main_frame, text="Role:", anchor="w")
        self.role_label.pack(padx=30, pady=(15, 5), anchor="w")

        self.role_var = ctk.StringVar(value="Role")
        self.role_combobox = ctk.CTkComboBox(
            self.main_frame,
            values=["officer", "armorer"],
            variable=self.role_var,
            width=340,
        )
        self.role_combobox.pack(padx=30, pady=(0, 15))

        # Password
        pwd_label = ctk.CTkLabel(self.main_frame, text="Password:", anchor="w")
        pwd_label.pack(padx=30, pady=(15, 5), anchor="w")

        self.password_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Enter password",
            show="*",
            height=35,
            width=340,
        )
        self.password_entry.pack(padx=30, pady=(0, 0))

        # Confirm Password
        confirm_label = ctk.CTkLabel(self.main_frame, text="Confirm Password:", anchor="w")
        confirm_label.pack(padx=30, pady=(15, 5), anchor="w")

        self.confirm_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Re-enter password",
            show="*",
            height=35,
            width=340,
        )
        self.confirm_entry.pack(padx=30, pady=(0, 0))

        # Buttons
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(fill=tk.X, padx=30, pady=(20, 0))

        self.cancel_button = ctk.CTkButton(
            self.button_frame,
            text="Cancel",
            fg_color="#F44336",
            hover_color="#D32F2F",
            command=self.destroy,
            width=150,
        )
        self.cancel_button.pack(side=tk.LEFT, padx=(0, 10))

        self.save_button = ctk.CTkButton(
            self.button_frame,
            text="Save",
            fg_color="#4CAF50",
            hover_color="#388E3C",
            command=self.save_user,
            width=150,
        )
        self.save_button.pack(side=tk.RIGHT)

        # Set focus to the first field
        self.after(100, lambda: self.name_entry.focus())

        # Make this window modal
        self.grab_set()
        self.transient(self.master)

        # Center the dialog
        self.center()

        # Add mousewheel binding
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)

        # Add cleanup binding
        self.bind("<Destroy>", self._on_destroy)

    def center(self):
        """Center the dialog on the parent window."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def create_form_field(self, label_text, entry_name, placeholder_text):
        """Helper method to create form fields."""
        label = ctk.CTkLabel(self.main_frame, text=label_text, anchor="w")
        label.pack(padx=30, pady=(15, 5), anchor="w")

        entry = ctk.CTkEntry(
            self.main_frame, placeholder_text=placeholder_text, height=35, width=340
        )
        entry.pack(padx=30, pady=(0, 0))

        # Save the entry widget as an instance attribute
        setattr(self, entry_name, entry)

    def save_user(self):
        """Save officer/armorer to the database."""
        name = self.name_entry.get()
        service_number = self.service_entry.get().strip()
        telephone = self.phone_entry.get().strip()
        unit = self.unit_entry.get().strip()
        role = (self.role_var.get() or "").strip().lower()
        password = self.password_entry.get()
        confirm = self.confirm_entry.get()

        if not name or not service_number or not telephone or not unit:
            CTkMessageBox(
                self,
                title="Warning",
                message="All fields are required!",
                icon="warning",
            )
            return

        if not password or len(password) < 6:
            messagebox.showerror("Error", "Password is required (min 6 chars).")
            return
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        db = SessionLocal()

        try:
            created = create_user(db, service_number, name, telephone, unit, role, password)
            # ^ make sure your CRUD signature supports role+password (see below)
            if created:
                self.destroy()
                CTkMessageBox(
                    self.master,
                    title="Success",
                    message="Officer added successfully!",
                    icon="check",
                )
                self.controller.load_users()
            else:
                CTkMessageBox(
                    self,
                    title="Error",
                    message="Failed to add officer. Please try again.",
                    icon="warning",
                )
        finally:
            db.close()

    def _on_mousewheel(self, event):
        """Handle mousewheel scrolling"""
        try:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except tk.TclError:
            pass  # Ignore errors if widget is destroyed

    def _on_destroy(self, event=None):
        canvas = getattr(self, "canvas", None)
        if not canvas:
            return
        try:
            exists = canvas.winfo_exists()
        except TclError:
            return

        if exists and getattr(self, "_wheel_bind_id", None):
            try:
                canvas.unbind("<MouseWheel>", self._wheel_bind_id)
            except TclError:
                pass
            self._wheel_bind_id = None


class EditUserDialog(ctk.CTkToplevel):
    """Dialog for editing an existing officer or armorer."""

    def __init__(self, parent, controller, user_data):
        super().__init__(parent)
        self.title("Edit Officer")
        self.geometry("400x450")
        self.resizable(False, False)

        # Store the controller reference to refresh data
        self.controller = controller
        # Get the actual user ID from database (not the display index)
        users = get_all_users(SessionLocal())
        self.user_id = users[user_data[0] - 1].id  # Convert display index back to user ID

        # Update canvas background
        self.canvas = ctk.CTkCanvas(self, highlightthickness=0, bg="#2b2b2b")  # Dark background
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add vertical scrollbar
        self.scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create main frame with proper background
        self.main_frame = ctk.CTkFrame(
            self.canvas, corner_radius=15, fg_color="#2b2b2b"  # Match canvas background
        )
        self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")

        # Bind the configure event to update scroll region
        self.main_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        # Bind mousewheel to canvas for scrolling
        self._wheel_bind_id = self.canvas.bind("<MouseWheel>", self._on_mousewheel)

        # Add cleanup binding
        self.bind("<Destroy>", self._on_destroy)

        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Edit Officer",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.title_label.pack(pady=(20, 30))

        # Form fields
        self.create_form_field("Name:", "name_entry", "Enter full name", user_data[1])
        self.create_form_field("Service No:", "service_entry", "Enter service number", user_data[2])
        self.create_form_field("Telephone:", "phone_entry", "Enter telephone number", user_data[3])
        self.create_form_field("Unit:", "unit_entry", "Enter unit/department", user_data[4])

        # Role selection
        self.role_label = ctk.CTkLabel(self.main_frame, text="Role:", anchor="w")
        self.role_label.pack(padx=30, pady=(15, 5), anchor="w")

        # Get the actual user from database to get the correct role
        users = get_all_users(SessionLocal())
        user_id = users[user_data[0] - 1].id  # Convert display index back to user ID
        actual_user = next((u for u in users if u.id == user_id), None)
        current_role = "armorer" if actual_user and actual_user.role == "armorer" else "officer"
        self.role_var = ctk.StringVar(value=current_role)
        self.role_combobox = ctk.CTkComboBox(
            self.main_frame,
            values=["officer", "armorer"],
            variable=self.role_var,
            width=340,
        )
        self.role_combobox.pack(padx=30, pady=(0, 15))

        # Buttons
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(fill=tk.X, padx=30, pady=(20, 0))

        self.cancel_button = ctk.CTkButton(
            self.button_frame,
            text="Cancel",
            fg_color="#F44336",
            hover_color="#D32F2F",
            command=self.destroy,
            width=150,
        )
        self.cancel_button.pack(side=tk.LEFT, padx=(0, 10))

        self.update_button = ctk.CTkButton(
            self.button_frame,
            text="Update",
            fg_color="#2196F3",
            hover_color="#1976D2",
            command=self.update_user,
            width=150,
        )
        self.update_button.pack(side=tk.RIGHT)

        # Make this window modal
        self.grab_set()
        self.transient(parent)

        # Center the dialog
        self.center()

    def center(self):
        """Center the dialog on the parent window."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def create_form_field(self, label_text, entry_name, placeholder_text, default_value=""):
        """Helper method to create form fields with default values."""
        label = ctk.CTkLabel(self.main_frame, text=label_text, anchor="w")
        label.pack(padx=30, pady=(15, 5), anchor="w")

        entry = ctk.CTkEntry(
            self.main_frame, placeholder_text=placeholder_text, height=35, width=340
        )
        entry.pack(padx=30, pady=(0, 0))

        # Set default value if provided
        if default_value:
            entry.insert(0, default_value)

        # Save the entry widget as an instance attribute
        setattr(self, entry_name, entry)

    def _on_mousewheel(self, event):
        """Handle mousewheel scrolling"""
        try:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except tk.TclError:
            pass  # Ignore errors if widget is destroyed

    def _on_destroy(self, event=None):
        """Defensive unbind to avoid 'bad window path name' if widget is already gone."""
        canvas = getattr(self, "canvas", None)
        if not canvas:
            return

        try:
            exists = canvas.winfo_exists()
        except TclError:
            return

        bid = getattr(self, "_wheel_bind_id", None)
        if exists and bid:
            try:
                canvas.unbind("<MouseWheel>", bid)
            except TclError:
                pass
            self._wheel_bind_id = None

    def update_user(self):
        """Update officer/armorer details in the database."""
        name = self.name_entry.get().strip()
        service_number = self.service_entry.get().strip()
        telephone = self.phone_entry.get().strip()
        unit = self.unit_entry.get().strip()
        role = (self.role_var.get() or "").strip().lower()  # ✅ fixed

        if not name or not service_number or not telephone or not unit:
            CTkMessageBox(
                self,
                title="Warning",
                message="All fields are required!",
                icon="warning",
            )
            return

        db = SessionLocal()
        try:
            updated = update_user(db, self.user_id, name, service_number, telephone, role, unit)
            if updated:
                self.destroy()
                CTkMessageBox(
                    self.master,
                    title="Success",
                    message="Officer updated successfully!",
                    icon="check",
                )
                self.controller.load_users()
            else:
                CTkMessageBox(
                    self,
                    title="Error",
                    message="Failed to update officer. Please try again.",
                    icon="warning",
                )
        finally:
            db.close()


class CTkMessageBox(ctk.CTkToplevel):
    """Custom message box implementation for CustomTkinter."""

    def __init__(
        self,
        parent,  # Add parent parameter
        title="Message",
        message="Message",
        icon="info",
        option_1="OK",
        option_2=None,
        option_3=None,
    ):
        super().__init__(parent)  # Pass parent to super

        self.title(title)
        self.geometry("400x200")
        self.resizable(False, False)

        self.result = None

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Message
        self.message_label = ctk.CTkLabel(self.main_frame, text=message, font=ctk.CTkFont(size=14))
        self.message_label.grid(row=0, column=0, padx=20, pady=(20, 30), sticky="nsew")

        # Buttons frame
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))

        # Configure button style based on icon
        if icon == "warning":
            button_1_color = "#F44336"
            button_1_hover = "#D32F2F"
        elif icon == "check":
            button_1_color = "#4CAF50"
            button_1_hover = "#388E3C"
        else:  # info
            button_1_color = "#2196F3"
            button_1_hover = "#1976D2"

        # Button 1 (always present)
        self.button_1 = ctk.CTkButton(
            self.button_frame,
            text=option_1,
            fg_color=button_1_color,
            hover_color=button_1_hover,
            command=lambda: self.set_result(option_1),
        )

        # If we have multiple buttons, set up a grid layout
        has_multiple_buttons = option_2 is not None

        if has_multiple_buttons:
            self.button_frame.columnconfigure((0, 1), weight=1)
            if option_3 is not None:
                self.button_frame.columnconfigure(2, weight=1)

            # Place button 1 in its grid position
            self.button_1.grid(row=0, column=0, padx=(0, 5), sticky="ew")

            # Button 2
            self.button_2 = ctk.CTkButton(
                self.button_frame,
                text=option_2,
                fg_color="#757575",  # Gray
                hover_color="#616161",
                command=lambda: self.set_result(option_2),
            )
            self.button_2.grid(row=0, column=1, padx=5, sticky="ew")

            # Button 3 (if provided)
            if option_3 is not None:
                self.button_3 = ctk.CTkButton(
                    self.button_frame,
                    text=option_3,
                    fg_color="#757575",  # Gray
                    hover_color="#616161",
                    command=lambda: self.set_result(option_3),
                )
                self.button_3.grid(row=0, column=2, padx=(5, 0), sticky="ew")
        else:
            # Single button, center it
            self.button_frame.columnconfigure(0, weight=1)
            self.button_1.grid(row=0, column=0, sticky="ew", pady=10)

        # Make the dialog modal
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", lambda: self.set_result(None))

        # Center the dialog on parent
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

        self.wait_window()

    def set_result(self, result):
        self.result = result
        self.destroy()

    def get(self):
        return self.result
