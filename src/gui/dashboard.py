from src.main import ArmoryApp


def open_dashboard(user):
    # Create and launch ArmoryApp directly
    app = ArmoryApp(user)
    app.mainloop()


if __name__ == "__main__":
    # For debugging, run without login
    dummy_user = type("User", (), {"name": "Test User"})()
    open_dashboard(dummy_user)
