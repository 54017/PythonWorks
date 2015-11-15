# -*- coding:utf-8 -*-

import random
import getopt, sys
import random_queen, random_digits
import time
import re
import math, copy

'''曼哈顿距离'''
def manhattan(array):
	count = 0
	for i, subArray in enumerate(array):
		for j, val in enumerate(subArray):
			if int(val) != 0:
				count += abs(i - (int(val) - 1) / 3) + abs(j - (int(val) - 1) % 3)
	return count

def getMovableNeighbors(blank):
	neighbors = []
	directions = [(-1, 0),(1, 0),(0, 1),(0, -1)]
	for direction in directions:
		if blank[0] + direction[0] < 0 or blank[0] + direction[0] > 2 or blank[1] + direction[1] < 0 or blank[1] + direction[1] > 2:
			pass
		else:
			neighbors.append((blank[0] + direction[0], blank[1] + direction[1]))
	return neighbors


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

def arrayToMatrix(array):
	blank = []
	matrix = [[0, 0, 0] for i in range(3)]
	for i in range(3):
		for j in range(3):
			matrix[i][j] = int(array[3*i + j])
			if (matrix[i][j] == 0):
				blank.append(i)
				blank.append(j)
	return matrix, blank

def move(matrix, neighbor, blank):
	matrix[blank[0]][blank[1]] = matrix[neighbor[0]][neighbor[1]]
	blank[0] = neighbor[0]
	blank[1] = neighbor[1]
	matrix[neighbor[0]][neighbor[1]] = 0

def annealing_digits(array):
	count = 0
	(matrix, blank) = arrayToMatrix(array)
	h = manhattan(matrix)
	flag = 1
	t = 1000
	while(t > 0):
		flag = 0
		count += 1
		neighbors = getMovableNeighbors(blank)
		neighbor = random.choice(neighbors)
		tempMatrix = copy.deepcopy(matrix)
		tempBlank = copy.deepcopy(blank)
		move(tempMatrix, neighbor, tempBlank)
		diff = manhattan(tempMatrix) - h
		if diff < 0 or (diff > 0 and math.exp(float(-diff)/t) < random.random()):
			matrix = tempMatrix
			blank = tempBlank
			h = manhattan(matrix)
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
	return tempArray

if __name__ == '__main__':
	random_queen.generate_random_queen()
	random_digits.generate_random_digits()
	fileReader = open("data.txt", "r")
	digitsReader = open("digits.txt", "r")
	sum = 0
	amount = 0
	failed = 0
	flag = 0
	startTime = time.time()
	for line in fileReader:
		amount += 1
		line = line.strip('\n')
		(count, flag) = simulated_annealing(line)
		if (flag == 0):
			failed += 1
		sum += count
	print "average search times for eight queens: ", sum / amount
	print "average search time for eight queens: ", str((time.time() - startTime) / amount)
	print "successful rate: ", float(amount - failed) / amount
	fileReader.close()
	'''八数码'''
	sum = 0
	amount = 0
	failed = 0
	startTime = time.time()
	for line in digitsReader:
		amount += 1
		line = line.strip('\n')
		(count, flag) = annealing_digits(line)
		if (flag == 0):
			failed += 1
		sum += count
	print "average search times for eight digits: ", sum / amount
	print "average search time for eight digits:", str((time.time() - startTime) / amount)
	print "successful rate: ", float(amount - failed) / amount
	digitsReader.close()