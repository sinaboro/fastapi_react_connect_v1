from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
import crud.user_crud as crud

SECRET_KEY = "12345678901234567890"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# JWT 액세스 토큰을 생성하는 함수
# 전달받은 사용자 정보(data)에 만료시간(exp)을 추가한 뒤
# SECRET_KEY와 알고리즘을 이용해 JWT 문자열로 암호화해서 반환한다.
def create_access_token(data: dict):
    # 원본 data를 직접 수정하지 않기 위해 복사본을 만든다.
    to_encode = data.copy()

    # 현재 UTC 시간 기준으로 토큰 만료 시간을 계산한다.
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # JWT payload에 만료 시간(exp)을 추가한다.
    to_encode.update({"exp": expire})

    # payload를 SECRET_KEY와 알고리즘으로 서명하여 JWT 토큰 문자열을 생성한다.
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# JWT 토근 검증 후 현재 로그인한 사용자 조회
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="인증 정보가 유효하지 않습니다",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = crud.get_user(db, int(user_id))
    if user is None:
        raise credentials_exception
    
    return user