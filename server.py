from flask import Flask, json
import openai
import subprocess
import threading

openai.api_key = "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"

def get_tag_contents(str, start_tag, end_tag):
    msg = ""

    start_index = str.find(start_tag)
    end_index = str.find(end_tag, start_index + len(start_tag) + 1)

    msg = str[start_index:end_index].strip()
    msg = msg[len(start_tag) + 1:]

    return msg

prompt_to_inject = None

with open("System.MD") as file:
    prompt_to_inject = file.read()

api = Flask("assistant_server")

def run_command(cmd):
    r = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE) # Grab the output of the command
    r.wait()
    o = ""
    if (r.stderr):
        o = "System: Command failed. stderr: " + r.stderr
    elif (r.stdin):
        o = "System: Command succeeded. Output: " + r.stdin
    
    if (not o):
        return ""
    return run_prompt(prompt_to_inject, conversation_history + "Fiosa: ", "gpt-3.5-turbo").choices[0].message.content

def run_prompt(systemPrompt, userPrompt, model): # The prompt, the OpenAI model to use, e.g gpt-3.5-turbo or davinci
        completion = openai.ChatCompletion.create(
            model=model, # Latest GPT model
            messages=[{"role": "system", "content": systemPrompt}, {"role": "user", "content": userPrompt}]
        )

        return completion

conversation_history = ""

def send_message(message):
    global conversation_history

    conversation_history = conversation_history + "User: " + message + "\n"
    r = run_prompt(prompt_to_inject, conversation_history + "Fiosa: ", "gpt-3.5-turbo")
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

    msg = get_tag_contents(val, fmt_start_tag, fmt_end_tag)

    print(msg)
    
    cmd = ""
    
    if (val.find(fmt_cmd_elev_tag) > -1):
        print("Contains elevated command!")
        cmd = get_tag_contents(val, fmt_cmd_elev_tag, fmt_end_tag)

        p = run_command("pkexec " + cmd)
        conversation_history += p

    elif (val.find(fmt_cmd_tag) > -1):
        print("Contains command!")
        cmd = get_tag_contents(val, fmt_cmd_tag, fmt_end_tag)
        
        p = run_command(cmd)
        conversation_history += p



        



    
    return json.dumps({"val": msg, "commandExecution": cmd}), 200


api.run(port=4999)
