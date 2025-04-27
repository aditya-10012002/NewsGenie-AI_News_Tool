from fastapi import APIRouter, HTTPException, Depends, Request
from app.db.mongo import get_collection
from passlib.context import CryptContext
from jose import jwt
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")
    try:
        token = token.split("Bearer ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        users = await get_collection("users")
        user = await users.find_one({"_id": ObjectId(user_id)})
        if user:
            return {"email": user.get("email"), "favorites_count": len(user.get("favorites", []))}
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/me")
async def read_current_user(user: dict = Depends(get_current_user)):
    return user

@router.post("/signup")
async def signup(email: str, password: str):
    users = await get_collection("users")
    existing = await users.find_one({"email": email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(password)
    user = {"email": email, "password": hashed_password, "favorites": []}
    await users.insert_one(user)
    return {"message": "Signup successful!"}

@router.post("/login")
async def login(email: str, password: str):
    users = await get_collection("users")
    user = await users.find_one({"email": email})
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user["_id"])})
    return {"access_token": token}
