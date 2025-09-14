import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from src.database import SessionLocal
from src.crud.crud_ammunition import (
    list_ammunition,
    create_ammunition,
    update_ammunition,
    delete_ammunition,
    adjust_stock,
    get_ammunition_by_id,
)

LOW_STOCK_BG = "#3b2f2f"  # subtle dark-maroon highlight row if low stock

class AmmunitionManagement(ctk.CTkFrame):
    """
    Ammunition Management screen:
    - Search/filter
    - Table of ammo lines
    - Add / Edit / Delete
    - Stock +/- adjustment
    - Low-stock highlighting based on reorder_level
    """

    def __init__(self, parent):
        super().__init__(parent, corner_radius=10)
        self.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.parent = parent
        self.db_session = SessionLocal()
        self.dialog_open = False
        self.search_var = tk.StringVar()

        # Canvas scaffold (match User UI)
        self.content_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = ctk.CTkCanvas(self.content_frame, highlightthickness=0, bg="#2b2b2b")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ctk.CTkScrollbar(self.content_frame, orientation="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.main_container = ctk.CTkFrame(self.canvas, corner_radius=15, fg_color="#2b2b2b")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.main_container, anchor="nw")
        self.main_container.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_window, width=self.canvas.winfo_width()))
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.bind("<Destroy>", self._on_destroy)

        # Header
        header_frame = ctk.CTkFrame(self.main_container, corner_radius=0, fg_color="transparent")
        header_frame.pack(fill=tk.X, pady=(0, 20))
        ctk.CTkLabel(header_frame, text="Ammunition Management",
                     font=ctk.CTkFont(size=24, weight="bold")).pack(pady=10)

        # Search + actions
        actions = ctk.CTkFrame(self.main_container, height=50, corner_radius=10)
        actions.pack(fill=tk.X, pady=(0, 20))

        search_entry = ctk.CTkEntry(actions, textvariable=self.search_var, placeholder_text="Search by platform/caliber...")
        search_entry.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)

        ctk.CTkButton(actions, text="Search", width=100, command=self.refresh_table).pack(side=tk.LEFT, padx=10, pady=10)
        ctk.CTkButton(actions, text="Refresh", width=100, fg_color="#4CAF50", hover_color="#388E3C",
                      command=lambda: (self.search_var.set(""), self.refresh_table())).pack(side=tk.LEFT, padx=10, pady=10)

        # Buttons row
        btn_bar = ctk.CTkFrame(self.main_container, corner_radius=10, fg_color="transparent")
        btn_bar.pack(fill=tk.X, pady=(0, 10))
        btn_bar.columnconfigure((0,1,2), weight=1)

        ctk.CTkButton(btn_bar, text="Add Ammunition", fg_color="#4CAF50", hover_color="#388E3C",
                      height=40, corner_radius=8, command=self.open_add_dialog).grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        ctk.CTkButton(btn_bar, text="Edit Selected", fg_color="#2196F3", hover_color="#1976D2",
                      height=40, corner_radius=8, command=self.open_edit_dialog).grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        ctk.CTkButton(btn_bar, text="Delete Selected", fg_color="#F44336", hover_color="#D32F2F",
                      height=40, corner_radius=8, command=self.delete_selected).grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        # Table
        self.tree_frame = ctk.CTkFrame(self.main_container, corner_radius=10, fg_color="#2b2b2b")
        self.tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0,20))

        self.tree_scroll_y = ctk.CTkScrollbar(self.tree_frame, orientation="vertical", fg_color="#2b2b2b")
        self.tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_scroll_x = ctk.CTkScrollbar(self.tree_frame, orientation="horizontal", fg_color="#2b2b2b")
        self.tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        style = ttk.Style()
        style.configure("Treeview", background="#2b2b2b", foreground="white",
                        fieldbackground="#2b2b2b", rowheight=30, borderwidth=0)
        style.configure("Treeview.Heading", background="#1f6aa5", foreground="#000000",
                        relief="flat", font=('TkDefaultFont', 12, 'bold'), borderwidth=0)
        style.map("Treeview", background=[("selected", "#1f6aa5")], foreground=[("selected", "white")])

        columns = ("id","category","platform","caliber","count","reorder_level","bin_location")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings",
                                 yscrollcommand=self.tree_scroll_y.set, xscrollcommand=self.tree_scroll_x.set)
        self.tree_scroll_y.configure(command=self.tree.yview)
        self.tree_scroll_x.configure(command=self.tree.xview)

        for col, header, width, anchor in [
            ("id","ID",60,"center"),
            ("category","Category",120,"w"),
            ("platform","Platform",220,"w"),
            ("caliber","Caliber",180,"w"),
            ("count","Count",90,"center"),
            ("reorder_level","Reorder @",100,"center"),
            ("bin_location","Bin",120,"center")
        ]:
            self.tree.heading(col, text=header)
            self.tree.column(col, width=width, anchor=anchor)

        self.tree.tag_configure("low", background=LOW_STOCK_BG)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<Double-1>", lambda e: self.open_edit_dialog())

        
        self.refresh_table()
        
    def _on_mousewheel(self, event):
        try:
        
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except Exception:
            pass
        return "break" 

        
        
    def _on_dialog_saved(self):
        self.refresh_table()
        try:
            CTkMessagebox(self, title="Saved", message="Ammunition saved.", icon="check")
        except Exception:
            pass
        self.dialog_open = False

    def open_add_dialog(self):
        if self.dialog_open: 
            return
        self.dialog_open = True
        dlg = AddEditAmmoDialog(self, mode="add", on_saved=self._on_dialog_saved)
        self.parent.wait_window(dlg)
        self.dialog_open = False

    def open_edit_dialog(self):
        if self.dialog_open:
            return
        ammo_id = self._selected_ammo_id()
        if not ammo_id:
            CTkMessagebox(self, title="Info", message="Select a row first.", icon="info")
            return
        self.dialog_open = True
        dlg = AddEditAmmoDialog(self, mode="edit", ammo_id=ammo_id, on_saved=self._on_dialog_saved)
        self.parent.wait_window(dlg)
        self.dialog_open = False


    def _on_destroy(self, _event=None):
        try:
            if self.db_session:
                self.db_session.close()
        except Exception:
            pass

    def _clear_search(self):
        self.search_var.set("")
        self.refresh_table()

    def refresh_table(self):
        for row_id in self.tree.get_children():
            self.tree.delete(row_id)

        query_text = self.search_var.get().strip()
        rows = list_ammunition(self.db_session, query_text=query_text, limit=500)

        for ammo in rows:
            tags = []
            if ammo.reorder_level and ammo.count is not None and ammo.count <= ammo.reorder_level:
                tags.append("low")
            self.tree.insert(
                "",
                "end",
                values=(
                    ammo.id,
                    ammo.category or "",
                    ammo.platform or "",
                    ammo.caliber or "",
                    ammo.count or 0,
                    ammo.reorder_level or 0,
                    ammo.bin_location or "",
                ),
                tags=tags
            )

    def _selected_ammo_id(self) -> int | None:
        selected = self.tree.selection()
        if not selected:
            return None
        values = self.tree.item(selected[0], "values")
        if not values:
            return None
        try:
            return int(values[0])
        except Exception:
            return None
        

    def delete_selected(self):
        ammo_id = self._selected_ammo_id()
        if not ammo_id:
            CTkMessagebox(self, title="Info", message="Select a row first.", icon="info")
            return

        confirm = CTkMessagebox(
            self, title="Confirm",
            message="Delete selected ammunition line?",
            icon="warning", option_1="Cancel", option_2="Delete"
        )
        if confirm.get() != "Delete":
            return

        ok = delete_ammunition(self.db_session, ammo_id)
        if ok:
            self.refresh_table()
            CTkMessagebox(self, title="Deleted", message="Ammunition line removed.", icon="check")
        else:
            CTkMessagebox(self, title="Error", message="Delete failed.", icon="warning")


        self.refresh_table()


class AddEditAmmoDialog(ctk.CTkToplevel):
    def __init__(self, parent, mode: str, ammo_id: int | None = None, on_saved=None):
        super().__init__(parent)
        self.title("Ammunition")
        self.geometry("420x460")
        self.resizable(False, False)
        self.parent = parent
        self.mode = mode
        self.on_saved = on_saved
        self.db_session = parent.db_session
        self.ammo_id = ammo_id

        # layout
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=16, pady=16)

        # Category (use widget .get(), not a StringVar)
        ctk.CTkLabel(body, text="Category").pack(anchor="w")
        self.category_combo = ctk.CTkComboBox(
            body, values=["Rifle", "Pistol/SMG", "Shotgun"], width=360
        )
        self.category_combo.pack(pady=(0, 8))
        self.category_combo.set("Rifle")  # default

        # Platform
        ctk.CTkLabel(body, text="Platform").pack(anchor="w")
        self.platform_entry = ctk.CTkEntry(
            body, width=360, placeholder_text="e.g., AK47 / CZ 809 BREN"
        )
        self.platform_entry.pack(pady=(0, 8))

        # Caliber
        ctk.CTkLabel(body, text="Caliber").pack(anchor="w")
        self.caliber_entry = ctk.CTkEntry(
            body, width=360, placeholder_text="e.g., 7.62×39mm"
        )
        self.caliber_entry.pack(pady=(0, 8))

        # Count
        ctk.CTkLabel(body, text="Initial Count (for Add) / Current Count (Edit)").pack(anchor="w")
        self.count_entry = ctk.CTkEntry(body, width=220)
        self.count_entry.insert(0, "0")
        self.count_entry.pack(pady=(0, 8), anchor="w")

        # Reorder level
        ctk.CTkLabel(body, text="Reorder Level").pack(anchor="w")
        self.reorder_entry = ctk.CTkEntry(body, width=220)
        self.reorder_entry.insert(0, "0")
        self.reorder_entry.pack(pady=(0, 8), anchor="w")

        # Bin
        ctk.CTkLabel(body, text="Bin / Location (optional)").pack(anchor="w")
        self.bin_entry = ctk.CTkEntry(body, width=260)
        self.bin_entry.pack(pady=(0, 8), anchor="w")

        # Buttons
        btns = ctk.CTkFrame(body, fg_color="transparent")
        btns.pack(fill="x", pady=(8, 0))
        ctk.CTkButton(btns, text="Cancel", fg_color="#9e9e9e",
                      hover_color="#757575", command=self.destroy).pack(side="left")
        ctk.CTkButton(btns, text="Save", command=self._save).pack(side="right")

        # Load existing row in edit mode
        if self.mode == "edit" and self.ammo_id:
            self._load_ammo()

        self.grab_set()
        self.transient(parent)
        self._center()

    def _load_ammo(self):
        ammo = get_ammunition_by_id(self.db_session, self.ammo_id)
        if not ammo:
            messagebox.showerror("Error", "Ammunition not found.")
            self.destroy()
            return
        self.category_combo.set(ammo.category or "Rifle")
        self.platform_entry.delete(0, tk.END); self.platform_entry.insert(0, ammo.platform or "")
        self.caliber_entry.delete(0, tk.END);  self.caliber_entry.insert(0, ammo.caliber or "")
        self.count_entry.delete(0, tk.END);    self.count_entry.insert(0, str(ammo.count or 0))
        self.reorder_entry.delete(0, tk.END);  self.reorder_entry.insert(0, str(ammo.reorder_level or 0))
        self.bin_entry.delete(0, tk.END);      self.bin_entry.insert(0, ammo.bin_location or "")

    def _save(self):
        # Read directly from widgets
        category = self.category_combo.get().strip()
        platform = self.platform_entry.get().strip()
        caliber  = self.caliber_entry.get().strip()
        bin_location = (self.bin_entry.get().strip() or None)

        if not category or not platform or not caliber:
            messagebox.showwarning("Missing data", "Category, Platform and Caliber are required.")
            return

        try:
            desired_count = int((self.count_entry.get() or "0").strip())
            reorder_level = int((self.reorder_entry.get() or "0").strip())
        except ValueError:
            messagebox.showwarning("Invalid numbers", "Count and Reorder level must be integers.")
            return

        if self.mode == "add":
            create_ammunition(
                self.db_session,
                category=category, platform=platform, caliber=caliber,
                count=desired_count, reorder_level=reorder_level,
                bin_location=bin_location
            )
        else:
            # Update meta fields first
            updated = update_ammunition(
                self.db_session, ammo_id=self.ammo_id,
                category=category, platform=platform, caliber=caliber,
                reorder_level=reorder_level, bin_location=bin_location
            )
            if not updated:
                messagebox.showerror("Error", "Update failed.")
                return
            # Normalize stock by delta if user changed the count
            current = updated.count or 0
            if desired_count != current:
                adjust_stock(self.db_session, self.ammo_id, desired_count - current)

        # Notify parent & close
        if callable(self.on_saved):
            try:
                self.on_saved()
            except Exception:
                pass
        self.destroy()
        # mark parent dialog flag off if present
        if hasattr(self.parent, "dialog_open"):
            self.parent.dialog_open = False
                
    def _center(self):
        self.update_idletasks()
        try:
            px, py = self.parent.winfo_rootx(), self.parent.winfo_rooty()
            pw, ph = self.parent.winfo_width(), self.parent.winfo_height()
            w, h = self.winfo_reqwidth(), self.winfo_reqheight()
            x = px + (pw // 2) - (w // 2)
            y = py + (ph // 2) - (h // 2)
        except Exception:
            sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
            w, h = self.winfo_reqwidth(), self.winfo_reqheight()
            x = (sw // 2) - (w // 2)
            y = (sh // 2) - (h // 2)

        x = max(0, min(x, self.winfo_screenwidth() - w))
        y = max(0, min(y, self.winfo_screenheight() - h))
        self.geometry(f"+{x}+{y}")