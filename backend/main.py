# main.py
from fastapi import FastAPI
from typing import Optional
from routers import user

app = FastAPI()

app.include_router(user.router)

# [Path Parameter] URL 경로에 값이 포함되는 방식
# 예: GET /users/42 → user_id = 42
# @app.get("/users/{user_id}")
# def get_user(user_id: int): # int 선언 시 타입 자동 검증
#     return {"user_id": user_id}

# [Query Parameter] URL 뒤에 ?key=value 형태로 전달
# 예: GET /items?skip=0&limit=5&keyword=노트북
@app.get("/items")
def get_items(
    skip: int = 0,
    limit: int = 10,
    keyword: Optional[str] = None
    ):
    return {"skip": skip, "limit": limit, "keyword": keyword}

# [혼합] Path + Query 동시 사용
# 예: GET /users/1/items?active=false
@app.get("/users/{user_id}/items")
def get_user_items(user_id: int, active: bool = True):
    return {"user_id": user_id, "active": active}
