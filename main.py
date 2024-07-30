from fastapi import FastAPI
from fastapi.responses import JSONResponse
from routers import user, file
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(file.router)

@app.get("/")
def greet():
    return JSONResponse(content={"Author":"Swoyam Siddharth Nayak"}, status_code=200)