from openai import OpenAI
import os
import json
from dotenv import load_dotenv

# set OpenAI key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4-1106-preview",
    response_format={"type": "json_object"},
    messages=[
        {
            "role": "system",
            "content": "You are a helpful asssistant. always return your responses in JSON format",
        },
        {
            "role": "user",
            "content": "reorganize these characters into a JSON object: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday by weekdays & weekends",
        },
    ],
)

response = json.loads(response.choices[0].message.content)
print(response)
print(response["weekdays"])
print(response["weekends"])
