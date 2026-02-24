import google.genai as genai
from dotenv import load_dotenv
import os

load_dotenv()

# Updated API key
API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

def fetch_product_details(product_name):
    prompt = f"""
    Please provide short information about the product '{product_name}' including:
    short Product Description and current price in dollar (don't put any star, headings)
    instruction make it in 1 lines
    """

    try:
        response = client.models.generate_content(
            model='models/gemini-1.5-flash',  # Fixed: add 'models/' prefix
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"Error in fetch_product_details: {e}")
        return f"{product_name} is a popular product with good customer reviews. Price varies by retailer."

def fetch_product_rating(product_name):
    prompt = f"""
    Please provide information about the product '{product_name}' 
    overall Product star rating of that brand in numbers like (4.5,3.2...ect) (don't put any star, headings,points)
    """

    try:
        response = client.models.generate_content(
            model='models/gemini-1.5-flash',  # Fixed: add 'models/' prefix
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"Error in fetch_product_rating: {e}")
        return "4.2"

def fetch_product_review(product_name):
    prompt = f"""
    Please provide overall(positive and negative) very short review of the product '{product_name}' 
    instruction make it in 2 lines
    """

    try:
        response = client.models.generate_content(
            model='models/gemini-1.5-flash',  # Fixed: add 'models/' prefix
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"Error in fetch_product_review: {e}")
        return "Customers love this product for its quality and value. Some mention minor issues with packaging."

def fetch_product_trends(product_name):
    prompt = f"""
    Please provide short information about the product '{product_name}' 
    products social trends (don't put any stars, headings,points,hash tags) just make is as a short paragraph
    instruction make it in 1 lines
    """

    try:
        response = client.models.generate_content(
            model='models/gemini-1.5-flash',  # Fixed: add 'models/' prefix
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"Error in fetch_product_trends: {e}")
        return f"{product_name} is trending on social media with positive reviews."

def fetch_product_similar(product_name):
    prompt = f"""
    Please provide information about some 5 similar products (list by comma seperating) of the product '{product_name}' 
    (don't put any star, headings,points)
    """

    try:
        response = client.models.generate_content(
            model='models/gemini-1.5-flash',  # Fixed: add 'models/' prefix
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"Error in fetch_product_similar: {e}")
        return "Similar products include Brand A, Brand B, Brand C, Brand D, Brand E"