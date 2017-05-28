from flask import Flask, request
from watson_developer_cloud import ConversationV1, ToneAnalyzerV3
import requests, json

app = Flask(__name__)

ACCESS_TOKEN = "EAAEbpvAZCHIcBAOdDzq3rduzWMsbZCtXS32K68r8HW8GoHnfJH7gFVdOv7nrZBKbO7qpYW3oI4x8HUcGda5DFljZAUGrq5z8h9uskfLlbqM278o70VRLGPkwIqOt1wYT937Lm7KTiFo5YEbw3Kbg3okkPI45SMyEV7O2nKjITwZDZD"

conversation = ConversationV1(
    username='f6c37b3c-273c-4df0-ba2f-d23402b57263',
    password='g3SUoO2hnKj2',
    version='2017-04-21')


tone_analyzer = ToneAnalyzerV3(
    username='4d70fcda-bafc-4159-bddd-b4a321193cb6',
    password='eqJ6PHWv8rhY',
    version='2016-02-11')

# replace with your own workspace_id
workspace_id = '32db12f1-71f6-44eb-a507-2af675c7b65a'
context = {}

@app.route('/', methods=['GET'])
def handle_verification():
    return request.args['hub.challenge']


def reply(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(resp.content)


@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = request.json
    sender = data['entry'][0]['messaging'][0]['sender']['id']
    message = data['entry'][0]['messaging'][0]['message']['text']
    global context
    tone = tone_analyzer.tone(text=message)
    max_emotion_id = None
    tone_cats = tone['document_tone']['tone_categories']

    max_emot_score = 0
    for tone_cat in tone_cats:
                if tone['score'] > max_emot_score:
        if tone_cat['category_id'] == 'emotion_tone':
            for tone in tone_cat['tones']:
                    max_emot_score = tone['score']
                    eeemax_emotion_id = tone['tone_id']
    emotion_context = {"emotion": {"current": max_emotion_id}}
    context["user"] = emotion_context
    response = conversation.message(workspace_id=workspace_id, message_input={'text': message}, context=context)
    context = response['context']
    '''
    max_intent = None
    max_conf = 0
    for conf, intent in response:
        if conf > max_conf:
            max_conf = conf
            max_intent = intent
    '''

    reply(sender, response['output']['text'][0])

    return "ok"


if __name__ == '__main__':
    app.run(debug=True)
