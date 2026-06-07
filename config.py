RSS_FEEDS = [
    {
        "name": "TechCrunch AI",
        "url": "https://techcrunch.com/category/artificial-intelligence/feed/",
    },
    {
        "name": "The Verge AI",
        "url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    },
    {
        "name": "MIT Technology Review",
        "url": "https://www.technologyreview.com/feed/",
    },
    {
        "name": "VentureBeat AI",
        "url": "https://venturebeat.com/category/ai/feed/",
    },
    {
        "name": "Google AI Blog",
        "url": "https://blog.google/technology/ai/rss/",
    },
    {
        "name": "OpenAI Blog",
        "url": "https://openai.com/blog/rss.xml",
    },
    {
        "name": "Ars Technica AI",
        "url": "https://arstechnica.com/ai/feed/",
    },
]

SCRAPE_SOURCES = [
    {
        "name": "Hacker News",
        "url": "https://hn.algolia.com/api/v1/search?query=AI+artificial+intelligence+LLM&tags=story&hitsPerPage=15",
        "type": "api",
    },
]

REDDIT_RSS_FEEDS = [
    {
        "name": "Reddit r/artificial",
        "url": "https://www.reddit.com/r/artificial/hot.rss?limit=15",
    },
    {
        "name": "Reddit r/MachineLearning",
        "url": "https://www.reddit.com/r/MachineLearning/hot.rss?limit=15",
    },
]

GOOGLE_NEWS_RSS = "https://news.google.com/rss/search?q=artificial+intelligence+AI+trends&hl=en-US&gl=US&ceid=US:en"

MAX_ARTICLES_PER_SOURCE = 10
MAX_TREND_AGE_DAYS = 3

STYLE_PROMPT = """You are writing LinkedIn posts in the style of Armaan Vala, an AI Engineer.

STYLE RULES (follow these exactly):
1. OPENING HOOK: Start with a bold, contrarian, or thought-provoking statement (1-2 short lines). Challenge a common belief or state something surprising.
2. STRUCTURE: Hook → Personal observation/story → Key insight → Bullet points → Reflective conclusion
3. PARAGRAPHS: Very short (1-2 sentences). Lots of white space between paragraphs.
4. TONE: Conversational, first-person, reflective. Share observations like "I noticed..." or "After working with...", NOT preachy "you should..."
5. EMOJIS: Maximum 1-2 per post. Use sparingly. 👉 for emphasis if needed.
6. BULLET POINTS: Use "-" for lists. Keep each bullet to one clear line.
7. SENTENCES: Short and punchy. No complex jargon.
8. ENDING: Reflective one-liner that makes people think. Then add 8-12 hashtags on the last line, formatted as: hashtag#AI hashtag#Topic etc.
9. LENGTH: 150-250 words. Not too short, not too long.
10. PATTERN: Acknowledge popular view → Add nuance from real experience → "But here's the real thing" insight.

EXAMPLE POST STRUCTURE:
---
[Bold contrarian hook - 1 line]
[Optional second hook line]

[Personal context - "After doing X, I realized..."]

[Key insight paragraph]

[Bullet points with "-"]
- Point 1
- Point 2
- Point 3

[Reflective conclusion - 1-2 lines]

[One-liner that sticks]

hashtag#AI hashtag#Topic1 hashtag#Topic2 ...
---
"""
