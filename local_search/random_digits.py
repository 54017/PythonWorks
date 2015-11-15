# -*- coding: utf-8 -*-

import random
import getopt, sys
import re
import copy

def getMovableNeighbors(blank):
	neighbors = []
	directions = [(-1, 0),(1, 0),(0, 1),(0, -1)]
	for direction in directions:
		if blank[0] + direction[0] < 0 or blank[0] + direction[0] > 2 or blank[1] + direction[1] < 0 or blank[1] + direction[1] > 2:
			pass
		else:
			neighbors.append((blank[0] + direction[0], blank[1] + direction[1]))
	return neighbors

def randomMove(matrix, neighbors, blank):
	neighbor = random.choice(neighbors)
	matrix[blank[0]][blank[1]] = matrix[neighbor[0]][neighbor[1]]
	blank[0] = neighbor[0]
	blank[1] = neighbor[1]
	matrix[neighbor[0]][neighbor[1]] = 0


def generate_random_digits():
	queen = range(0, 8)
	amount = 0
	opts, args = getopt.getopt(sys.argv[1:], "n:t:", [])
	for opt, value in opts:
		if opt == '-n':
			amount = value

	fileReader = open("digits.txt", "w")
	for i in range(int(amount)):
		matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
		blank = [2, 2]
		'''从终止状态随机走100步生成有解初始状态'''
		for j in range(2000):
			neighbors = getMovableNeighbors(blank)
			randomMove(matrix, neighbors, blank)
		reg = re.compile(r', |\[|\]')
		fileReader.writelines(reg.sub('', str(matrix)) + "\n")

	fileReader.close()

if __name__ == "__main__":
	generate_random_digits()