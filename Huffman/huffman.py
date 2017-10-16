from collections import defaultdict
from operator import *
import itertools

filename = "seneca.txt"
N = 5

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

#a = map(''.join, itertools.product(''.join(frequency1.keys()), repeat=N))
#print(list(a))

frequency = defaultdict(int)
for symbol in splitteddata:
    frequency[symbol] += 1

sorted_x = sorted(frequency.items(), key=lambda x:x[1])
nodesList = []
for key, value in sorted_x:
    if(value > 0):
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


import json
json.dump(codes, open("codes.txt",'w'))
codes = json.load(open("codes.txt"))

codedData = "".join([codes[x] for x in splitteddata])

# first split into 8-bit chunks
bit_strings = [codedData[i:i + 8] for i in range(0, len(codedData), 8)]
byte_list = [int(b, 2) for b in bit_strings]
ba = bytearray(byte_list)
#print([b for b in ba])
with open('compressed.bin', 'wb') as f:
	f.write(ba)  	# convert to bytearray before writing

#############################
print("wspolczynnik kompresji: " + str((len(data)+len(codedData))/len(data)))
#############################
# print(c)
# print(codedData)
data = open("compressed.bin", "rb").read()
ba = bytearray(data)
bins = ['{:08b}'.format(x) for x in ba]
# intsss = [int.from_bytes(x, byteorder='big') for x in ba]
#print(bit_strings)
#print([b for b in bins])
dataC = "".join(bins)
# print(len(dataC))
# print(len(codedData))
#
reverseCodes= {y:x for x,y in codes.items()}
#print(reverseCodes)
current_code = ""
decoded_text = ""
for bit in dataC:
    current_code += bit
    if(current_code in reverseCodes):
    	character = reverseCodes[current_code]
    	decoded_text += character
    	current_code = ""
#print("Decoded:" + decoded_text)
file = open('decompresed.txt', 'w')
file.write(decoded_text)
file.close()
