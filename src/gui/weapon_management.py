import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk
from src.database import SessionLocal
from src.crud.crud_weapon import (
    create_weapon, get_all_weapons, update_weapon, delete_weapon
)

class WeaponManagement(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=10)
        
        # Initialize dialog_open flag at the start
        self.dialog_open = False
        
        self.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create main content frame
        self.content_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        self.parent = parent
        self.db = SessionLocal()

        # Create a canvas with scrollbar
        self.canvas = ctk.CTkCanvas(
            self.content_frame,
            highlightthickness=0,
            bg='#2b2b2b'
        )
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add vertical scrollbar
        self.scrollbar = ctk.CTkScrollbar(
            self.content_frame,
            orientation="vertical",
            command=self.canvas.yview
        )
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        # Create main container
        self.main_container = ctk.CTkFrame(
            self.canvas,
            corner_radius=15,
            fg_color="#2b2b2b"
        )
        self.canvas_window = self.canvas.create_window((0, 0), window=self.main_container, anchor="nw")
        
        # Configure the canvas window
        self.main_container.bind("<Configure>", self.configure_canvas_window)

        # Header with title
        self.header_frame = ctk.CTkFrame(self.main_container, corner_radius=0, fg_color="transparent")
        self.header_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Weapon Management",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=10)

        # Search frame
        self.search_frame = ctk.CTkFrame(self.main_container, height=50, corner_radius=10)
        self.search_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Search by serial number..."
        )
        self.search_entry.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)
        
        self.search_button = ctk.CTkButton(
            self.search_frame,
            text="Search",
            width=100,
            command=self.search_weapons
        )
        self.search_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.refresh_button = ctk.CTkButton(
            self.search_frame,
            text="Refresh",
            width=100,
            fg_color="#4CAF50",
            hover_color="#388E3C",
            command=self.load_weapons
        )
        self.refresh_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Create tree frame
        self.tree_frame = ctk.CTkFrame(
            self.main_container,
            corner_radius=10,
            fg_color="#2b2b2b"
        )
        self.tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # Configure Treeview style
        style = ttk.Style()
        
        # Configure the main Treeview style
        style.configure(
            "Treeview",
            background="#2b2b2b",
            foreground="white",
            fieldbackground="#2b2b2b",
            rowheight=30,
            borderwidth=0,
            font=('TkDefaultFont', 10)
        )
        
        # Configure the Treeview headers with specific colors
        style.configure(
            "Treeview.Heading",
            background="#1f6aa5",
            foreground="#000000",  # Black text for better visibility
            relief="flat",
            font=('TkDefaultFont', 10, 'bold'),
            borderwidth=0
        )
        
        # Remove the borders
        style.layout("Treeview", [
            ('Treeview.treearea', {'sticky': 'nswe'})
        ])
        
        # Important: Add specific mapping for the header background and text color
        style.map(
            "Treeview.Heading",
            background=[('active', '#1f6aa5'), ('pressed', '#1f6aa5')],
            foreground=[('active', '#000000'), ('pressed', '#000000')],  # Keep text black in all states
            relief=[('pressed', 'flat'), ('!pressed', 'flat')]
        )
        
        # Configure selection colors
        style.map(
            "Treeview",
            background=[("selected", "#1f6aa5")],
            foreground=[("selected", "white")]
        )

        # Create Treeview
        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=("ID", "Type", "Serial No", "Status", "Condition", "Last Service"),
            show="headings",
            height=15
        )

        # Configure columns
        self.tree.heading("ID", text="ID", anchor="w")
        self.tree.heading("Type", text="Weapon Type", anchor="w")
        self.tree.heading("Serial No", text="Serial Number", anchor="w")
        self.tree.heading("Status", text="Status", anchor="w")
        self.tree.heading("Condition", text="Condition", anchor="w")
        self.tree.heading("Last Service", text="Last Service", anchor="w")

        # Set column widths
        self.tree.column("ID", width=50)
        self.tree.column("Type", width=150)
        self.tree.column("Serial No", width=150)
        self.tree.column("Status", width=100)
        self.tree.column("Condition", width=100)
        self.tree.column("Last Service", width=150)

        # Create scrollbars
        self.y_scrollbar = ctk.CTkScrollbar(
            self.tree_frame,
            orientation="vertical",
            command=self.tree.yview
        )
        self.x_scrollbar = ctk.CTkScrollbar(
            self.tree_frame,
            orientation="horizontal",
            command=self.tree.xview
        )
        
        self.tree.configure(
            yscrollcommand=self.y_scrollbar.set,
            xscrollcommand=self.x_scrollbar.set
        )

        # Pack scrollbars and tree
        self.y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Action buttons frame
        self.button_frame = ctk.CTkFrame(self.main_container, corner_radius=10, fg_color="transparent")
        self.button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Grid layout for buttons
        self.button_frame.columnconfigure((0, 1, 2), weight=1)
        
        # Action buttons
        self.add_button = ctk.CTkButton(
            self.button_frame,
            text="Add Weapon",
            fg_color="#4CAF50",
            hover_color="#388E3C",
            height=40,
            corner_radius=8,
            command=self.add_weapon
        )
        self.add_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        self.edit_button = ctk.CTkButton(
            self.button_frame,
            text="Edit Weapon",
            fg_color="#2196F3",
            hover_color="#1976D2",
            height=40,
            corner_radius=8,
            command=self.edit_weapon
        )
        self.edit_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        self.delete_button = ctk.CTkButton(
            self.button_frame,
            text="Delete Weapon",
            fg_color="#F44336",
            hover_color="#D32F2F",
            height=40,
            corner_radius=8,
            command=self.delete_weapon
        )
        self.delete_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        # Bind events
        self.tree.bind("<Double-1>", lambda event: self.edit_weapon())
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.bind("<Destroy>", self._on_destroy)

        # Load initial data
        self.load_weapons()

    def load_weapons(self):
        """Load weapons into the treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get weapons from database
        weapons = get_all_weapons(self.db)
        
        # Insert weapons into treeview
        for idx, weapon in enumerate(weapons, start=1):
            values = (
                idx,
                weapon.type,
                weapon.serial_number,
                weapon.status,
                weapon.condition,
                weapon.last_service.strftime("%Y-%m-%d") if weapon.last_service else "N/A"
            )
            tags = ('oddrow',) if idx % 2 else ()
            self.tree.insert("", "end", values=values, tags=tags)

        # Configure row colors
        self.tree.tag_configure('oddrow', background='#333333')

    def search_weapons(self):
        """Search weapons by serial number"""
        search_term = self.search_entry.get().strip().lower()
        
        # Clear current display
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # If search term is empty, reload all weapons
        if not search_term:
            self.load_weapons()
            return
        
        # Get all weapons and filter
        weapons = get_all_weapons(self.db)
        filtered_weapons = [
            w for w in weapons 
            if search_term in w.serial_number.lower()
        ]
        
        # Display filtered results
        for idx, weapon in enumerate(filtered_weapons, start=1):
            values = (
                idx,
                weapon.type,
                weapon.serial_number,
                weapon.status,
                weapon.condition,
                weapon.last_service.strftime("%Y-%m-%d") if weapon.last_service else "N/A"
            )
            tags = ('oddrow',) if idx % 2 else ()
            self.tree.insert("", "end", values=values, tags=tags)

    def add_weapon(self):
        """Open dialog to add a new weapon"""
        if self.dialog_open:
            return
            
        self.dialog_open = True
        dialog = AddWeaponDialog(self.parent, self)
        self.wait_window(dialog)
        self.dialog_open = False

    def edit_weapon(self):
        """Open dialog to edit selected weapon"""
        if self.dialog_open:
            return
            
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a weapon to edit!")
            return
            
        weapon_data = self.tree.item(selected_item)["values"]
        self.dialog_open = True
        dialog = EditWeaponDialog(self.parent, self, weapon_data)
        self.wait_window(dialog)
        self.dialog_open = False

    def delete_weapon(self):
        """Delete selected weapon"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a weapon to delete!")
            return
        
        # Get the weapon data
        display_values = self.tree.item(selected_item)["values"]
        weapons = get_all_weapons(self.db)
        weapon_id = weapons[display_values[0] - 1].id
        
        # Show confirmation dialog
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            "Are you sure you want to delete this weapon?"
        )
        
        if confirm:
            try:
                delete_weapon(self.db, weapon_id)
                self.load_weapons()
                messagebox.showinfo("Success", "Weapon deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete weapon: {str(e)}")

    def configure_canvas_window(self, event):
        """Configure the canvas window to adjust to the size of the content"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.itemconfig(self.canvas_window, width=self.canvas.winfo_width())

    def _on_mousewheel(self, event):
        """Handle mousewheel scrolling"""
        try:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except tk.TclError:
            pass

    def _on_destroy(self, event):
        """Clean up bindings when widget is destroyed"""
        if event.widget == self:
            try:
                self.canvas.unbind("<MouseWheel>")
                self.canvas.unbind_all("<MouseWheel>")
            except tk.TclError:
                # Canvas already destroyed, ignore the error
                pass

class AddWeaponDialog(ctk.CTkToplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.title("Add Weapon")
        self.geometry("400x500")
        self.resizable(False, False)
        
        # Store controller reference
        self.controller = controller
        
        # Create canvas with scrollbar
        self.canvas = ctk.CTkCanvas(
            self,
            highlightthickness=0,
            bg='#2b2b2b'
        )
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.scrollbar = ctk.CTkScrollbar(
            self,
            orientation="vertical",
            command=self.canvas.yview
        )
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(
            self.canvas,
            corner_radius=15,
            fg_color="#2b2b2b"
        )
        self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")
        
        # Bind configure event
        self.main_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Add New Weapon",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack(pady=(20, 30))

        # Form fields
        self.create_form_field("Weapon Type:", "type_entry", "Enter weapon type")
        self.create_form_field("Serial Number:", "serial_entry", "Enter serial number")
        
        # Status selection
        self.status_label = ctk.CTkLabel(self.main_frame, text="Status:", anchor="w")
        self.status_label.pack(padx=30, pady=(15, 5), anchor="w")
        
        self.status_var = ctk.StringVar(value="Available")
        self.status_combobox = ctk.CTkComboBox(
            self.main_frame,
            values=["Available", "Booked Out", "Maintenance"],
            variable=self.status_var,
            width=340
        )
        self.status_combobox.pack(padx=30, pady=(0, 15))
        
        # Condition selection
        self.condition_label = ctk.CTkLabel(self.main_frame, text="Condition:", anchor="w")
        self.condition_label.pack(padx=30, pady=(15, 5), anchor="w")
        
        self.condition_var = ctk.StringVar(value="Good")
        self.condition_combobox = ctk.CTkComboBox(
            self.main_frame,
            values=["Excellent", "Good", "Fair", "Poor"],
            variable=self.condition_var,
            width=340
        )
        self.condition_combobox.pack(padx=30, pady=(0, 15))
        
        # Buttons
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(fill=tk.X, padx=30, pady=(20, 20))
        
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
            command=self.save_weapon,
            width=150
        )
        self.save_button.pack(side=tk.RIGHT)
        
        # Make dialog modal
        self.grab_set()
        self.transient(parent)
        
        # Center dialog
        self.center()
        
        # Add mousewheel binding
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.bind("<Destroy>", self._on_destroy)

    def center(self):
        """Center the dialog on the parent window"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def create_form_field(self, label_text, entry_name, placeholder_text):
        """Helper method to create form fields"""
        label = ctk.CTkLabel(self.main_frame, text=label_text, anchor="w")
        label.pack(padx=30, pady=(15, 5), anchor="w")
        
        entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text=placeholder_text,
            height=35,
            width=340
        )
        entry.pack(padx=30, pady=(0, 0))
        
        setattr(self, entry_name, entry)

    def save_weapon(self):
        """Save weapon to database"""
        weapon_type = self.type_entry.get()
        serial_number = self.serial_entry.get()
        status = self.status_var.get()
        condition = self.condition_var.get()

        if not all([weapon_type, serial_number]):
            messagebox.showwarning("Warning", "All fields are required!")
            return

        try:
            create_weapon(
                self.controller.db,
                weapon_type,
                serial_number,
                status,
                condition
            )
            self.destroy()
            messagebox.showinfo("Success", "Weapon added successfully!")
            self.controller.load_weapons()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add weapon: {str(e)}")

    def _on_mousewheel(self, event):
        """Handle mousewheel scrolling"""
        try:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except tk.TclError:
            pass

    def _on_destroy(self, event):
        """Clean up bindings when widget is destroyed"""
        if event.widget == self:
            try:
                self.canvas.unbind("<MouseWheel>")
                self.canvas.unbind_all("<MouseWheel>")
            except tk.TclError:
                # Canvas already destroyed, ignore the error
                pass

class EditWeaponDialog(AddWeaponDialog):
    def __init__(self, parent, controller, weapon_data):
        super().__init__(parent, controller)
        
        self.title("Edit Weapon")
        self.weapon_data = weapon_data
        
        # Update title
        self.title_label.configure(text="Edit Weapon")
        
        # Populate fields with existing data
        self.populate_fields()
        
    def populate_fields(self):
        """Fill form fields with existing weapon data"""
        self.type_entry.insert(0, self.weapon_data[1])
        self.serial_entry.insert(0, self.weapon_data[2])
        self.status_var.set(self.weapon_data[3])
        self.condition_var.set(self.weapon_data[4])
        
    def save_weapon(self):
        """Update weapon in database"""
        weapon_type = self.type_entry.get()
        serial_number = self.serial_entry.get()
        status = self.status_var.get()
        condition = self.condition_var.get()

        if not all([weapon_type, serial_number]):
            messagebox.showwarning("Warning", "All fields are required!")
            return

        try:
            # Get the actual weapon ID from the database
            weapons = get_all_weapons(self.controller.db)
            weapon_id = weapons[self.weapon_data[0] - 1].id
            
            update_weapon(
                self.controller.db,
                weapon_id,
                weapon_type,
                serial_number,
                status,
                condition
            )
            self.destroy()
            messagebox.showinfo("Success", "Weapon updated successfully!")
            self.controller.load_weapons()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update weapon: {str(e)}") 