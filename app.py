from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FileMessage
)
from chatterbot import ChatBot
from chatterbot.trainers import (ListTrainer, TwitterTrainer)

import psycopg2

# -*- coding: utf-8 -*-
from chatterbot import ChatBot
import logging

logging.basicConfig(level=logging.INFO)

chatbot = ChatBot(
    "molin",
    trainer = 'chatterbot.trainers.ListTrainer',
    database_uri='postgres://lhbvkxmyghvnof:78be1cfb01151074d64ad1bcee4d0e14b83ef949bb6c2eae2ff037f16245bdb1@ec2-75-101-142-91.compute-1.amazonaws.com:5432/d9et88q8kcrht',
    storage_adapter="chatterbot.storage.SQLStorageAdapter")

conversation = ["สวัสดี", "ทำอะไรอยู่", "กินอะไรหรือยัง", "นั่งเล่น", "กินแล้ว", "ฝันดี"]
chatbot.set_trainer(ListTrainer)
chatbot.train(conversation)

chatbot.logger.info('Trained database generated successfully!')

app = Flask(__name__)

line_bot_api = LineBotApi('JUP4WQJpFIadCiuOYhMSdUu52kvj2CXCCXIqW24CdQraXX+ofJpTUGrMPchZHJ22C4r0R0v/HMbF9dBfZRnxDEMz6tiehsbPWD3bZJb2V2D7AyoeIkfa49rHvsdf5ioZyBwKm7unj6aEN6BNJkUbPQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('34d0bb3fdd56fa35bf77bd83b8672ffe')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
        print(body)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    a = str(chatbot.get_response(event.message.text))
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=a))

@handler.add(MessageEvent, message=FileMessage)
def handled(event):
    a = event.message.id
    message_content = line_bot_api.get_message_content(a)
    with open(file_path, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)

if __name__ == "__main__":
    app.run()
