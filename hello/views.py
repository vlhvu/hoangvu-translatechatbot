from django.shortcuts import render
from django.http import HttpResponse
import pychatwork as ch
from django.views.decorators.csrf import csrf_exempt
import json
from googletrans import Translator
from langdetect import detect

from .models import Greeting

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    payload = str(request.body, encoding='utf-8')
    return render(request, "index.html")


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
# Create your views here.
def decode_payload(request):
    payload = str(request.body, encoding='utf-8')
    return json.loads(payload)

@csrf_exempt
def chatwork_webhook(request):
    payload = decode_payload(request)
    messageChat = payload["webhook_event"]["body"]
    messageChat1 = messageChat.replace("[To:5130876]Bot_Translate","")

    translator = Translator()
    lang = detect(messageChat1)
    locale = "vi"
    if lang == "vi":
        locale = "ja"
    translated = translator.translate(messageChat1, src=lang, dest=locale)
    #Send Data back to chatwork
    client = ch.ChatworkClient('2cba8973da48609ecb1415490a15a331')
    # get message from room 1234
    res = client.get_messages(room_id='197925987', force=True)

    # post message to room 1234
    client.post_messages(room_id='197925987', message=translated.text)

    return HttpResponse('Webhook received', status=200)
