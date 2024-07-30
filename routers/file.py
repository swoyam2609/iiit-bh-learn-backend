from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from dependencies import pass_jwt, mongo
import os

router = APIRouter()

@router.get("/browse")
def browseCourses(username: str = Depends(pass_jwt.get_current_user)):
    user = mongo.db.users.find_one({"username": username})
    if user is None:
        return JSONResponse(content={"message":"unauthenticated"})
    else:
        courses = os.listdir("./files")
        return JSONResponse(content={"courses": courses})
    
@router.get("/course")
def getCourse(coursename: str, username: str = Depends(pass_jwt.get_current_user)):
    user = mongo.db.users.find_one({"username": username})
    if user is None:
        return JSONResponse(content={"message":"unauthenticated"})
    else:
        content = os.listdir(f"./files/{coursename}")
        content.sort()
        return JSONResponse(content={"courses": content})