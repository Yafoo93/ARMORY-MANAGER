from tkinter import messagebox

import customtkinter as ctk

from src.database import SessionLocal
from src.gui.fingerprint_verify import FingerprintVerify
from src.models.user import User
from src.services.auth_service import AuthService

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

        # ✅ Inline error label (hidden by default)
        self.error_label = ctk.CTkLabel(
            self.login_frame,
            text="",
            text_color="#ff4d4f",
            font=ctk.CTkFont(size=12, weight="normal"),
        )
        self.error_label.pack(pady=(4, 0))

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
            self.login_frame,
            text="🔒 Secure Access | v1.0",
            font=ctk.CTkFont(size=12),
            text_color="gray",
        )
        self.footer_label.pack(pady=(10, 20))

    def login(self):
        service_number = self.username_entry.get().strip()
        password = self.password_entry.get()

        # clear inline error
        self.error_label.configure(text="")

        if not service_number or not password:
            self.error_label.configure(text="Both fields are required!")
            return

        # ✅ Database Authentication
        session = SessionLocal()
        try:
            user = session.query(User).filter_by(service_number=service_number).first()
        finally:
            session.close()

        if not user:
            self.error_label.configure(text="Invalid credentials")
            return

        # Ensure your User model exposes verify_password() or change this to user.check_password()
        if not user.verify_password(password):
            self.error_label.configure(text="Invalid credentials")
            return

        # ✅ Role-Based Access Control
        role = (user.role or "").strip().lower()
        allowed = "armorer"
        if role != allowed:
            self.error_label.configure(text="Only Armorers can log in.")
            return

        # Route directly to dashboard without success popup
        self._launch_main(user)

    def open_fingerprint_login(self):
        db = SessionLocal()
        auth = AuthService(db)

        def on_success(user_id):
            user = auth.get_user_by_id(user_id)
            if user:
                self.login_success(user)
            else:
                messagebox.showwarning(title="Error", message="User not found", icon="cancel")

        FingerprintVerify(self, callback_on_success=on_success)

    def _launch_main(self, user):
        # Import here to avoid circular import at module import time
        from src.main import ArmoryApp

        try:
            # Hide login window to avoid pending after-callback issues, destroy later
            try:
                self.withdraw()
            except Exception:
                pass
            app = ArmoryApp(user)
            app.mainloop()
        except Exception as e:
            import traceback

            print("[Login->Main] Failed to launch main app:")
            traceback.print_exc()
            messagebox.showerror("Launch Error", str(e))
        finally:
            try:
                self.destroy()
            except Exception:
                pass


# ✅ Run Login UI
if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
