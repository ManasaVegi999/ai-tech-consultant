
import json
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://support.brilliantdirectories.com/support/solutions"

DATA_FILE = Path(__file__).parent / "articles.json"



def fetch_article_links(max_pages=30):
    """Discover articles by following support categories and folders."""
    from collections import deque

    start_urls = [
        "https://support.brilliantdirectories.com/support/home",
        "https://support.brilliantdirectories.com/support/solutions",
    ]

    queue = deque(start_urls)
    visited = set()
    article_links = set()

    while queue and len(visited) < max_pages:
        page_url = queue.popleft().split("#")[0].split("?")[0]

        if page_url in visited:
            continue

        visited.add(page_url)

        try:
            response = requests.get(
                page_url,
                headers={"User-Agent": "AITechConsultant/1.0"},
                timeout=20,
            )
            response.raise_for_status()
        except requests.RequestException as error:
            print(f"Could not open {page_url}: {error}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        for anchor in soup.find_all("a", href=True):
            url = urljoin(page_url, anchor["href"])
            parsed = urlparse(url)
            path = parsed.path

            if parsed.netloc != "support.brilliantdirectories.com":
                continue

            url = f"{parsed.scheme}://{parsed.netloc}{path}"

            if "/support/solutions/articles/" in path:
                article_links.add(url)

            elif (
                path == "/support/home"
                or path == "/support/solutions"
                or "/support/solutions/folders/" in path
            ):
                if url not in visited:
                    queue.append(url)

    print(f"Pages checked: {len(visited)}")
    print(f"Article links discovered: {len(article_links)}")

    return sorted(article_links)



def extract_article(url):
    """Extract readable text and title from one article."""
    try:
        response = requests.get(
            url,
            headers={"User-Agent": "AITechConsultant/1.0"},
            timeout=20,
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        title_tag = soup.find("h1") or soup.find("title")
        title = title_tag.get_text(" ", strip=True) if title_tag else "Untitled"

        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        content_tag = soup.find("article") or soup.find("main") or soup.body
        content = content_tag.get_text(" ", strip=True) if content_tag else ""

        if not content:
            return None

        return {
            "title": title,
            "url": url,
            "content": content[:15000],
        }

    except requests.RequestException as error:
        print(f"Could not retrieve {url}: {error}")
        return None


def refresh_knowledge_base(max_articles=30):
    """Fetch articles and save them locally as JSON."""
    links = fetch_article_links()[:max_articles]
    articles = []

    for index, url in enumerate(links, start=1):
        print(f"Fetching article {index}/{len(links)}")
        article = extract_article(url)

        if article:
            articles.append(article)

    DATA_FILE.write_text(
        json.dumps(articles, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Saved {len(articles)} articles to {DATA_FILE}")
    return len(articles)


def search_articles(query, limit=5):
    """Find articles whose titles or text match the query."""
    if not DATA_FILE.exists():
        return []

    articles = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    words = set(re.findall(r"\w+", query.lower()))

    if not words:
        return []

    results = []

    for article in articles:
        title_words = set(re.findall(r"\w+", article["title"].lower()))
        content_words = set(re.findall(r"\w+", article["content"].lower()))

        title_matches = len(words & title_words)
        content_matches = len(words & content_words)
        score = title_matches * 3 + content_matches

        if score > 0:
            results.append({
                "title": article["title"],
                "url": article["url"],
                "score": score,
                "excerpt": article["content"][:350],
            })

    results.sort(key=lambda item: item["score"], reverse=True)
    return results[:limit]


if __name__ == "__main__":
    count = refresh_knowledge_base()

    if count:
        print("\nExample search: membership plans")
        for result in search_articles("membership plans"):
            print(f"\nTitle: {result['title']}")
            print(f"Source: {result['url']}")
            print(f"Excerpt: {result['excerpt']}")
