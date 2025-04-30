from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import motor.motor_asyncio
from uuid import uuid4
import os
from datetime import datetime, timedelta

# Import services and models
from middleware.auth import AuthMiddleware
from models.schemas import TextInput, SummaryResponse
from services.summarizer import SummarizerService

app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# MongoDB setup
MONGO_URL = os.getenv("MONGO_URL")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client.mydb

# Initialize services
auth = AuthMiddleware(db)
summarizer_service = SummarizerService(db)

@app.get("/")
async def root():
    return RedirectResponse(url="/login", status_code=302)

# Authentication routes
@app.get("/login")
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def post_login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = await auth.authenticate_user(username, password)
    
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

    # Create JWT token
    access_token_expires = timedelta(minutes=30)
    access_token = auth.create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    
    # For backward compatibility, also create a session
    session_id = str(uuid4())
    await db.sessions.insert_one({"session_id": session_id, "username": username})
    
    response = RedirectResponse(url="/dashboard", status_code=302)
    response.set_cookie("access_token", access_token, httponly=True)
    response.set_cookie("session_id", session_id, httponly=True)  # For backward compatibility
    return response

@app.get("/signup")
async def get_signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup")
async def post_signup(request: Request, username: str = Form(...), password: str = Form(...)):
    existing_user = await db.users.find_one({"username": username})
    if existing_user:
        return templates.TemplateResponse("signup.html", {"request": request, "error": "Username already exists"})
    
    # Hash the password
    hashed_password = auth.get_password_hash(password)
    
    # Store user with hashed password
    await db.users.insert_one({"username": username, "password": hashed_password})
    return RedirectResponse(url="/login", status_code=302)

# Dashboard and summary routes
@app.get("/dashboard")
async def dashboard(request: Request, session: dict = Depends(auth.verify_session)):
    summaries = await summarizer_service.get_user_summaries(session["username"])
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "user": session["username"],
        "summaries": summaries
    })

@app.get("/summarize")
async def get_summarize_page(request: Request, session: dict = Depends(auth.verify_session)):
    return templates.TemplateResponse("summarize.html", {"request": request, "user": session["username"]})

@app.post("/api/summarize")
async def summarize_text(
    text_input: TextInput,
    session: dict = Depends(auth.verify_session)
):
    try:
        summary, summary_id = await summarizer_service.summarize_text(
            text_input.text, 
            text_input.summary_type, 
            text_input.groq_api_key,
            session["username"]
        )
        return {"summary": summary, "summary_id": summary_id}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/summary/{summary_id}")
async def view_summary(
    request: Request, 
    summary_id: str, 
    session: dict = Depends(auth.verify_session)
):
    summary = await summarizer_service.get_summary_by_id(summary_id, session["username"])
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    
    return templates.TemplateResponse(
        "summary_detail.html", 
        {"request": request, "user": session["username"], "summary": summary}
    )

@app.post("/api/save_summary/{summary_id}")
async def save_summary(
    summary_id: str,
    session: dict = Depends(auth.verify_session)
):
    try:
        success = await summarizer_service.save_summary(summary_id, session["username"])
        if not success:
            raise HTTPException(status_code=404, detail="Summary not found or could not be saved")
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Add JWT token refresh endpoint
@app.post("/api/refresh-token")
async def refresh_token(session: dict = Depends(auth.verify_session)):
    access_token_expires = timedelta(minutes=30)
    access_token = auth.create_access_token(
        data={"sub": session["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=302)
    # Clear cookies
    response.delete_cookie("access_token")
    response.delete_cookie("session_id")
    return response