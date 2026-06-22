from dotenv import load_dotenv
import os
load_dotenv()

API_KEY= os.getenv("API_KEY")
MODEL = "gemini-2.5-flash-lite"