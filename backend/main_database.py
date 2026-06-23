from fastapi import FastAPI
from database import engine
from models import Base

app = FastAPI()

#서버 시작시 테이블 자동 생성
# user테이블, items테이블이 없다면 만들고, 있으면 그냥 유지
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "DB연결 성공! app.db파일을 확인하세요"}



