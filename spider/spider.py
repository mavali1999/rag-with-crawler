import requests
import xml.etree.ElementTree as ET

# Sitemap URL
sitemap_url = "https://www.varzesh3.com/sitemap.xml"

try:
    response = requests.get(sitemap_url, timeout=10)
    response.raise_for_status()  # Raise error if request failed

    # Parse the XML
    root = ET.fromstring(response.content)

    # Find all <loc> tags (these contain URLs)
    urls = root.findall(".//{*}loc")

    # Count URLs
    print(f"Total pages in sitemap: {len(urls)}")

except requests.exceptions.RequestException as e:
    print(f"Error fetching sitemap: {e}")
