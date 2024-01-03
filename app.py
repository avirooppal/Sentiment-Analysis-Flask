from flask import Flask, render_template, request
from textblob import TextBlob
from dataclasses import dataclass

app = Flask(__name__)

@dataclass
class Mood:
    emoji: str
    sentiment: float

def get_mood(input_text: str, *, threshold: float) -> Mood:
    sentiment: float = TextBlob(input_text).sentiment.polarity

    friendly_threshold: float = threshold
    hostile_threshold: float = -threshold

    if sentiment >= friendly_threshold:
        return Mood('😊 Happy', sentiment)
    elif sentiment <= hostile_threshold:
        return Mood('😠 Unhappy', sentiment)
    else:
        return Mood('😐 Neutral', sentiment)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        mood = get_mood(text, threshold=0.3)
        return render_template('result.html', emoji=mood.emoji, sentiment=mood.sentiment, input_text=text)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
