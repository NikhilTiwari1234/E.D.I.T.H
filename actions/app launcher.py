import subprocess
import os
import json
try:
    from rapidfuzz import fuzz
except ImportError:
    print("Install rapidfuzz: pip install rapidfuzz")
    exit()


def getAppsList():
    result = subprocess.run(
        ["powershell","-Command","Get-StartApps | Sort-Object Name | ConvertTo-Json -Depth 3 | Set-Content -Path AppsList.json -Encoding UTF8"],
        text=True
    )

    if result.returncode != 0:
        print("Failed to create app list")
        exit()
    print("Apps list created")

def normalize(text):
    text=text.lower()
    clean = ''.join(char for char in text if char.isalnum() or char == ' ')
    return clean

def generateAliases():
    for app in appList:
        text = app["Name"]
        words = text.split()

        combinations = set()

        for i in range(len(words)):
            for j in range(i + 1, len(words) + 1):
                combinations.add(normalize(" ".join(words[i:j])))
        

        for i in range(len(words)):
            prefix = ''.join(word[0] for word in words[:i+1])
            suffix = words[i+1:]

            if suffix:
                combinations.add(normalize(prefix + " " + " ".join(suffix)))
            else:
                combinations.add(normalize(prefix))

        app["Aliases"]=list(combinations)
    
    with open("AppsList.json", "w", encoding="utf-8") as f:
        json.dump(appList, f, indent=4)

def find_name(alias):
    for item in appList:
        if alias in item["Aliases"]:
            return item["AppID"]
    return None

def fuzzyMatch(key):
    bestMatch = None
    bestScore = 0

    for app in appList:
        for alias in app["Aliases"]:
            score = fuzz.ratio(key,alias)

            if score > bestScore:
                bestScore = score
                bestMatch = app["AppID"]
                # bestMatch = {
                #     "matched_alias":alias,
                #     "score":score,
                #     "app" : app
                # }
    if bestScore < 60:
        return None
    return bestMatch

def run(app):
    command = f"explorer \"shell:AppsFolder\\{app}\""
    subprocess.run(
        ["powershell","-Command",command],
        text=True
    )


if not os.path.exists("AppsList.json"):
    getAppsList()
    
with open("AppsList.json","r", encoding="utf-8-sig") as f:
    appList = json.load(f)
    if isinstance(appList, dict):
        appList = [appList]

if not all("Aliases" in app for app in appList):
    generateAliases()

print("Welcome to app launcher")
print("-"*20)
print("(Command should be in format \"open Appname\")")
command = input().strip().split(" ",1)
if command[0].lower() != "open":
    print("Invalid command")
    exit()
if len(command) < 2:
    print("Error: app name not specified")
    exit()

app=normalize(command[1])
match = find_name(app)

if(match==None):
    match = fuzzyMatch(app)
    if match is None:
        print("App not found")
        exit()


run(match)