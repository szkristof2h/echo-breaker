from fastapi import FastAPI, Security, HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader, APIKey
from openai import OpenAI, OpenAIError
from pydantic import BaseModel
from starlette.status import HTTP_401_UNAUTHORIZED
import os

client = OpenAI()

app = FastAPI()

API_KEY = os.environ['ECHO_API_KEY']
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def authenticate(api_key: str = Security(api_key_header)):
  if (API_KEY != api_key):
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Missing or invalid API key")

def generate(text):
  try:
    suggestion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
        {"role": "user", "content": text}
    ])

    return suggestion.choices[0].message
  except OpenAIError as e:
    print(f"Error: {e}")
    return "No suggestions"

class Echo(BaseModel):
  text: str

@app.get("/")
async def root(api_key: APIKey = Depends(authenticate)):
  return {"greeting": "Hello, World!", "message": "Welcome to FastAPI!"}

@app.post("/suggestion")
def create_suggestion(echo: Echo, api_key: APIKey = Depends(authenticate)):
  suggestion = generate(echo.text)
  return {"suggestion": suggestion}