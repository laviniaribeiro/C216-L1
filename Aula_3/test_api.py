import requests

base_url = "http://localhost:8000"

def test_get_root():
    response = requests.get(f"{base_url}/")
    print(f"GET /: {response.status_code} - {response.json()}")

def test_get_hello_query():
    response = requests.get(f"{base_url}/api/v1/hello?name=João")
    print(f"GET /api/v1/hello?name=João: {response.status_code} - {response.json()}")

def test_get_hello_path():
    response = requests.get(f"{base_url}/api/v1/hello/João")
    print(f"GET /api/v1/hello/João: {response.status_code} - {response.json()}")

def test_post_hello():
    data = {"name": "João"}
    response = requests.post(f"{base_url}/api/v1/hello", json=data)
    print(f"POST /api/v1/hello: {response.status_code} - {response.json()}")

def test_put_update():
    data = {"name": "João"}
    response = requests.put(f"{base_url}/api/v1/update", json=data)
    print(f"PUT /api/v1/update: {response.status_code} - {response.json()}")

def test_delete_user():
    response = requests.delete(f"{base_url}/api/v1/delete?name=João")
    print(f"DELETE /api/v1/delete?name=João: {response.status_code} - {response.json()}")

def test_patch_user():
    data = {"name": "João"}
    response = requests.patch(f"{base_url}/api/v1/patch", json=data)
    print(f"PATCH /api/v1/patch: {response.status_code} - {response.json()}")

if __name__ == "__main__":
    test_get_root()
    test_get_hello_query()
    test_get_hello_path()
    test_post_hello()
    test_put_update()
    test_delete_user()
    test_patch_user()