import os
import streamlit as st
from dotenv import load_dotenv

from sources.rss_feeds import fetch_rss_trends
from sources.web_scraper import fetch_scraped_trends
from sources.google_news import fetch_google_news_trends
from analyzer import analyze_trends
from post_generator import generate_posts

load_dotenv()

st.set_page_config(
    page_title="LinkedIn Post Generator",
    page_icon="🚀",
    layout="wide",
)

st.markdown("""
<style>
    /* Force light theme */
    .stApp {
        background-color: #f8f9fa !important;
    }

    .main-header {
        font-size: 2.4rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.1rem;
        color: #1a1a2e;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
        font-size: 1.05rem;
    }

    /* Steps bar */
    .steps-bar {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin: 1.5rem 0 2rem 0;
    }
    .step {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #999;
        font-size: 0.9rem;
        font-weight: 500;
    }
    .step.active {
        color: #0077b5;
        font-weight: 700;
    }
    .step-num {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        background: #e0e0e0;
        color: #999;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.85rem;
    }
    .step.active .step-num {
        background: #0077b5;
        color: white;
    }

    /* Topic cards */
    .topic-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 0.7rem;
        border: 1px solid #e8e8e8;
        border-left: 4px solid #0077b5;
        transition: box-shadow 0.2s;
    }
    .topic-card:hover {
        box-shadow: 0 2px 12px rgba(0,119,181,0.12);
    }
    .topic-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #1a1a2e;
    }
    .topic-summary {
        color: #555;
        font-size: 0.88rem;
        margin-top: 0.4rem;
        line-height: 1.5;
    }
    .topic-angles {
        color: #0077b5;
        font-size: 0.8rem;
        margin-top: 0.4rem;
        font-style: italic;
    }
    .score-badge {
        background: #0077b5;
        color: white;
        padding: 3px 12px;
        border-radius: 12px;
        font-weight: 700;
        font-size: 0.8rem;
        margin-left: 0.5rem;
    }
    .score-badge.high {
        background: #0077b5;
    }
    .score-badge.mid {
        background: #e6a817;
    }
    .score-badge.low {
        background: #dc3545;
    }

    /* Post cards */
    .post-card {
        background: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 14px;
        padding: 1.6rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 1px 6px rgba(0,0,0,0.06);
        transition: box-shadow 0.2s;
    }
    .post-card:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    }
    .post-card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1rem;
        padding-bottom: 0.8rem;
        border-bottom: 1px solid #f0f0f0;
    }
    .angle-tag {
        background: #e8f4fd;
        color: #0077b5;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 700;
        display: inline-block;
    }
    .version-num {
        color: #999;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .post-content {
        color: #333;
        white-space: pre-wrap;
        line-height: 1.75;
        font-size: 0.92rem;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    /* LinkedIn-style preview header */
    .linkedin-preview {
        display: flex;
        align-items: center;
        gap: 0.7rem;
        margin-bottom: 1rem;
    }
    .linkedin-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: linear-gradient(135deg, #0077b5, #00a0dc);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 700;
        font-size: 1rem;
    }
    .linkedin-name {
        font-weight: 700;
        color: #1a1a2e;
        font-size: 0.9rem;
    }
    .linkedin-headline {
        color: #888;
        font-size: 0.75rem;
    }

    /* Stats bar */
    .stats-bar {
        display: flex;
        gap: 1.5rem;
        justify-content: center;
        margin: 1rem 0;
    }
    .stat-item {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 0.8rem 1.5rem;
        text-align: center;
    }
    .stat-num {
        font-size: 1.5rem;
        font-weight: 800;
        color: #0077b5;
    }
    .stat-label {
        font-size: 0.75rem;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Section headers */
    .section-header {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1a1a2e;
        margin: 1.5rem 0 0.3rem 0;
    }
    .section-sub {
        color: #777;
        font-size: 0.9rem;
        margin-bottom: 1.2rem;
    }

    /* Button overrides */
    .stButton > button {
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)


def fetch_all_articles():
    all_articles = []
    rss = fetch_rss_trends()
    all_articles.extend(rss)
    scraped = fetch_scraped_trends()
    all_articles.extend(scraped)
    gnews = fetch_google_news_trends()
    all_articles.extend(gnews)
    return all_articles, len(rss), len(scraped), len(gnews)


def render_steps(active_step):
    steps = ["Fetch Trends", "Pick Topic", "Generate Posts", "Copy & Post"]
    html = '<div class="steps-bar">'
    for i, label in enumerate(steps, 1):
        cls = "step active" if i <= active_step else "step"
        html += f'<div class="{cls}"><div class="step-num">{i}</div>{label}</div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def main():
    api_key = os.getenv("GROQ_API_KEY")

    st.markdown('<div class="main-header">LinkedIn Post Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Fetch latest AI trends &rarr; Pick a topic &rarr; Get ready-to-post LinkedIn content</div>', unsafe_allow_html=True)

    if not api_key:
        st.error("GROQ_API_KEY not found! Add it to your `.env` file.")
        st.stop()

    if "topics" not in st.session_state:
        st.session_state.topics = None
    if "posts" not in st.session_state:
        st.session_state.posts = None
    if "selected_topic_idx" not in st.session_state:
        st.session_state.selected_topic_idx = None

    # Determine active step
    active = 1
    if st.session_state.topics:
        active = 2
    if st.session_state.selected_topic_idx is not None:
        active = 3
    if st.session_state.posts:
        active = 4

    render_steps(active)

    st.markdown("---")

    # --- Step 1: Fetch Trends ---
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        fetch_btn = st.button("🔍  Fetch Latest AI Trends", use_container_width=True, type="primary")

    if fetch_btn:
        st.session_state.posts = None
        st.session_state.selected_topic_idx = None

        with st.spinner("Fetching articles from 10+ sources..."):
            articles, rss_count, web_count, gnews_count = fetch_all_articles()

        st.markdown(f"""
<div class="stats-bar">
    <div class="stat-item"><div class="stat-num">{len(articles)}</div><div class="stat-label">Total Articles</div></div>
    <div class="stat-item"><div class="stat-num">{rss_count}</div><div class="stat-label">RSS Feeds</div></div>
    <div class="stat-item"><div class="stat-num">{web_count}</div><div class="stat-label">Web Sources</div></div>
    <div class="stat-item"><div class="stat-num">{gnews_count}</div><div class="stat-label">Google News</div></div>
</div>
""", unsafe_allow_html=True)

        with st.spinner("Analyzing trends with AI..."):
            topics_data = analyze_trends(articles, api_key)
            st.session_state.topics = topics_data.get("topics", [])

    # --- Step 2: Show Topics ---
    if st.session_state.topics:
        st.markdown('<div class="section-header">Trending AI Topics</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Click on a topic to generate LinkedIn posts in your style</div>', unsafe_allow_html=True)

        topics = st.session_state.topics

        for i, topic in enumerate(topics):
            score = topic.get("post_worthiness", 0)
            score_cls = "high" if score >= 7 else "mid" if score >= 5 else "low"
            angles = topic.get("key_angles", [])
            angles_text = " | ".join(angles[:2]) if angles else ""

            col_main, col_btn = st.columns([5, 1])

            with col_main:
                st.markdown(f"""
<div class="topic-card">
    <div class="topic-title">{topic['title']} <span class="score-badge {score_cls}">{score}/10</span></div>
    <div class="topic-summary">{topic['summary']}</div>
    <div class="topic-angles">Angles: {angles_text}</div>
</div>
""", unsafe_allow_html=True)

            with col_btn:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Generate ✍️", key=f"topic_{i}", use_container_width=True):
                    st.session_state.selected_topic_idx = i
                    st.session_state.posts = None
                    st.rerun()

    # --- Step 3: Generate Posts ---
    if st.session_state.selected_topic_idx is not None and st.session_state.posts is None:
        topic = st.session_state.topics[st.session_state.selected_topic_idx]

        with st.spinner(f"Generating 4 post versions for \"{topic['title']}\"..."):
            posts_data = generate_posts(topic, api_key)
            st.session_state.posts = posts_data.get("posts", [])
            st.rerun()

    # --- Step 4: Show Posts ---
    if st.session_state.posts:
        topic = st.session_state.topics[st.session_state.selected_topic_idx]
        st.markdown(f'<div class="section-header">Your LinkedIn Posts — {topic["title"]}</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-sub">Each version has a different angle. Pick the one that feels right, copy it, and post!</div>', unsafe_allow_html=True)

        cols = st.columns(2)

        for i, post in enumerate(st.session_state.posts):
            with cols[i % 2]:
                angle = post.get("angle", "Unknown")
                version = post.get("version", i + 1)

                st.markdown(f"""
<div class="post-card">
    <div class="post-card-header">
        <div class="angle-tag">{angle}</div>
        <div class="version-num">Version {version}</div>
    </div>
    <div class="linkedin-preview">
        <div class="linkedin-avatar">A</div>
        <div>
            <div class="linkedin-name">Armaan Vala</div>
            <div class="linkedin-headline">AI Engineer</div>
        </div>
    </div>
    <div class="post-content">{post["post"]}</div>
</div>
""", unsafe_allow_html=True)

                st.code(post["post"], language=None)

        st.markdown("---")
        col1, col2, col3, col4 = st.columns([1, 1.5, 1.5, 1])
        with col2:
            if st.button("🔄  Regenerate Posts", use_container_width=True):
                st.session_state.posts = None
                st.rerun()
        with col3:
            if st.button("⬅️  Back to Topics", use_container_width=True):
                st.session_state.posts = None
                st.session_state.selected_topic_idx = None
                st.rerun()


if __name__ == "__main__":
    main()
