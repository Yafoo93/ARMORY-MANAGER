import threading

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from src.crud import crud_fingerprint
from src.database import SessionLocal
from src.services.fingerprint_service import (
    FingerprintCaptureError,
    capture_fingerprint,
)


class FingerprintVerify(ctk.CTkToplevel):
    def __init__(self, master, callback_on_success):
        super().__init__(master)
        self.db = SessionLocal()
        self.callback_on_success = callback_on_success
        self.title("Verify Fingerprint")
        self.geometry("450x280")
        self.grab_set()

        # Title
        ctk.CTkLabel(
            self, text="Fingerprint Verification", font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(20, 10))

        # Instructions
        instruction_text = (
            "Click 'Scan & Verify' and place your finger\n"
            "on the fingerprint reader when prompted."
        )
        ctk.CTkLabel(
            self, text=instruction_text, font=ctk.CTkFont(size=12), text_color="gray"
        ).pack(pady=10)

        # Verify button
        self.verify_btn = ctk.CTkButton(
            self,
            text="Scan & Verify",
            command=self.verify,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14),
        )
        self.verify_btn.pack(pady=20)

        # Status label
        self.status_label = ctk.CTkLabel(
            self, text="Ready to verify...", text_color="gray", font=ctk.CTkFont(size=12)
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

    def verify(self):
        """Verify fingerprint in a separate thread to avoid blocking UI."""
        self.verify_btn.configure(state="disabled", text="Scanning...")
        self.status_label.configure(text="Place your finger on the reader...", text_color="blue")
        self.progress_label.pack(pady=5)
        self.progress_label.configure(text="Waiting for fingerprint...")

        # Run verification in background thread
        thread = threading.Thread(target=self._verify_in_thread, daemon=True)
        thread.start()

    def _verify_in_thread(self):
        """Perform fingerprint verification in background thread."""
        try:
            # Capture current fingerprint
            scanned_template = capture_fingerprint()

            # Verify against stored templates
            user_id = crud_fingerprint.verify_fingerprint(self.db, scanned_template)

            # Update UI in main thread
            if user_id:
                self.after(0, self._verification_success, user_id)
            else:
                self.after(0, self._verification_failed)

        except FingerprintCaptureError as e:
            error_msg = str(e)
            self.after(0, self._verification_error, error_msg)
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self.after(0, self._verification_error, error_msg)

    def _verification_success(self, user_id):
        """Handle successful verification."""
        self.status_label.configure(text="✅ Verified successfully", text_color="green")
        self.progress_label.pack_forget()
        self.verify_btn.configure(state="normal", text="Scan & Verify")

        # Call success callback after short delay
        self.after(800, lambda: self._call_callback(user_id))

    def _verification_failed(self):
        """Handle failed verification."""
        self.status_label.configure(text="❌ Verification failed", text_color="red")
        self.progress_label.pack_forget()
        self.verify_btn.configure(state="normal", text="Scan & Verify")

        self._safe_messagebox(
            title="Access Denied",
            message="Fingerprint not recognized. Please try again.",
            icon="cancel",
        )

    def _verification_error(self, error_msg):
        """Handle verification error."""
        self.status_label.configure(text="❌ Error occurred", text_color="red")
        self.progress_label.pack_forget()
        self.verify_btn.configure(state="normal", text="Scan & Verify")

        self._safe_messagebox(title="Error", message=error_msg, icon="cancel")

    def _call_callback(self, user_id):
        """Call the success callback and close window."""
        try:
            self.callback_on_success(user_id)
        finally:
            self.destroy()
