import sys
import re
from os import listdir, linesep
from os.path import isfile, join, splitext

def clearLine(line):
	return line.strip().replace(r'\&', '').replace(r'\fB', '').replace(r'\fC', '').replace(r'\fP', '').replace(r'\-', '-').replace(r'#', '<nowiki>#</nowiki>')

def convert(in_filename, out_filename):
	f = open(out_filename, 'w')
	for line in open(in_filename):
		m = re.match(r'^\.\\\"', line)
		if m is not None:
			continue
		if line.strip() == '.TP' or line.strip() == '.PP' or line.strip() == '.nh':
			continue
		m = re.match(r'^\.TH\s+', line)
		if m is not None:
			continue
		m = re.match(r'^\.SH\s+("?)(.*)(\1)\s*$', line)
		if m is not None:
			f.write(linesep)
			f.write("== " + clearLine(m.group(2)) + " ==")
			f.write(linesep)
			continue
		m = re.match(r'^\.R?B\s+(.*)\s*$', line)
		if m is not None:
			f.write("**" + clearLine(m.group(1)) + "**")
			f.write(linesep)
			continue
		m = re.match(r'^\.I\s+(.*)\s*$', line)
		if m is not None:
			f.write("//" + clearLine(m.group(1)) + "//")
			f.write(linesep)
			continue
		if line.strip() == ".br":
			f.write(linesep)
			continue
		m = re.match(r'^\.in\s', line)
		if m is not None:
			continue
		m = re.match(r'^\.ti\s', line)
		if m is not None:
			continue
		m = re.match(r'^\.ad\s', line)
		if m is not None:
			continue 
		m = re.match(r'^\.SS\s+("?)(.*)(\1)\s*$', line)
		if m is not None:
			f.write(linesep)
			f.write("=== " + clearLine(m.group(2)) + " ===")
			f.write(linesep)
			continue
		m = re.match(r'^\.RI\s+("?)(\\fI)(.*)(\\fP)(\1)\s*$', line)
		if m is not None:
			f.write(linesep)
			f.write(clearLine(m.group(3)))
			f.write(linesep)
			continue
		m = re.match(r'^\.RI\s+("?)(.*)(\1)\s*$', line)
		if m is not None:
			f.write(linesep)
			f.write("==== " + clearLine(m.group(2)) + " ====")
			f.write(linesep)
			continue
		f.write(clearLine(line))
	
	f.close()
		
if len(sys.argv) != 3:
	print("Usage: python man2wiki.py [man folder] [wiki folder]")
else:
	for f in [f for f in listdir(sys.argv[1]) if isfile(join(sys.argv[1],f))]:
		convert(join(sys.argv[1], f), join(sys.argv[2], splitext(f)[0] + ".wiki"))