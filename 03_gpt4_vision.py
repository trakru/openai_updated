from openai import OpenAI
import os
from dotenv import load_dotenv

# set OpenAI key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Making a request to the OpenAI API to process an image
response = client.chat.completions.create(
    model="gpt-4-vision-preview",  # Specify the model that can process images
    stream=True,  # Use streaming to get a real-time response
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What’s in this image?"},  # User's request to analyze an image
                {
                    "type": "image_url",
                    "image_url": r"https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Cambados-Ruinas_de_Santa_Mari%C3%B1a03_%2810610795003%29.jpg/1920px-Cambados-Ruinas_de_Santa_Mari%C3%B1a03_%2810610795003%29.jpg",  # Replace with the new image URL
                },
            ],
        }
    ],
    max_tokens=300,  # Define the limit of the response length
)

# Initialize a variable to accumulate the responses
responses = ''

# Iterate over each chunk of the response as it streams in
for chunk in response:
    # Uncomment this to print all chunk objects (for debugging)
    # print(chunk)
    
    # Check if the current chunk has content and append it to the 'responses'
    if chunk.choices[0].delta.content: 
        text_chunk = chunk.choices[0].delta.content 
        print(text_chunk, end="", flush=True)  # Print the text part of the response
        responses += str(text_chunk)  # Accumulate the text parts into one string

# If not streaming, you would handle the response like this:
# print(response.choices[0].message.content)
