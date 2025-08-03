# fetch_api.py
import requests
import xml.etree.ElementTree as ET


def fetch_from_api(url):
    """Fetch raw XML root from API URL."""
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch API data: {response.status_code}")
    return ET.fromstring(response.text)