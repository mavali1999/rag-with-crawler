import asyncio
import os
import xml.etree.ElementTree as ET

import requests
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig

import config
from url_normalizer import normalize_url

INDEX_LOCATION = "index"


def extract_sitemap_index_entries(sitemap_index_urls: list[str]):
    entries = []
    while sitemap_index_urls:
        sitemap_index_url = sitemap_index_urls.pop()
        print(sitemap_index_url)

        response = requests.get(sitemap_index_url)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        ns = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}

        for sitemap in root.findall("ns:sitemap", ns):
            loc = sitemap.find("ns:loc", ns).text
            sitemap_index_urls.append(loc)

        for url in root.findall("ns:url", ns):
            loc = url.find("ns:loc", ns).text
            lastmod_elem = url.find("ns:lastmod", ns)
            lastmod = lastmod_elem.text if lastmod_elem is not None else None
            changefreq_elem = url.find("ns:changefreq", ns)
            changefreq = changefreq_elem.text if changefreq_elem is not None else None
            entries.append(
                {
                    "loc": loc,
                    "lastmod": lastmod,
                    "changefreq": changefreq
                }
            )

    return entries


def save_file(save_location, markdown):

    assert isinstance(markdown, str)
    os.makedirs(os.path.dirname(save_location), exist_ok=True)
    with open(save_location, "w", encoding='utf-8') as f:
        f.write(markdown)


async def crawl_website(crawler: AsyncWebCrawler, url: str, save_location: str) -> None:
    if os.path.isfile(save_location):
        return
    
    result = await crawler.arun(
        url=url,
        config=CrawlerRunConfig(

            # Content
            exclude_external_links=True,
            exclude_all_images=True,
            # css_selector="main.content",
        
            only_text=True,
            exclude_internal_links=True,
            exclude_social_media_links=True,
            remove_forms=True,
            # scan_full_page=True,
            excluded_tags=[
                "form",
                "header",
                "footer",
                "nav",
                "span",
                "label",
                "a"
            ]
        )
    )
    markdown = result.markdown
    save_file(save_location=save_location, markdown=markdown)


async def main():
    sitemap_index_urls = config.SEED_SITES
    entries = extract_sitemap_index_entries(sitemap_index_urls)
    entries = entries[::-1]
    async with AsyncWebCrawler() as crawler:
        for entry in entries:
            url = entry["loc"]
            file_path = "./" + INDEX_LOCATION + '/' + normalize_url(url) + '.md'
            await crawl_website(
                crawler=crawler,
                url=url,
                save_location=file_path,
            )


if __name__ == "__main__":
    asyncio.run(main())
