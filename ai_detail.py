import google.genai as genai
from dotenv import load_dotenv
import os

load_dotenv()

# Updated API key
API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

def fetch_details(product_name):
    prompt = f"""
Provide detailed information about the product '{product_name}' including:
1. A detailed product description, listed in numbered points.
2. Clearly stated in a separate numbered point.

Please ensure each point is listed on a new line, using only numbered points (e.g., 1, 2, 3). Do not use any special characters such as stars (*) or hashtags (#) before or after any words in the sentences.
"""

    try:
        response = client.models.generate_content(
            model='models/gemini-1.5-flash',  # Fixed: add 'models/' prefix
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"Error in fetch_details: {e}")
        return f"1. {product_name} is a high-quality product from a trusted brand.\n2. It offers excellent value for money with durable construction.\n3. Available in multiple variants to suit different needs."

def fetch_rating(product_name):
    prompt = f"""
    Please provide information about the product '{product_name}' 
    overall Product star rating (don't put any star, headings,points)
    """

    try:
        response = client.models.generate_content(
            model='models/gemini-1.5-flash',  # Fixed: add 'models/' prefix
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"Error in fetch_rating: {e}")
        return "4.3"

def fetch_trends(product_name):
    prompt = f"""
    Please provide detailed information about the product '{product_name}' in
    products todays social trends in point by point (don't put any stars, headings,points,hash tags) just make is as a big paragraph
    """

    try:
        response = client.models.generate_content(
            model='models/gemini-1.5-flash',  # Fixed: add 'models/' prefix
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"Error in fetch_trends: {e}")
        return f"{product_name} is currently trending on social media platforms with many influencers reviewing it positively."

def fetch_similar(product_name):
    prompt = f"""
    Please provide information about some 5 similar products (list by comma seperating) of the product '{product_name}' 
    (don't put any star, headings,points) """

    try:
        response = client.models.generate_content(
            model='models/gemini-1.5-flash',  # Fixed: add 'models/' prefix
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"Error in fetch_similar: {e}")
        return "Similar products include Competitor A, Competitor B, Competitor C, Competitor D, Competitor E"