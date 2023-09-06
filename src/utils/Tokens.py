import os
from dotenv import load_dotenv

# Load environment variables from a .env file (containing OPENAI_API_KEY)
load_dotenv()

apikey = os.environ.get("OPENAI_API_KEY")
