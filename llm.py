import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Set the OpenAI API key
openai.api_key = api_key

def generate_response(user_query):
    """
    Generate an intelligent response using OpenAI's API for chat models.
    
    Parameters:
      prompt (str): The input text.
    
    Returns:
      generated_text (str): The AI-generated response in Hindi.
    """
    try:
        prompt = f"""
        This is the user query that may be in hindi or english, as per user query you need to answer,
        User Query: {user_query}
        """
        # Make a request to OpenAI's chat-based API using gpt-3.5-turbo or gpt-4
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Or use "gpt-4" for better results
            messages=[
                {"role": "system", "content": "You are a helpful assistant that always responds in Hindi."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,  # Set a reasonable token length limit
            temperature=0.7,  # Control randomness (0 = deterministic, 1 = creative)
        )

        # Return the generated text from the chat-based model
        return response['choices'][0]['message']['content']

    except Exception as e:
        raise Exception(f"Error generating response: {e}")

# Example usage
if __name__ == "__main__":
    prompt = "hi"
    response = generate_response(prompt)
    print("AI Response:", response)
