import requests
import threading
import time

def send(file_path, i):
    with open(file_path, "rb") as f:
        r = requests.post("http://localhost:8000/segment", files={"file": f})
        print(f"[{i}] {r.status_code}")

for i in range(1000):
    threading.Thread(target=send, args=("test_images/test1.jpg", i)).start()
    if i % 20 == 0:
        time.sleep(1)  # short pause to let workers breathe