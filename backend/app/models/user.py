from werkzeug.security import generate_password_hash, check_password_hash
from app.services.database import Database
import uuid

class User:
    @staticmethod
    def collection():
        db = Database.get_db()
        return db.users if db is not None else None
    
    @staticmethod
    def create_user(email, password, name):
        col = User.collection()
        if col is None:
            # Fallback for mock mode if DB isn't running
            return {"_id": str(uuid.uuid4()), "email": email, "name": name}
            
        if col.find_one({"email": email}):
            raise Exception("User with this email already exists")
            
        user_doc = {
            "email": email,
            "password": generate_password_hash(password),
            "name": name,
            "_id": str(uuid.uuid4())
        }
        col.insert_one(user_doc)
        return user_doc

    @staticmethod
    def authenticate(email, password):
        col = User.collection()
        if col is None:
            # Fallback for mock mode if DB isn't running
            return {"_id": "mock_id", "email": email, "name": "Mock User"}
            
        user = col.find_one({"email": email})
        if user and check_password_hash(user['password'], password):
            return user
        return None
