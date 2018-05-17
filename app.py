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

import os
SEC = os.getenv('CAT')
SEC_CS = os.getenv('CS')

app = Flask(__name__)

line_bot_api = LineBotApi(SEC)
handler = WebhookHandler(SEC_CS)


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

import psycopg2

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    a = event.message.text
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
    
    DATABASE_URL = os.environ['DATABASE_URL']

    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    except:
        print("I am unable to connect to the database")
    
    cur = conn.cursor()
<<<<<<< HEAD
=======

<<<<<<< HEAD
>>>>>>> parent of 0c5b1c4... Revert "try to use IF NOT EXISTS"
    cur.execute("CREATE TABLE IF NOT EXISTS inputmes (word text);")
=======
    try:
        cur.execute("CREATE TABLE inputmes (word text);")
    except psycopg2.ProgrammingError:
        conn.rollback()
    
>>>>>>> parent of 4e74bda... try to use IF NOT EXISTS
    cur.execute("INSERT INTO inputmes VALUES (%(str)s);", {'str':a})
    
<<<<<<< HEAD
<<<<<<< HEAD
    cur.execute("CREATE TABLE IF NOT EXISTS pocha (kam);")
    cur.execute("INSERT INTO pocha SELECT DISTINCT word FROM inputmes;")
    
=======
    cur.execute("CREATE TABLE IF NOT EXISTS pocha (kam) AS SELECT DISTINCT word FROM inputmes;")
>>>>>>> parent of 0c5b1c4... Revert "try to use IF NOT EXISTS"
=======
    try:
        cur.execute("CREATE TABLE pocha (kam) AS SELECT DISTINCT word FROM inputmes;")
    except psycopg2.ProgrammingError:
        conn.rollback()

>>>>>>> parent of 4e74bda... try to use IF NOT EXISTS
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    app.run()
