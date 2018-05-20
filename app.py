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

import random
import os
import psycopg2

SEC = os.getenv('CAT')
SEC_CS = os.getenv('CS')

import deepcut

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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    a = event.message.text
    DATABASE_URL = os.environ['DATABASE_URL']
    
    def inputmes():
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        except:
            print("I am unable to connect to the database")
        cur = conn.cursor()
        
        cur.execute("CREATE TABLE IF NOT EXISTS inputmes (word text);")

        cur.execute("INSERT INTO inputmes VALUES (%(str)s);", {'str':a})
        conn.commit()
        
        cur.close()
        conn.close()
    
    def pocha():
        B = deepcut.tokenize(a)
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        except:
            print("I am unable to connect to the database")
        cur = conn.cursor()
    
        cur.execute("CREATE TABLE IF NOT EXISTS pocha (kam text, prapet INT);")
      
        for C in B:
            cur.execute("INSERT INTO pocha VALUES (%(str)s);", {'str':C})
        conn.commit()
    
        #delete duplicate record using code from https://stackoverflow.com/questions/6583916/delete-duplicate-records-in-postgresql
        cur.execute("DELETE FROM pocha a USING (SELECT MIN(ctid) as ctid, kam FROM pocha GROUP BY kam HAVING COUNT(*) > 1) b WHERE a.kam = b.kam AND a.ctid <> b.ctid;")
        conn.commit()
    
        cur.close()
        conn.close()
        
    def out():
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        except:
            print("I am unable to connect to the database")
        cur = conn.cursor()
        
        cur.execute("SELECT kam FROM pocha WHERE prapet IS NULL;")
        m = cur.fetchall()
        b = []
        for x in m:
            b.append(x)
        c = [str(x)[2:-3] for x in b]
        conn.commit()
        cur.close()
        conn.close()
        return c

    def kamout(L):
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        except:
            print("I am unable to connect to the database")
        cur = conn.cursor()
        
        cur.execute("SELECT kam FROM pocha WHERE prapet = %(lektan)s;", {'lektan':L})
        m = cur.fetchall()
        b = []
        for x in m:
            b.append(x)
        c = [str(x)[2:-3] for x in b]
        conn.commit()
        cur.close()
        conn.close()
        return c
    
    def ran(S):
        b = random.choice(S)
        return b
        
    inputmes()
    pocha()
    I = deepcut.tokenize(a)
    def vicr():
        for x in I:
            if x in kamout(1):
                n = "คุณกำลังพูดถึง" + I[I.index(x)]
        return n
    
    def vi():
        for x in I:
            if x in kamout(3):
                n = "คุณกำลังพูดถึง การ" + I[I.index(x)] + " หรือความ" + I[I.index(x)]
        return n
    i = vicr()
    t = vi()
    
    
    #i = ran(kamout(1))
    #t = ran(kamout(2))
    #w = ran(kamout(3))
    #k = ran(kamout(4))
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text = i + t))
    
    
if __name__ == "__main__":
    app.run()
