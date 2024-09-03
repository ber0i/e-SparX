import requests


def register(name: str, description: str):
    response = requests.post(
        "http://localhost:8080/register",
        json={"name": name, "description": description},
    )
    if response.status_code == 200:
        print("Entry registered successfully", response.json())
    else:
        print("Failed to register entry:", response.text)
