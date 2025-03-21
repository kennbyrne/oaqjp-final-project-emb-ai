from flask import Flask, render_template, request, jsonify
from EmotionDetection import emotion_detector

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/emotionDetector', methods=['GET'])  
def emotionDetector():
    text_to_analyze = request.args.get('textToAnalyze')  

    if not text_to_analyze:  
        return "Please provide text to analyze."

    result = emotion_detector(text_to_analyze)

    if result is None:
        return "Invalid text! Please try again."

    dominant_emotion = result['dominant_emotion']
    del result['dominant_emotion']

    response_text = f"For the given statement, the system response is "
    for emotion, score in result.items():
        response_text += f"'{emotion}': {score}, "
    response_text = response_text[:-2]
    response_text += f". The dominant emotion is {dominant_emotion}."

    return response_text

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)