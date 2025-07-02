# VaakyaAI – Speak, Analyze, Understand 🎙️

> Speak naturally, and let AI write it beautifully for you.

---

## 🧠 Overview

**VaakyaAI** is an AI-powered voice journaling and analysis tool that helps you convert spoken audio into grammatically correct, emotionally intelligent text. It analyzes your tone, detects emotions, creates word clouds, and exports everything as a structured PDF.

---

## ✨ Features

- 🎤 **Voice-to-Text Transcription**  
  Upload `.wav` audio and get real-time transcription using Google’s Speech Recognition.

- 📝 **Grammar Correction**  
  Automatically corrects grammatical errors using TextBlob.

- ☁️ **Word Cloud Generation**  
  Generates a word cloud from your transcript for visual insight.

- 😊 **Sentiment Analysis**  
  Classifies the sentiment as Positive, Neutral, or Negative with reasoning.

- 💬 **Emotion Detection**  
  Detects and visualizes emotions such as Joy, Anger, Sadness using HuggingFace models.

- 📄 **Export to PDF**  
  Download a well-formatted PDF report with all text and visual analysis included.

---

## 🛠 Tech Stack

| Area               | Technology                                  |
|--------------------|---------------------------------------------|
| Web Interface      | Streamlit                                   |
| NLP / AI Models    | Hugging Face Transformers, TextBlob         |
| Audio Processing   | SpeechRecognition, PyDub                    |
| Visualizations     | WordCloud, Matplotlib                       |
| PDF Export         | ReportLab                                   |
| Utilities          | NLTK, tempfile, NumPy                       |
| Programming Lang   | Python 3.9+                                 |

---

## 🔍 Sample Input & Output

### 🎧 Input
A `.wav` audio file:
> “I’m feeling quite excited today. The project went really well!”

### 🧾 Output

- **Transcribed Text**:  
  `I’m feeling quite excited today. The project went really well!`

- **Corrected Transcript**:  
  `I'm feeling quite excited today. The project went really well!`

- **Sentiment**:  
  `Positive (0.91)`  
  _The text expresses positive emotions or opinions._

- **Top Emotions**:  
  `Joy (0.76), Optimism (0.64), Excitement (0.58)`

- **PDF Export**:  
  📄 A clean, downloadable report with text, visuals, and emotion insights.

---
