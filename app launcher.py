import subprocess
import os
import json

def getAppsList():
    subprocess.run(
        ["powershell","-Command","Get-StartApps | Sort-Object Name | ConvertTo-Json -Depth 3 | Set-Content -Path AppsList.json -Encoding UTF8"],
        text=True
    )
    print("Apps list created")

def normalize(text):
    text=text.lower()
    clean = ''.join(char for char in text if char.isalpha() or char == ' ')
    return clean

def generateAliases():
    with open("AppsList.json","r", encoding="utf-8-sig") as f:
        appList = json.load(f)
    for app in appList:
        text = app["Name"]
        words = text.split()

        combinations = []

        for i in range(len(words)):
            for j in range(i + 1, len(words) + 1):
                combinations.append(" ".join(words[i:j]).lower())
        

        for i in range(len(words)):
            prefix = ''.join(word[0] for word in words[:i+1])
            suffix = words[i+1:]

            if suffix:
                combinations.append(prefix.lower() + " " + " ".join(suffix).lower())
            else:
                combinations.append(prefix.lower())

        app["Aliases"]=combinations
    
    with open("AppsList.json", "w", encoding="utf-8") as f:
        json.dump(appList, f, indent=4)

def find_name(alias):
    with open("AppsList.json","r", encoding="utf-8-sig") as f:
        appList = json.load(f)
    for item in appList:
        if alias in item["Aliases"]:
            return item["Name"]
    return None





if not os.path.exists("AppsList.json"):
    getAppsList()
    generateAliases()

print("Welcome to app launcher")
print("-"*20)
print("(Command should be in format \"open Appname\")")
command = input().split(" ",1)
app=normalize(command[1])
print(app)
print(find_name(app))
# agar find name none return kare to fuzzy match use karna he varna run karna he
