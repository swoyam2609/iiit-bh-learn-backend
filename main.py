from fastapi import FastAPI
from fastapi.responses import JSONResponse
from routers import user

app = FastAPI()

app.include_router(user.router)

@app.get("/")
def greet():
    return JSONResponse(content={"Author":"Swoyam Siddharth Nayak"}, status_code=200)