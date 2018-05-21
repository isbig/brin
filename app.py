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
        
        cur.execute("CREATE TABLE IF NOT EXISTS inputmes (word text, time TIMESTAMP NOT NULL);")

        cur.execute("INSERT INTO inputmes (word, time) VALUES (%(str)s, NOW());", {'str':a})
        conn.commit()
        
        cur.close()
        conn.close()
        
    def usinputcur():
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        except:
            print("I am unable to connect to the database")
        cur = conn.cursor()
        
        #from https://stackoverflow.com/questions/6267887/get-last-record-of-a-table-in-postgres
        cur.execute("SELECT word FROM inputmes ORDER BY time DESC LIMIT 1;")
        m = cur.fetchall()
        n = str(m)[3:-4]
        conn.commit()
        cur.close()
        conn.close()
        return n
        
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
        
    def inputoutmes(q):
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        except:
            print("I am unable to connect to the database")
        cur = conn.cursor()
        
        cur.execute("CREATE TABLE IF NOT EXISTS inputoutmes (word text, time TIMESTAMP NOT NULL);")

        cur.execute("INSERT INTO inputoutmes (word, time) VALUES (%(str)s, NOW());", {'str':q})
        conn.commit()
        
        cur.close()
        conn.close()
        
    def usinputoutcur():
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        except:
            print("I am unable to connect to the database")
        cur = conn.cursor()
        
        #from https://stackoverflow.com/questions/6267887/get-last-record-of-a-table-in-postgres
        cur.execute("SELECT word FROM inputoutcur ORDER BY time DESC LIMIT 1;")
        m = cur.fetchall()
        n = str(m)[3:-4]
        conn.commit()
        cur.close()
        conn.close()
        return n
    
    def ran(S):
        b = random.choice(S)
        return b
        
    inputmes()
    pocha()
   
    z = usinputcur()
    s = deepcut.tokenize(z)

    def vicr(P, G):
        v = [x for x in P if x in G]
        return v
    
    t = vicr(s, out())
    e = vicr(s, kamout(1))
    z = vicr(s, kamout(2))
    c = vicr(s, kamout(3))    

    def pood():
        if e == [] and c != []:
            u = "อะไรหรือใครที่" + ''.join(z) + ''.join(c)
            return u
        if e != [] and c == []:
            w = e[0] + "ทำอะไร"
            return w
        if e == [] and c == []:
            q = "ใครทำอะไร"
            return q
        if e != [] and c != []:
            y = "แล้วยังไงต่อ"
            return y
            
    # มีคำที่ไม่รู้ประเภทหรือไม่ ถ้าไม่มี ถ้ามีให้ถามว่าเป็นคำประเภทใด
    def kwam():
        if t == []:
            ka = pood()
            return ka
        elif t != []:
            try:
                m = random.choice(t) + " เป็นคำประเภทใด"
            except IndexError:
                pass
            return m
    
    kamkorn = usinputoutcur()
    
    # มีประโยคที่รู้จักหรือไม่
    def first():
        #i เปน q แรก    
        i = kamkorn[0]
        if z == i + " เป็นคำประเภท 1":
            # เก็บค่า r ให้ i ในตาราง pocha
            n = "ขอบคุณที่ให้ข้อมูลว่า " + i + " เป็นคำประเภท " + 1
            return n
        elif z != i + " เป็นคำประเภท 1":
            return kwam()
            
    q = first()

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text = q))
    
    inputoutmes(q)
    
        
if __name__ == "__main__":
    app.run()
