# 🔗 fastapi_react_connect_v1

**FastAPI(백엔드) + React(프론트엔드)** 로 구성된, **JWT 인증 기반 아이템(Item) CRUD** 실습 프로젝트입니다.
Spring/Java 계열과 비교 학습이 가능하도록 코드 곳곳에 "Spring OO와 비슷한 역할" 형태의 한글 주석이 달려 있는 **교육용 예제 저장소**입니다.

> 원본 저장소: https://github.com/sinaboro/fastapi_react_connect_v1

---

## 1. 프로젝트 구성

```
fastapi_react_connect_v1/
├── FastAPI_교안_V10.pdf     # 수업용 교안 PDF
├── git_python.sh            # git add/commit/push 단축 스크립트
├── backend/                  # FastAPI 서버
└── frontend/                 # React 클라이언트 (CRA)
```

---

## 2. 기술 스택

| 구분 | 사용 기술 |
|---|---|
| 백엔드 프레임워크 | FastAPI |
| ORM | SQLAlchemy 2.x |
| DB | SQLite (`app.db`) |
| 인증 | JWT (`python-jose`) + OAuth2PasswordBearer |
| 비밀번호 암호화 | passlib (bcrypt) |
| 데이터 검증 | Pydantic v2 (`EmailStr`, `field_validator`) |
| 테스트 | pytest + FastAPI `TestClient` |
| 프론트엔드 | React 19 (Create React App) |
| HTTP 통신 | axios (interceptor로 JWT 자동 첨부) |
| 배포 | Docker (backend 단독 컨테이너화) |

---

## 3. 백엔드(backend) 구조

```
backend/
├── main.py              # ⚠️ 학습용 기초 예제 (Path/Query Parameter 실습) — 실제 서비스 엔트리포인트 아님
├── main_database.py      # 학습용: DB 연결 & 테이블 자동 생성 확인용 엔트리포인트
├── main_schemas.py       # 학습용: Pydantic 스키마 검증 실습용 엔트리포인트 (DB 미연동, 더미 응답)
├── main_crud.py           # ✅ 실제 서비스용 엔트리포인트 (Docker CMD가 실행하는 파일)
├── database.py            # SQLAlchemy engine / SessionLocal / get_db() 정의
├── models.py               # User, Item 테이블 정의 (1:N 관계)
├── schemas.py               # Pydantic 요청/응답 스키마
├── auth.py                   # JWT 토큰 발급 & 현재 로그인 사용자 검증
├── routers/
│   ├── auth.py                # /auth/register, /auth/login, /auth/me
│   ├── user.py                 # /users (CRUD, 페이징)
│   └── item.py                  # /items (CRUD, 소유자 검증)
├── crud/
│   ├── user_crud.py             # 사용자 관련 DB 접근 로직
│   └── item_crud.py              # 아이템 관련 DB 접근 로직
├── test_main.py                  # pytest 기반 통합 테스트 (인증 흐름 포함)
├── requirements.txt                # 패키지 목록 (Spring 대응 주석 포함)
├── Dockerfile                       # 컨테이너 빌드 설정
└── app.db                            # SQLite DB 파일 (실행 시 자동 생성)
```

### 📌 왜 `main.py`, `main_database.py`, `main_schemas.py`, `main_crud.py`가 여러 개인가요?
이 프로젝트는 **FastAPI를 단계별로 학습**할 수 있도록 진행 단계별 엔트리포인트를 남겨둔 구조입니다.

| 파일 | 학습 단계 | 내용 |
|---|---|---|
| `main.py` | 1단계 | Path Parameter / Query Parameter 기본 문법 실습 |
| `main_database.py` | 2단계 | SQLAlchemy DB 연결 + 테이블 자동 생성 확인 |
| `main_schemas.py` | 3단계 | Pydantic 스키마로 요청/응답 검증 (DB 미연동, 더미 데이터 반환) |
| `main_crud.py` | 4단계(최종) | DB + 스키마 + 인증(JWT) + CORS까지 모두 결합한 **완성본** |

실제로 `Dockerfile`의 `CMD`는 `uvicorn main_crud:app ...`으로 지정되어 있어, **`main_crud.py`가 최종 서비스 진입점**입니다.

---

## 4. 데이터 모델 (`models.py`)

```
User (users)                     Item (items)
├─ id (PK)                       ├─ id (PK)
├─ username (unique)             ├─ name
├─ email (unique)                ├─ price (Float)
├─ password (bcrypt hash)        ├─ owner_id (FK → users.id)
├─ is_active (bool)              └─ owner ──┐
├─ created_at (자동 생성)                    │
└─ items (1:N) ───────────────────────────┘
```

- **User 1 : Item N** 관계 (`relationship(back_populates=...)`로 양방향 매핑)
- Item의 `owner_id`는 로그인한 사용자의 id가 자동으로 들어감 (아래 API 참고)

---

## 5. API 엔드포인트 (`main_crud.py` 기준)

### 🔐 인증 (`/auth`) — `routers/auth.py`
| Method | 경로 | 설명 | 인증 필요 |
|---|---|---|---|
| POST | `/auth/register` | 회원가입 | ❌ |
| POST | `/auth/login` | 로그인 (OAuth2 Form, `username`=이메일) → JWT 발급 | ❌ |
| GET | `/auth/me` | 내 정보 조회 | ✅ |

### 👤 사용자 (`/users`) — `routers/user.py`
| Method | 경로 | 설명 | 인증 필요 |
|---|---|---|---|
| GET | `/users/` | 사용자 목록 (페이징: `skip`, `limit`) | ❌ |
| GET | `/users/{user_id}` | 사용자 단건 조회 | ❌ |
| POST | `/users/` | 사용자 생성 | ❌ |
| DELETE | `/users/{user_id}` | 사용자 삭제 | ❌ |

### 📦 아이템 (`/items`) — `routers/item.py`
| Method | 경로 | 설명 | 인증 필요 | 비고 |
|---|---|---|---|---|
| GET | `/items/` | 아이템 목록 조회 | ❌ | |
| GET | `/items/{item_id}` | 아이템 단건 조회 | ❌ | |
| POST | `/items/` | 아이템 생성 | ✅ | `owner_id`는 로그인 사용자로 자동 지정 |
| PUT | `/items/{item_id}` | 아이템 수정 | ✅ | **본인 소유 아이템만** 수정 가능 (403) |
| DELETE | `/items/{item_id}` | 아이템 삭제 | ✅ | **본인 소유 아이템만** 삭제 가능 (403) |

> 인증이 필요한 API는 요청 헤더에 `Authorization: Bearer <access_token>` 을 포함해야 합니다.

---

## 6. 인증(JWT) 흐름

```
1) POST /auth/register  → 회원가입 (비밀번호 bcrypt 해시 저장)
2) POST /auth/login     → 이메일/비밀번호 검증 → JWT access_token 발급 (60분 유효)
3) 이후 요청             → Authorization: Bearer {token} 헤더로 전달
4) get_current_user()   → 토큰 디코딩 → user_id(sub) 추출 → DB에서 사용자 조회
```

- `auth.py`의 `SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES`로 토큰 정책 관리
- `OAuth2PasswordBearer(tokenUrl="/auth/login")` 를 사용해 FastAPI 자동 문서(Swagger UI, `/docs`)에서도 로그인 테스트 가능

---

## 7. 프론트엔드(frontend) 구조

```
frontend/src/
├── App.js                    # 로그인 상태에 따라 로그인/회원가입 화면 or 아이템 관리 화면 분기
├── api/
│   ├── authApi.js               # register / login / fetchMyInfo (axios)
│   └── itemApi.js                # fetchItems / createItem / updateItem / deleteItem
│                                  # → axios interceptor로 모든 요청에 JWT 자동 첨부
└── components/
    ├── LoginForm.jsx               # 로그인 폼
    ├── RegisterForm.jsx             # 회원가입 폼
    ├── ItemForm.jsx                  # 아이템 등록/수정 폼 (editItem prop으로 모드 전환)
    └── ItemList.jsx                   # 아이템 목록 + 수정/삭제 버튼
```

### 화면 흐름
1. 앱 최초 로드 시 `localStorage`의 토큰으로 `/auth/me` 호출 → 로그인 여부 확인
2. 비로그인 상태 → `LoginForm` ↔ `RegisterForm` 전환 가능
3. 로그인 성공 → 토큰을 `localStorage`에 저장 → 아이템 관리 화면(`ItemForm` + `ItemList`) 렌더링
4. `ItemForm`에서 등록/수정 성공 시 `refreshKey`를 변경해 `ItemList`가 목록을 다시 불러오는 구조 (React 상태 끌어올리기 패턴)
5. 로그아웃 시 토큰 삭제 후 로그인 화면으로 복귀

> 💡 **학습 포인트**: `itemApi.js`는 `axios.interceptors.request.use()`를 이용해 **모든 요청에 JWT를 자동으로 붙이는 패턴**을 보여줍니다. 반면 `authApi.js`의 `fetchMyInfo`는 개별 요청에 직접 헤더를 넣는 방식이라, 두 방식의 차이를 비교해보기 좋습니다.

---

## 8. 실행 방법

### 🐍 백엔드 (로컬 실행)
```bash
cd backend
python -m venv myprj
myprj\Scripts\activate        # Windows
# source myprj/bin/activate   # macOS/Linux

pip install -r requirements.txt
uvicorn main_crud:app --reload --host 0.0.0.0 --port 8000
```
- Swagger 문서: http://localhost:8000/docs

### 🐳 백엔드 (Docker 실행)
```bash
cd backend
docker build -t fastapi-app .
docker run -p 8000:8000 fastapi-app
docker ps
```

### ⚛️ 프론트엔드
```bash
cd frontend
npm install
npm start        # http://localhost:3000
```

### ✅ 테스트
```bash
cd backend
pytest test_main.py -v
```

---

## 9. 알아두면 좋은 코드 이슈 (수업용 디버깅 포인트)

- **`crud/user_crud.py`**의 `get_user_by_email` 함수 끝에 `;`(세미콜론)이 있습니다. Python에서는 문법 오류는 아니지만 불필요한 코드이므로, 학생들에게 "왜 이게 문제가 안 되는지 / 좋은 습관은 아닌지" 질문해보기 좋습니다.
- **CORS 설정**(`main_crud.py`)이 `http://localhost:3000`만 허용하도록 되어 있어, 배포 시 실제 프론트엔드 도메인으로 변경이 필요합니다.
- **`SECRET_KEY`가 소스코드에 하드코딩**되어 있습니다 (`auth.py`). 실무에서는 `.env` 파일(`python-dotenv`)로 분리해야 하며, 현재 `.env` 파일은 비어 있어 실습용으로 채워보는 과제가 가능합니다.
- **`models.py`의 `price` 컬럼 주석**에 "원래 nullable=True/False를 써야 하는데 오타"라는 설명이 코드에 직접 남아 있어, 코드 리뷰 실습 소재로 활용할 수 있습니다.
- `test_main.py`에 들여쓰기가 어긋난 함수(`test_register_and_duplicate_email`가 `test_create_user` 내부에 중첩되어 보이는 부분)가 있어 pytest 수집 시 정상 동작하는지 직접 확인해보는 실습이 가능합니다.
- 프론트엔드는 JWT를 `localStorage`에 저장합니다. XSS 공격에 취약할 수 있다는 점을 언급하며 `httpOnly` 쿠키 방식과 비교 설명하기 좋은 포인트입니다.

---

## 10. 참고 자료
- 저장소에 포함된 `FastAPI_교안_V10.pdf`: 본 프로젝트와 함께 사용하는 수업용 교안
