def makeConn(db):
  conn = pymysql.connect(host = <hostip> , user = <user> , passwd = <passwd> , database = <db>)
  cur = conn.cursor()
  return [conn,cur]

import pymysql
