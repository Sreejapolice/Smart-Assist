# smart_assist_app.py

import streamlit as st
from googleapiclient.discovery import build
import random

# YouTube API Setup (replace with your actual key)
YOUTUBE_API_KEY = “YOUR_API_KEY_HERE”
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def search_youtube(query):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=YOUTUBE_API_KEY)
    search_response = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        videoDuration="medium",  # medium = 4–20 minutes; use "long" for >20 mins
        maxResults=5
    ).execute()

    for item in search_response.get("items", []):
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        return f"https://www.youtube.com/watch?v={video_id}", title

    return None, None

def generate_realistic_mcqs(topic):
    mcqs = []
    keywords = topic.split()[:4]  # Take first 4 keywords from the topic

    for i in range(5):
        question = f"What is an important point about {topic}?"

        # Pick one keyword to base this question on
        word = random.choice(keywords)

        # Now use this keyword to form options
        options = [
            f"{word} explanation",
            f"Definition of {word}",
            f"{word} in daily life",
            f"Wrong concept about {word}"
        ]
        correct = options[0]
        random.shuffle(options)

        mcqs.append({
            "question": question,
            "options": options,
            "answer": correct
        })

    return mcqs


# UI
st.set_page_config(page_title="SMART ASSIST", layout="centered")
st.title("📺 SMART ASSIST")
st.caption("Ensuring continuous classroom learning using YouTube & Quizzes")

query = st.text_input("👩‍🏫 Enter your lesson topic (e.g., 'Photosynthesis for Class 8'):")

if query:
    video_url, video_title = search_youtube(query)
    if video_url:
        st.video(video_url)
        st.success(f"🎬 Playing: {video_title}")

        if st.button("🧠 Generate Quiz"):
            st.session_state["mcqs"] = generate_realistic_mcqs(query)

if "mcqs" in st.session_state:
    st.subheader("📝 Quiz Time")
    answers = []
    for idx, mcq in enumerate(st.session_state["mcqs"], 1):
        choice = st.radio(f"{idx}. {mcq['question']}", mcq["options"], key=f"q{idx}")
        answers.append((mcq["question"], choice, mcq["answer"]))

    if st.button("✅ Submit Answers"):
        score = sum([1 for _, selected, correct in answers if selected == correct])
        st.success(f"You scored {score}/5 ✅")
