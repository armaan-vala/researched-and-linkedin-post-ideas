import feedparser
from datetime import datetime, timezone, timedelta
from config import RSS_FEEDS, MAX_ARTICLES_PER_SOURCE, MAX_TREND_AGE_DAYS


def fetch_rss_trends():
    articles = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=MAX_TREND_AGE_DAYS)

    for feed_config in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_config["url"])
            count = 0
            for entry in feed.entries:
                if count >= MAX_ARTICLES_PER_SOURCE:
                    break

                published = None
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                    published = datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)

                if published and published < cutoff:
                    continue

                summary = ""
                if hasattr(entry, "summary"):
                    summary = entry.summary[:500]
                elif hasattr(entry, "description"):
                    summary = entry.description[:500]

                articles.append({
                    "title": entry.get("title", "No title"),
                    "link": entry.get("link", ""),
                    "summary": summary,
                    "source": feed_config["name"],
                    "published": published.isoformat() if published else "Unknown",
                    "type": "rss",
                })
                count += 1
        except Exception as e:
            print(f"  [!] Failed to fetch {feed_config['name']}: {e}")

    return articles
