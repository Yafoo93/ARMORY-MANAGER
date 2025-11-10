"""
Authentication Dialog Component
Simulates fingerprint authentication with password fallback.
"""

import customtkinter as ctk

from src.models.user import User


class AuthDialog(ctk.CTkToplevel):
    """Dialog for authenticating users (simulated fingerprint + password fallback)."""

    def __init__(self, parent, user: User, user_label: str, callback_on_success=None):
        """
        Args:
            parent: Parent window
            user: User object to authenticate
            user_label: Label describing the user (e.g., "Armorer" or "Officer")
            callback_on_success: Callback function(user_id) called when authentication succeeds
        """
        super().__init__(parent)
        self.user = user
        self.user_label = user_label
        self.callback_on_success = callback_on_success
        self.authenticated = False

        self.title(f"Authenticate {user_label}")
        self.geometry("450x500")
        self.grab_set()

        # Main frame
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text=f"Authenticate {user_label}",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        title_label.pack(pady=(10, 5))

        # User info
        user_info = ctk.CTkLabel(
            main_frame,
            text=f"{user.name}\nService No: {user.service_number}",
            font=ctk.CTkFont(size=12),
            text_color="gray",
        )
        user_info.pack(pady=(0, 20))

        # === Fingerprint Section ===
        fingerprint_frame = ctk.CTkFrame(main_frame)
        fingerprint_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            fingerprint_frame,
            text="Fingerprint Authentication",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(pady=(10, 5))

        # Fingerprint icon/placeholder
        fingerprint_icon = ctk.CTkLabel(
            fingerprint_frame,
            text="👆",
            font=ctk.CTkFont(size=48),
        )
        fingerprint_icon.pack(pady=10)

        ctk.CTkLabel(
            fingerprint_frame,
            text="Place your finger on the scanner",
            font=ctk.CTkFont(size=11),
            text_color="gray",
        ).pack(pady=(0, 10))

        # Confirm Fingerprint Button
        self.fingerprint_btn = ctk.CTkButton(
            fingerprint_frame,
            text="Confirm Fingerprint",
            fg_color="#007ACC",
            hover_color="#005B99",
            command=self._simulate_fingerprint,
        )
        self.fingerprint_btn.pack(pady=(0, 10))

        # === Password Fallback Section ===
        separator = ctk.CTkFrame(main_frame, height=2, fg_color="gray")
        separator.pack(fill="x", padx=10, pady=10)

        fallback_label = ctk.CTkLabel(
            main_frame,
            text="Fingerprint failed? Enter password",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#e69138",
        )
        fallback_label.pack(pady=(5, 5))

        # Password entry
        self.password_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="Enter password",
            show="*",
            width=300,
        )
        self.password_entry.pack(pady=5)
        self.password_entry.bind("<Return>", lambda e: self._verify_password())

        # Verify Password Button
        self.password_btn = ctk.CTkButton(
            main_frame,
            text="Verify Password",
            fg_color="#2D8C4A",
            hover_color="#1B7035",
            command=self._verify_password,
        )
        self.password_btn.pack(pady=(5, 10))

        # Status label
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="red",
        )
        self.status_label.pack(pady=(0, 10))

        # Cancel button
        cancel_btn = ctk.CTkButton(
            main_frame,
            text="Cancel",
            fg_color="gray",
            hover_color="darkgray",
            command=self._cancel,
        )
        cancel_btn.pack(pady=(0, 10))

        # Focus on password entry
        self.password_entry.focus()

    def _simulate_fingerprint(self):
        """Simulate fingerprint authentication (always succeeds for simulation)."""
        self.status_label.configure(text="Fingerprint verified successfully!", text_color="green")
        self.authenticated = True
        self._on_success()

    def _verify_password(self):
        """Verify password against user's stored password."""
        password = self.password_entry.get().strip()

        if not password:
            self.status_label.configure(text="Please enter a password", text_color="red")
            return

        if self.user.verify_password(password):
            self.status_label.configure(text="Password verified successfully!", text_color="green")
            self.authenticated = True
            self._on_success()
        else:
            self.status_label.configure(
                text="Invalid password. Please try again.", text_color="red"
            )
            self.password_entry.delete(0, "end")

    def _on_success(self):
        """Handle successful authentication."""
        # Store callback and user_id before destroying
        callback = self.callback_on_success
        user_id = self.user.id
        parent = self.master

        # Release grab before destroying to avoid conflicts
        try:
            self.grab_release()
        except Exception:
            pass

        # Destroy the dialog
        try:
            self.destroy()
        except Exception:
            pass

        # Call callback after dialog is destroyed using parent's after method
        # This ensures the dialog is fully destroyed before the callback runs
        if callback and parent:
            try:
                # Schedule callback to run after a short delay to ensure dialog is fully destroyed
                parent.after(100, lambda: callback(user_id))
            except Exception:
                # Fallback: try to call directly if after fails
                try:
                    callback(user_id)
                except Exception:
                    pass

    def _cancel(self):
        """Cancel authentication."""
        self.authenticated = False
        self.destroy()


def authenticate_user(parent, user: User, user_label: str, callback_on_success=None):
    """
    Helper function to show authentication dialog and wait for result.

    Args:
        parent: Parent window
        user: User object to authenticate
        user_label: Label describing the user
        callback_on_success: Callback function(user_id) called when authentication succeeds

    Returns:
        AuthDialog instance (caller can check .authenticated property)
    """
    dialog = AuthDialog(parent, user, user_label, callback_on_success)
    dialog.wait_window()
    return dialog
