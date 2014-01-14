"""
Run using python 3.x

Uses the PyMySQL package to access database, select random ld block, and compare that block with ones generated by the Broad Institute's SNAP program
"""

def getRandomRsids(cur):
  """
  Choose random ld block and write RSIDs to .txt file for submission to
  """
  pops = ['CEU','CHB','JPT','YRI']

  chroms = ['chrX']

  [chroms.append('chr' + str(i)) for i in range(1,23)]

  pop = pops[random.randrange(0,4)]

  chridx = random.randrange(1,24)
  if chridx is 23:
    chrom = 'chrX'
  else:
    chrom = chroms[chridx]

  sql = "select max("+ pop + ") from blocks"
  cur.execute(sql)
  
  for row in cur:
    maxblock = int(row[0])

  block = random.randrange(1,maxblock+1)

  return [pop , chrom, block]


def getTestRsids(cur):

  test_rsids = []

  while len(test_rsids) == 0:
    [pop , chrom , block] = getRandomRsids(cur)
  
    sql = "select blocks.rsid from blocks inner join rsids on blocks.rsid=rsids.rs where blocks.%s=%s and rsids.chrom='%s'"

    cur.execute(sql % (pop,str(block),chrom))

    for row in cur:
      test_rsids.append(row[0])

  return(test_rsids,pop)

def getSNAPResults(test_rsids,pop):
  #Use curl to submit a POST form to SNAP in order to retrieve data via command line

  rsidString = "%0D%0A".join(test_rsids) #joins separate RSIDs into one string separated by returns (required for SNAP POST format)
  hapMapPanel = pop
  if pop is "JPT" or pop is "CHB":
    hapMapPanel = "CHBJPT" #SNAP combines these two groups

  searchString = """
    SearchPairwise=
    &snpList=%s
    &hapMapRelease=onekgpilot
    &hapMapPanel=%s
    &RSquaredLimit=0.8
    &distanceLimit=500000
    &downloadType=File
    &includeQuerySnp=on
    &arrayFilter=query
    &columnList[]=DP
    &columnList[]=GP
    &columnList[]=AM
    &submit=search
    """ % (rsidString , hapMapPanel)

  subprocess.call(["curl","-s","-d",searchString,"-o","SNAPResults.txt","http://www.broadinstitute.org/mpg/snap/ldsearch.php"])
  time.sleep(1) #wait 1 second to prevent server overload

def compareResults():
  
  fh_match = open("match.txt",'w')
  fh_nomatch_num = open('nomatch.txt','w')
  fh_nomatch = open('nomatch_pairs.txt','a+')
  fh_in = open('SNAPResults.txt','r')
  fh_dne = open('dne.txt','w') #file to handle SNPs not in either db
  linenum = 0

  for line in fh_in:
    linenum+=1
    
    if "SNP" in line: #skip first line
      continue
    
    if "Error" in line: #sometimes connection fails, returns file with "Error:" at beginning of second line
      return False

    entries = line.strip().split('\t')
    
    if 'WARNING' in line: #skip lines where rsid doesn't exist in SNAP data
      fh_dne.write('\t'.join([entries[0],entries[1] , str(linenum)]) + '\n')
      continue

    sql = "select %s from blocks where rsid='%s'"
    cur.execute(sql % (pop, entries[0]))

    for row in cur:
      try:
        block1 = int(row[0])
        
      except IndexError: #throws IndexError if SNAP RSID doesn't exist in MySQL db
        fh_dne.write('\t'.join([entries[0] ,entries[1]]),"\n")
        continue
    
    cur.execute(sql % (pop, entries[1]))

    for row in cur:

      try:
        block2 = int(row[0])
        
      except IndexError:
        fh_dne.write(entries[0] + "\t" + entries[1] + "\n")
        continue

      if block1 == block2: #SNAP pairs are in same block in MySQL data
        fh_match.write('\t'.join([entries[0] , entries[1] , str(block1)]) + '\n')

      else: #SNAP pairs are not in the same block
        fh_nomatch_num.write('\t'.join([entries[0] , str(block1) , entries[1] , str(block2)]) + '\n')
        if random.randrange(10) == 1: #write only 10% of nomatch
          fh_nomatch.write(pop +'\t'.join([entries[0] , str(block1) , entries[1] , str(block2)]) + '\n')

  fh_match.close()
  fh_nomatch_num.close()
  fh_nomatch.close()
  fh_in.close()
  fh_dne.close()

def analyzeResults(out):
  
  i = 0 
  with open("match.txt","r") as f:
    for i, l in enumerate(f,start=1):
      pass
  out.write(str(i))
  out.write('\t')
  f.close()

  del i
  i=0
  with open("nomatch.txt","r") as f:
    for i, l in enumerate(f,start=1):
      pass
  out.write(str(i))
  out.write('\t')
  f.close()
 
  del i
  i=0 
  with open("dne.txt","r") as f:
    for i, l in enumerate(f,start=1):
      pass
  out.write(str(i))
  out.write('\n')
  f.close()

import pymysql
import random
import sys
import subprocess
import time
import connect

#conn = pymysql.connect(host = <ip>, user = <user> , passwd =<pass>, database = <db>)

#cur = conn.cursor()
[conn,cur] = connect.makeConn('ld')

if ".py" in sys.argv[-1]:
  runTimes = 1
else:
  runTimes = int(sys.argv[-1])

ana_fh = open("analyze.txt","w")

falseCount = 0

for i in range(0,runTimes):
  [test_rsids,pop] = getTestRsids(cur)

  getSNAPResults(test_rsids,pop)

  if compareResults() is False: #make sure SNAP is sending data
    i-= 1
    falseCount+=1
    if falseCount > 100:
      break
    continue

  analyzeResults(ana_fh)

ana_fh.close()
cur.close()
conn.close()
