import sys
import pymysql
import connect
import random

file = sys.argv[-1]

[conn,cur] = connect.makeConn('ld')
wrong = 0
with open(file,'r') as f:
  
  for line in f:
    if random.randrange(0,10) > 3:
      continue

    data = line.strip().split('\t')

    sql = "select %s from blocks where rsid='%s'"

    cur.execute(sql % (data[0],data[1]))

    result = cur.fetchall()

    if int(result[0][0]) == int(data[2]):
        pass
    else:
      wrong+=1

    sql = "select %s from blocks where rsid='%s'"

    cur.execute(sql % (data[0],data[3]))

    result = cur.fetchall()

    if int(result[0][0]) == int(data[4]):
        pass
    else:
      wrong+=1



print(wrong)
