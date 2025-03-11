import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file

openai.api_key = os.getenv("OPENAI_API_KEY")
