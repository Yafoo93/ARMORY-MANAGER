from sqlalchemy.orm import Session
from src.models.user import User
from src.models.fingerprint import Fingerprint
from cryptography.fernet import Fernet
import jwt
from datetime import datetime, timedelta
from typing import Optional
import bcrypt


class AuthService:
    def __init__(self, db_session: Session):
        self.db = db_session
        # Initialize encryption key (in production, this should be in env variables)
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)

    def register_user(
        self, 
        service_number: str, 
        name: str, 
        telephone: str, 
        role: str,
        fingerprint_template: Optional[bytes] = None
    ) -> User:
        """Register a new user with optional fingerprint"""
        # Check if user already exists
        existing_user = self.db.query(User).filter(
            User.service_number == service_number
        ).first()
        
        if existing_user:
            raise ValueError("User with this service number already exists")

        # Create new user
        new_user = User(
            service_number=service_number,
            name=name,
            telephone=telephone,
            role=role
        )
        
        self.db.add(new_user)
        self.db.commit()

        # If fingerprint provided, store it
        if fingerprint_template:
            fingerprint = Fingerprint(
                template=fingerprint_template,
                user_id=new_user.id
            )
            self.db.add(fingerprint)
            self.db.commit()

        return new_user

    def verify_fingerprint(self, user_id: int, fingerprint_template: bytes) -> bool:
        """Verify user's fingerprint"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user or not user.fingerprint:
            return False

        # In a real application, you would use the fingerprint SDK to compare templates
        # This is a placeholder for the actual fingerprint comparison logic
        stored_template = user.fingerprint.template
        return self._compare_fingerprints(stored_template, fingerprint_template)

    def _compare_fingerprints(self, template1: bytes, template2: bytes) -> bool:
        """
        Placeholder for actual fingerprint comparison logic
        You'll need to implement this using your chosen fingerprint SDK
        """
        # TODO: Implement actual fingerprint comparison
        return True  # Placeholder return

    def create_session(self, user_id: int) -> str:
        """Create a session token for authenticated user"""
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(hours=8)  # Token expires in 8 hours
        }
        return jwt.encode(payload, str(self.key), algorithm='HS256')

    def verify_session(self, token: str) -> Optional[int]:
        """Verify session token and return user_id if valid"""
        try:
            payload = jwt.decode(token, str(self.key), algorithms=['HS256'])
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Retrieve user by ID"""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_service_number(self, service_number: str) -> Optional[User]:
        """Retrieve user by service number"""
        return self.db.query(User).filter(
            User.service_number == service_number
        ).first()
        
    def check_password(password: str, hashed: str) -> bool:
        """Verify a password against its hash."""
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
