import threading

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from src.crud import crud_fingerprint
from src.database import SessionLocal
from src.services.fingerprint_service import (
    FingerprintCaptureError,
    capture_fingerprint,
)


class FingerprintEnroll(ctk.CTkToplevel):
    def __init__(self, master, user_id):
        super().__init__(master)
        self.db = SessionLocal()
        self.user_id = user_id
        self.title("Enroll Fingerprint")
        self.geometry("450x300")
        self.resizable(False, False)
        self.grab_set()

        # Title
        ctk.CTkLabel(
            self, text="Fingerprint Enrollment", font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(20, 10))

        # Instructions
        instruction_text = (
            "Click 'Scan Fingerprint' and place your finger\n"
            "on the fingerprint reader when prompted."
        )
        ctk.CTkLabel(
            self, text=instruction_text, font=ctk.CTkFont(size=12), text_color="gray"
        ).pack(pady=10)

        # Capture button
        self.capture_btn = ctk.CTkButton(
            self,
            text="Scan Fingerprint",
            command=self.scan_fingerprint,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14),
        )
        self.capture_btn.pack(pady=20)

        # Status label
        self.status_label = ctk.CTkLabel(
            self, text="Ready to scan...", text_color="gray", font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(pady=10)

        # Progress indicator (initially hidden)
        self.progress_label = ctk.CTkLabel(
            self, text="", text_color="blue", font=ctk.CTkFont(size=11)
        )

    def _safe_messagebox(self, **kwargs):
        """Show CTkMessagebox safely when a parent Toplevel has a grab set.

        Releases the grab, shows the messagebox (modal), then re-grabs the parent.
        """
        try:
            try:
                self.grab_release()
            except Exception:
                pass
            box = CTkMessagebox(**kwargs)
            # Force wait for user action to ensure modality completes
            try:
                box._window.wait_window()  # type: ignore[attr-defined]
            except Exception:
                pass
            return box
        finally:
            try:
                self.grab_set()
            except Exception:
                pass

    def scan_fingerprint(self):
        """Scan fingerprint in a separate thread to avoid blocking UI."""
        self.capture_btn.configure(state="disabled", text="Scanning...")
        self.status_label.configure(text="Place your finger on the reader...", text_color="blue")
        self.progress_label.pack(pady=5)
        self.progress_label.configure(text="Waiting for fingerprint...")

        # Run capture in background thread
        thread = threading.Thread(target=self._capture_in_thread, daemon=True)
        thread.start()

    def _capture_in_thread(self):
        """Perform fingerprint capture in background thread."""
        try:
            # This will attempt to use Windows Biometric Framework or available hardware
            template_data = capture_fingerprint()

            # Update UI in main thread
            self.after(0, self._enrollment_success, template_data)

        except FingerprintCaptureError as e:
            error_msg = str(e)
            self.after(0, self._enrollment_error, error_msg)
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self.after(0, self._enrollment_error, error_msg)

    def _enrollment_success(self, template_data):
        """Handle successful fingerprint capture."""
        try:
            # Check if fingerprint already exists for this user
            existing = crud_fingerprint.get_fingerprint_by_user(self.db, self.user_id)
            if existing:
                # Update existing fingerprint
                existing.template = template_data
                self.db.commit()
                self.db.refresh(existing)
            else:
                # Create new fingerprint
                crud_fingerprint.enroll_fingerprint(self.db, self.user_id, template_data)

            self.status_label.configure(
                text="✅ Fingerprint enrolled successfully", text_color="green"
            )
            self.progress_label.pack_forget()
            self.capture_btn.configure(state="normal", text="Scan Fingerprint")

            self._safe_messagebox(
                title="Success", message="Fingerprint registered successfully!", icon="check"
            )

            # Close after short delay
            self.after(1500, self.destroy)

        except Exception as e:
            self._enrollment_error(f"Database error: {str(e)}")

    def _enrollment_error(self, error_msg):
        """Handle fingerprint capture error."""
        self.status_label.configure(text="❌ Enrollment failed", text_color="red")
        self.progress_label.pack_forget()
        self.capture_btn.configure(state="normal", text="Scan Fingerprint")

        self._safe_messagebox(title="Error", message=error_msg, icon="cancel")
