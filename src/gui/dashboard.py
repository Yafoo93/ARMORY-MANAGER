import tkinter as tk

def open_dashboard(self, user):
    from src.gui.dashboard import ArmoryApp  # ✅ Import Dashboard Class
    self.root.destroy()  # ✅ Close login window
    open_dashboard(user)  # ✅ Open dashboard



    tk.Label(dashboard, text=f"Welcome, {user.name}!", font=("Arial", 14)).pack(pady=20)

    # Logout Button
    tk.Button(dashboard, text="Logout", command=dashboard.destroy).pack(pady=20)

    dashboard.mainloop()

if __name__ == "__main__":
    app = ArmoryApp()
    app.mainloop()
