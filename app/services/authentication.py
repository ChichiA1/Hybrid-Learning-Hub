import bcrypt
from passlib.context import CryptContext
from app.models.users import UserPasswordUpdate

# creates an object. "bcrypt" is the hashing algorithm to be used.
# deprecated="auto" setting ensures that deprecated hashes are automatically updated
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def create_salt_and_hashed_password(self, *, plaintext_password: str) -> UserPasswordUpdate:
        salt = self.generate_salt()
        hashed_password = self.hash_password(password=plaintext_password, salt=salt)

        return UserPasswordUpdate(salt=salt, password=hashed_password)

    def generate_salt(self) -> str:
        # generate a new salt and then decodes it from bytes to a string
        return bcrypt.gensalt().decode()

    def hash_password(self, *, password: str, salt: str) -> str:
        return pwd_context.hash(password + salt)



auth_service = AuthService()
