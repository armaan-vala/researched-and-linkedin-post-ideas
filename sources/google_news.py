import feedparser
from config import GOOGLE_NEWS_RSS, MAX_ARTICLES_PER_SOURCE
from datetime import datetime, timezone


def fetch_google_news_trends():
    articles = []
    try:
        feed = feedparser.parse(GOOGLE_NEWS_RSS)
        count = 0
        for entry in feed.entries:
            if count >= MAX_ARTICLES_PER_SOURCE:
                break

            published = None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)

            articles.append({
                "title": entry.get("title", "No title"),
                "link": entry.get("link", ""),
                "summary": getattr(entry, "summary", entry.get("title", ""))[:500],
                "source": "Google News",
                "published": published.isoformat() if published else "Unknown",
                "type": "google_news",
            })
            count += 1
    except Exception as e:
        print(f"  [!] Failed to fetch Google News: {e}")
    return articles
