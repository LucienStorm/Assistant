import requests

while True:
    command = input("Command: ")
    if (command == "exit"):
        break
    response = requests.get("http://127.0.0.1:4999/postrequest/" + command)
    if response.status_code == 200:
        if (response.json()['commandExecution']):
            print("--> Executing command `" + response.json()['commandExecution'] + "`")
        print("Recieved response: " + str(response.json()['val']))
    else:
        print("Uh oh. Fiosa didn't reply. This could be due to an error in the server component or with the OpenAI services.")