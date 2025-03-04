import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk
from src.database import SessionLocal
from src.crud.crud_user import create_user, get_all_users, update_user, delete_user

class UserManagement(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        self.pack(fill=tk.BOTH, expand=True)

        self.db = SessionLocal()  # Database session

        ttk.Label(self, text="User Management", font="Arial 16 bold").pack(pady=10)

        # Table for displaying users
        self.tree = ttk.Treeview(self, columns=("ID", "Name", "Service No", "Telephone", "Role"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Service No", text="Service No")
        self.tree.heading("Telephone", text="Telephone")
        self.tree.heading("Role", text="Role")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Name", width=150)
        self.tree.column("Service No", width=100, anchor="center")
        self.tree.column("Telephone", width=120, anchor="center")
        self.tree.column("Role", width=100, anchor="center")

        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)
        self.load_users()

        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Add User", bootstyle="success", command=self.add_user).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Edit User", bootstyle="info", command=self.edit_user).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Delete User", bootstyle="danger", command=self.delete_user).grid(row=0, column=2, padx=5)

    def load_users(self):
        """Load users into the table."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        users = get_all_users(self.db)
        for user in users:
            self.tree.insert("", "end", values=(user.id, user.name, user.service_number, user.telephone, user.role))

    def add_user(self):
        """Open a dialog to add a new user."""
        AddUserDialog(self)

    def edit_user(self):
        """Open a dialog to edit a selected user."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a user to edit!")
            return
        user_data = self.tree.item(selected_item)["values"]
        EditUserDialog(self, user_data)

    def delete_user(self):
        """Delete the selected user."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a user to delete!")
            return
        
        user_id = self.tree.item(selected_item)["values"][0]
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this user?")
        if confirm:
            delete_user(self.db, user_id)
            self.load_users()
            messagebox.showinfo("Success", "User deleted successfully!")

class AddUserDialog(tk.Toplevel):
    """Dialog for adding a new user."""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add User")
        self.geometry("300x250")

        ttk.Label(self, text="Name:").pack(pady=5)
        self.name_entry = ttk.Entry(self)
        self.name_entry.pack()

        ttk.Label(self, text="Service No:").pack(pady=5)
        self.service_entry = ttk.Entry(self)
        self.service_entry.pack()

        ttk.Label(self, text="Telephone:").pack(pady=5)
        self.phone_entry = ttk.Entry(self)
        self.phone_entry.pack()

        ttk.Label(self, text="Role:").pack(pady=5)
        self.role_entry = ttk.Entry(self)
        self.role_entry.pack()

        ttk.Button(self, text="Save", bootstyle="success", command=self.save_user).pack(pady=10)

    def save_user(self):
        """Save user to database."""
        name = self.name_entry.get()
        service_number = self.service_entry.get()
        telephone = self.phone_entry.get()
        role = self.role_entry.get()

        if not name or not service_number or not telephone or not role:
            messagebox.showwarning("Warning", "All fields are required!")
            return

        db = SessionLocal()
        create_user(db, service_number, name, telephone, role)
        db.close()
        self.destroy()
        messagebox.showinfo("Success", "User added successfully!")

class EditUserDialog(tk.Toplevel):
    """Dialog for editing an existing user."""
    def __init__(self, parent, user_data):
        super().__init__(parent)
        self.title("Edit User")
        self.geometry("300x250")

        self.user_id = user_data[0]

        ttk.Label(self, text="Name:").pack(pady=5)
        self.name_entry = ttk.Entry(self)
        self.name_entry.insert(0, user_data[1])
        self.name_entry.pack()

        ttk.Label(self, text="Service No:").pack(pady=5)
        self.service_entry = ttk.Entry(self)
        self.service_entry.insert(0, user_data[2])
        self.service_entry.pack()

        ttk.Label(self, text="Telephone:").pack(pady=5)
        self.phone_entry = ttk.Entry(self)
        self.phone_entry.insert(0, user_data[3])
        self.phone_entry.pack()

        ttk.Label(self, text="Role:").pack(pady=5)
        self.role_entry = ttk.Entry(self)
        self.role_entry.insert(0, user_data[4])
        self.role_entry.pack()

        ttk.Button(self, text="Update", bootstyle="info", command=self.update_user).pack(pady=10)

    def update_user(self):
        """Update user details in the database."""
        name = self.name_entry.get()
        service_number = self.service_entry.get()
        telephone = self.phone_entry.get()
        role = self.role_entry.get()

        if not name or not service_number or not telephone or not role:
            messagebox.showwarning("Warning", "All fields are required!")
            return

        db = SessionLocal()
        update_user(db, self.user_id, name, service_number, telephone, role)
        db.close()
        self.destroy()
        messagebox.showinfo("Success", "User updated successfully!")
