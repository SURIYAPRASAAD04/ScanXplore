import requests
from bs4 import BeautifulSoup
import os
import webbrowser
from PIL import Image
from io import BytesIO

# Predefined product data
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
            },
            {
                "name": "Lifebuoy Neem and Aloe Vera Soap",
                "description": "A soap that combines the benefits of neem and aloe vera to cleanse and nourish the skin.",
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
                "name": "Dazller Moisturizing Liquid Makeup",
                "description": "A moisturizing foundation that provides a natural, matte finish.",
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
                "name": "Moisturizing Cream For Dry To Very Dry Skin",
                "description": "A deeply nourishing cream that helps replenish the skin's moisture levels.",
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
                "name": "Hide & Seek Parle Chocolate Chip Cookies",
                "description": "Cookies made with real chocolate chips for a delicious taste.",
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
                "name": "Organic Bamboo Diapers",
                "description": "Eco-friendly diapers made from natural bamboo fibers.",
            },
            {
                "name": "Little Angel Baby Easy Dry Diaper Pants",
                "description": "Lightweight, easy-to-use diaper pants that provide reliable protection.",
            }
        ]
    }
}

# Function to scrape images based on the product name
def scrape_images(product_name):
    search_url = f"https://www.google.com/search?hl=en&tbm=isch&q={product_name.replace(' ', '+')}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all image tags
    img_tags = soup.find_all('img')
    image_links = []

    # Extract the src attribute from each img tag
    for img in img_tags:
        img_url = img.get('src')
        if img_url and img_url.startswith('http'):
            image_links.append(img_url)

    return image_links

def open_image_in_browser(image_url):
    webbrowser.open(image_url)

def save_and_open_image(image_url, product_name):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img_path = f"{product_name.replace(' ', '_')}.jpg"
    img.save(img_path)
    img.show()  # This will open the image using the default image viewer

def main():
    product_name = "Dove pink bar soap"

    # Check if the product name exists in the predefined data
    if product_name in product_data:
        print("Product Name:", product_name)
        print("\nRelated Products:\n")

        # Get images for each product
        for product in product_data[product_name]["products"]:
            img_urls = scrape_images(product["name"])  # Scrape images for each similar product
            if img_urls:  # Check if images were found
                first_img_url = img_urls[0]
                print(f"Opening image for {product['name']} in browser...")
                open_image_in_browser(first_img_url)  # Option 1: Open in browser
                
                # Uncomment the following lines for Option 2: Save and open locally
                # print(f"Saving and opening image for {product['name']}...")
                # save_and_open_image(first_img_url, product['name'])
            else:
                print(f"No images found for {product['name']}.")

    else:
        print("Product not found in the database.")

# Run the main function
if __name__ == "__main__":
    main()
