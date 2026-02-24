
from flask import Flask, request, jsonify, render_template_string
import feedparser
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

OPENCAGE_API_KEY = os.getenv("OPENCAGE_API_KEY")  # Ensure

prod = 'Oreo,biscuit'  

def get_google_news_rss(product, country):
    rss_url = f"https://news.google.com/rss/search?q={product}+{country}&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(rss_url)
    
    articles = []
    for entry in feed.entries[:5]:
        articles.append({
            'title': entry.title,
            'url': entry.link,
            'published_at': entry.published
        })
    
    return articles

def get_country_from_coordinates(lat, lon):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={lat}+{lon}&key={OPENCAGE_API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if data['results']:
        country = data['results'][0]['components'].get('country')
        return country
    else:
        return None

@app.route('/', methods=['GET'])
def index():
    return render_template_string(template)

@app.route('/get_news', methods=['POST'])
def get_news():
    data = request.json
    lat = data.get('lat')
    lon = data.get('lon')
    
    country = get_country_from_coordinates(lat, lon)
    if country:
        google_news = get_google_news_rss(prod, country)
        return jsonify({'articles': google_news, 'country': country})
    else:
        return jsonify({'error': 'Unable to determine country from the provided coordinates.'}), 400

template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Google News Search</title>
    <script>
        window.onload = function() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(fetchNews, showError);
            } else {
                alert("Geolocation is not supported by this browser.");
            }
        };

        function fetchNews(position) {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;

            fetch('/get_news', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ lat: lat, lon: lon })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    displayArticles(data.articles, data.country);
                }
            })
            .catch(error => console.error('Error:', error));
        }

        function showError(error) {
            switch(error.code) {
                case error.PERMISSION_DENIED:
                    alert("User denied the request for Geolocation.");
                    break;
                case error.POSITION_UNAVAILABLE:
                    alert("Location information is unavailable.");
                    break;
                case error.TIMEOUT:
                    alert("The request to get user location timed out.");
                    break;
                case error.UNKNOWN_ERROR:
                    alert("An unknown error occurred.");
                    break;
            }
        }

        function displayArticles(articles, country) {
            const resultDiv = document.getElementById('results');
            resultDiv.innerHTML = `<h2>Google News Articles related to '{{ prod }}' in '${country}':</h2>`;
            const list = document.createElement('ul');
            articles.forEach(article => {
                const listItem = document.createElement('li');
                listItem.innerHTML = `<a href="${article.url}">${article.title}</a><br><small>Published at: ${article.published_at}</small>`;
                list.appendChild(listItem);
            });
            resultDiv.appendChild(list);
        }
    </script>
</head>
<body>
    <div id="results">Fetching news articles...</div>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True)
