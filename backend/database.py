#database.py

# SQLAlchemy에서 데이터베이스 엔진 생성 함수 import
from sqlalchemy import create_engine

# ORM의 기본 클래스(Base)와 세션(Session) 생성 도구 import
from sqlalchemy.orm import declarative_base, sessionmaker


# -------------------------------
# 데이터베이스 연결 주소(URL)
# sqlite:///./app.db
# -> 현재 프로젝트 폴더에 app.db 파일 생성
# -> SQLite는 별도 DB 서버 설치 없이 사용 가능
# -------------------------------
DATABASE_URL = "sqlite:///./app.db"


# -------------------------------
# Engine 생성
# Engine = 데이터베이스와 실제 연결을 관리하는 객체
#
# check_same_thread=False
# -> SQLite 전용 옵션
# -> 여러 스레드에서 같은 DB 연결 사용 허용
# -> FastAPI는 비동기/멀티스레드 환경이라 보통 설정함
# -------------------------------
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


# -------------------------------
# Session 클래스 생성
#
# autocommit=False
# -> commit()을 직접 호출해야 DB에 저장
#
# autoflush=False
# -> 자동 flush 비활성화
# -> 필요할 때만 DB에 SQL 전송
#
# bind=engine
# -> 위에서 만든 Engine과 연결
# -------------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# -------------------------------
# 모든 ORM 모델이 상속받는 부모 클래스
#
# 예)
# class User(Base):
#     __tablename__ = "users"
#     ...
#
# Base를 상속하면 테이블과 매핑됨
# -------------------------------
Base = declarative_base()


# -------------------------------
# 데이터베이스 세션을 생성하고 반환하는 함수
#
# FastAPI의 Depends()와 함께 사용
#
# 예)
# @app.get("/users")
# def get_users(db: Session = Depends(get_db)):
#     ...
# -------------------------------
def get_db():

    # DB 세션 생성
    db = SessionLocal()

    try:
        # 호출한 함수에 세션 전달
        yield db

    finally:
        # 요청이 끝나면 세션 종료
        # DB 연결 누수 방지
        db.close()

