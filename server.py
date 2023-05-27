from flask import Flask, json
import openai
import queue
import subprocess
import threading

openai.api_key = "INSERT_KEY_HERE"

prompt_to_inject = None
prompt_queue = queue.Queue()
command_queue = queue.Queue()

with open("System.MD") as file:
    prompt_to_inject = file.read()

api = Flask("assistant_server")

def run_command(cmd):
    r = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE) # Grab the output of the command
    r.wait()
    return r

def run_prompt(systemPrompt, userPrompt, model): # The prompt, the OpenAI model to use, e.g gpt-3.5-turbo or davinci
        completion = openai.ChatCompletion.create(
            model=model, # Latest GPT model
            messages=[{"role": "system", "content": systemPrompt}, {"role": "user", "content": userPrompt}]
        )

        return completion

conversation_history = ""

def process_command_queue():
    global prompt_to_inject
    global conversation_history
    while True:
        try:
            cmd = command_queue.get(block=False)
            cmd_run = run_command(cmd)
            if (cmd_run != "Command cancelled by user"):
                output = cmd_run.stdout.read().decode() # stdout
                stderr = cmd_run.stderr

                print("[DEBUG] Output: ", output)
                if (output):
                    prompt_to_inject = prompt_queue.get()
                    if (cmd_run.returncode != 0):
                        conversation_history += "\n" + "[INTERNAL] Do not show to user: Return code of command is not zero."
                    elif stderr:
                        conversation_history += "\n" + "[INTERNAL] Do not show to user: Command returned error: " + stderr.read().decode()
                    elif output:
                        conversation_history += "\n" + "[INTERNAL] Do not show to user: Command returned output: " + output
                    else:
                        conversation_history += "\n" + "[INTERNAL] Do not show to user: Command produced no output or error."  
    
                print("[DEBUG] Running completion")
            else:
                conversation_history += "\n" + "[INTERNAL] Do not show to user: Command cancelled by user"
            completion = run_prompt(prompt_to_inject, conversation_history + "\n" + "Fiosa: ", "gpt-3.5-turbo")
            print("Response: " + completion.choices[0].message.content)

        except queue.Empty:
            break

def send_message(message):
    global conversation_history

    conversation_history = conversation_history + "User: " + message + "\n"
    r = run_prompt(prompt_to_inject, conversation_history, "gpt-3.5-turbo")
    return r.choices[0].message.content

fmt_start_tag = "%[message]"
fmt_end_tag = "\n"
fmt_cmd_tag = "%[command]"
fmt_cmd_elev_tag = "%[command_elev]"

@api.route('/postrequest/<query>', methods=['GET'])
def post_req(query):
    global conversation_history

    val = send_message(query)

    print(val)

    conversation_history += "Fiosa: " + val + "\n"

    start_index = val.find(fmt_start_tag)
    end_index = val.find(fmt_end_tag, start_index + len(fmt_start_tag) + 1)

    print("start_index: " + str(start_index))
    print("start index value: " + val[start_index])
    print("end_index: " + str(end_index))
    print("end index value: " + val[end_index])


    msg = val[start_index:end_index].strip()
    msg = msg[len(fmt_start_tag) + 1:]

    print(msg)

    if (val.find(fmt_cmd_tag) > -1 or val.find(fmt_cmd_elev_tag) > -1):
        print("Contains command!")

        



    
    return json.dumps({"val": msg}), 200


api.run(port=4999)
