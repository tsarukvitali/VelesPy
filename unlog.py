#! python3

import os
import subprocess
import re

rootdir = os.path.dirname(os.path.realpath(__file__))
decrypter = "decrypt_log"
decrypterPath = os.path.join(rootdir, decrypter)
if not os.path.isfile(decrypterPath):
	decrypter2 = "decrypt_log.exe"
	decrypterPath2 = os.path.join(rootdir, decrypter2)
	if not os.path.isfile(decrypterPath2):
		print ("can not find decrypter by path " + decrypterPath + " or " + decrypterPath2)
	else:
		decrypterPath = decrypterPath2

pattern = re.compile("\.log[\.\d+]*$")

for subdir, dirs, files in os.walk(rootdir):
	for file in files:
		if pattern.search(file):
			logged = os.path.join(subdir, file)
			unloggedName = file + ".txt"
			unlogged = os.path.join(subdir, unloggedName)
			#subprocess.call(["C:/Documents and Settings/flow_model/flow.exe"])
			print (logged + " > " + unlogged)
			with open(unlogged, "w") as outfile:
				subprocess.run([ decrypterPath, logged], stdout=outfile)
