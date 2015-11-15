# -*- coding:utf-8 -*-


import random
import getopt, sys
import random_queen, random_digits
import time
import re, copy


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
	count = 0
	for i, val in  enumerate(array):
		for j, arg in  enumerate(array):
			if (i != j and abs(i - j) == abs(int(val) - int(arg))) or (i != j and int(val) == int(arg)):
				count += 1
	return count/2


'''曼哈顿距离'''
def manhattan(array):
	count = 0
	for i, subArray in enumerate(array):
		for j, val in enumerate(subArray):
			if int(val) != 0:
				count += abs(i - (int(val) - 1) / 3) + abs(j - (int(val) - 1) % 3)
	return count

def random_restart_climb(array):
	count = 0
	h = isConflict(array)
	flag = 1
	while (h != 0):
		flag = 0
		for i, val in enumerate(array):
			for j in range(0, 8):
				count += 1
				tempArray = list(array)
				tempArray[i] = j
				temp = isConflict(tempArray)
				if temp < h:
					array = tempArray
					flag = 1
					h = temp
		if flag == 0:
			array = generate_new_queen()
			h = isConflict(array)
	return count

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

def random_restart_digits(array):
	count = 0
	(matrix, blank) = arrayToMatrix(array)
	h = manhattan(matrix)
	flag = 1
	while(h != 0):
		flag = 0
		neighbors = getMovableNeighbors(blank)
		for neighbor in neighbors:
			count += 1
			tempMatrix = copy.deepcopy(matrix)
			tempBlank = copy.deepcopy(blank)
			move(tempMatrix, neighbor, tempBlank)
			temp = manhattan(tempMatrix)
			if (temp < h):
				matrix = tempMatrix
				flag = 1
				h = temp
				blank = tempBlank
		if flag == 0:
			(matrix, blank) = generate_new_digits()
			count += 1
			h = manhattan(matrix)
	return count


def generate_new_digits():
	queen = range(0, 9)
	random.shuffle(queen)
	(matrix, blank) = arrayToMatrix(queen)
	return matrix, blank

def generate_new_queen():
	queen = range(0, 8)
	random.shuffle(queen)
	return queen

if __name__ == '__main__':
	random_queen.generate_random_queen()
	random_digits.generate_random_digits()
	fileReader = open("data.txt", "r")
	digitsReader = open("digits.txt", "r")
	sum = 0
	amount = 0
	startTime = time.time()
	for line in fileReader:
		amount += 1
		line = line.strip('\n')
		count = random_restart_climb(line)
		sum += count
	print "average search times for eight queen: ", sum / amount
	print "average search time for eight queen:", str((time.time() - startTime) / amount)
	fileReader.close()
	'''八数码'''
	sum = 0
	amount = 0
	startTime = time.time()
	for line in digitsReader:
		amount += 1
		line = line.strip('\n')
		count = random_restart_digits(line)
		sum += count
	print "average search times for eight digits: ", sum / amount
	print "average search time for eight digits:", str((time.time() - startTime) / amount)
	digitsReader.close()


