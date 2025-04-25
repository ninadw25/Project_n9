from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse
from typing import Optional

class AuthMiddleware:
    def __init__(self, db):
        self.db = db

    async def verify_session(self, request: Request) -> Optional[dict]:
        # Skip auth for login and signup routes
        if request.url.path in ["/login", "/signup", "/static"]:
            return None

        session_id = request.cookies.get("session_id")
        if not session_id:
            raise HTTPException(status_code=303, detail="Not authenticated", headers={"Location": "/login"})
        
        session = await self.db.sessions.find_one({"session_id": session_id})
        if not session:
            raise HTTPException(status_code=303, detail="Not authenticated", headers={"Location": "/login"})
        
        return session