from pathlib import Path
import os
from firecrawl import FirecrawlApp
from dotenv import load_dotenv, dotenv_values 
load_dotenv() 
app = FirecrawlApp(api_key=os.getenv("FIRE_CRAWLER_API"))

OUTPUT_DIR = Path("knowledge_base")


def download_docs(name: str, base_url: str, limit: int = 5):
    print(f"Finding pages for {name}...")

    result = app.map_url(base_url)
    print(result.links[0])
    # فقط لینک‌های مستندات
    urls = [
        url.url
        for url in result.links
        if "docs" in url.url
    ][:limit]

    folder = OUTPUT_DIR / name
    folder.mkdir(parents=True, exist_ok=True)

    print(f"Downloading {len(urls)} pages...")
    print(result.links)
    print(urls[0])
    # print(urls[1])
    for i, url in enumerate(urls, start=1):

        page = app.scrape_url(
            url=url,
            formats=["markdown"],
        )

        title = (
            page.metadata.title
            if page.metadata and page.metadata.title
            else f"page_{i}"
        )

        safe_title = (
            title.replace("/", "-")
                 .replace("\\", "-")
                 .replace(":", "")
                 .replace("?", "")
                 .replace("<", "")
                 .replace(">", "")
        )

        filepath = folder / f"{i:02d}_{safe_title}.md"

        filepath.write_text(
            page.markdown,
            encoding="utf-8",
        )

        print(filepath)


download_docs(
    "mcp",
    "https://modelcontextprotocol.io/docs",
)

download_docs(
    "langchain",
    "https://docs.langchain.com/oss/python/langchain/overview",
)


print("Done!")