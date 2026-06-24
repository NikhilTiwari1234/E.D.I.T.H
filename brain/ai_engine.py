import config
from google import genai
from google.genai import types
import pyautogui
import io

client=genai.Client(api_key=config.API_KEY)

chat = client.chats.create(model=config.MODEL)
def sendmessage(prompt):
    response = chat.send_message(prompt)
    return response.text

def SendPrompt(prompt,history):
    content = history + [
        {"user:"+prompt}
    ]
    response = client.models.generate_content(
        model=config.MODEL, contents=content
    )
    return response.text

def sendScreen():
    currentScreen= pyautogui.screenshot()
    
    img_byte_arr = io.BytesIO()
    currentScreen.save(img_byte_arr,format='PNG')
    img_bytes=img_byte_arr.getvalue()
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite", 
        contents=[
            types.Part.from_text(text='Analyze this image and tell' \
                '1.Which application is open?' \
                '2. What is user doing?' \
                '3. is there any mistake, and if yes than what can be solution or right approach? if no then return only \"no\" ' \
                'Answer these questions in max 2 line for each'),
            types.Part.from_bytes(
                data=img_bytes,
                mime_type='image/png',
            )
        ]
    )
    return response