#!/usr/bin/python
# coding=utf-8
import sys
import time
import sqlite3
import telepot
from pprint import pprint
from datetime import date, datetime
import re
import traceback

ROOT = '/root/git/stock-analyzer/'

def sendMessage(id, msg):
    try:
        bot.sendMessage(id, msg)
    except:
        print str(datetime.now()).split('.')[0]
        traceback.print_exc(file=sys.stdout)

def help(id):
    sendMessage(id, """< Stock analyzer 명령어 >
 /sub : 구독
 /unsub : 구독해제
""")

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return
    #pprint(msg["from"])
    try:
        name = msg["from"]["last_name"] + msg["from"]["first_name"]
    except:
        name = ""

    text = msg['text'].lower()

    args = text.split(' ')
    if text.startswith('/'):
        if text.startswith('/sub'):
            conn = sqlite3.connect(ROOT+'subscribe.db')
            c = conn.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS subscribe( user TEXT, name TEXT, PRIMARY KEY(user) )')
            conn.commit()

                try:
                    c.execute( 'INSERT INTO subscribe (user, name) VALUES ("%s", "%s")'%(chat_id,name) )
                except sqlite3.IntegrityError:
                    # means already inserted
                    sendMessage(chat_id, "동일한 신청목록이 존재합니다.")
                else:
                    # means success
                    conn.commit()
                    sendMessage(chat_id, "성공적으로 추가되었습니다.")

        elif text.startswith('/unsub'):
            conn = sqlite3.connect(ROOT+'subscribe.db')
            c = conn.cursor()
            try:
                c.execute( 'DELETE FROM subscribe WHERE user="%s"'%(chat_id) )
            except sqlite3.IntegrityError:
                # means already inserted
                sendMessage(chat_id, "삭제가 실패했습니다.")
            else:
                # means success
                conn.commit()
                sendMessage(chat_id, "성공적으로 삭제 되었습니다.")

        else:
            help(chat_id)
    else:
        help(chat_id)


TOKEN = sys.argv[1]
print 'received token :', TOKEN

bot = telepot.Bot(TOKEN)
pprint( bot.getMe() )

bot.notifyOnMessage(handle)

print 'Listening...'

while 1:
    time.sleep(10)