import os
import json

jsonFile = open(os.getcwd()+"/Users.json","r")
line = jsonFile.readline()
while(len(line)>1):
	if line[-2:-1] == ',':
		line = line[:-2]
	jsonObj = json.loads(line)
	print('BEGIN:VCARD')
	print('VERSION:2.1')
	print("N:;{};;;".format(jsonObj['userID']))
	print("FN:{}".format(jsonObj['userID']))
	print("TEL;CELL:{}".format(jsonObj['cellNumber']))
	print('END:VCARD')
	line = jsonFile.readline()


"""
BEGIN:VCARD

N:;Jonathan;;;
FN:J Second Sim
TEL;CELL:0643062806
END:VCARD
"""