import requests
import xml.etree.ElementTree as ET

def count_sitemap_pages(sitemap_url):
    try:
        response = requests.get(sitemap_url, timeout=10)
        response.raise_for_status()
        root = ET.fromstring(response.content)

        # Detect if this is a sitemap index (contains <sitemap> tags)
        sitemap_tags = root.findall(".//{*}sitemap")
        if sitemap_tags:
            total_urls = 0
            for sitemap in sitemap_tags:
                loc = sitemap.find("{*}loc")
                if loc is not None:
                    count = count_sitemap_pages(loc.text.strip())  # Recursive call
                    total_urls += count
            return total_urls
        else:
            # Normal sitemap with <loc> URLs
            urls = root.findall(".//{*}loc")
            return len(urls)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching sitemap: {e}")
        return 0

# Example usage
sitemap_url = "https://www.itrc.ac.ir/sitemap.xml"
total_pages = count_sitemap_pages(sitemap_url)
print(f"Total pages in sitemap(s): {total_pages}")
