import requests
import feedparser
from config import SCRAPE_SOURCES, REDDIT_RSS_FEEDS

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


def fetch_hackernews(url):
    articles = []
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        for hit in data.get("hits", []):
            articles.append({
                "title": hit.get("title", ""),
                "link": hit.get("url", f"https://news.ycombinator.com/item?id={hit.get('objectID', '')}"),
                "summary": hit.get("title", ""),
                "source": "Hacker News",
                "published": hit.get("created_at", "Unknown"),
                "points": hit.get("points", 0),
                "type": "hackernews",
            })
    except Exception as e:
        print(f"  [!] Failed to fetch Hacker News: {e}")
    return articles


def fetch_reddit_rss():
    articles = []
    for feed_config in REDDIT_RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_config["url"])
            for entry in feed.entries[:15]:
                articles.append({
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "summary": getattr(entry, "summary", entry.get("title", ""))[:500],
                    "source": feed_config["name"],
                    "published": getattr(entry, "published", "Recent"),
                    "type": "reddit",
                })
        except Exception as e:
            print(f"  [!] Failed to fetch {feed_config['name']}: {e}")
    return articles


def fetch_scraped_trends():
    all_articles = []
    for source in SCRAPE_SOURCES:
        if source["type"] == "api":
            all_articles.extend(fetch_hackernews(source["url"]))
    all_articles.extend(fetch_reddit_rss())
    return all_articles
