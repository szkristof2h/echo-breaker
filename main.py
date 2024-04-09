from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()

app = FastAPI()

class Echo(BaseModel):
    text: str

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

@app.get("/")
def read_root():
    return {"Hello": "there"}

@app.post("/suggestion")
def create_suggestion(echo_text: Echo):
  suggestion = generate(echo_text.text)
  return {"suggestion": suggestion}