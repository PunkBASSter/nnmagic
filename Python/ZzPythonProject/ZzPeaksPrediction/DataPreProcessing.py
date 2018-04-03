import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

path = "C:\\Users\\PunkBASSter\\AppData\\Roaming\\MetaQuotes\\Terminal\\Common\\Files\\"

fileName = "DzzExportEURUSD.mPERIOD_H1.csv"
outputFilePrefix = "Normalized_"
quoteDigits = 5

rawData = pd.read_csv(fileName,usecols=["Value"], dtype=np.float32).as_matrix().transpose()[0]

#если потолок лог бэйса искусственно занизить в деннормализации(сделать 4 вместо 10, то получится грааль)
def calculateNextPeak(currentZz, prevZz, nnPredicted, logBase = 9.677489177489505):
    currentSign = -1 if currentZz > prevZz else 1
    divDv = math.pow(logBase, math.fabs(nnPredicted)) * currentSign
    nextZz = currentZz + math.fabs(currentZz - prevZz) * divDv
    return nextZz


with open(path+fileName, 'r') as f:
    content = f.readlines()
content = [x.strip() for x in content]


#Parsing CSV with filtering of empty lines into [Timestamp, Value] pairs array
filtered = []
for c in content:
    splitted = c.split(",")
    if len(splitted) > 1:
        filtered.append(splitted)

peaksCount = len(filtered)


#Sorting by increasing of timestamp
filtered.sort(key=lambda x: int(x[0]), reverse=False)

#Splitting Time and Value to calculate difference arrays for them separately
t = []
v = []
for f in filtered:
    t.append(int(f[0]))
    v.append(float(f[1]))


def getDiffArray(array):
    res = []
    for i in range(1, len(array)):
        res.append(array[i] - array[i-1])
    return res


dt = getDiffArray(t)
dv = getDiffArray(v)


def getDividedArray(array):
    res = []
    for i in range(1, len(array)):
        sign = 1
        if array[i-1] > 0 > array[i]:
            sign = -1
        res.append(sign*array[i]/array[i-1])
    return res


#divDt = getDividedArray(dt)
divDv = getDividedArray(dv)


#Ln(dv) calculation
limit = 10
logBase = max(abs(min(divDv)), max(divDv))
#logBase = min(logBase, limit)

logDiv = []
for x in divDv:
    sign = 1
    if x < 0:
        sign = -1

    value = abs(x) if abs(x) <= logBase else logBase
    logDiv.append(sign*math.log(value, logBase))


#Write output
lines = ["Timestamp,Value,TimeDiff,ValueDiffRatio,ValueDiffRatio_LogWithMaxAbsBase\n"]
for i in range(0, len(divDv)):
    lines.append(str(t[i+2])+","+str(v[i+2])+","+str(dt[i])+","+str(divDv[i])+","+str(logDiv[i])+'\n')
f = open("data\\"+outputFilePrefix+fileName, 'wt')
f.writelines(lines)


#Fun with plots
fig = plt.figure()
ax0 = fig.add_subplot(311)
ax0.plot(v)
ax0.grid(True)
ax1 = fig.add_subplot(312)
ax1.plot(logDiv, 'r+')
ax1.grid(True)
ax2 = fig.add_subplot(313)
ax2.hist(logDiv, 1000, normed=1, facecolor='g', alpha=0.75)
ax2.grid(True)
plt.show()


print("end")



