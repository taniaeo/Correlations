import csv
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

#Read Data ECounts and Dates
HC=pd.read_csv('MerapiEq_Hgap0.csv')
HCounts = list(HC["Count"])
Datel=list(HC["Date"])

#Verify dates are complete
date_F = datetime.datetime.strptime(Datel[len(Datel)-1], '%m/%d/%Y')
end_date = datetime.datetime.strptime(Datel[0], '%m/%d/%Y') + datetime.timedelta(days=len(Datel)-1)

if date_F == end_date:
    print("Dates are consistent")
else:
    print("There are gaps/mistakes in the dates")


#Input Dates of Onsets, Better if select from the list within the range of Min(date)-Max(date) of Datel
input1=input("Onset Dates (coma separated):").split(",")
Onsets = [Datel.index(x)-1 for x in input1]
Onsets.sort()
NOn=len(Onsets)


#Define the lenght (tm, tx) of the time series that we will compare
DifOn = [Onsets[i+1]-Onsets[i] for i in range(NOn-1)]
if min(DifOn) >= 60:
  tx= min([180, min(DifOn)-2]) 
else:
   print("Onsets are too close, need to be at least 2 months appart")
for t in range(10,tx-15):
  stt=[np.std(HCounts[x-t:x-1]) for x in Onsets]
  if min(stt) > 0:
    tm=t+1
    break

#Cross-Correlation of all posible pairs of the events given in list Onsets
MCC=[] #Mean of correlations
MdCC=[] #Median of correlations
Pars=['C'+ str((j+1,i+1)) for i in range(NOn)  for j in range(i)] #All posible pairs

for t in range(tm,tx):
  CCl=[np.corrcoef(HCounts[Onsets[j]-t+1:Onsets[j]+1], HCounts[Onsets[i]-t+1:Onsets[i]+1])[0,1] for i in range(NOn)  for j in range(i)]
  MCC.append(np.mean(CCl))
  MdCC.append(np.median(CCl))

print('Max Mean at t='+ str(MCC.index(max(MCC))+tm))
print('Max Median at t='+ str(MdCC.index(max(MdCC))+tm))


#Plot of the cross-correlations for a specific time
#In the interface time can be selected interactively

t0=MCC.index(max(MCC))+tm #lenght of the time series to calculate the cross-correlations
CC0=[np.corrcoef(HCounts[Onsets[j]-t0+1:Onsets[j]+1], HCounts[Onsets[i]-t0+1:Onsets[i]+1])[0,1] for i in range(NOn)  for j in range(i)]

plt.figure(figsize=(NOn-1,4))
plt.stem(range(len(Pars)),CC0, use_line_collection=True)
plt.title('Comparing'+ str(t0)+' days before events (i,j)')
plt.ylabel(' Cross-Correlation')
plt.xticks(range(len(Pars)), Pars,rotation='vertical')
plt.subplots_adjust(bottom=0.25)
plt.show()

 #Plot of the mean and median of all the correlations as a function of time
#the optimun time is the one that maximizes the value of cross-corr
plt.plot(range(tm,tx),MCC)
plt.plot(range(tm,tx),MdCC)
plt.ylabel('Mean/Median Cross-Correlation')
plt.xlabel('time series lenght (days)')
plt.legend(['Mean', 'Median'], loc='lower right')
plt.subplots_adjust(left=0.15)
plt.show()