# import asyncio
# from crawl4ai import AsyncWebCrawler

def write_in_file(text, location='output.txt'):

    with open(location, "w") as file:
        file.write(text)
    
    print('write on file successful')

url = 'https://www.zoomg.ir/movie-tv-show-review/312697-dance-with-me-movie-review/'

# async def main():
#     # Create an instance of AsyncWebCrawler
#     async with AsyncWebCrawler() as crawler:
#         # Run the crawler on a URL
#         result = await crawler.arun(url=url)

#         # Print the extracted content
#         write_in_file(result.markdown)

# # Run the async main function
# asyncio.run(main())


import asyncio
# from crawl4ai import AsyncWebCrawler

# async def main():
#     async with AsyncWebCrawler() as crawler:
#         result = await crawler.arun("https://example.com")
#         print(result.markdown[:300])  # Print first 300 chars

# if __name__ == "__main__":
#     asyncio.run(main())

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BrowserConfig, CacheMode
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

md_generator = DefaultMarkdownGenerator(
    content_filter=PruningContentFilter(threshold=0.4, threshold_type="fixed")
)

config = CrawlerRunConfig(
    cache_mode=CacheMode.BYPASS,
    markdown_generator=md_generator
)



async def main():

    async with AsyncWebCrawler() as crawler:

        result = await crawler.arun(url, config=config)
        write_in_file(result.markdown.raw_markdown, location='output1.txt')
        write_in_file(result.markdown.fit_markdown, location='output2.txt')

if __name__ == "__main__":
    asyncio.run(main())