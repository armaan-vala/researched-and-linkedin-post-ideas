import json
from groq import Groq

MODEL = "llama-3.3-70b-versatile"
MAX_ARTICLES_FOR_ANALYSIS = 30


def _dedupe_and_trim(articles):
    seen_titles = set()
    trimmed = []
    for a in articles:
        title_lower = a["title"].lower().strip()
        if title_lower in seen_titles or not title_lower:
            continue
        seen_titles.add(title_lower)
        trimmed.append(a)
        if len(trimmed) >= MAX_ARTICLES_FOR_ANALYSIS:
            break
    return trimmed


def analyze_trends(articles, api_key):
    client = Groq(api_key=api_key)

    articles = _dedupe_and_trim(articles)

    articles_text = ""
    for i, article in enumerate(articles, 1):
        articles_text += f"{i}. [{article['source']}] {article['title']}\n"

    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=3000,
        temperature=0.7,
        messages=[
            {
                "role": "system",
                "content": "You are a tech trend analyst. Always respond with valid JSON only, no extra text.",
            },
            {
                "role": "user",
                "content": f"""Analyze these AI/tech article titles and identify the TOP 8 most interesting, trending, and LinkedIn-post-worthy topics.

Group similar articles into themes. For each topic return:
- id (1-8)
- title: catchy topic title
- summary: 2-3 sentences on what's happening
- why_interesting: why it matters for tech professionals on LinkedIn
- post_worthiness: score 1-10
- key_angles: 2 possible angles for a LinkedIn post

Return ONLY valid JSON:
{{"topics": [{{"id": 1, "title": "...", "summary": "...", "why_interesting": "...", "post_worthiness": 8, "key_angles": ["...", "..."]}}]}}

ARTICLES:
{articles_text}""",
            },
        ],
    )

    text = response.choices[0].message.content
    start = text.find("{")
    end = text.rfind("}") + 1
    if start != -1 and end > start:
        return json.loads(text[start:end], strict=False)
    return {"topics": []}
