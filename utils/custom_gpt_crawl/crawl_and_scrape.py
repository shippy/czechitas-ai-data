"""Expose CLI for crawling and scraping."""

import os
from dotenv import load_dotenv
from firecrawl import FirecrawlApp  # type: ignore
from pathlib import Path
import typer
from rich import print


app = typer.Typer()


@app.command()
def crawl_and_scrape(url: str, limit: int = 10, output_dir: Path = Path("output")):
    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    client = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

    crawl = client.crawl_url(
        url, params={"limit": limit, "scrapeOptions": {"formats": ["markdown"]}}
    )
    print(crawl)
    return crawl


@app.command()
def scrape_to_md(url: str, output_dir: Path = Path("output")):
    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    client = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

    crawl = client.scrape_url(url, params={"formats": ["markdown"]})

    print(crawl)

    # Save to output_dir
    with open(
        output_dir
        / f"{crawl['metadata'].get('title', 'no-title').replace('/', '-')}.md",
        "w",
    ) as f:
        f.write(crawl["markdown"])

    return crawl


if __name__ == "__main__":
    _ = load_dotenv()
    app()
