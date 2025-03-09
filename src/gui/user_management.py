import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
from src.database import SessionLocal
from src.crud.crud_user import create_user, get_all_users, update_user, delete_user

# Set appearance mode and default color theme
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class UserManagement(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=10)
        self.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.parent = parent  # Store the parent reference for modal dialogs
        self.db = SessionLocal()  # Database session

        # Create a canvas with scrollbar for the main content
        self.canvas = ctk.CTkCanvas(self, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add vertical scrollbar to canvas
        self.scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure the canvas to use the scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        # Create a main container inside the canvas
        self.main_container = ctk.CTkFrame(self.canvas, corner_radius=15, fg_color="transparent")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.main_container, anchor="nw")
        
        # Configure the canvas window to expand with the main container
        self.main_container.bind("<Configure>", self.configure_canvas_window)

        # Header with title
        self.header_frame = ctk.CTkFrame(self.main_container, corner_radius=0, fg_color="transparent")
        self.header_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="Officer & Armorer Management",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=10)

        # Search and filter frame
        self.search_frame = ctk.CTkFrame(self.main_container, height=50, corner_radius=10)
        self.search_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Search by name or service number...")
        self.search_entry.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)
        
        self.search_button = ctk.CTkButton(
            self.search_frame, 
            text="Search",
            width=100,
            command=self.search_users
        )
        self.search_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.refresh_button = ctk.CTkButton(
            self.search_frame, 
            text="Refresh",
            width=100,
            fg_color="#4CAF50",
            hover_color="#388E3C",
            command=self.load_users
        )
        self.refresh_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Create a frame for the treeview and scrollbar
        self.tree_frame = ctk.CTkFrame(self.main_container, corner_radius=10)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # Since CustomTkinter doesn't have its own Treeview, we use the standard ttk Treeview
        # But we can style it to fit better with our custom theme
        self.style = tk.ttk.Style()
        self.style.configure("Treeview", background="#2a2d2e", foreground="white", fieldbackground="#2a2d2e", rowheight=30)
        self.style.configure("Treeview.Heading", background="#1f6aa5", foreground="white", relief="flat")
        self.style.map("Treeview", background=[("selected", "#1f6aa5")])
        
        # Create scrollbars
        self.tree_scroll_y = ctk.CTkScrollbar(self.tree_frame, orientation="vertical")
        self.tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree_scroll_x = ctk.CTkScrollbar(self.tree_frame, orientation="horizontal")
        self.tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Create Treeview with scrollbars
        self.tree = tk.ttk.Treeview(
            self.tree_frame, 
            columns=("ID", "Name", "Service No", "Telephone", "Unit"), 
            show="headings",
            yscrollcommand=self.tree_scroll_y.set,
            xscrollcommand=self.tree_scroll_x.set
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
        
        # Load initial data
        self.load_users()

        # Action buttons frame
        self.button_frame = ctk.CTkFrame(self.main_container, corner_radius=10, fg_color="transparent")
        self.button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Grid layout for buttons
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.columnconfigure(2, weight=1)
        
        # Modern buttons with icons
        self.add_button = ctk.CTkButton(
            self.button_frame, 
            text="Add Officer",
            fg_color="#4CAF50",  # Green
            hover_color="#388E3C",
            height=40,
            corner_radius=8,
            command=self.add_user
        )
        self.add_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        self.edit_button = ctk.CTkButton(
            self.button_frame, 
            text="Edit Officer",
            fg_color="#2196F3",  # Blue
            hover_color="#1976D2",
            height=40,
            corner_radius=8,
            command=self.edit_user
        )
        self.edit_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        self.delete_button = ctk.CTkButton(
            self.button_frame, 
            text="Delete Officer",
            fg_color="#F44336",  # Red
            hover_color="#D32F2F",
            height=40,
            corner_radius=8,
            command=self.delete_user
        )
        self.delete_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        # Add event binding for double-click edit
        self.tree.bind("<Double-1>", lambda event: self.edit_user())
        
        # Bind mousewheel to canvas for scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
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
        # Scroll up or down based on the mouse wheel direction
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def load_users(self):
        """Load users into the table."""
        # Clear existing data
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Get all users from database
        users = get_all_users(self.db)
        
        # Insert users into treeview
        for user in users:
            role_display = "Armorer" if user.role == "Armory Manager" else "Unit"
            self.tree.insert("", "end", values=(user.id, user.name, user.service_number, user.telephone, role_display))

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
        for user in users:
            if (search_text in user.name.lower() or 
                search_text in user.service_number.lower() or
                search_text in user.telephone.lower()):
                
                role_display = "Armorer" if user.role == "Armory Manager" else "Unit"
                self.tree.insert("", "end", values=(user.id, user.name, user.service_number, user.telephone, role_display))

    def add_user(self):
        """Open a dialog to add a new user."""
        # Check if a dialog is already open
        if self.dialog_open:
            return
            
        self.dialog_open = True
        dialog = AddUserDialog(self.parent, self)  # Use parent window instead of self
        self.parent.wait_window(dialog)  # Wait for dialog to close
        self.dialog_open = False

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
        
        user_id = self.tree.item(selected_item)["values"][0]
        
        # Create a custom confirmation dialog
        confirm_dialog = CTkMessageBox(
            self.parent,  # Use parent window
            title="Confirm Deletion",
            message="Are you sure you want to delete this officer?",
            icon="warning",
            option_1="Cancel",
            option_2="Delete"
        )
        
        if confirm_dialog.get() == "Delete":
            delete_user(self.db, user_id)
            self.load_users()
            messagebox.showinfo("Success", "Officer deleted successfully!")


class AddUserDialog(ctk.CTkToplevel):
    """Dialog for adding a new officer or armorer."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.title("Add Officer")
        self.geometry("400x450")
        self.resizable(False, False)
        
        # Store the controller reference to refresh data
        self.controller = controller
        
        # Create a canvas with scrollbar
        self.canvas = ctk.CTkCanvas(self, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Create a main frame inside the canvas
        self.main_frame = ctk.CTkFrame(self.canvas, corner_radius=15)
        self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")
        
        # Bind the configure event to update the scroll region
        self.main_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="Add New Officer",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack(pady=(20, 30))

        # Form fields
        self.create_form_field("Name:", "name_entry", "Enter full name")
        self.create_form_field("Service No:", "service_entry", "Enter service number")
        self.create_form_field("Telephone:", "phone_entry", "Enter telephone number")
        
        # Role selection
        self.role_label = ctk.CTkLabel(self.main_frame, text="Role:", anchor="w")
        self.role_label.pack(padx=30, pady=(15, 5), anchor="w")
        
        self.role_var = ctk.StringVar(value="Unit")
        self.role_combobox = ctk.CTkComboBox(
            self.main_frame,
            values=["Unit", "Armory Manager"],
            variable=self.role_var,
            width=340
        )
        self.role_combobox.pack(padx=30, pady=(0, 15))
        
        # Unit field
        self.create_form_field("Unit:", "unit_entry", "Enter unit/department")
        
        # Buttons
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(fill=tk.X, padx=30, pady=(20, 0))
        
        self.cancel_button = ctk.CTkButton(
            self.button_frame,
            text="Cancel",
            fg_color="#F44336",
            hover_color="#D32F2F",
            command=self.destroy,
            width=150
        )
        self.cancel_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.save_button = ctk.CTkButton(
            self.button_frame,
            text="Save",
            fg_color="#4CAF50",
            hover_color="#388E3C",
            command=self.save_user,
            width=150
        )
        self.save_button.pack(side=tk.RIGHT)
        
        # Set focus to the first field
        self.after(100, lambda: self.name_entry.focus())
        
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

    def create_form_field(self, label_text, entry_name, placeholder_text):
        """Helper method to create form fields."""
        label = ctk.CTkLabel(self.main_frame, text=label_text, anchor="w")
        label.pack(padx=30, pady=(15, 5), anchor="w")
        
        entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text=placeholder_text,
            height=35,
            width=340
        )
        entry.pack(padx=30, pady=(0, 0))
        
        # Save the entry widget as an instance attribute
        setattr(self, entry_name, entry)

    def save_user(self):
        """Save officer/armorer to the database."""
        name = self.name_entry.get()
        service_number = self.service_entry.get()
        telephone = self.phone_entry.get()
        unit = self.unit_entry.get()
        role = self.role_var.get()

        if not name or not service_number or not telephone or not unit:
            CTkMessageBox(
                self,
                title="Warning", 
                message="All fields are required!",
                icon="warning"
            )
            return

        db = SessionLocal()
        # Create the user in the database - removed role parameter to match function signature
        created = create_user(db, service_number, name, telephone, unit)
        db.close()
        
        if created:
            # Destroy this dialog
            self.destroy()
            
            # Show success message
            CTkMessageBox(
                self.master,  # Use the parent as parent for message box
                title="Success", 
                message="Officer/Armorer added successfully!",
                icon="check"
            )
            
            # Refresh the user list
            self.controller.load_users()
        else:
            # Show error message
            CTkMessageBox(
                self,
                title="Error", 
                message="Failed to add officer/armorer. Please try again.",
                icon="warning"
            )

class EditUserDialog(ctk.CTkToplevel):
    """Dialog for editing an existing officer or armorer."""
    def __init__(self, parent, controller, user_data):
        super().__init__(parent)
        self.title("Edit Officer/Armorer")
        self.geometry("400x450")
        self.resizable(False, False)
        
        # Store the controller reference to refresh data
        self.controller = controller
        self.user_id = user_data[0]
        
        # Create a canvas with scrollbar
        self.canvas = ctk.CTkCanvas(self, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add vertical scrollbar
        self.scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Create main frame inside canvas
        self.main_frame = ctk.CTkFrame(self.canvas, corner_radius=15)
        self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")
        
        # Bind the configure event to update scroll region
        self.main_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        # Bind mousewheel to canvas for scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="Edit Officer/Armorer",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack(pady=(20, 30))

        # Form fields
        self.create_form_field("Name:", "name_entry", "Enter full name", user_data[1])
        self.create_form_field("Service No:", "service_entry", "Enter service number", user_data[2])
        self.create_form_field("Telephone:", "phone_entry", "Enter telephone number", user_data[3])
        
        # Role selection
        self.role_label = ctk.CTkLabel(self.main_frame, text="Role:", anchor="w")
        self.role_label.pack(padx=30, pady=(15, 5), anchor="w")
        
        current_role = "Armory Manager" if user_data[4] == "Armorer" else "Unit"
        self.role_var = ctk.StringVar(value=current_role)
        self.role_combobox = ctk.CTkComboBox(
            self.main_frame,
            values=["Unit", "Armory Manager"],
            variable=self.role_var,
            width=340
        )
        self.role_combobox.pack(padx=30, pady=(0, 15))
        
        # Unit field (might be role depending on your structure)
        self.create_form_field("Unit:", "unit_entry", "Enter unit/department", user_data[4])
        
        # Buttons
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(fill=tk.X, padx=30, pady=(20, 0))
        
        self.cancel_button = ctk.CTkButton(
            self.button_frame,
            text="Cancel",
            fg_color="#F44336",
            hover_color="#D32F2F",
            command=self.destroy,
            width=150
        )
        self.cancel_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.update_button = ctk.CTkButton(
            self.button_frame,
            text="Update",
            fg_color="#2196F3",
            hover_color="#1976D2",
            command=self.update_user,
            width=150
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
            self.main_frame,
            placeholder_text=placeholder_text,
            height=35,
            width=340
        )
        entry.pack(padx=30, pady=(0, 0))
        
        # Set default value if provided
        if default_value:
            entry.insert(0, default_value)
        
        # Save the entry widget as an instance attribute
        setattr(self, entry_name, entry)

    def _on_mousewheel(self, event):
        """Handle mousewheel scrolling"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def update_user(self):
        """Update officer/armorer details in the database."""
        name = self.name_entry.get()
        service_number = self.service_entry.get()
        telephone = self.phone_entry.get()
        unit = self.unit_entry.get()
        
        if not name or not service_number or not telephone or not unit:
            CTkMessageBox(
                self,
                title="Warning",
                message="All fields are required!",
                icon="warning"
            )
            return

        db = SessionLocal()
        # Update the user in the database with only the supported parameters
        updated = update_user(db, self.user_id, name, service_number, telephone)
        db.close()
        
        if updated:
            # Destroy this dialog
            self.destroy()
            
            # Show success message
            CTkMessageBox(
                self.master,
                title="Success", 
                message="Officer/Armorer updated successfully!",
                icon="check"
            )
            
            # Refresh the user list
            self.controller.load_users()
        else:
            # Show error message
            CTkMessageBox(
                self,
                title="Error", 
                message="Failed to update officer/armorer. Please try again.",
                icon="warning"
            )


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
        option_3=None
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
        self.message_label = ctk.CTkLabel(
            self.main_frame,
            text=message,
            font=ctk.CTkFont(size=14)
        )
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
            command=lambda: self.set_result(option_1)
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
                command=lambda: self.set_result(option_2)
            )
            self.button_2.grid(row=0, column=1, padx=5, sticky="ew")
            
            # Button 3 (if provided)
            if option_3 is not None:
                self.button_3 = ctk.CTkButton(
                    self.button_frame,
                    text=option_3,
                    fg_color="#757575",  # Gray
                    hover_color="#616161",
                    command=lambda: self.set_result(option_3)
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