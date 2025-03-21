import requests
import json
import re

def emotion_detector(text_to_analyze):
 
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = {"raw_document": {"text": text_to_analyze}}

    try:
        response = requests.post(url, headers=headers, json=input_json)
        response.raise_for_status()
        result = response.json()
        if 'emotionPredictions' in result and result['emotionPredictions']:
            emotions = result['emotionPredictions'][0]['emotion']
            emotion_scores = {
                'anger': emotions.get('anger', 0),
                'disgust': emotions.get('disgust', 0),
                'fear': emotions.get('fear', 0),
                'joy': emotions.get('joy', 0),
                'sadness': emotions.get('sadness', 0)
            }
            dominant_emotion = max(emotion_scores, key=emotion_scores.get)
            emotion_scores['dominant_emotion'] = dominant_emotion

            # Check for blank input
            if not text_to_analyze.strip():
                return {'anger': None, 'disgust': None, 'fear': None, 'joy': None, 'sadness': None, 'dominant_emotion': None}

            # Check for garbelled input
            if re.search(r'^[a-zA-Z0-9\s.,!?]*$', text_to_analyze) is None:
                return {'anger': None, 'disgust': None, 'fear': None, 'joy': None, 'sadness': None, 'dominant_emotion': None}

            return emotion_scores
        else:
            return None
    except requests.exceptions.RequestException as e:
        if response.status_code == 400:
          return {'anger': None, 'disgust': None, 'fear': None, 'joy': None, 'sadness': None, 'dominant_emotion': None}
        print(f"Error during request: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return None
