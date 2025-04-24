from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import motor.motor_asyncio
from uuid import uuid4
from datetime import datetime, timedelta
import os

app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# MongoDB Atlas setup (replace with your credentials)
MONGO_URL = os.getenv("MONGO_URL")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client.mydb

@app.get("/login")
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def post_login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = await db.users.find_one({"username": username})
    if not user or password != user["password"]:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

    # Create session
    session_id = str(uuid4())
    await db.sessions.insert_one({"session_id": session_id, "username": username})

    response = RedirectResponse(url="/dashboard", status_code=302)
    response.set_cookie("session_id", session_id, httponly=True)
    return response

@app.get("/signup")
async def get_signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup")
async def post_signup(request: Request, username: str = Form(...), password: str = Form(...)):
    # Check if username already exists
    existing_user = await db.users.find_one({"username": username})
    if existing_user:
        return templates.TemplateResponse("signup.html", {"request": request, "error": "Username already exists"})
    
    # Create new user
    await db.users.insert_one({"username": username, "password": password})
    
    # Redirect to login page
    return RedirectResponse(url="/login", status_code=302)

@app.get("/dashboard")
async def dashboard(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id:
        return RedirectResponse(url="/login")

    session = await db.sessions.find_one({"session_id": session_id})
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": session["username"]})

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie("session_id")
    return response