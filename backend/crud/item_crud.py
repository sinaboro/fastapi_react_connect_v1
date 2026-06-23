# crud/item_crud.py

from sqlalchemy.orm import Session
from models import Item
from schemas import ItemCreate, ItemUpdate

def get_item(db:Session, item_id:int):
    return db.query(Item).filter(Item.id == item_id).first()

def get_items(db:Session, skip: int=0, limit: int=10):
    return db.query(Item).offset(skip).limit(limit).all()

def create_item(db: Session, item: ItemCreate, owner_id: int = None):
    db_item = Item(name=item.name, price=item.price,owner_id=owner_id )
    
    print("-"*50)
    print(db_item)
    db.add(db_item)
    print("-"*50)

    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_id: int, item_data: ItemUpdate):
    db_item = get_item(db, item_id)
    
    if not db_item:
        return None
    
    if item_data.name is not None:
        db_item.name = item_data.name
    
    if item_data.price is not None:
        db_item.price = item_data.price

    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    db_item = get_item(db, item_id)

    if db_item:
        db.delete(db_item)
        db.commit()
        
    return db_item
