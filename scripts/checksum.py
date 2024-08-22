import hashlib
import os

with open('ToDo.txt', 'r') as file_name:
	f = file_name.read()
	m = hashlib.sha256(f.encode('UTF-8'),usedforsecurity = True)
	

print(m.hexdigest())