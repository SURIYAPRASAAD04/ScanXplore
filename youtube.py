def fetch_youtube_videos(product_name):
    product_videos = {
        "Nivea Soft, Light Moisturizer": [
            "https://www.youtube.com/embed/LQrbZOHPzBk",
            "https://www.youtube.com/embed/5qBwhTbJuVw",
            "https://www.youtube.com/embed/axKXRC3wXX4"
        ],
        "Lakme Forever Matte Foundation": [
            "https://www.youtube.com/embed/qtwGwy10hmU",
            "https://www.youtube.com/embed/QVWCq8H35vY",
            "https://www.youtube.com/embed/Pm-8SlyNkhY"
        ],
        "Oreo, biscuit": [
            "https://www.youtube.com/embed/mGwGryJvaRQ",
            "https://www.youtube.com/embed/7m1xN7RS-hI",
            "https://www.youtube.com/embed/oio3JCUhl5Q"
        ],
        "Ahaglow Moisturizer, Acne control, cosmetics": [
            "https://www.youtube.com/embed/QdrcLZikPbs",
            "https://www.youtube.com/embed/sIJtTgnc_3s",
            "https://www.youtube.com/embed/HgGmdYYji_s"
        ],
        "Pampers All Round Protection Pants": [
            "https://www.youtube.com/embed/yqpuFDDGPug",
            "https://www.youtube.com/embed/GbbvoK5UTP8",
            "https://www.youtube.com/embed/BKy2fSDm870"
        ],
        "Dove pink bar soap": [
            "https://www.youtube.com/embed/KwTlkzFTHpE",
            "https://www.youtube.com/embed/GZSGdVThePc",
            "https://www.youtube.com/embed/1owKNSOfdSE"
        ]
    }
    
    # Get videos for the product or return empty list
    video_urls = product_videos.get(product_name, [])
    
    # Return three values (empty string if not available)
    a = video_urls[0] if len(video_urls) > 0 else ""
    b = video_urls[1] if len(video_urls) > 1 else ""
    c = video_urls[2] if len(video_urls) > 2 else ""
    
    return a, b, c