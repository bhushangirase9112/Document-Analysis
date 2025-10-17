
## 1. Upload a PDF or TXT File


# import requests

# url = "http://127.0.0.1:8000/upload"
# file_path = r"C:\Users\Admin\Documents\GitHub\Document-Analysis\sample_document.txt"  # Change to your file path

# with open(file_path, "rb") as f:
#     files = {"file": (file_path, f, "application/pdf")}
#     response = requests.post(url, files=files)

# print("Status code:", response.status_code)
# print("Response:", response.json())

# # Save job_id for next steps
# job_id = response.json().get("job_id")






## 2. Start Analysis on Uploaded Document
# import requests

# url = "http://127.0.0.1:8000/analyze"
# job_id = "4dd8df7c-bca7-4afb-a0b8-90a760676a13"  # Use the job_id from the upload response

# payload = {"job_id": job_id}
# response = requests.post(url, json=payload)

# print("Status code:", response.status_code)
# print("Response:", response.json())




## 3. Get Analysis Results
import requests
import time

job_id = "4dd8df7c-bca7-4afb-a0b8-90a760676a13"  # Use the job_id from previous steps
url = f"http://127.0.0.1:8000/results/{job_id}"

# Wait a few seconds if analysis is asynchronous
for _ in range(5):
    response = requests.get(url)
    print("Status code:", response.status_code)
    print("Response:", response.json())
    if response.json().get("status") == "completed":
        break
    time.sleep(2)