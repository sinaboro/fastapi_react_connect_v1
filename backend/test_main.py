# test_main.py ← 프로젝트 루트에 생성 (인증 반영 최종본)
from fastapi.testclient import TestClient
from main import app
client = TestClient(app)
def get_token():
 # 테스트마다 매번 가입+로그인 반복 — 독립적인 테스트 보장
 client.post("/auth/register", json={
 "username": "tester1", "email": "tester1@example.com", "password":
"securepass123"
 })
 r = client.post("/auth/login", data={"username": "tester1@example.com", "password":
"securepass123"})
 return r.json()["access_token"]
def auth_headers():
 token = get_token()
 return {"Authorization": f"Bearer {token}"}
def test_create_item():
 response = client.post("/items", json={"name": "테스트 상품", "price": 10000},
headers=auth_headers())
 assert response.status_code == 201
 data = response.json()
 assert data["name"] == "테스트 상품"
 assert data["price"] == 10000
def test_create_item_without_token():
 response = client.post("/items", json={"name": "무인증 시도", "price": 1000})
 assert response.status_code == 401
def test_get_items():
 response = client.get("/items")
 assert response.status_code == 200
 assert isinstance(response.json(), list)
def test_update_item():
 headers = auth_headers()
 create_res = client.post("/items", json={"name": "원래 이름", "price": 5000},
headers=headers)
 item_id = create_res.json()["id"]
 update_res = client.put(f"/items/{item_id}", json={"name": "수정된 이름", "price":
9000}, headers=headers)
 assert update_res.status_code == 200
 assert update_res.json()["name"] == "수정된 이름"
def test_delete_item():
 headers = auth_headers()
 create_res = client.post("/items", json={"name": "삭제할 상품", "price": 1000},
headers=headers)
 item_id = create_res.json()["id"]
 del_res = client.delete(f"/items/{item_id}", headers=headers)
 assert del_res.status_code == 204
def test_item_not_found():
 response = client.get("/items/99999")
 assert response.status_code == 404
def test_create_user():
 response = client.post("/auth/register", json={
 "username": "testuser",
 "email": "test@example.com",
 "password": "securepass123"
 })
 assert response.status_code == 201
 assert "password" not in response.json() # 비밀번호 노출 X

 def test_register_and_duplicate_email():
    response = client.post("/auth/register", json={
    "username": "dupuser", "email": "dup@example.com", "password": "securepass123"
    })
    
 assert response.status_code == 201
 assert "password" not in response.json()
 dup = client.post("/auth/register", json={
 "username": "dupuser2", "email": "dup@example.com", "password": "securepass123"
 })
 assert dup.status_code == 400
def test_login_wrong_password():
 client.post("/auth/register", json={
 "username": "wronguser", "email": "wrong@example.com", "password": "correctpass1"
 })
 response = client.post("/auth/login", data={"username": "wrong@example.com",
"password": "incorrect"})
 assert response.status_code == 401
def test_get_user_not_found():
 response = client.get("/users/99999")
 assert response.status_code == 404