# routers/item.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import crud.item_crud as crud
import schemas
from auth import get_current_user

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/", response_model=list[schemas.ItemResponse])
def list_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_items(db, skip=skip, limit=limit)

@router.get("/{item_id}", response_model=schemas.ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")
    return item

@router.post("/", response_model=schemas.ItemResponse, status_code=201)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db),
                current_user=Depends(get_current_user) ):
    return crud.create_item(db, item, owner_id=current_user.id)

@router.put("/{item_id}", response_model=schemas.ItemResponse)
def update_item(item_id: int, item: schemas.ItemUpdate, db: Session = Depends(get_db),
                current_user=Depends(get_current_user) ):
    existing = crud.get_item(db, item_id)
    if not existing:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")
    if existing.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="본인이 등록한 아이템만 수정할 수 있습니다")
    
    return crud.update_item(db, item_id, item)

@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db),
        current_user=Depends(get_current_user)):
    existing = crud.get_item(db, item_id)
    
    if not existing:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")
    
    if existing.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="본인이 등록한 아이템만 삭제할 수 있습니다")
    
    crud.delete_item(db, item_id)