# main.py
from fastapi import FastAPI
from datetime import datetime
import schemas

app = FastAPI()

# ── User 엔드포인트 ──────────────────────────────
# response_model=schemas.UserResponse → 응답 시 password 등 불필요한 필드 자동 제거

@app.post("/users", response_model=schemas.UserResponse, status_code=201)
def create_user(user: schemas.UserCreate):   # Body를 UserCreate로 자동 검증

    return {
        "id": 1,
        "username": user.username,
        "email": user.email,
        "created_at": datetime.now()
    }

# ── Item 엔드포인트 ──────────────────────────────
@app.post("/items", response_model=schemas.ItemResponse, status_code=201)
def create_item(item: schemas.ItemCreate):
    return {
        "id": 1,
        "name": item.name,
        "price": item.price,
        "owner_id": None
    }

@app.put("/items/{item_id}", response_model=schemas.ItemResponse)
def update_item(item_id: int, item: schemas.ItemUpdate):
    # item.name, item.price 가 None이면 수정 안 함
    return {
        "id": item_id,
        "name": item.name or "기존이름",
        "price": item.price or 9999,
        "owner_id": None
    }