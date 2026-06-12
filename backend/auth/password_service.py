from passlib.context import CryptContext

class PasswordService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, plain: str) -> str:
        """Hashes a password using bcrypt."""
        return self.pwd_context.hash(plain)

    def verify_password(self, plain: str, hashed: str) -> bool:
        """Verifies a plain password against a hashed password."""
        return self.pwd_context.verify(plain, hashed)

    def validate_password(self, plain: str) -> bool:
        """Validates a password strength."""
        if len(plain) < 8:
            return False
        return True
