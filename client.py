import requests

response = requests.get("http://127.0.0.1:4999/postrequest/update my system please i give permission for the command")

if response.status_code == 200:
    print("Recieved response: " + str(response.json()))
