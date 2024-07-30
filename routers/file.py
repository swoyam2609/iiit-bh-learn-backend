from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from dependencies import pass_jwt, mongo
import os
from pathlib import Path
import zipfile
import aiofiles

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
    
@router.post("/uploadcourse", tags=["Course"])
async def uploadCourse(courseName: str, courseFile: UploadFile = File(...)):
    filePath = f"./files/temp/{courseFile.filename}"
    async with aiofiles.open(filePath, "wb") as f:
        content = await courseFile.read()
        await f.write(content)

    coursePath = f"./files/{courseName}"
    os.makedirs(coursePath, exist_ok=True)  # Ensure the directory exists

    # Extract the ZIP file
    with zipfile.ZipFile(filePath, 'r') as zipRef:
        zipRef.extractall(coursePath)

    # Remove the ZIP file
    os.remove(filePath)

    return JSONResponse(content={"message": "course uploaded"})
