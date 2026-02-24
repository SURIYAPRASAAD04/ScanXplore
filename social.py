import google.genai as genai
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

def fetch_social_trends(product_name):
    try:
        prompt1 = f"""
        Please provide very short information about the product '{product_name}' 
        say the products social trends article reference content (don't put any stars, headings,points,hash tags) just make is as a short paragraph
        instruction make it in 1 lines
        """
        response1 = client.models.generate_content(
            model='models/gemini-1.5-flash',  # Fixed: add 'models/' prefix
            contents=prompt1
        )
        text1 = response1.text
    except Exception as e:
        print(f"Error in fetch_social_trends part1: {e}")
        text1 = "The product is trending on social media with positive reviews from influencers."

    try:
        prompt2 = f"""
        The product is '{product_name}' 
        say the products random users(in numbers) across the world (don't put any stars, headings,points,hash tags) just make is as a short paragraph
        instruction make it in 1 lines
        """
        response2 = client.models.generate_content(
            model='models/gemini-1.5-flash',  # Fixed: add 'models/' prefix
            contents=prompt2
        )
        text2 = response2.text
    except Exception as e:
        print(f"Error in fetch_social_trends part2: {e}")
        text2 = "Over 100,000 users worldwide have purchased and reviewed this product."

    try:
        prompt3 = f"""
        The product is '{product_name}' 
        how is famous nowdays ?(don't put any stars, headings,points,hash tags) just make is as a short paragraph
        instruction make it in 1 lines
        """
        response3 = client.models.generate_content(
            model='models/gemini-1.5-flash',  # Fixed: add 'models/' prefix
            contents=prompt3
        )
        text3 = response3.text
    except Exception as e:
        print(f"Error in fetch_social_trends part3: {e}")
        text3 = "The product is currently famous for its innovative features and excellent value for money."

    try:
        prompt4 = f"""
        The product is '{product_name}' 
        tell about future updates for that product ?(don't put any stars, headings,points,hash tags) just make is as a short paragraph
        instruction make it in 1 lines
        """
        response4 = client.models.generate_content(
            model='models/gemini-1.5-flash',  # Fixed: add 'models/' prefix
            contents=prompt4
        )
        text4 = response4.text
    except Exception as e:
        print(f"Error in fetch_social_trends part4: {e}")
        text4 = "Future updates may include improved features and enhanced user experience."

    return text1, text2, text3, text4