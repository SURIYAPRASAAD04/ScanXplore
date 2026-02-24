from flask import Flask, render_template, Response, jsonify, request, session, redirect, url_for, send_from_directory
import cohere
from roboflow import Roboflow
import cv2
from flask import Response, jsonify
import threading
import requests
import feedparser
from bs4 import BeautifulSoup
from social import fetch_social_trends 
from shopping import main
from ai import fetch_product_details, fetch_product_rating, fetch_product_review, fetch_product_trends, fetch_product_similar
from ai_detail import fetch_details, fetch_similar
from negative import fetch_review1
from review import fetch_review
from youtube import fetch_youtube_videos
import time
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# Initialize Roboflow
try:
    rf = Roboflow(api_key=os.getenv("ROBOFLOW_API_KEY"))
    project = rf.workspace().project("obj-k7ktz")  
    model = project.version("1").model 
except Exception as e:
    print(f"Error initializing Roboflow: {e}")
    model = None

cohere_api_key = os.getenv("COHERE_API_KEY")
co = cohere.Client(cohere_api_key)

@app.route('/') 
def index():
    return render_template('index.html')

def remove_symbols(sentence):
    if sentence:
        sentence = sentence.replace('*', '')
        sentence = sentence.replace('#', '')
    return sentence

@app.route('/frame')
def serve_frame():
    """Serve the frame image."""
    return send_from_directory(directory='.', path='frame.jpg')

@app.route('/about')
def about():
    product_name = session.get('productname')
    if not product_name:
        return redirect(url_for('index'))
    
    product_in = fetch_details(product_name)
    product_info = remove_symbols(product_in)
    return render_template('about.html', product_info=product_info, product_name=product_name)

@app.route('/review')
def review():
    product_name = session.get('productname')
    if not product_name:
        return redirect(url_for('index'))
    
    # Add delay between API calls to avoid rate limiting
    product_re = fetch_review(product_name)
    time.sleep(0.5)
    product_re1 = fetch_review(product_name)
    time.sleep(0.5)
    product_re2 = fetch_review1(product_name)
    time.sleep(0.5)
    product_re3 = fetch_review(product_name)
    time.sleep(0.5)
    product_re4 = fetch_review(product_name)
    
    product_review = remove_symbols(product_re)
    product_review1 = remove_symbols(product_re1)
    product_review2 = remove_symbols(product_re2)
    product_review3 = remove_symbols(product_re3)
    product_review4 = remove_symbols(product_re4)
    
    return render_template('review.html', 
                          product_review=product_review,
                          product_review1=product_review1,
                          product_review2=product_review2,
                          product_review3=product_review3,
                          product_review4=product_review4,
                          product_name=product_name)

def is_valid_url(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def fetch_logo_url(provider_name):
    specific_publishers = {
        "the times of india": "timesofindia.indiatimes.com",
        "the economic times": "economictimes.indiatimes.com",
        "times now": "timesnow.indiatimes.com",
        "mirror now": "mirrornow.indiatimes.com",
        "et brandequity": "brandequity.economictimes.indiatimes.com"
    }
    
    normalized_provider = provider_name.lower()
    
    if normalized_provider in specific_publishers:
        domain = specific_publishers[normalized_provider]
        clearbit_url = f"https://logo.clearbit.com/{domain}"
        if is_valid_url(clearbit_url):
            return clearbit_url
    
    domain_patterns = [
        '{}.com', '{}.in', '{}.co.in', '{}.org',
        '{}news.com', '{}.co', '{}.net', '{}.edu'
    ]
    
    provider_variants = [
        '-'.join(normalized_provider.split()),
        ''.join(normalized_provider.split())
    ]
    
    for pattern in domain_patterns:
        for variant in provider_variants:
            clearbit_url = f"https://logo.clearbit.com/{pattern.format(variant)}"
            if is_valid_url(clearbit_url):
                return clearbit_url
    
    fallback_domain = provider_variants[1] if provider_variants else normalized_provider
    google_favicon_url = f"https://www.google.com/s2/favicons?sz=64&domain={fallback_domain}.com"
    if is_valid_url(google_favicon_url):
        return google_favicon_url
    
    return "https://upload.wikimedia.org/wikipedia/commons/0/0b/Google_News_icon.png"

def get_google_news_rss(product):
    rss_url = f"https://news.google.com/rss/search?q={product}&hl=en-US&gl=US&ceid=US:en"
    try:
        feed = feedparser.parse(rss_url)
    except:
        return []
    
    articles = []
    for entry in feed.entries:
        if len(articles) >= 5:
            break
    
        if '-' in entry.title:
            title_parts = entry.title.rsplit('-', 1)
            title = title_parts[0].strip()
            provider = title_parts[1].strip()
        else:
            title = entry.title.strip()
            provider = 'Unknown'
        
        logo_url = fetch_logo_url(provider)
        
        articles.append({
            'provider': provider,
            'title': title,
            'url': entry.link,
            'date': entry.published,
            'logo_url': logo_url
        })
    
    return articles

@app.route('/SocialTrends')
def Social_Trends():
    product_name = session.get('productname')
    if not product_name:
        return redirect(url_for('index'))
    
    prod = product_name.replace(' ', ',') 
    google_news = get_google_news_rss(prod)
    p1, p2, p3, p4 = fetch_social_trends(product_name)
    link1, link2, link3 = fetch_youtube_videos(product_name)

    return render_template('Social_Trends.html', 
                          p1=p1, p2=p2, p3=p3, p4=p4,
                          product_name=product_name,
                          link1=link1, link2=link2, link3=link3,
                          product_data=google_news, prod=prod)

# Product data for similar products
product_data = {
    "Ahaglow Moisturizer, Acne control, cosmetics": {
        "products": [
            {
                "name": "Pond's Super Light Gel Oil Free Moisturiser",
                "description": "A lightweight, oil-free moisturizer that provides hydration without clogging pores.",
            },
            {
                "name": "Mamaearth Vitamin C Oil-Free Moisturizer",
                "description": "An oil-free moisturizer infused with vitamin C and fruit extracts.",
            },
            {
                "name": "Lakme Peach Milk Intense Moisturizer Lotion",
                "description": "A creamy moisturizer that nourishes and hydrates the skin.",
            },
            {
                "name": "Cetaphil Moisturising Lotion",
                "description": "A gentle, non-greasy moisturizer suitable for sensitive skin.",
            }
        ]
    },
    "Dove pink bar soap": {
        "products": [
            {
                "name": "Pears Soft & Fresh Soap Bar",
                "description": "A mild, glycerin-based soap that cleanses the skin without stripping its natural oils.",
            },
            {
                "name": "NIVEA Creme Soft Soap",
                "description": "A creamy soap that gently cleanses and moisturizes the skin.",
            },
            {
                "name": "Sheny Soft Soap Glowing",
                "description": "A soap that helps improve skin texture and radiance.",
            },
            {
                "name": "Lux International Creamy Perfection Soap",
                "description": "A luxurious soap that provides a rich, creamy lather.",
            }
        ]
    },
    "Lakme Forever Matte Foundation": {
        "products": [
            {
                "name": "Maybelline New York Fit Me Matte+Poreless Liquid Foundation Tube",
                "description": "A liquid foundation that provides a natural, matte finish.",
            },
            {
                "name": "FACES CANADA All Day Hydra Matte Foundation",
                "description": "A long-lasting, hydrating foundation that gives a smooth, matte finish.",
            },
            {
                "name": "MAC Studio Fix Professional Waterproof Foundation",
                "description": "A long-wearing, waterproof foundation that provides a matte finish.",
            },
            {
                "name": "Colorbar Xoxo Everlasting Foundation - Sand 004",
                "description": "A lightweight, buildable foundation that gives a natural, matte finish.",
            }
        ]
    },
    "Nivea Soft, Light Moisturizer": {
        "products": [
            {
                "name": "Dove Beauty Cream",
                "description": "A rich, creamy moisturizer that deeply nourishes and hydrates the skin.",
            },
            {
                "name": "Olay Moisturising Cream",
                "description": "A lightweight, non-greasy moisturizer that provides long-lasting hydration.",
            },
            {
                "name": "Neutriderm Moisturising Lotion",
                "description": "A gentle, non-comedogenic moisturizer suitable for sensitive skin.",
            },
            {
                "name": "Pond's Super Light Gel Oil Free Moisturiser",
                "description": "A lightweight, oil-free gel moisturizer that provides hydration.",
            }
        ]
    },
    "Oreo, biscuit": {
        "products": [
            {
                "name": "Britannia Hi-Fibre Digestive Biscuits",
                "description": "Digestive biscuits made with high-fiber ingredients.",
            },
            {
                "name": "Sunfeast Marie Light Biscuits",
                "description": "Light, airy biscuits with a delicate flavor.",
            },
            {
                "name": "Parle Hide Seek Black Bourbon Biscuits",
                "description": "Chocolate-flavored biscuits with a creamy filling.",
            },
            {
                "name": "Britannia Milk Bikis Biscuits",
                "description": "Milk-flavored biscuits with a creamy taste.",
            }
        ]
    },
    "Pampers All Round Protection Pants": {
        "products": [
            {
                "name": "MamyPoko Tape Diapers for Premature Babies",
                "description": "Soft, comfortable diapers designed for premature babies.",
            },
            {
                "name": "Huggies Complete Comfort Wonder Pants",
                "description": "Breathable, stretchy diaper pants that offer a snug fit.",
            },
            {
                "name": "Himalaya Total Care Baby Pants Diapers",
                "description": "Organic, bamboo-based diaper pants that are gentle on sensitive skin.",
            },
            {
                "name": "Little Angel Baby Easy Dry Diaper Pants",
                "description": "Lightweight, easy-to-use diaper pants that provide reliable protection.",
            }
        ]
    }
}

def scrape_images(product_name):
    search_url = f"https://www.google.com/search?hl=en&tbm=isch&q={product_name.replace(' ', '+')}"
    try:
        response = requests.get(search_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img')
        image_links = []
        
        for img in img_tags:
            img_url = img.get('src')
            if img_url and img_url.startswith('http'):
                image_links.append(img_url)
            if len(image_links) >= 5:
                break
        return image_links
    except:
        return []

@app.route('/similar')
def similar():
    product_name = session.get('productname')
    if not product_name:
        return redirect(url_for('index'))
    
    # Try to get from product_data first, otherwise use API
    products = product_data.get(product_name, {}).get("products", [])
    images_data = []
    
    if products:
        for product in products:
            img_urls = scrape_images(product["name"])
            if img_urls:
                images_data.append({
                    'name': product['name'],
                    'description': product['description'],
                    'image_url': img_urls[0]
                })
    
    product_si = fetch_similar(product_name)
    product_similar = remove_symbols(product_si)
    
    return render_template('similar.html', 
                          product_similar=product_similar,
                          product_name=product_name, 
                          images=images_data)

@app.route('/explore_product', methods=['POST'])
def explore_product():
    data = request.get_json()
    product_name = data.get('product_name')
    session['productname'] = product_name
    return jsonify({"status": "success", "redirect": url_for('service')})

@app.route('/project')
def project():
    return render_template('project.html')

@app.route("/get_response", methods=["POST"])
def get_response_route():
    user_message = request.json.get("message")
    
    try:
        # Use Chat API instead of Generate API
        response = co.chat(
            message=user_message,
            model='command-xlarge-nightly',
            temperature=0.7,
        )
        fulfillment_text = response.text.strip()
        return jsonify({"response": fulfillment_text})
    except Exception as e:
        print(f"Cohere error: {e}")
        return jsonify({"response": "I'm here to help with product questions! What would you like to know?"}), 200

class_data_mapping = {
    "Ahaglow Moisturizer": "Ahaglow Moisturizer, Acne control, cosmetics",
    "Dove": "Dove pink bar soap",
    "Lakme Foundation": "Lakme Forever Matte Foundation",
    "Nivea Soft cream": "Nivea Soft, Light Moisturizer",
    "Oreo": "Oreo, biscuit",
    "Pampers": "Pampers All Round Protection Pants"
}

detected_object = None
detection_found = False
camera_active = False
cap = None
camera_lock = threading.Lock()

def initialize_camera():
    """Function to initialize the camera when the app starts."""
    global cap, camera_active
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open camera")
            camera_active = False
            return
        camera_active = True
        print(f"Camera active: {camera_active}")
    except Exception as e:
        print(f"Error initializing camera: {e}")
        camera_active = False

def activate_camera():
    """Function to activate the camera and perform detection."""
    global cap, detected_object, detection_found, camera_active
    
    if not camera_active or cap is None:
        print("Error: Camera not initialized.")
        return
    
    detection_start_time = time.time()
    max_detection_time = 30  # Stop after 30 seconds if no detection
    
    with camera_lock:
        while camera_active:
            try:
                ret, frame = cap.read()
                if not ret:
                    print("Error: Could not read frame.")
                    break
                
                # Check timeout
                if time.time() - detection_start_time > max_detection_time:
                    print("Detection timeout reached")
                    break
                
                cv2.imwrite("frame.jpg", frame)
                
                if model:
                    prediction = model.predict("frame.jpg").json()
                    detections = prediction.get('predictions', [])
                    
                    for detection in detections:
                        class_name = detection['class']
                        confidence = detection['confidence']
                        
                        if confidence >= 0.75:
                            detected_object = class_data_mapping.get(class_name, class_name)
                            detection_found = True
                            camera_active = False
                            break
                
                time.sleep(0.1)  # Small delay to prevent CPU overload
                
            except Exception as e:
                print(f"Error in detection loop: {e}")
                break
    
    # Don't call destroyAllWindows() - it causes issues
    if cap:
        cap.release()

@app.route('/start_camera')
def start_camera():
    """Route to start the camera."""
    global detected_object, detection_found, camera_active
    detected_object = None
    detection_found = False
    
    if not camera_active:
        initialize_camera()
        if not camera_active:
            return jsonify({"status": "Camera not ready"}), 500
    
    threading.Thread(target=activate_camera, daemon=True).start()
    return jsonify({"status": "Camera started"})

@app.route('/video_feed')
def video_feed():
    """Video streaming route."""
    global cap
    if not cap or not camera_active:
        return Response(status=404)
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen():
    """Video streaming generator function."""
    global cap, camera_active
    while camera_active and cap:
        try:
            ret, frame = cap.read()
            if not ret:
                break
            
            ret, jpeg = cv2.imencode('.jpg', frame)
            if ret:
                frame_bytes = jpeg.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')
            time.sleep(0.03)  # Limit frame rate
        except Exception as e:
            print(f"Error in video feed: {e}")
            break
    
    if cap:
        cap.release()

@app.route('/detect')
def detect():
    """Route to check detection results."""
    global detected_object, detection_found
    print(f"Detection check: {detected_object}, found: {detection_found}")
    
    if detection_found and detected_object:
        product_name = detected_object
        session['productname'] = product_name
        return jsonify({
            "alert": f"Product detected: {detected_object}", 
            "status": "success",
            "redirect_url": url_for('service')
        })
    else:
        return jsonify({
            "alert": "No matching image detected", 
            "status": "failure"
        })

def get_google_news_rss1(product):
    rss_url = f"https://news.google.com/rss/search?q={product}&hl=en-US&gl=US&ceid=US:en"
    try:
        feed = feedparser.parse(rss_url)
    except:
        return []
    
    articles = []
    for entry in feed.entries:
        if len(articles) >= 2:
            break
       
        if '-' in entry.title:
            title_parts = entry.title.rsplit('-', 1)
            title = title_parts[0].strip()
            provider = title_parts[1].strip()
        else:
            title = entry.title.strip()
            provider = 'Unknown'
        
        logo_url = fetch_logo_url(provider)
        articles.append({
            'provider': provider,
            'title': title,
            'url': entry.link,
            'date': entry.published,
            'logo_url': logo_url
        })
    
    return articles

@app.route('/service')
def service():
    """Route to render the service page after detection."""
    product_name = session.get('productname')
    if not product_name:
        return redirect(url_for('index'))
    
    try:
        prod = product_name.replace(' ', ',')
        google_news = get_google_news_rss1(prod)
        
        # Add delays between API calls to avoid rate limiting
        product_info = fetch_product_details(product_name)
        time.sleep(0.5)
        product_rating = fetch_product_rating(product_name)
        time.sleep(0.5)
        product_review = fetch_product_review(product_name)
        time.sleep(0.5)
        product_trends = fetch_product_trends(product_name)
        time.sleep(0.5)
        product_similar = fetch_product_similar(product_name)
        time.sleep(0.5)
        product_re6 = fetch_review(product_name)
        time.sleep(0.5)
        product_re7 = fetch_review(product_name)
        time.sleep(0.5)
        product_re8 = fetch_review1(product_name)
        
        online_link = main(product_name)
        
        # Get YouTube videos - this will now use your predefined mapping
        link1, link2, link3 = fetch_youtube_videos(product_name)
        
        # Debug print to check if videos are being fetched
        print(f"YouTube links for {product_name}: {link1}, {link2}, {link3}")
        
        return render_template('service.html',
                               product_info=remove_symbols(product_info),
                               product_name=product_name,
                               product_rating=remove_symbols(product_rating),
                               product_review=remove_symbols(product_review),
                               product_trends=remove_symbols(product_trends),
                               product_data=google_news,
                               prod=prod,
                               product_similar=remove_symbols(product_similar),
                               online_link=online_link,
                               product_review6=remove_symbols(product_re6),
                               product_review7=remove_symbols(product_re7),
                               product_review8=remove_symbols(product_re8),
                               link1=link1,
                               link2=link2,
                               link3=link3)  # Make sure link3 is passed
    except Exception as e:
        print(f"Error in service route: {e}")
        return render_template('service.html',
                               product_info="Product information temporarily unavailable",
                               product_name=product_name,
                               product_rating="4.2",
                               product_review="Customers love this product for its quality and value.",
                               product_trends="This product is trending on social media.",
                               product_data=[],
                               prod=product_name.replace(' ', ','),
                               product_similar="Similar products include Brand A, Brand B, Brand C",
                               online_link="#",
                               product_review6="Great product! Highly recommended.",
                               product_review7="Good value for money.",
                               product_review8="Quality could be improved.",
                               link1="",
                               link2="",
                               link3="")
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)