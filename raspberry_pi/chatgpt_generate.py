import requests
import json
import time

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

quotemap = {}

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


def generateQuoteMapForEmotion(emotion):
    try:
        quotemap[emotion] = []
        for i in range(5):
            quote = prompt(f"Generate a inspiration quote, my current emotional state is {emotion}. Make it starwars themed", "gpt-3.5-turbo")
            quotemap[emotion].append(quote)
            print(f"Generated quote \"{i}\" for {emotion}")
    except:
        f = open("quotemap.json", "w")
        f.write(json.dumps(quotemap, indent=4))
        f.close()
        exit()

    f = open("quotemap.json", "w")
    f.write(json.dumps(quotemap, indent=4))
    f.close()

generateQuoteMapForEmotion("angry")
generateQuoteMapForEmotion("disgust")
print("Finished the first two :)")
generateQuoteMapForEmotion("fear")
generateQuoteMapForEmotion("happy")
print("Finished the first two :)")
generateQuoteMapForEmotion("sad")
generateQuoteMapForEmotion("surprise")
print("Finished the first two :)")
generateQuoteMapForEmotion("neutral")

print("Done!")