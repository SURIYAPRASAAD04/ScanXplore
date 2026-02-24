from flask import Flask, render_template, jsonify, request, session, redirect, url_for, send_from_directory
import os
import time
import requests
import feedparser
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# External modules
from social import fetch_social_trends 
from shopping import main
from ai import fetch_product_details, fetch_product_rating, fetch_product_review, fetch_product_trends, fetch_product_similar
from ai_detail import fetch_details, fetch_similar
from negative import fetch_review1
from review import fetch_review
from youtube import fetch_youtube_videos

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "fallback-secret-key")

# ==========================
# SAFE API INITIALIZATION
# ==========================

# Cohere Safe Init
co = None
try:
    import cohere
    cohere_api_key = os.getenv("COHERE_API_KEY")
    if cohere_api_key:
        co = cohere.Client(cohere_api_key)
        print("Cohere initialized successfully")
    else:
        print("Cohere API key missing")
except Exception as e:
    print(f"Cohere initialization failed: {e}")
    co = None


# Roboflow Safe Init
model = None
try:
    from roboflow import Roboflow
    roboflow_key = os.getenv("ROBOFLOW_API_KEY")
    if roboflow_key:
        rf = Roboflow(api_key=roboflow_key)
        project = rf.workspace().project("obj-k7ktz")
        model = project.version("1").model
        print("Roboflow initialized successfully")
    else:
        print("Roboflow API key missing")
except Exception as e:
    print(f"Roboflow initialization failed: {e}")
    model = None


# ==========================
# BASIC ROUTES
# ==========================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/project')
def project():
    return render_template('project.html')


@app.route('/frame')
def serve_frame():
    return send_from_directory(directory='.', path='frame.jpg')


# ==========================
# CHATBOT ROUTE
# ==========================

@app.route("/get_response", methods=["POST"])
def get_response_route():
    if not co:
        return jsonify({"response": "AI service not configured."})

    user_message = request.json.get("message")

    try:
        response = co.chat(
            message=user_message,
            model='command-xlarge-nightly',
            temperature=0.7,
        )
        return jsonify({"response": response.text.strip()})
    except Exception as e:
        print(f"Cohere error: {e}")
        return jsonify({"response": "AI temporarily unavailable."})


# ==========================
# PRODUCT FLOW
# ==========================

@app.route('/explore_product', methods=['POST'])
def explore_product():
    data = request.get_json()
    product_name = data.get('product_name')
    session['productname'] = product_name
    return jsonify({"status": "success", "redirect": url_for('service')})


@app.route('/service')
def service():
    product_name = session.get('productname')
    if not product_name:
        return redirect(url_for('index'))

    try:
        product_info = fetch_product_details(product_name)
        time.sleep(0.3)
        product_rating = fetch_product_rating(product_name)
        time.sleep(0.3)
        product_review = fetch_product_review(product_name)
        time.sleep(0.3)
        product_trends = fetch_product_trends(product_name)
        time.sleep(0.3)
        product_similar = fetch_product_similar(product_name)
        time.sleep(0.3)

        online_link = main(product_name)
        link1, link2, link3 = fetch_youtube_videos(product_name)

        return render_template('service.html',
                               product_info=product_info,
                               product_name=product_name,
                               product_rating=product_rating,
                               product_review=product_review,
                               product_trends=product_trends,
                               product_similar=product_similar,
                               online_link=online_link,
                               link1=link1,
                               link2=link2,
                               link3=link3)

    except Exception as e:
        print(f"Service error: {e}")
        return render_template('service.html',
                               product_info="Temporarily unavailable",
                               product_name=product_name,
                               product_rating="4.2",
                               product_review="Reviews unavailable",
                               product_trends="Trending data unavailable",
                               product_similar="Similar products unavailable",
                               online_link="#",
                               link1="",
                               link2="",
                               link3="")


# ==========================
# RUN (LOCAL ONLY)
# ==========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)