import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.database import SessionLocal
from src.crud.crud_user import create_user, get_all_users

# Start a database session
db = SessionLocal()

# Create a test user
user = create_user(db, "GP55351", "kassim mutawakil", "0240286508", "officer")
print(f"✅ User created: {user}")

# Fetch all users
users = get_all_users(db)
print("✅ All Users:", users)

# Close session
db.close()
