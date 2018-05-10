from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import os.path
from boto.s3.connection import S3Connection
s3 = S3Connection(os.environ['CAT'], os.environ['CS'])

bucket = s3.create_bucket('CATCS')

from boto.s3.key import Key
k = key(bucket)
k.key = 'CAT'
m = key(bucket)
m.key = 'CS'


app = Flask(__name__)

line_bot_api = LineBotApi(k.get_contents_as_string())
handler = WebhookHandler(m.get_contents_as_string())


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
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
