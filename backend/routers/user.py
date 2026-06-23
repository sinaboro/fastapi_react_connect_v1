from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import crud.user_crud as crud
import schemas

router = APIRouter(prefix="/users", tags=["users"])

# /users - 전체 조회(페이징 처리)
@router.get("/", response_model=list[schemas.UserResponse])
def list_users(skip: int=0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)

# /users/{user_id} -  단건 조회(user_id)
@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db:Session = Depends(get_db)):
    user =crud.get_user(db,user_id)

    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return user

# 회원 등록
@router.post("/", response_model=schemas.UserResponse, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, user.email)

    if existing:
        raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다.")
    return crud.create_user(db, user)

# 회원 삭제
@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session=Depends(get_db)):
    if not crud.delete_user(db, user_id):
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
