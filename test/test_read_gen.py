import sys

import numpy as np
import matplotlib.pyplot as plt

#import lichen.lichen as lch

infile = open(sys.argv[1])
line = infile.readline()

parent = []
kids = []
count = 0
while line:

	if line.find("Event")>=0:
		#print("New Event:")
		line = infile.readline()
		#print(line)
	if line.find("GEN") >= 0:
		vals = line.split()

		ndau = int(vals[-1])
		pdg = vals[2].split('=')[1]
		pdg = int(pdg.split(',')[0])
		pt = vals[3].split('=')[1]
		if pt[:1] == '+':		
			pt = float(pt[1:])
		else:
			pt = float(pt)
		#print(pt)
		if pdg == 6 or pdg == -6:
			#print(line)
			if ndau > 1:
				parent.append([pdg,pt])
				count += 1
				#print(line)
				kidInfo = []
				for i in range(ndau):
					line = infile.readline()
					#print(line)
					
					part = line.split()
					kidpdg = int(part[2])
					kidpt = float(part[4])
					parentpt = float(part[5])
					kidInfo.append([kidpdg,kidpt,parentpt])
				kids.append(kidInfo)
				kidInfo = 0
	line = infile.readline()



top = []
for i in range(count):
	if parent[i][0] == 6:
		top.append(parent[i][1])
print('this should be plotting >:(')
#print(top)

plt.figure()
plt.hist(top)
plt.show()
