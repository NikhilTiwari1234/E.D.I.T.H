from brain.ai_engine import SendPrompt,sendScreen,sendmessage
from brain.memory_engine import createDB,updateHistory

def run():
    # createDB()
    # sessionHistory = []
    
    while True:
        prompt = input("ASK: ").strip()
        if prompt.lower() == "quit":
            break
        # reply = SendPrompt(prompt,sessionHistory[len(sessionHistory)-10:])
        # sessionHistory = updateHistory(sessionHistory,prompt,reply)

        reply = sendmessage(prompt)

        print("AI's reply:"+reply)