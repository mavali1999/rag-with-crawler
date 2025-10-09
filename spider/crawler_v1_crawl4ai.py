import asyncio
import hashlib
import os.path
import random
import xml.etree.ElementTree as ET

import requests
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from sqlalchemy.orm import Session

from app.db import WebPage, engine

INDEX_LOCATION = "index"


def url_hash(url: str) -> str:
    return hashlib.sha1(url.encode("utf-8")).hexdigest()


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
            entries.append(
                {
                    "loc": loc,
                    "lastmod": lastmod,
                }
            )

    return entries


async def crawl_website(crawler: AsyncWebCrawler, url: str, save_location: str) -> None:
    if os.path.isfile(save_location):
        return
    result = await crawler.arun(
        url=url,
        config=CrawlerRunConfig(
            only_text=True,
            exclude_all_images=True,
            exclude_external_links=True,
            exclude_internal_links=True,
            exclude_social_media_links=True,
            remove_forms=True,
            scan_full_page=True,
            excluded_tags=[
                "form",
                "header",
                "footer",
                "nav",
                "span",
                "label",
            ],
        ),
    )
    markdown = result.markdown
    assert isinstance(markdown, str)
    with open(save_location, "w") as f:
        f.write(markdown)


async def main():
    sitemap_index_urls = [
        "https://www.itrc.ac.ir/sitemap.xml",
    ]
    entries = extract_sitemap_index_entries(sitemap_index_urls)
    random.shuffle(entries)
    async with AsyncWebCrawler() as crawler:
        for entry in entries:
            url = entry["loc"]
            file_name = url_hash(url)
            save_location = f"{INDEX_LOCATION}/{file_name}.md"
            await crawl_website(
                crawler=crawler,
                url=url,
                save_location=save_location,
            )
            with Session(engine) as session:
                web_page = WebPage(
                    id=id,
                    url=url,
                    save_location=save_location,
                )
                session.add(web_page)


if __name__ == "__main__":
    asyncio.run(main())
