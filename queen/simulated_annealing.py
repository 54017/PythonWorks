# -*- coding:utf-8 -*-

import random
import getopt, sys
import random_queen
import datetime
import re
import math


'''返回冲突的个数'''
def isConflict(array):
	count = 0;
	for i, val in  enumerate(array):
		for j, arg in  enumerate(array):
			if (i != j and abs(i - j) == abs(int(val) - int(arg))) or (i != j and int(val) == int(arg)):
				count += 1
	return count/2

def simulated_annealing(array):
	count = 0
	h = isConflict(array)
	reg = re.compile(r', |\[|\]|\'')
	flag = 1
	t = 1000
	while (t > 0):
		flag = 0
		count += 1
		neighbor = generate_new_neighbor(array)
		diff = isConflict(neighbor) - h
		if diff < 0 or (diff > 0 and math.exp(float(-diff)/t) < random.random()):
			array = neighbor
			h = isConflict(array)
			if h == 0:
				flag = 1
				break
		t -= 1
	return count, flag


def generate_new_neighbor(array):
	a = random.randint(0, 7)
	b = random.randint(0, 7)
	if array[a] == b:
		return generate_new_neighbor(array)
	tempArray = list(array)
	tempArray[a] = b
	reg = re.compile(r', |\[|\]|\'')
	tempArray = reg.sub('', str(tempArray))
	return tempArray

if __name__ == '__main__':
	random_queen.generate_random_queen()
	fileReader = open("data.txt", "r")
	sum = 0
	amount = 0
	failed = 0
	flag = 0
	startTime = datetime.datetime.now()
	for line in fileReader:
		amount += 1
		line = line.strip('\n')
		(count, flag) = simulated_annealing(line)
		if (flag == 0):
			failed += 1
		sum += count
	print "average search times: ", sum / amount
	print "average search time: ", str((datetime.datetime.now() - startTime) / amount)[6:]
	print "successful rate: ", float(amount - failed) / amount
	fileReader.close()