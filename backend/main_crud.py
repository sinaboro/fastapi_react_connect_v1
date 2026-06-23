from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from models import Base
from routers import user, item, auth

app = FastAPI(title="Item Management API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(item.router)
@app.get("/")
def root():
    return {"message": "FastAPI + React CRUD API 정상 동작 중"}