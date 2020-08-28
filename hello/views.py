from django.shortcuts import render
from django.http import HttpResponse
from .models import Greeting

from googletrans import Translator
from django.views.decorators.csrf import csrf_exempt
from langdetect import detect
import json
import pychatwork as ch

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
    #messageChat1 = messageChat.replace("[To:5130876]Bot_Translate","")
    messageChat2 = messageChat.replace("translated","")

    translator = Translator()
    lang = detect(messageChat2)

    locale = "vi"
    if lang == "vi":
        locale = "ja"
    translated = translator.translate(messageChat2, src=lang, dest=locale)
    #Send Data back to chatwork
    client = ch.ChatworkClient('fd0602c43dd83cae39e7ebfb08d5793d')
    # get message from room 1234
    res = client.get_messages(room_id='197925987', force=True)

    # post message to room 1234
    client.post_messages(room_id='197925987', message=translated.text)

    return HttpResponse('Webhook received', status=200)
