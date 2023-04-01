import requests
import json

f = open(".env", "r")
lines = f.readlines()
f.close()

# Load Environment Variables
env = {}
for line in lines:
    line = line.strip()
    if line.startswith("#"):
        continue
    key, value = line.split("=")
    env[key.strip()] = value.strip()

def prompt(text, model):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + env["OPENAI_TOKEN"],
        "OpenAI-Organization": env["OPENAI_ORG_ID"]
    }
    data = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": text
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    json = response.json()
    if json["object"] != "chat.completion":
        return "Error"
    return json["choices"][0]["message"]["content"]


# Print the response
print(prompt("What is 3 + 3?", "gpt-3.5-turbo"))