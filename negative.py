import google.genai as genai
from dotenv import load_dotenv
import os

load_dotenv()

# Updated API key
API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

def fetch_review1(product_name):
    prompt = f"""
    customer review of the product '{product_name}' 
    instruction to make it as one customer negative review in 30 words just make is as a short paragraph
    instruction make it in 1 lines and don't need any heading for this
    """

    try:
        response = client.models.generate_content(
            model='models/gemini-1.5-flash',  # Fixed: add 'models/' prefix
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"Error in fetch_review1: {e}")
        return "The product quality could be improved, and the packaging was damaged upon arrival. Not worth the price."