# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 21:58:47 2018

@author: kaspar
Extract data from C header file (.h)
	output format: request --> response
"""

def readFile(filename):
    f = open(filename);
    lines = f.readlines();
    res = [];
    data = [];
    for line in lines:
        if 'static const unsigned char' in line:
            res.append(data);
            data = [];
            continue;
        if ('x' in line):
            data.append(line[:46].strip());
    res.append(data);
    return res;

def filterData(data):
	start = False
	result = []
	temp = []
	for packet in data:
		for line in packet:
			if '0x2f' in line:
				start = True;
				temp.append(line[18:])
			elif start:
				temp.append(line)
		start = False
		result.append([", ".join(temp)])
		temp = []
	return result

def render(filename1, filename2):
	data = [i for i in readFile(filename1) if i]
	data2 = [i for i in readFile(filename2) if i]
	data = filterData(data)
	data2 = filterData(data2)
	for i in range(len(data)):
		#line = "{0} --> {1}".format(data[i][0], data2[i][0])
		line = "{0}".format(data2[i][0])
		print(line)

if __name__ == '__main__':
	import sys
	if (len(sys.argv) > 1):
		requests_filename = sys.argv[1]
		response_filename = sys.argv[2]
		render(requests_filename, response_filename)
