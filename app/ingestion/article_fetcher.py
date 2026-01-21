"""The core idea
Instead of trying to “scrape the internet”, we:
Request the page like a browser
Parse its HTML
Extract only the meaningful content
Ignore everything else
Fail gracefully if structure changes
This is controlled scraping, not brute force.

URL
 ↓
requests.get()  ← with User-Agent
 ↓
HTML
 ↓
BeautifulSoup
 ↓
Site-specific extractor
 ↓
{ title, text, word_count, url }
"""
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}


STARTER_URLS = [
    "https://dev.to/dannwaneri/my-chrome-tabs-tell-a-story-we-havent-processed-yet-ec9",
    "https://en.wikipedia.org/wiki/History_of_writing#Emergence"
]


def fetch_url(url):
    res = requests.get(url, headers=HEADERS, timeout=30)
    res.raise_for_status()
    return BeautifulSoup(res.text, "html.parser")


def parse_devto(soup):
    title = soup.find("h1").get_text(strip=True)
    body = soup.find("div", class_="crayons-article__main")
    paragraphs = [p.get_text() for p in body.find_all("p")]
    return title, "\n".join(paragraphs)

"""
def parse_freecodecamp(soup):
    title = soup.find("h1").get_text(strip=True)
    article = soup.find("article")
    paragraphs = [p.get_text() for p in article.find_all("p")]
    return title, "\n".join(paragraphs)


def parse_waitbutwhy(soup):
    title = soup.find("h1").get_text(strip=True)
    content = soup.find("div", class_="content")
    paragraphs = [p.get_text() for p in content.find_all("p")]
    return title, "\n".join(paragraphs)


def parse_lesswrong(soup):
    title = soup.find("h1").get_text(strip=True)
    content = soup.find("div", class_="PostsPage-postContent")
    paragraphs = [p.get_text() for p in content.find_all("p")]
    return title, "\n".join(paragraphs)

"""
def parse_wikipedia(soup):
    title = soup.find("h1").get_text(strip=True)
    content = soup.find("div", id="mw-content-text")
    paragraphs = [p.get_text() for p in content.find_all("p")]
    return title, "\n".join(paragraphs)


def fetch_articles():
    articles = []

    for url in STARTER_URLS:
        try:
            soup = fetch_url(url)

            if "dev.to" in url:
                title, text = parse_devto(soup)
            elif "freecodecamp.org" in url:
                title, text = parse_freecodecamp(soup)
            elif "waitbutwhy.com" in url:
                title, text = parse_waitbutwhy(soup)
            elif "lesswrong.com" in url:
                title, text = parse_lesswrong(soup)
            elif "wikipedia.org" in url:
                title, text = parse_wikipedia(soup)
            else:
                continue

            articles.append({
                "title": title,
                "text": text,
                "word_count": len(text.split()),
                "url": url
            })

        except Exception as e:
            print(f"Failed to process {url}: {e}")

    return articles



