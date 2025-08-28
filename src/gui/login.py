import customtkinter as ctk
from tkinter import messagebox
from src.database import SessionLocal
from src.models.user import User
from src.main import run_main_app

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")  # Can be "dark-blue" or "green"


class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🔐 Armory Manager - Login")
        self.geometry("400x500")
        self.resizable(False, False)

        # ✅ Frame to hold login form
        self.login_frame = ctk.CTkFrame(self, corner_radius=12)
        self.login_frame.pack(pady=40, padx=30, fill="both", expand=True)

        # ✅ Title
        self.title_label = ctk.CTkLabel(
            self.login_frame, text="🔐 Armory Login", font=ctk.CTkFont(size=22, weight="bold")
        )
        self.title_label.pack(pady=(20, 10))

        # ✅ Username Entry
        self.username_entry = ctk.CTkEntry(
            self.login_frame, placeholder_text="Service Number", width=250, height=40
        )
        self.username_entry.pack(pady=10)

        # ✅ Password Entry
        self.password_entry = ctk.CTkEntry(
            self.login_frame, placeholder_text="Password", show="*", width=250, height=40
        )
        self.password_entry.pack(pady=10)

        # ✅ Login Button
        self.login_button = ctk.CTkButton(
            self.login_frame,
            text="Login",
            fg_color="#2fa572",  # Green button
            hover_color="#258d5a",
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.login,
        )
        self.login_button.pack(pady=20)

        # ✅ Footer Message
        self.footer_label = ctk.CTkLabel(
            self.login_frame, text="🔒 Secure Access | v1.0", font=ctk.CTkFont(size=12), text_color="gray"
        )
        self.footer_label.pack(pady=(10, 20))

    def login(self):
        service_number = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not service_number or not password:
            messagebox.showerror("Error", "Both fields are required!")
            return

        # ✅ Database Authentication
        session = SessionLocal()
        user = session.query(User).filter_by(service_number=service_number).first()
        session.close()
        
        if not user:
            messagebox.showerror("Error", "Invalid credentials")
            return
        
        if not user.verify_password(password):
            messagebox.showerror("Error", "Invalid credentials")
            return
        
         # ✅ Role-Based Access Control
        role = (user.role or "").strip().lower()
        allowed = "armorer"
        if role != allowed:
            messagebox.showerror("ERROR!!, Access Denied", "Only Armorers can log in.")
            return
        
        messagebox.showinfo("Success", f"Welcome, {user.name}!")
        self.withdraw()
        # Launch main app on next loop tick
        self.after(50, lambda: run_main_app(user))


# ✅ Run Login UI
if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
