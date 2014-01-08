def makeConn(db):
  conn = pymysql.connect(host = '152.2.15.164' , user = 'charlesczysz' , passwd = 'CharlesSquared' , database = db)
  cur = conn.cursor()
  return [conn,cur]

import pymysql
