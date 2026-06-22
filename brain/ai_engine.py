import config
from google import genai

def SendPrompt():
    client=genai.Client(api_key=config.API_KEY)

    prompt = input("ASK: ")
    response = client.models.generate_content(
        model=config.MODEL, contents=prompt
    )
    print("AI's response : "+response.text)