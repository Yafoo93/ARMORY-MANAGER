# src/gui/duty_point_management.py
import customtkinter as ctk
from tkinter import messagebox
from src.database import SessionLocal
from src.crud import crud_duty_point

class DutyPointManagement(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = SessionLocal()

        # Title
        ctk.CTkLabel(self, text="Duty Point Management",
                     font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(10, 0))

        # --- Create Form ---
        form = ctk.CTkFrame(self)
        form.pack(fill="x", padx=12, pady=12)

        self.location_entry = ctk.CTkEntry(form, placeholder_text="Location (unique)")
        self.location_entry.grid(row=0, column=0, padx=(10, 8), pady=8, sticky="ew")

        self.description_entry = ctk.CTkEntry(form, placeholder_text="Description (optional)")
        self.description_entry.grid(row=0, column=1, padx=(8, 10), pady=8, sticky="ew")

        form.grid_columnconfigure(0, weight=1)
        form.grid_columnconfigure(1, weight=2)

        ctk.CTkButton(form, text="Add Duty Point", command=self.add_duty_point).grid(
            row=0, column=2, padx=(8, 10), pady=8
        )

        # --- List Container ---
        self.list_container = ctk.CTkScrollableFrame(self, height=360)
        self.list_container.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        # Header row
        header = ctk.CTkFrame(self.list_container, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=6, pady=(6, 2))
        ctk.CTkLabel(header, text="ID", width=50, anchor="w",
                     font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(header, text="Location", anchor="w",
                     font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, sticky="w", padx=(10,0))
        ctk.CTkLabel(header, text="Description", anchor="w",
                     font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, sticky="w", padx=(10,0))
        ctk.CTkLabel(header, text="Actions", anchor="w",
                     font=ctk.CTkFont(weight="bold")).grid(row=0, column=3, sticky="w", padx=(10,0))

        self.refresh_list()

    # --- Actions ---
    def add_duty_point(self):
        location = (self.location_entry.get() or "").strip()
        description = (self.description_entry.get() or "").strip()
        if not location:
            messagebox.showerror("Error", "Location is required.")
            return
        _, err = crud_duty_point.create_duty_point(self.db, location, description)
        if err:
            messagebox.showerror("Error", err)
        else:
            self.location_entry.delete(0, "end")
            self.description_entry.delete(0, "end")
            self.refresh_list()

    def refresh_list(self):
        # clear rows (keep header at row 0)
        for child in self.list_container.winfo_children():
            if isinstance(child, ctk.CTkFrame) and child.grid_info().get("row", 0) != 0:
                child.destroy()

        dps = crud_duty_point.get_all_duty_points(self.db)
        for i, dp in enumerate(dps, start=1):
            row = ctk.CTkFrame(self.list_container, fg_color="transparent")
            row.grid(row=i, column=0, sticky="ew", padx=6, pady=4)
            row.grid_columnconfigure(1, weight=1)
            row.grid_columnconfigure(2, weight=2)

            ctk.CTkLabel(row, text=str(dp.id), width=50, anchor="w").grid(row=0, column=0, sticky="w")
            loc = ctk.CTkLabel(row, text=dp.location or "", anchor="w")
            loc.grid(row=0, column=1, sticky="w", padx=(10,0))
            desc = ctk.CTkLabel(row, text=dp.description or "", anchor="w")
            desc.grid(row=0, column=2, sticky="w", padx=(10,0))

            actions = ctk.CTkFrame(row, fg_color="transparent")
            actions.grid(row=0, column=3, sticky="w", padx=(10,0))

            ctk.CTkButton(actions, text="Edit", width=60,
                          command=lambda d=dp: self.open_edit_dialog(d)).pack(side="left", padx=(0, 6))
            ctk.CTkButton(actions, text="Delete", width=70, fg_color="#c75450", hover_color="#b44743",
                          command=lambda d=dp: self._delete(d.id)).pack(side="left")

    def _delete(self, dp_id: int):
        ok, err = crud_duty_point.delete_duty_point(self.db, dp_id)
        if err:
            messagebox.showerror("Error", err)
        else:
            self.refresh_list()

    # --- Simple inline edit dialog ---
    def open_edit_dialog(self, duty_point):
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Edit Duty Point #{duty_point.id}")
        dialog.geometry("480x200")
        dialog.grab_set()

        loc = ctk.CTkEntry(dialog)
        loc.insert(0, duty_point.location or "")
        loc.pack(fill="x", padx=12, pady=(16, 8))

        desc = ctk.CTkEntry(dialog)
        desc.insert(0, duty_point.description or "")
        desc.pack(fill="x", padx=12, pady=8)

        def save():
            # we will do a straightforward delete+create for simplicity or you can add an update in CRUD
            # Better: write an update method. Here's a quick inline version to avoid more files:
            try:
                duty_point.location = (loc.get() or "").strip()
                duty_point.description = (desc.get() or "").strip() or None
                self.db.commit()
                self.db.refresh(duty_point)
                dialog.destroy()
                self.refresh_list()
            except Exception as e:
                self.db.rollback()
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(dialog, text="Save Changes", command=save).pack(pady=12)
