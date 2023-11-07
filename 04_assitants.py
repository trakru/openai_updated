from openai import OpenAI
import os
import time
from dotenv import load_dotenv

# Initialize the OpenAI client with your API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Upload a CSV file containing email analytics data
file = client.files.create(
  file=open("email_analytics.csv", "rb"), 
  purpose='assistants'
)

# Create an assistant designed to analyze and visualize email campaign data
assistant = client.beta.assistants.create(
  name="Email Analytics Visualizer",
  description="Analyzes email campaign data from CSV files, identifies trends, and generates visualizations with summaries.",
  model="gpt-4-1106-preview",
  tools=[{"type": "code_interpreter"}],
  file_ids=[file.id]
)

# Initiate a thread asking the assistant to create visualizations based on the email data trends
thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content": "Create visualizations summarizing the key trends from the email campaign data in this file.",
      "file_ids": [file.id]
    }
  ]
)

# Start running the thread with the assistant
run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id
)

# Polling for the completion of the run
while run.status != "completed":
  print("Waiting for run to complete...")
  time.sleep(1)
  run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
  if run.status == "failed":
    print("Run failed.")
    break

# Once the run is completed, retrieve and display the results
if run.status == "completed":
    print("Run completed.")

    # Retrieve the message object that contains the results
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )

    # Print the messages that contain the visualization and analysis
    for message in messages.data:
        print("Message content: ", message.content)

    # Additional code to process and display the visualizations gors here. Not implemented yet
