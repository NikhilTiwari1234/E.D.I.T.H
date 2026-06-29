from brain.ai_engine import SendPrompt,sendScreen,sendmessage
import brain.memory_engine 
import time

def run():
    # createDB()
    # sessionHistory = []
    start=time.time()
    while True:
        t1 = time.time()
        prompt = input("ASK: ").strip()
        print("input time",time.time() - t1)
        if prompt.lower() == "quit":
            t2 = time.time()
            prompt = "You are a memory extraction system for an AI agent." \
            "recall our full conversation in this session." \
            "Your job is to analyze our full conversation so far and extract only durable, useful long-term memories that may help in future conversations" \
            "Rules:" \
            "    - Store only facts likely useful in future conversations." \
            "    - Ignore temporary details unless they matter long-term." \
            "    - Avoid storing trivial chit-chat." \
            "    - Separate factual memory from preferences and goals." \
            "    - If uncertain, do not store." \
            "Return only JSON:" \
            "{" \
            "memories: [" \
            "    {" \
            "    document: concise memory statement," \
            "    metadata: {" \
            "        type: identity | preference | goal | project | relationship | skill | habit | context | episodic," \
            "        importance: 1-10," \
            "        confidence: 0-1," \
            "        validity: permanent | long_term | short_term," \
            "        tags: [tag1, tag2]" \
            "    }" \
            "    }" \
            "]" \
            "}"
            memory = sendmessage(prompt)
            print("extraction time",time.time() - t2)
            t3 = time.time()
            brain.memory_engine.updateLongTermMemory(memory)
            print("memory update time",time.time() - t3)
            break
        # reply = SendPrompt(prompt,sessionHistory[len(sessionHistory)-10:])
        # sessionHistory = updateHistory(sessionHistory,prompt,reply)

        t4 = time.time()
        retrieved_memory=brain.memory_engine.retrieveMemory(prompt)
        prompt=f"""
        Relevent memories:
        {retrieved_memory}

        user query:
        {prompt}
        """
        sendmessage(prompt,stream=True)
        print("reply time",time.time() - t4)
    print(memory)