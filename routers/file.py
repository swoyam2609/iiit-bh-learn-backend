from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from dependencies import pass_jwt, mongo
import os
from pathlib import Path
import key
from datetime import datetime

router = APIRouter()

@router.get("/browse", tags=["Course"])
async def browseCourses(username: str = Depends(pass_jwt.get_current_user)):
    user = mongo.db.users.find_one({"username": username})
    if user is None:
        return JSONResponse(content={"message":"unauthenticated"})
    else:
        courses = mongo.db.courses.find({})
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
    
@router.post("/uploadcourse", tags=["Course"])
async def uploadCourse(courseName: str, playlistId: str, pin:int):
    if(pin!=key.KEY):
        return JSONResponse(content={"message":"unauthorized"})
    data = {
        "courseName": courseName,
        "playlistId": playlistId,
        "dateUploaded": datetime.today().strftime('%d%m%Y')
    }
    mongo.db.courses.insert_one(data)
    return JSONResponse(content={"message": "course uploaded"})
