import google.generativeai as genai
import os

if "GEMINI_API_KEY" not in os.environ:
    raise EnvironmentError("GEMINI_API_KEY is not set in the environment variables.")

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

generation_config = {
  "temperature": 0.2,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 40,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction="Context: \nYou summarize the user's news preferences. The user tells you what topics they are interested in. Your job is to understand these topics and condense them into 3 or fewer.\n\nSteps:\n1. Identify the topics the user is interested in.\n2. If there are more than 3 topics, combine them into 3 or fewer.\n3. Write the topics clearly, keeping the original meaning.\n\nOutput format:\nEach topic should be 3 words or less. Topics should be written in lowercase, separated by 'AND', 'AND NOT', or 'OR' depending on the user's request.\n\nExample output:\ntechnology AND NOT war OR politics\n\nIMPORTANT:\nIf you can't identify a topic, write: 'no topic'.\nIf the topics have different meanings, separate them with 'OR'.\n"
)
