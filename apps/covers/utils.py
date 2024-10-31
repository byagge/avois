# covers/pixabay_service.py

import requests
from django.conf import settings

PIXABAY_API_URL = "https://pixabay.com/api/"

def get_cover_image(query):
    params = {
        "key": settings.PIXABAY_API_KEY,
        "q": query,
        "image_type": "photo",
        "orientation": "horizontal",
        "per_page": 1,
    }
    response = requests.get(PIXABAY_API_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data["hits"]:
            return data["hits"][0]["webformatURL"]
    return None
