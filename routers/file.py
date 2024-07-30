from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, StreamingResponse
from dependencies import pass_jwt, mongo
import os
from pathlib import Path

router = APIRouter()

@router.get("/browse", tags=["Course"])
async def browseCourses(username: str = Depends(pass_jwt.get_current_user)):
    user = mongo.db.users.find_one({"username": username})
    if user is None:
        return JSONResponse(content={"message":"unauthenticated"})
    else:
        courses = os.listdir("./files")
        return JSONResponse(content={"courses": courses})
    
@router.get("/course", tags=["Course"])
async def getCourse(courseName: str, username: str = Depends(pass_jwt.get_current_user)):
    user = mongo.db.users.find_one({"username": username})
    if user is None:
        return JSONResponse(content={"message":"unauthenticated"})
    else:
        content = os.listdir(f"./files/{courseName}")
        content.sort()
        return JSONResponse(content={"courses": content})
    
@router.get("/play", tags=["Course"])
async def playCourse(courseName: str, fileName: str, username: str = Depends(pass_jwt.get_current_user)):
    user = mongo.db.users.find_one({"username": username})
    if user is None:
        return JSONResponse(content={"message":"unauthenticated"})
    else:
        videoPath = Path(f"./files/{courseName}/{fileName}")
        videoFile = open(videoPath, mode="rb")
        return StreamingResponse(videoFile, media_type="video/mp4")