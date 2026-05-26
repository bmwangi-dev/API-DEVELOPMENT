import requests

BASE_URL = "http://127.0.0.1:8000"

# Register & Login
requests.post(f"{BASE_URL}/users/register", json={"name": "test2", "email": "test2@test.com", "password": "password"})
res = requests.post(f"{BASE_URL}/users/login", json={"email": "test2@test.com", "password": "password"})
token = res.json().get("access_token")

headers = {"Authorization": f"Bearer {token}"}

# Create Habit
res = requests.post(f"{BASE_URL}/habits/", json={"title": "Drink Water"}, headers=headers)
print("Create:", res.status_code, res.text)
if res.status_code == 201:
    habit_id = res.json().get("id")

    # Read Habit
    res = requests.get(f"{BASE_URL}/habits/{habit_id}", headers=headers)
    print("Read:", res.status_code, res.text)

    # Read Habits
    res = requests.get(f"{BASE_URL}/habits/", headers=headers)
    print("Read All:", res.status_code, len(res.json()))

    # Update Habit
    res = requests.patch(f"{BASE_URL}/habits/{habit_id}", json={"completed": True}, headers=headers)
    print("Update:", res.status_code, res.text)

    # Delete Habit
    res = requests.delete(f"{BASE_URL}/habits/{habit_id}", headers=headers)
    print("Delete:", res.status_code)

