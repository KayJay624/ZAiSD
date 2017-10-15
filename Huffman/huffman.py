from collections import defaultdict
from operator import *

filename = "seneca.txt"
N = 2

class Node(object):
	left = None
	right = None
	item = None
	weight = 0

	def __init__(self, i, w):
		self.item = i
		self.weight = w

	def setChildren(self, ln, rn):
		self.left = ln
		self.right = rn

with open('seneca.txt', 'r') as myfile:
    data=myfile.read()
#data = "TO BE OR NOT TO BE"

splitteddata = [data[i:i + N] for i in range(0, len(data), N)];

frequency = defaultdict(int)
for symbol in splitteddata:
    frequency[symbol] += 1

sorted_x = sorted(frequency.items(), key=lambda x:x[1])
nodesList = []
for key, value in sorted_x:
    n = Node(key, value)
    nodesList.append(n)

while(len(nodesList) > 1):
    nodesList.sort(key=lambda x: x.weight, reverse=False)
    r = nodesList.pop(0);
    l = nodesList.pop(0);
    n = Node(None, r.weight+l.weight)
    n.setChildren(l, r)
    nodesList.append(n)

codes = {}
def codeIt(s, node):
	if node.item:
		if not s:
			codes[node.item] = "_"
		else:
			codes[node.item] = s
	else:
		codeIt(s+"0", node.left)
		codeIt(s+"1", node.right)

codeIt("",nodesList[0])
print(codes)
reverseCodes= {y:x for x,y in codes.items()}
codedData = "".join([codes[a] for a in data])
print(reverseCodes)

current_code = ""
decoded_text = ""
for bit in codedData:
    current_code += bit
    if(current_code in reverseCodes):
    	character = reverseCodes[current_code]
    	decoded_text += character
    	current_code = ""
print("Decoded:" + decoded_text)
file = open('decompresed.txt', 'w')
file.write(decoded_text)
file.close()


print(data)
print(codedData)
print("wspolczynnik: " + str((len(data)+len(codedData))/len(data)))

# for key, value in sorted_x:
#     print(key, value)

for k,v in codes.items():
     print("'" + k + "'\t" + v)
#for symbol, weight in so.items():
#    print("'" + str(symbol) + "': " + str(weight))

file = open('compresed.txt', 'w')
file.write(codedData)
file.close()
