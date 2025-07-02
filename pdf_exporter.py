from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.utils import ImageReader

def wrap_text(text, font_name, font_size, max_width):
    lines = []
    for paragraph in text.split('\n'):
        words = paragraph.split()
        line = ''
        for word in words:
            test_line = f'{line} {word}'.strip()
            if stringWidth(test_line, font_name, font_size) <= max_width:
                line = test_line
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines

def save_to_pdf(title, summary, body, filename, corrected_text=None, sentiment=None, sentiment_explanation=None, emotions=None, wordcloud_img_path=None, emotion_graph_img_path=None):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    y = height - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, title)
    y -= 30
    c.setFont("Helvetica-Oblique", 12)
    c.drawString(50, y, f"Summary: {summary}")
    y -= 40
    c.setFont("Helvetica", 11)
    max_width = width - 100
    # Raw transcript
    c.drawString(50, y, "Raw Transcript:")
    y -= 20
    for line in wrap_text(body, "Helvetica", 11, max_width):
        if y < 50:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 11)
        c.drawString(50, y, line)
        y -= 20
    # Grammar-corrected transcript
    if corrected_text:
        y -= 20
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Corrected Transcript:")
        y -= 20
        c.setFont("Helvetica", 11)
        for line in wrap_text(corrected_text, "Helvetica", 11, max_width):
            if y < 50:
                c.showPage()
                y = height - 50
                c.setFont("Helvetica", 11)
            c.drawString(50, y, line)
            y -= 20
    # Sentiment and emotions
    if sentiment or emotions:
        y -= 20
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Analysis:")
        y -= 20
        c.setFont("Helvetica", 11)
        if sentiment:
            c.drawString(50, y, f"Sentiment: {sentiment}")
            y -= 20
        if sentiment_explanation:
            for line in wrap_text(sentiment_explanation, "Helvetica", 11, max_width):
                if y < 50:
                    c.showPage()
                    y = height - 50
                    c.setFont("Helvetica", 11)
                c.drawString(70, y, line)
                y -= 20
        if emotions:
            c.drawString(50, y, "Top Emotions:")
            y -= 20
            for emo, score in emotions:
                c.drawString(70, y, f"{emo}: {score:.2f}")
                y -= 20
    # Word cloud image
    if wordcloud_img_path:
        y -= 30
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Word Cloud:")
        y -= 220
        try:
            c.drawImage(ImageReader(wordcloud_img_path), 50, y, width=400, height=200)
            y -= 20
        except Exception as e:
            c.drawString(50, y, f"[Could not render word cloud: {e}]")
            y -= 20
    # Emotion graph image
    if emotion_graph_img_path:
        img_width = 400
        img_height = 180
        margin = 30
        # Check if there's enough space, else start a new page
        if y - img_height - margin < 50:
            c.showPage()
            y = height - 50
        y -= margin
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Emotion Graph:")
        y -= (img_height + 10)
        try:
            c.drawImage(ImageReader(emotion_graph_img_path), 50, y, width=img_width, height=img_height)
            y -= 20
        except Exception as e:
            c.drawString(50, y, f"[Could not render emotion graph: {e}]")
            y -= 20
    c.save()