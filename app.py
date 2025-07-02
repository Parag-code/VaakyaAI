import streamlit as st
from audio_processor import transcribe_audio
from pdf_exporter import save_to_pdf
from formatter import analyze_sentiment, analyze_emotions, split_sentences
import os
import nltk
from wordcloud import WordCloud
from textblob import TextBlob
import matplotlib.pyplot as plt
import tempfile
import numpy as np
nltk.download('punkt')

st.set_page_config(page_title="VaakyaAI", layout="centered")

st.image("logo.png", width=200)

st.title("VaakyaAI – Speak, Analyze, Understand")
st.markdown("Speak naturally, and let AI write it beautifully for you.")

# Use session_state to store transcript and file name
if 'raw_text' not in st.session_state:
    st.session_state['raw_text'] = ''
if 'audio_filename' not in st.session_state:
    st.session_state['audio_filename'] = None

audio_file = st.file_uploader("Upload your voice (.wav)", type=["wav"])

if audio_file:
    # Only transcribe if a new file is uploaded
    if audio_file.name != st.session_state['audio_filename']:
        with st.spinner("Transcribing your audio..."):
            st.session_state['raw_text'] = transcribe_audio(audio_file, language="en")
        st.session_state['audio_filename'] = audio_file.name
    raw_text = st.session_state['raw_text']
    st.subheader("📝 Transcribed Text")
    st.text_area("Raw Transcript", value=raw_text, height=300)

    # Grammar Correction
    st.subheader("📝 Grammar Correction")
    corrected_text = str(TextBlob(raw_text).correct())
    st.text_area("Corrected Transcript", value=corrected_text, height=300)

    # Word Cloud Visualization
    st.subheader("☁️ Word Cloud")
    wordcloud_img_path = None
    if raw_text.strip():
        wc = WordCloud(width=800, height=300, background_color='white').generate(raw_text)
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.imshow(wc, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)
        # Save word cloud image to temp file for PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_img:
            wc.to_file(tmp_img.name)
            wordcloud_img_path = tmp_img.name
    else:
        st.write("No words to display in word cloud.")

    # Sentiment Analysis
    sentiment, score, explanation = analyze_sentiment(raw_text)
    st.markdown(f"**Sentiment:** {sentiment} ({score:.2f})")
    st.info(explanation)

    # Emotion Analysis
    st.subheader("🔎 Emotion Analysis")
    emotions = analyze_emotions(raw_text)
    emotion_graph_img_path = None
    if emotions:
        st.bar_chart({e[0]: e[1] for e in emotions})
        st.markdown(
            "**Top Emotions:** " + ", ".join([f"{e[0]} ({e[1]:.2f})" for e in emotions[:3]])
        )
        # Save emotion bar chart as image for PDF
        labels = [e[0] for e in emotions]
        scores = [e[1] for e in emotions]
        fig2, ax2 = plt.subplots(figsize=(8, 3))
        ax2.bar(labels, scores, color='skyblue')
        ax2.set_ylabel('Score')
        ax2.set_title('Emotion Scores')
        plt.tight_layout()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_img2:
            fig2.savefig(tmp_img2.name)
            emotion_graph_img_path = tmp_img2.name
        plt.close(fig2)
    else:
        st.write("No emotions detected.")

    st.subheader("📤 Export")
    if st.button("Export as PDF"):
        title = "Transcript"
        summary = ""
        body = raw_text
        filename = f"{title.replace(' ', '_')}.pdf"
        save_to_pdf(
            title,
            summary,
            body,
            filename,
            corrected_text=corrected_text,
            sentiment=sentiment,
            sentiment_explanation=explanation,
            emotions=emotions[:3] if emotions else None,
            wordcloud_img_path=wordcloud_img_path,
            emotion_graph_img_path=emotion_graph_img_path
        )
        with open(filename, "rb") as f:
            st.download_button("Download PDF", f, filename, "application/pdf")