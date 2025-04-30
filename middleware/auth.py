from fastapi import Request, HTTPException, Depends, Header
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Dict
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
import os

# Configure JWT settings
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-here")  # In production, use env var
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthMiddleware:
    def __init__(self, db):
        self.db = db
        self.security = HTTPBearer(auto_error=False)
    
    def verify_password(self, plain_password, hashed_password):
        """Verify password against hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password):
        """Hash password"""
        return pwd_context.hash(password)
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """Create JWT token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return encoded_jwt
    
    async def authenticate_user(self, username: str, password: str):
        """Authenticate user with username and password"""
        user = await self.db.users.find_one({"username": username})
        if not user:
            return False
        if not self.verify_password(password, user["password"]):
            return False
        return user
    
    async def get_current_user(self, token: str):
        """Decode and validate JWT token"""
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            username = payload.get("sub")
            if username is None:
                return None
            
            user = await self.db.users.find_one({"username": username})
            return user
        except JWTError:
            return None
    
    async def verify_session(self, request: Request) -> Optional[Dict]:
        """Verify session from cookies or authorization header"""
        # Skip auth for login and signup routes
        if request.url.path in ["/login", "/signup", "/static"]:
            return None
        
        # First check cookies for backward compatibility
        session_id = request.cookies.get("session_id")
        if session_id:
            session = await self.db.sessions.find_one({"session_id": session_id})
            if session:
                return session
        
        # Then check JWT token in authorization header
        token = request.cookies.get("access_token")
        if not token:
            # Check for Authorization header
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
        
        if not token:
            raise HTTPException(status_code=303, detail="Not authenticated", headers={"Location": "/login"})
        
        user = await self.get_current_user(token)
        if not user:
            raise HTTPException(status_code=303, detail="Invalid token", headers={"Location": "/login"})
        
        return {"username": user["username"]}