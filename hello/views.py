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
    print(messageChat)
    # messageChat1 = messageChat.replace("[To:5130876]Bot_Translate","")

    if "\u0020" in messageChat:
        return HttpResponse('Webhook received', status=200)

    translator = Translator()
    lang = detect(messageChat)

    locale = "vi"
    if lang == "vi":
        locale = "ja"
    translated = translator.translate(messageChat, src=lang, dest=locale).text + "\u0020"

    #Send Data back to chatwork
    client = ch.ChatworkClient('fd0602c43dd83cae39e7ebfb08d5793d')
    # get message from room 1234
    res = client.get_messages(room_id='197925987', force=True)
    print(translated)
    # post message to room 1234
    client.post_messages(room_id='197925987', message=translated)

    return HttpResponse('Webhook received', status=200)
