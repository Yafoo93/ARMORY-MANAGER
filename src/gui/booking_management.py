import tkinter as tk

# from datetime import datetime
from tkinter import ttk

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from src.crud import crud_booking

# from src.database import SessionLocal
from src.models.ammunition import Ammunition
from src.models.booking import Booking
from src.models.duty_point import DutyPoint
from src.models.user import User
from src.models.weapon import Weapon


class BookingManagement(ctk.CTkFrame):
    def __init__(self, master, db, *args, **kwargs):
        super().__init__(master, corner_radius=10, *args, **kwargs)
        self.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.db = db
        self.parent = master  # parent reference for dialogs

        # === Top toolbar ===
        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.pack(fill=tk.X, pady=(10, 5), padx=20)

        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(
            toolbar,
            textvariable=self.search_var,
            placeholder_text="Search by Officer name, Service No, or Weapon...",
            width=400,
        )
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))

        ctk.CTkButton(
            toolbar,
            text="Search",
            command=self.search_booking,
            width=100,
            fg_color="#007ACC",
            hover_color="#005B99",
        ).pack(side=tk.LEFT)

        ctk.CTkButton(
            toolbar,
            text="Refresh",
            command=self.refresh_table,
            width=100,
            fg_color="#2D8C4A",
            hover_color="#1B7035",
        ).pack(side=tk.LEFT, padx=(10, 0))

        # === Treeview Frame ===
        tree_frame = ctk.CTkFrame(self, fg_color="transparent")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(5, 10))

        columns = (
            "id",
            "service_no",
            "officer_name",
            "weapon",
            "duty_point",
            "ammunition",
            "ammo_count",
            "status",
            "issued_at",
            "returned_at",
        )

        # Treeview styling
        style = ttk.Style()
        style.configure(
            "Treeview",
            background="#2b2b2b",
            foreground="white",
            fieldbackground="#2b2b2b",
            rowheight=30,
            borderwidth=0,
            font=("TkDefaultFont", 10),
        )
        style.configure(
            "Treeview.Heading",
            background="#1f6aa5",
            foreground="#000000",
            relief="flat",
            font=("TkDefaultFont", 12, "bold"),
            borderwidth=0,
        )
        style.map(
            "Treeview",
            background=[("selected", "#1f6aa5")],
            foreground=[("selected", "white")],
        )

        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)

        # Headings
        self.tree.heading("id", text="ID")
        self.tree.heading("service_no", text="Service No")
        self.tree.heading("officer_name", text="Officer Name")
        self.tree.heading("weapon", text="Weapon")
        self.tree.heading("duty_point", text="Duty Point")
        self.tree.heading("ammunition", text="Ammunition")
        self.tree.heading("ammo_count", text="Ammo Count")
        self.tree.heading("status", text="Status")
        self.tree.heading("issued_at", text="Issued At")
        self.tree.heading("returned_at", text="Returned At")

        # Column widths
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("service_no", width=120, anchor="w")
        self.tree.column("officer_name", width=180, anchor="w")
        self.tree.column("weapon", width=150, anchor="w")
        self.tree.column("duty_point", width=130, anchor="w")
        self.tree.column("ammunition", width=150, anchor="w")
        self.tree.column("ammo_count", width=100, anchor="center")
        self.tree.column("status", width=100, anchor="center")
        self.tree.column("issued_at", width=130, anchor="center")
        self.tree.column("returned_at", width=130, anchor="center")

        # Scrollbars
        self.tree_scroll_y = ctk.CTkScrollbar(
            tree_frame,
            orientation="vertical",
            command=self.tree.yview,
            fg_color="#2b2b2b",
            button_color="#1f6aa5",
            button_hover_color="#2980b9",
        )
        self.tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree_scroll_x = ctk.CTkScrollbar(
            tree_frame,
            orientation="horizontal",
            command=self.tree.xview,
            fg_color="#2b2b2b",
            button_color="#1f6aa5",
            button_hover_color="#2980b9",
        )
        self.tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.tree.configure(
            yscrollcommand=self.tree_scroll_y.set, xscrollcommand=self.tree_scroll_x.set
        )
        self.tree.pack(fill=tk.BOTH, expand=True)

        # === Bottom action buttons ===
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill=tk.X, pady=(0, 15))

        ctk.CTkButton(
            button_frame,
            text="+ Book Weapon",
            width=150,
            fg_color="#007ACC",
            hover_color="#005B99",
            command=self.open_booking_form,
        ).pack(side=tk.LEFT, padx=(30, 10))

        ctk.CTkButton(
            button_frame,
            text="Return Weapon",
            width=150,
            fg_color="#8B0000",
            hover_color="#5A0000",
            command=self.return_weapon,
        ).pack(side=tk.LEFT)

        # Initial table load
        self.refresh_table()

    # ---------------------------------------------------------------------
    # Table helpers
    # ---------------------------------------------------------------------
    def _format_status(self, status_obj: object) -> str:
        """Normalize Booking.status to a clean human string.

        Supports both Enum(BookingStatus) and plain string values.
        """
        try:
            value = getattr(status_obj, "value", None)
            if isinstance(value, str):
                return value.capitalize()
            text = str(status_obj) if status_obj is not None else ""
            if text.startswith("BookingStatus."):
                text = text.split(".", 1)[1]
            return text.capitalize() if text else "—"
        except Exception:
            return "—"

    def refresh_table(self):
        """Reload all booking data."""
        try:
            for row in self.tree.get_children():
                self.tree.delete(row)

            bookings = crud_booking.list_bookings(self.db)
            if not bookings:
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        "—",
                        "—",
                        "No bookings available yet",
                        "—",
                        "—",
                        "—",
                        "—",
                        "—",
                        "—",
                        "—",
                    ),
                )
                return

            for b in bookings:
                status_text = self._format_status(b.status)

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        b.id,
                        getattr(b.officer, "service_number", "N/A") if b.officer else "N/A",
                        getattr(b.officer, "name", "N/A") if b.officer else "N/A",
                        getattr(b.weapon, "type", "N/A") if b.weapon else "N/A",
                        getattr(b.duty_point, "location", "N/A") if b.duty_point else "N/A",
                        getattr(b.ammunition, "caliber", "—") if b.ammunition else "—",
                        b.ammunition_count or 0,
                        status_text,
                        b.issued_at.strftime("%Y-%m-%d %H:%M") if b.issued_at else "—",
                        b.returned_at.strftime("%Y-%m-%d %H:%M") if b.returned_at else "—",
                    ),
                )

        except Exception as e:
            print(f"Error loading bookings: {e}")
            CTkMessagebox(
                title="Error",
                message=f"Error loading bookings: {str(e)}",
                icon="error",
            )

    def search_booking(self):
        """Search bookings by officer name, service number, or weapon."""
        try:
            query = (self.search_var.get() or "").strip().lower()
            for row in self.tree.get_children():
                self.tree.delete(row)

            all_bookings = crud_booking.list_bookings(self.db)
            results = []
            for b in all_bookings:
                officer_name = (getattr(b.officer, "name", "") or "").lower() if b.officer else ""
                officer_service_number = (
                    (getattr(b.officer, "service_number", "") or "").lower() if b.officer else ""
                )
                weapon_type = (getattr(b.weapon, "type", "") or "").lower() if b.weapon else ""
                if query in officer_name or query in officer_service_number or query in weapon_type:
                    results.append(b)

            if not results:
                self.tree.insert(
                    "", "end", values=("—", "—", "No matching results", "", "", "", "", "", "", "")
                )
                return

            for b in results:
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        b.id,
                        getattr(b.officer, "service_number", "N/A") if b.officer else "N/A",
                        getattr(b.officer, "name", "N/A") if b.officer else "N/A",
                        getattr(b.weapon, "type", "N/A") if b.weapon else "N/A",
                        getattr(b.duty_point, "location", "N/A") if b.duty_point else "N/A",
                        getattr(b.ammunition, "caliber", "—") if b.ammunition else "—",
                        b.ammunition_count or 0,
                        self._format_status(b.status),
                        b.issued_at.strftime("%Y-%m-%d %H:%M") if b.issued_at else "—",
                        b.returned_at.strftime("%Y-%m-%d %H:%M") if b.returned_at else "—",
                    ),
                )
        except Exception as e:
            print(f"Error searching bookings: {e}")
            CTkMessagebox(
                title="Error", message=f"Error searching bookings: {str(e)}", icon="error"
            )

    def _selected_booking_id(self) -> int | None:
        """Return selected booking id from the tree (or None)."""
        sel = self.tree.selection()
        if not sel:
            return None
        values = self.tree.item(sel[0], "values")
        try:
            bid = int(values[0])
            return bid
        except (ValueError, IndexError):
            return None

    # ---------------------------------------------------------------------
    # Booking modal
    # ---------------------------------------------------------------------
    def open_booking_form(self):
        """Open modal to create a booking (no remarks here)."""
        win = ctk.CTkToplevel(self)
        win.title("Book Weapon")
        win.geometry("560x380")
        win.grab_set()

        form = ctk.CTkFrame(win)
        form.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Load choices
        officers = self.db.query(User).order_by(User.name.asc()).all()

        duty_points = self.db.query(DutyPoint).order_by(DutyPoint.location.asc()).all()
        weapons = (
            self.db.query(Weapon)
            .filter(Weapon.status == "AVAILABLE")
            .order_by(Weapon.type.asc())
            .all()
        )
        ammos = (
            self.db.query(Ammunition)
            .order_by(Ammunition.platform.asc(), Ammunition.caliber.asc())
            .all()
        )

        # Mappings for id lookup
        officer_display = [f"{u.service_number} — {u.name}" for u in officers]
        dp_display = [dp.location for dp in duty_points]
        weapon_display = [f"{w.id} — {w.type} ({w.serial_number})" for w in weapons]
        ammo_display = ["None"] + [
            f"{a.id} — {a.platform} ({a.caliber}) • stock={a.count}" for a in ammos
        ]

        ctk.CTkLabel(form, text="Officer").grid(row=0, column=0, sticky="w", padx=6, pady=(6, 2))
        officer_var = ctk.StringVar()
        ctk.CTkOptionMenu(form, variable=officer_var, values=officer_display or ["—"]).grid(
            row=0, column=1, sticky="ew", padx=6, pady=(6, 2)
        )

        ctk.CTkLabel(form, text="Duty Point").grid(row=1, column=0, sticky="w", padx=6, pady=2)
        dp_var = ctk.StringVar()
        ctk.CTkOptionMenu(form, variable=dp_var, values=dp_display or ["—"]).grid(
            row=1, column=1, sticky="ew", padx=6, pady=2
        )

        ctk.CTkLabel(form, text="Weapon").grid(row=2, column=0, sticky="w", padx=6, pady=2)
        weapon_var = ctk.StringVar()
        ctk.CTkOptionMenu(form, variable=weapon_var, values=weapon_display or ["—"]).grid(
            row=2, column=1, sticky="ew", padx=6, pady=2
        )

        ctk.CTkLabel(form, text="Ammunition (optional)").grid(
            row=3, column=0, sticky="w", padx=6, pady=2
        )
        ammo_var = ctk.StringVar(value="None")
        ctk.CTkOptionMenu(form, variable=ammo_var, values=ammo_display).grid(
            row=3, column=1, sticky="ew", padx=6, pady=2
        )

        ctk.CTkLabel(form, text="Ammo Count").grid(row=4, column=0, sticky="w", padx=6, pady=2)
        ammo_count_var = ctk.StringVar(value="0")
        ctk.CTkEntry(form, textvariable=ammo_count_var).grid(
            row=4, column=1, sticky="ew", padx=6, pady=2
        )

        form.columnconfigure(1, weight=1)

        def submit():
            # Validate selections
            try:
                if not officers or not duty_points or not weapons:
                    CTkMessagebox(
                        title="Error",
                        message="Please seed Users, Duty Points, and Weapons first.",
                        icon="warning",
                    )
                    return

                # Officer
                o_index = officer_display.index(officer_var.get())
                officer_id = officers[o_index].id

                # Duty point
                dp_index = dp_display.index(dp_var.get())
                duty_point_id = duty_points[dp_index].id

                # Weapon
                w_index = weapon_display.index(weapon_var.get())
                weapon_id = weapons[w_index].id

                # Ammo (optional)
                ammo_choice = ammo_var.get()
                ammunition_id = None
                ammunition_count = 0
                if ammo_choice != "None":
                    a_index = ammo_display.index(ammo_choice) - 1
                    ammo_row = ammos[a_index]
                    # Count
                    try:
                        ammunition_count = int(ammo_count_var.get())
                        if ammunition_count < 0:
                            raise ValueError
                    except ValueError:
                        CTkMessagebox(
                            title="Error",
                            message="Ammo count must be a non-negative integer.",
                            icon="error",
                        )
                        return

                    # If user chose ammo, count must be > 0
                    if ammunition_count == 0:
                        CTkMessagebox(
                            title="Error",
                            message="Enter ammo count when ammunition is selected.",
                            icon="error",
                        )
                        return

                    # Stock check, then deduct
                    if (ammo_row.count or 0) < ammunition_count:
                        stock_msg = (
                            f"Only {ammo_row.count or 0} in stock for "
                            f"{ammo_row.platform} ({ammo_row.caliber})."
                        )
                        CTkMessagebox(
                            title="Insufficient Stock",
                            message=stock_msg,
                            icon="warning",
                        )
                        return
                    ammo_row.count = (ammo_row.count or 0) - ammunition_count
                    ammunition_id = ammo_row.id

                # Create booking (also flips weapon to ISSUED)
                # Use logged-in armorer (current user) from parent if available;
                # fall back to officer_id
                current_user = getattr(self.parent, "current_user", None)
                armorer_id = getattr(current_user, "id", None) or officer_id

                # Perform in one transaction: ammo deduction is already staged in this session,
                # and create_booking will commit it together with the new booking.
                booking = crud_booking.create_booking(
                    self.db,
                    officer_id=officer_id,
                    armorer_id=armorer_id,
                    weapon_id=weapon_id,
                    duty_point_id=duty_point_id,
                    ammunition_id=ammunition_id,
                    ammunition_count=ammunition_count,
                )

                CTkMessagebox(
                    title="Success", message=f"Booking #{booking.id} created.", icon="check"
                )
                win.destroy()
                self.refresh_table()

            except Exception as e:
                # Roll back any staged changes in the session for safety
                try:
                    self.db.rollback()
                except Exception:
                    pass
                CTkMessagebox(title="Error", message=str(e))

        ctk.CTkButton(
            win, text="Book Weapon", fg_color="#007ACC", hover_color="#005B99", command=submit
        ).pack(pady=(0, 12))

    # ---------------------------------------------------------------------
    # Return modal
    # ---------------------------------------------------------------------
    def return_weapon(self):
        """Open modal to process a return with mandatory ammo return and conditional remarks."""
        booking_id = self._selected_booking_id()
        if not booking_id:
            CTkMessagebox(
                title="Select Booking", message="Please select a booking row.", icon="warning"
            )
            return

        booking = self.db.query(Booking).get(booking_id)
        if not booking:
            CTkMessagebox(title="Not Found", message="Booking no longer exists.", icon="warning")
            return
        if booking.status == "RETURNED":
            CTkMessagebox(
                title="Already Returned", message="This booking is already returned.", icon="info"
            )
            return

        win = ctk.CTkToplevel(self)
        win.title(f"Return Booking #{booking.id}")
        win.geometry("560x360")
        win.grab_set()

        form = ctk.CTkFrame(win)
        form.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        issued_count = booking.ammunition_count or 0
        ammo_label_text = (
            f"Ammunition to return (issued: {issued_count})"
            if booking.ammunition_id
            else "Ammunition to return (no ammo was issued)"
        )
        ctk.CTkLabel(form, text=ammo_label_text).grid(
            row=0, column=0, sticky="w", padx=6, pady=(6, 2)
        )
        returned_var = ctk.StringVar(value="0" if booking.ammunition_id else "0")
        return_entry = ctk.CTkEntry(form, textvariable=returned_var)
        return_entry.grid(row=0, column=1, sticky="ew", padx=6, pady=(6, 2))

        ctk.CTkLabel(form, text="Remarks (required if quantities differ)").grid(
            row=1, column=0, sticky="nw", padx=6, pady=(6, 2)
        )
        remarks = ctk.CTkTextbox(form, height=100)
        remarks.grid(row=1, column=1, sticky="nsew", padx=6, pady=(6, 2))

        form.columnconfigure(1, weight=1)
        form.rowconfigure(1, weight=1)

        def submit_return():
            try:
                try:
                    returned_cnt = int(returned_var.get() or "0")
                    if returned_cnt < 0:
                        raise ValueError
                except ValueError:
                    CTkMessagebox(
                        title="Error",
                        message="Returned ammo must be a non-negative integer.",
                        icon="error",
                    )
                    return

                text_remarks = remarks.get("1.0", "end").strip() or None

                # ✅ This single line replaces all the manual ammo/weapon/booking updates
                from src.crud import crud_booking

                crud_booking.return_booking(
                    self.db,
                    booking_id=booking.id,
                    ammunition_returned=returned_cnt,
                    remarks=text_remarks,
                )

                CTkMessagebox(
                    title="Success",
                    message=f"Booking #{booking.id} returned successfully.",
                    icon="check",
                )
                win.destroy()
                self.refresh_table()

            except Exception as e:
                try:
                    self.db.rollback()
                except Exception:
                    pass
                CTkMessagebox(title="Error", message=str(e), icon="error")

        ctk.CTkButton(
            win,
            text="Confirm Return",
            fg_color="#8B0000",
            hover_color="#5A0000",
            command=submit_return,
        ).pack(pady=(8, 12))
