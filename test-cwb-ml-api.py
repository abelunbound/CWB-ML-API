
import requests

url = 'https://us-central1-com-726-project.cloudfunctions.net/run-ml-model'
# https://us-central1-com-726-project.cloudfunctions.net/run-ml-model

data = {
    'applicant_id': 912345678,
    'required_amount': 14000
}

# Include the authentication token in the request header
# auth_token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImQ5NzQwYTcwYjA5NzJkY2NmNzVmYTg4YmM1MjliZDE2YTMwNTczYmQiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIzMjU1NTk0MDU1OS5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsImF1ZCI6IjMyNTU1OTQwNTU5LmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTA2MDEzOTE0OTkwODE3NTc0OTkxIiwiZW1haWwiOiJhYmVsYWtlbmlAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF0X2hhc2giOiJYeXphZ2Vndk02aDVNNW1fZXdXcmJnIiwiaWF0IjoxNzMyMDY0NTgxLCJleHAiOjE3MzIwNjgxODF9.nOy7Vio_J0u4_abc_tcLv9jo7CS3tpXJWueGy1zTqTbpTBd3LvaLq0nJAlBYDZJYG0teg0zd9mGAWiOp8rDVm331s9dabAbJNlg70bmQ3-gBvUzVAdz1V5TkKAxFUQfxrj_NfQ-p7PoK-bzmIAJKe6rsRTzlnCYxgsQKUkfxYtC0zd53evB9sH5fHI4z16cEoas-UVK_mDDeZaS0Lb545iyEcmM-0ht6sa7sontyWH8LBgeboXhgpAaoHtNCc-UZQqfBNpVD133gkyPR9xkjT9xtBQvH9RGBlU2jjLkldfZfDzYz86QtdFp0NShIglA4917JUEL3cQJ54o5BmJkh-A'  # Replace with your token

headers = {
    # 'Authorization': f'Bearer {auth_token}',
    'Content-Type': 'application/json'
}

# Make the POST request with headers
# response = requests.post(url, json=data, headers=headers)

response = requests.post(url, json=data, headers=headers)
print("Status Code:", response.status_code)
print("Response Text:", response.text)  # Print the raw response text !!! Very impoportant!

print("Status Code:", response.status_code)
print(response.json())