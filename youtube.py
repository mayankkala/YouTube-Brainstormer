from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_output(query, transcript, prompt):
    response = model.generate_content([query, transcript, prompt])
    return response.text

def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("v=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for entry in transcript_text:
            transcript += " " + entry["text"]

        return transcript

    except Exception as e:
        raise e

st.set_page_config('YouTube Video')
st.header("Brainstorm with YouTube Video")
input_text = st.text_input("Write your question here...")
input_link = st.text_input("Paste your YouTube video link here")
input_prompt = """
 You are an expert in understanding transcripts. Now you need to help the user by answering their questions in a structured and detailed way.
 """

if input_link:
    video_id = input_link.split("v=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

submit_button = st.button("Submit")

if submit_button and input_link:
    try:
        transcript_text = extract_transcript_details(input_link)        
        response = model.generate_content([input_text, transcript_text, input_prompt])
        st.subheader("The response is:")
        st.write(response.text)
    
    except Exception as e:
        st.error(f"Error processing YouTube video data: {e}")

elif submit_button and not input_link:
    st.error("Please provide a YouTube video link.")
