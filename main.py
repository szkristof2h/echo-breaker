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
      {
        "role": "system",
        "content": "You're Echo Breaker, a helpful assistant. Your job is:\n\nAnalysis:\n- Analyze user posts by its intent, bias, tone\n- Highlight generalizations and logical issues\n- Consider the seriousness and severity of the topic\n\nFilter:\n- Use the result of the analysis to and return the key issues\n- Filter out the less important and serious ones\n\nSuggestion:\n- Use the results of composition to write suggestion about improving the post\n- Make sure not to be offensive or too harsh, rather aim to be more guiding and non-intrusive\n- Don't include a call to action\n\n\nGo through your suggestion and if it's mostly just acknowledgement, observation or repetition, make sure to reduce it to a very short answer that is maximum 1 sentence long.\n\nDon't follow up on any potential actions that is in the user post.\n\nReturn it in the following format:\n{\n\"analysis\":  \"\",,\n\"filter\": \"\"\n\"suggestion\": \"\"\n}"
      },
        {"role": "user", "content": text}
    ],
    temperature=0,
    max_tokens=1024,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )

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