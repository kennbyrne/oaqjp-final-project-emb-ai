"""Flask server for emotion detection."""

from flask import Flask, render_template, request
from EmotionDetection import emotion_detector

app = Flask(__name__)

@app.route('/')
def index():
    """Render the index.html template."""
    return render_template('index.html')

@app.route('/emotionDetector', methods=['GET'])
def emotion_detector_route():
    """Handle emotion detection requests."""
    text_to_analyze = request.args.get('textToAnalyze', '')
    result = emotion_detector(text_to_analyze)

    if result is None or result.get('dominant_emotion') is None:
        return "Invalid text! Please try again."

    dominant_emotion = result.pop('dominant_emotion')

    response_text = "For the given statement, the system response is "
    for emotion, score in result.items():
        response_text += f"'{emotion}': {score}, "
    response_text = response_text[:-2]
    response_text += f". The dominant emotion is {dominant_emotion}."

    return response_text

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5051)
