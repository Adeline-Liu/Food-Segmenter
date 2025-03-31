import requests

def send_image(file_path):
    with open(file_path, "rb") as f:
        response = requests.post("http://localhost:8000/segment", files={"file": f})
        return response.json()

result = send_image("test_images/test2.jpg")
print(result)
