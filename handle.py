# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import web
import reply
import receive
import sae.const
import MySQLdb


class Handle(object):
    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "{"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "helloshfscut"

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            print "handle/GET func: hashcode, signature: ", hashcode, signature
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception, Argument:
            return Argument
	
    def POST(self):
        try:
            webData = web.data()
            print "Handle Post webdata is ", webData
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                content = None
                db=MySQLdb.connect(sae.const.MYSQL_HOST, sae.const.MYSQL_USER, sae.const.MYSQL_PASS, sae.const.MYSQL_DB)
                cursor=db.cursor()
                sql_query="SELECT * FROM switch where id=1"
                sql_update_1="UPDATE switch set state=1 where id=1"
                sql_update_0="UPDATE switch set state=0 where id=1"
                arduino_id, arduino_state=None, None
                try:
                    cursor.execute(sql)
                    results=cursor.fetchall()
                    for row in results:
                        arduino_id=row[0]
                        arduino_state=row[1]
                except:
                    content = "Error: unable to fetch data"
                if recMsg.Content=="open":
                    if arduino_state != 1:
                        
                        try:
                            cursor.execute(sql_update)
                            db.commit()
                        except:
                            db.rollback()
                elif recMsg.Content=="close":
                    if arduino_state != 0:
                        
                        try:
                            cursor.execute(sql_update)
                            db.commit()
                        except:
                            db.rollback()
                else:
                    content = recMsg.Content
                try:
                    cursor.execute(sql)
                    results=cursor.fetchall()
                    for row in results:
                        arduino_id=row[0]
                        arduino_state=row[1]
                    content = "arduino_state:"+str(arduino_state)
                except:
                    content = "Error: unable to fetch data"
                db.close()
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return replyMsg.send()
            else:
                print "暂且不处理"
                return "success"
        except Exception, Argment:
            return Argment