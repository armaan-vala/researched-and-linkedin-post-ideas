import json
from groq import Groq
from config import STYLE_PROMPT

MODEL = "llama-3.3-70b-versatile"


def generate_posts(topic, api_key, num_versions=4):
    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=6000,
        temperature=0.9,
        messages=[
            {
                "role": "system",
                "content": STYLE_PROMPT + "\nAlways respond with valid JSON only, no extra text.",
            },
            {
                "role": "user",
                "content": f"""TOPIC TO WRITE ABOUT:
Title: {topic['title']}
Summary: {topic['summary']}
Why it's interesting: {topic['why_interesting']}
Possible angles: {', '.join(topic.get('key_angles', []))}

Generate exactly {num_versions} different LinkedIn post versions about this topic.

Each version should take a DIFFERENT ANGLE:
- Version 1: Personal experience / observation angle
- Version 2: Contrarian / "unpopular opinion" angle
- Version 3: Educational / "here's what most people miss" angle
- Version 4: Industry impact / future prediction angle

Make each post feel authentic and natural, not AI-generated. Write like a real person sharing real thoughts.

Return ONLY valid JSON:
{{
  "posts": [
    {{
      "version": 1,
      "angle": "Personal experience",
      "post": "The full LinkedIn post text here...",
      "hook_preview": "First line of the post"
    }}
  ]
}}""",
            },
        ],
    )

    text = response.choices[0].message.content
    start = text.find("{")
    end = text.rfind("}") + 1
    if start != -1 and end > start:
        return json.loads(text[start:end], strict=False)
    return {"posts": []}
