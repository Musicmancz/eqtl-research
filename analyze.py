import numpy as np

f_in = open('analyze.txt','r')

percents = []
for line in f_in:

    (match, nomatch, dne) = line.split('\t')

    match = int(match)

    total = match + int(nomatch) + int(dne)

    if total == 0:
      continue
        
    percents.append(match / total)

f_in.close()

mean = np.mean(percents)
std = np.std(percents)

print([mean,std])
