import requests
import time

BASE_URL = "http://127.0.0.1:8000"

# 1. Register
res = requests.post(f"{BASE_URL}/users/register", json={
    "name": "test", "email": "test@test.com", "password": "StrongP1"
})
print("Register:", res.status_code)

# 2. Login
res = requests.post(f"{BASE_URL}/users/login", json={
    "email": "test@test.com", "password": "StrongP1"
})
print("Login:", res.status_code)
token = res.json().get("access_token")
print("Token:", token)

# 3. Get Me
res = requests.get(f"{BASE_URL}/users/me", headers={"Authorization": f"Bearer {token}"})
print("Get Me:", res.status_code)

# 4. Delete Me
res = requests.delete(f"{BASE_URL}/users/me", headers={"Authorization": f"Bearer {token}"})
print("Delete Me:", res.status_code)

