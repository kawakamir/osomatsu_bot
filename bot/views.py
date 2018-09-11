from django.shortcuts import render
from django.http import HttpResponse
import json
import random
import requests
from bot.load_serif import osomatsu_serif  # 先ほどのおそ松のセリフ一覧をimport


# Create your views here.

def index(request):
    return HttpResponse("This is bot api.")


def callback(request):
    reply = ""
    request_json = json.loads(request.body.decode('utf-8')) # requestの情報をdict形式で取得
    for e in request_json['events']:
        reply_token = e['replyToken']  # 返信先トークンの取得
        message_type = e['message']['type']   # typeの取得

        if message_type == 'text':
            text = e['message']['text']    # 受信メッセージの取得
            reply += reply_text(reply_token, text)   # LINEにセリフを送信する関数
    return HttpResponse(reply)  # テスト用


REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
ACCESS_TOKEN = 'ENTER YOUR Channel Access Token'
HEADER = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + ACCESS_TOKEN
}

def reply_text(reply_token, text):
    reply = random.choice(osomatsu_serif)
    payload = {
          "replyToken":reply_token,
          "messages":[
                {
                    "type":"text",
                    "text": reply
                }
            ]
    }

    requests.post(REPLY_ENDPOINT, headers=HEADER, data=json.dumps(payload)) # LINEにデータを送信
    return reply
