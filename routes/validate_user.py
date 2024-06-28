from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
router = APIRouter()

# Example data - replace with your actual database queries
users = {
    "station_user": {"password": "password123", "role": "police station"},
    "officer_user": {"password": "password456", "role": "police officer"},
}

class validate_user(BaseModel):
    username: str
    password: str
    role: str
    
    
@router.post("/validate_user/")
def validate_user(validate:validate_user):
    # user = users.get(username)
    # print(user)
    # if user and user["password"] == password and user["role"] == role:
    print(validate_user)
    print('hello')
    return {'valid': True}
    # raise HTTPException(status_code=400, detail="Invalid username or password")
