import os, sys
import getopt
from PIL import Image
import numpy as np
import multiprocessing
import math
import time


def rgb2lab(array, height, width):
	result = np.zeros((height, 3 * width), dtype=np.float)
	for i in xrange(0, height):
		for j in xrange(0, 3 * width):
			value = float(array[i][j]) / 255
			if value > 0.04045:
				value = ((value + 0.055) / 1.055) ** 2.4
			else:
				value /= 12.92
			result[i][j] = value * 100;
	for i in xrange(0, height):
		for j in xrange(0, 3 * width, 3):
			X = result[i][j] * 0.4124 + result[i][j + 1] * 0.3576 + result[i][j + 2] * 0.1805
			Y = result[i][j] * 0.2126 + result[i][j + 1] * 0.7152 + result[i][j + 2] * 0.0722
			Z = result[i][j] * 0.0193 + result[i][j + 1] * 0.1192 + result[i][j + 2] * 0.9505
			result[i][j] = float(round(X, 4)) / 95.047
			result[i][j + 1] = float(round(Y, 4)) / 100.0
			result[i][j + 2] = float(round(Z, 4)) / 108.883
	for i in xrange(0, height):
		for j in xrange(0, 3 * width):
			if result[i][j] > 0.008856:
				result[i][j] = result[i][j] ** (1.0/3)
			else:
				result[i][j] = (7.787 * result[i][j]) + (16 / 116)
	for i in xrange(0, height):
		for j in xrange(0, 3 * width, 3):
			L = (116 * result[i][j + 1]) - 16
			A = 500 * (result[i][j] - result[i][j + 1])
			B = 200 * (result[i][j + 1] - result[i][j + 2])
			result[i][j] = round(L, 4)
			result[i][j + 1] = round(A, 4)
			result[i][j + 2] = round(B, 4)
	return result

def stereoMatchASW(left, right, filename):


def computeDisparity(left, right, filename):
	stereoMatchSSD(left, right, filename)
	stereoMatchRightSSD(left, right, filename)
	stereoMatchNCC(left, right, filename)
	stereoMatchRightNCC(left, right, filename)


# use 5*5 window size

def stereoMatchSSD(left, right, filename):
	print filename
	startTime = time.time()
	DISPARITY = 79
	WINDOWSIZE = 5
	HALFSIZE = WINDOWSIZE/2
	leftWidth, leftHeight = left.size
	rightWidth, rightHeight = right.size
	leftPix = np.asarray(list(left.getdata())).reshape(leftHeight, leftWidth)
	rightPix = np.asarray(list(right.getdata())).reshape(rightHeight, rightWidth)
	leftPixPadding = np.pad(leftPix, (HALFSIZE, HALFSIZE), 'constant')
	rightPixPadding = np.pad(rightPix, (HALFSIZE, HALFSIZE), 'constant')
	leftResult = np.zeros((leftHeight, leftWidth), dtype=np.int)
	for i in xrange(HALFSIZE, leftHeight):
		print "leftSSD: ", i
		for j in xrange(HALFSIZE, leftWidth):
			min = sys.maxint
			resultDisparity = 0
			for d in xrange(0, DISPARITY + 1):
				if j - d >= HALFSIZE:
					tempSum = 0
					for k in xrange(-HALFSIZE, HALFSIZE + 1):
						for t in xrange(-HALFSIZE, HALFSIZE + 1):
							tempSum += pow(leftPixPadding[i + k][j + t] - rightPixPadding[i + k][j - d + t], 2)
					if tempSum < min:
						min = tempSum
						resultDisparity = d
				else:
					break
			leftResult[i][j] = resultDisparity
	leftResult *= 3
	result = Image.frombytes('L', (leftWidth, leftHeight), np.uint8(leftResult).tobytes())
	result.save('results_intensity_enhanced/' + filename + "_disp1_SSD.png")
	endTime = time.time()
	print "SSD left: ", endTime - startTime

def stereoMatchRightSSD(left, right, filename):
	startTime = time.time()
	DISPARITY = 79
	WINDOWSIZE = 5
	HALFSIZE = WINDOWSIZE/2
	leftWidth, leftHeight = left.size
	rightWidth, rightHeight = right.size
	leftPix = np.asarray(list(left.getdata())).reshape(leftHeight, leftWidth)
	rightPix = np.asarray(list(right.getdata())).reshape(rightHeight, rightWidth)
	leftPixPadding = np.pad(leftPix, (HALFSIZE, HALFSIZE), 'constant')
	rightPixPadding = np.pad(rightPix, (HALFSIZE, HALFSIZE), 'constant')
	rightResult = np.zeros((rightHeight, rightWidth), dtype=np.int)
	for i in xrange(HALFSIZE, rightHeight):
		print "rightSSD: ", i
		for j in xrange(HALFSIZE, rightWidth):
			min = sys.maxint
			resultDisparity = 0 
			for d in xrange(0, DISPARITY + 1):
				if j + d < rightWidth:
					tempSum = 0
					for k in xrange(-HALFSIZE, HALFSIZE + 1):
						for t in xrange(-HALFSIZE, HALFSIZE + 1):
							tempSum += pow(rightPixPadding[i + k][j + t] - leftPixPadding[i + k][j + d + t], 2)
					if tempSum < min:
						min = tempSum
						resultDisparity = d
				else:
					break
			rightResult[i][j] = resultDisparity
	rightResult *= 3
	result = Image.frombytes('L', (rightWidth, rightHeight), np.uint8(rightResult).tobytes())
	result.save('results_intensity_enhanced/' + filename + "_disp5_SSD.png")
	endTime = time.time()
	print "SSD right: ", endTime - startTime

def stereoMatchNCC(left, right, filename):
	startTime = time.time()
	DISPARITY = 79
	WINDOWSIZE = 5
	HALFSIZE = WINDOWSIZE/2
	leftWidth, leftHeight = left.size
	rightWidth, rightHeight = right.size
	leftPix = np.asarray(list(left.getdata())).reshape(leftHeight, leftWidth)
	rightPix = np.asarray(list(right.getdata())).reshape(rightHeight, rightWidth)
	leftPixPadding = np.pad(leftPix, (HALFSIZE, HALFSIZE), 'constant')
	rightPixPadding = np.pad(rightPix, (HALFSIZE, HALFSIZE), 'constant')
	leftResult = np.zeros((leftHeight, leftWidth), dtype=np.int)
	for i in xrange(HALFSIZE, leftHeight):
		print "leftNCC: ", i
		for j in xrange(HALFSIZE, leftWidth):
			min = 0
			averageLeft = 0
			for x in xrange(-HALFSIZE, HALFSIZE + 1):
				for y in xrange(-HALFSIZE, HALFSIZE + 1):
					averageLeft += leftPixPadding[i + x][j + y]
			averageLeft = averageLeft / (WINDOWSIZE * WINDOWSIZE)
			resultDisparity = 0 
			for d in xrange(0, DISPARITY + 1):
				if j - d >= HALFSIZE:
					averageRight = 0
					for k in xrange(-HALFSIZE, HALFSIZE + 1):
						for t in xrange(-HALFSIZE, HALFSIZE + 1):
							averageRight += rightPixPadding[i + k][j - d + t]
					averageRight = averageRight/(WINDOWSIZE * WINDOWSIZE)
					sumUp = 0
					sumDownLeft = 0
					sumDownRight = 0
					for k in xrange(-HALFSIZE, HALFSIZE + 1):
						for t in xrange(-HALFSIZE, HALFSIZE + 1):
							sumUp += (leftPixPadding[i + k][j + t] - averageLeft) * (rightPixPadding[i + k][j - d + t] - averageRight)
							sumDownLeft += pow(leftPixPadding[i + k][j + t] - averageLeft, 2)
							sumDownRight += pow(rightPixPadding[i + k][j - d + t] - averageRight, 2)
					result = sumUp / math.sqrt(sumDownLeft * sumDownRight)
					if result > min:
						min = result
						resultDisparity = d; 
				else:
					break
			leftResult[i][j] = resultDisparity
	leftResult *= 3
	result = Image.frombytes('L', (leftWidth, leftHeight), np.uint8(leftResult).tobytes())
	result.save('results_intensity_enhanced/' + filename + "_disp1_NCC.png")
	endTime = time.time()
	print "NCC left: ", endTime - startTime

def stereoMatchRightNCC(left, right, filename):
	startTime = time.time()
	DISPARITY = 79
	WINDOWSIZE = 5
	HALFSIZE = WINDOWSIZE/2
	leftWidth, leftHeight = left.size
	rightWidth, rightHeight = right.size
	leftPix = np.asarray(list(left.getdata())).reshape(leftHeight, leftWidth)
	rightPix = np.asarray(list(right.getdata())).reshape(rightHeight, rightWidth)
	leftPixPadding = np.pad(leftPix, (HALFSIZE, HALFSIZE), 'constant')
	rightPixPadding = np.pad(rightPix, (HALFSIZE, HALFSIZE), 'constant')
	rightResult = np.zeros((rightHeight, rightWidth), dtype=np.int)
	for i in xrange(HALFSIZE, rightHeight):
		print "rightNCC: ", i
		for j in xrange(HALFSIZE, rightWidth):
			min = 0
			averageRight = 0
			for x in xrange(-HALFSIZE, HALFSIZE + 1):
				for y in xrange(-HALFSIZE, HALFSIZE + 1):
					averageRight += rightPixPadding[i + x][j + y]

			averageRight = averageRight / (WINDOWSIZE * WINDOWSIZE)
			resultDisparity = 0 
			for d in xrange(0, DISPARITY + 1):
				if j + d < rightWidth:
					averageLeft = 0
					for k in xrange(-HALFSIZE, HALFSIZE + 1):
						for t in xrange(-HALFSIZE, HALFSIZE + 1):
							averageLeft += leftPixPadding[i + k][j + d + t]
					averageLeft = averageLeft/(WINDOWSIZE * WINDOWSIZE)
					sumUp = 0
					sumDownLeft = 0
					sumDownRight = 0
					for k in xrange(-HALFSIZE, HALFSIZE + 1):
						for t in xrange(-HALFSIZE, HALFSIZE + 1):
							sumUp += (rightPixPadding[i + k][j + t] - averageRight) * (leftPixPadding[i + k][j + d + t] - averageLeft)
							sumDownRight += pow(leftPixPadding[i + k][j + d + t] - averageLeft, 2)
							sumDownLeft += pow(rightPixPadding[i + k][j + t] - averageRight, 2)
					result = sumUp / math.sqrt(sumDownLeft * sumDownRight)
					if result > min:
						min = result
						resultDisparity = d; 
				else:
					break
			rightResult[i][j] = resultDisparity
	rightResult *= 3
	result = Image.frombytes('L', (rightWidth, rightHeight), np.uint8(rightResult).tobytes())
	result.save('results_intensity_enhanced/' + filename + "_disp5_NCC.png")
	endTime = time.time()
	print "NCC right: ", endTime - startTime

if __name__ == "__main__":
	absolutePath = os.getcwd()
	pool = multiprocessing.Pool(processes = 2)
	flag = 0
	opts, args = getopt.getopt(sys.argv[1:], "n", [])
	for opt, value in opts:
		if opt == '-n':
			flag = 1
	for root, dirnames, filenames in os.walk("ALL-2views"):
		counter = 0
		im = []
		locks = []
		for filename in filenames:
			if root == "ALL-2views":
				break
			if filename == ".DS_Store":
				continue
			imgPath = os.path.join(root, filename)
			try:
				im.append(Image.open(imgPath).convert('L'))
				counter += 1
			except IOError:
				print "cannot open image"
		if counter == 4:
			if flag:
				im[3] = im[3].point(lambda i: i + 10)
			pool.apply_async(computeDisparity, (im[2], im[3], root.split('/')[1]))
	pool.close()
	pool.join()

			