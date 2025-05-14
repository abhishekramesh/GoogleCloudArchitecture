import requests
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env

url = 'https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent'
headers = {
    'x-rapidapi-key': os.getenv('RAPIDAPI_KEY'),
    'x-rapidapi-host': 'cricbuzz-cricket.p.rapidapi.com'
}

response = requests.get(url, headers=headers)
print(response.json())