import os
from dotenv import load_dotenv
import google.generativeai as genai

def get_university_info(uni_name):
    # Load environment variables from the .env file
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

    # Get the API key
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

    if not GOOGLE_API_KEY:
        raise ValueError("API key not found. Please set the GOOGLE_API_KEY environment variable.")

    # Configure the generative AI client
    genai.configure(api_key=GOOGLE_API_KEY)

    # Define the system instruction
    instruction = (
        "You are a knowledgeable guide for international students applying as a first-year to universities in different countries. "
        "Provide a brief and laconic description (100 words) of the university, and an official university admissions website if possible. "
        "Your text should be HTML content."
    )

    # Initialize the model with the system instruction
    model = genai.GenerativeModel(
        "models/gemini-1.5-flash", system_instruction=instruction
    )

    # Generate content using the model
    response = model.generate_content(f"Tell me about applying to {uni_name}.")
    
    # Return the generated content
    return response.text

