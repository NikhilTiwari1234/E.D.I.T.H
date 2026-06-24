from dotenv import load_dotenv
import os
load_dotenv()

API_KEY= os.getenv("API_KEY")
# MODEL = "gemini-2.5-flash-lite"
# MODEL = "gemma-4-31B-it"
MODEL = "gemini-3.1-flash-lite"

LONG_TERM_MEMORY = "memory\\long_term.json"
SHORT_TERM_MEMORY = "memory\\short_term.json"
USER_PROFILE =  "memory\\user_profile.json"