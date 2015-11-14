# -*- coding:utf-8 -*-


import random
import getopt, sys
import random_queen
import datetime
import re

'''返回冲突的个数'''
def isConflict(array):
	count = 0;
	for i, val in  enumerate(array):
		for j, arg in  enumerate(array):
			if (i != j and abs(i - j) == abs(int(val) - int(arg))) or (i != j and int(val) == int(arg)):
				count += 1
	return count/2


def random_restart_climb(array):
	count = 0
	h = isConflict(array)
	reg = re.compile(r', |\[|\]|\'')
	flag = 1
	while (h != 0):
		flag = 0
		for i, val in enumerate(array):
			for j in range(0, 8):
				count += 1
				tempArray = list(array)
				tempArray[i] = j
				tempArray = reg.sub('', str(tempArray))
				temp = isConflict(tempArray)
				if temp < h:
					array = tempArray
					flag = 1
					h = temp
		if flag == 0:
			array = generate_new_queen()
			h = isConflict(array)
	return count

def generate_new_queen():
	queen = range(0, 8)
	random.shuffle(queen)
	reg = re.compile(r', |\[|\]')
	return reg.sub('', str(queen))

if __name__ == '__main__':
	random_queen.generate_random_queen()
	fileReader = open("data.txt", "r")
	sum = 0
	amount = 0
	startTime = datetime.datetime.now()
	for line in fileReader:
		amount += 1
		line = line.strip('\n')
		count = random_restart_climb(line)
		sum += count
	print "average search times: ", sum / amount
	print "average search time:", str((datetime.datetime.now() - startTime) / amount)[6:]
	fileReader.close()