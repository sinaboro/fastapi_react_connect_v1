#models.py

# models.py

# SQLAlchemy에서 사용하는 컬럼 타입들을 import
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey

# 테이블 간 연관관계(1:N, N:1)를 설정할 때 사용
from sqlalchemy.orm import relationship

# DB 함수(NOW(), CURRENT_TIMESTAMP 등)를 사용하기 위한 객체
from sqlalchemy.sql import func

# database.py에서 생성한 ORM의 부모 클래스(Base)를 import
from database import Base


# ==========================================
# User 테이블 (회원 테이블)
# ==========================================
class User(Base):

    # 실제 DB 테이블 이름
    __tablename__ = "users"

    # 회원번호 (PK)
    # primary_key=True -> 기본키
    # index=True -> 검색 속도 향상을 위한 인덱스 생성
    id = Column(Integer, primary_key=True, index=True)

    # 사용자 아이디
    # 최대 50자
    # unique=True -> 중복 불가
    # nullable=False -> NULL 허용 안함
    username = Column(String(50), unique=True, nullable=False)

    # 이메일
    # 중복 불가
    email = Column(String(100), unique=True, nullable=False)

    # 비밀번호
    # 암호화된 문자열 저장
    # bcrypt를 사용하면 길이가 길어지므로 보통 200자 정도 지정
    password = Column(String(200), nullable=False)

    # 회원 활성화 여부
    # True -> 사용 가능
    # False -> 탈퇴 또는 비활성화
    is_active = Column(Boolean, default=True)

    # 회원가입 날짜
    # server_default=func.now()
    # -> DB가 현재 시간을 자동 저장
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # User 1명은 여러 Item을 가질 수 있음
    # User(1) : Item(N)
    #
    # back_populates="owner"
    # -> Item 클래스의 owner 변수와 연결됨
    items = relationship(
        "Item",
        back_populates="owner"
    )


# ==========================================
# Item 테이블 (상품 또는 게시물 테이블)
# ==========================================
class Item(Base):

    # 실제 DB 테이블 이름
    __tablename__ = "items"

    # 상품번호(PK)
    id = Column(Integer, primary_key=True, index=True)

    # 상품명
    # 최대 100자
    # NULL 허용 안함
    name = Column(
        String(100),
        nullable=False
    )

    # 상품 가격
    # Float 타입 사용
    # ※ 원래 nullable=True 또는 False를 사용해야 함
    # 아래 코드는 오타입니다.
    # nullable=Float  -> 잘못된 코드
    price = Column(
        Float,
        nullable=True
    )

    # 외래키(FK)
    #
    # users 테이블의 id를 참조
    #
    # users.id
    #      ↑
    # ForeignKey("users.id")
    #
    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    # Item(N) : User(1)
    #
    # owner를 통해
    # item.owner.username
    # 처럼 작성 가능
    owner = relationship(
        "User",
        back_populates="items"
    )