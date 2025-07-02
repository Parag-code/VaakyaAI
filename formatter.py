from transformers import pipeline
from textblob import TextBlob
import re
import nltk
from nltk.tokenize import sent_tokenize

# Correct grammar using TextBlob
def correct_grammar(text):
    blob = TextBlob(text)
    return str(blob.correct())

# Summarizer from Hugging Face
# summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small")

# Sentiment analysis pipeline (multilingual)
sentiment_pipeline = pipeline("sentiment-analysis", model="cardiffnlp/twitter-xlm-roberta-base-sentiment")

# Emotion analysis pipeline (English only)
emotion_pipeline = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)

def analyze_sentiment(text):
    result = sentiment_pipeline(text)
    label = result[0]["label"]
    score = result[0]["score"]
    # Map model labels to user-friendly ones
    if label.lower().startswith("positive"):
        sentiment = "Positive"
        explanation = f"The text expresses positive emotions or opinions."
    elif label.lower().startswith("negative"):
        sentiment = "Negative"
        explanation = f"The text expresses negative emotions or opinions."
    else:
        sentiment = "Neutral"
        explanation = f"The text is neutral, with no strong positive or negative emotions."
    return sentiment, score, explanation

def analyze_emotions(text):
    results = emotion_pipeline(text)
    # results is a list of list of dicts (for each input sentence)
    # We'll aggregate scores for each emotion
    emotion_scores = {}
    for sentence_scores in results:
        for item in sentence_scores:
            label = item['label']
            score = item['score']
            if label not in emotion_scores:
                emotion_scores[label] = 0.0
            emotion_scores[label] += score
    # Normalize by number of sentences
    num_sentences = len(results)
    for label in emotion_scores:
        emotion_scores[label] /= num_sentences
    # Sort by score
    sorted_emotions = sorted(emotion_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_emotions

def split_sentences(text):
    # Use nltk for robust sentence splitting
    return sent_tokenize(text)