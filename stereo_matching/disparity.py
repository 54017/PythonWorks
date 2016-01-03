import os, sys
from PIL import Image
import numpy as np
import multiprocessing
import math
import time

def computeBadPixel(leftGroundTruth, rightGroundTruth, leftResult, rightResult, leftResultPath, rightResultPath):
	leftWidth, leftHeight = leftResult.size
	rightWidth, rightHeight = rightResult.size
	leftPix = np.array(leftResult.getdata()).reshape(leftHeight, leftWidth)
	rightPix = np.array(rightResult.getdata()).reshape(rightHeight, rightWidth)
	leftGroundPix = np.array(leftGroundTruth.getdata()).reshape(leftHeight, leftWidth)
	rightGroundPix = np.array(rightGroundTruth.getdata()).reshape(rightHeight, rightWidth)
	leftBadPixel = 0
	for i in xrange(0, leftHeight):
		for j in xrange(0, leftWidth):
			if (abs(leftPix[i][j] - leftGroundPix[i][j] > 3)):
				leftBadPixel += 1
	output = open('results/disparity_map.txt', 'a+')
	result = float(leftBadPixel)/(leftHeight * leftWidth)
	output.write(leftResultPath.split('/')[1] + "  " + format(result, '.2%') + "\n")
	rightBadPixel = 0
	for i in xrange(0, rightHeight):
		for j in xrange(0, rightWidth):
			if (abs(rightPix[i][j] - rightGroundPix[i][j] > 3)):
				rightBadPixel += 1
	result = float(rightBadPixel)/(rightHeight * rightWidth)
	output.write(rightResultPath.split('/')[1] + "  " + format(result, '.2%') + "\n")
	output.close()


if __name__ == "__main__":
	absolutePath = os.getcwd()
	pool = multiprocessing.Pool(processes = 2)
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
			leftResultPath = "results/" + root.split('/')[1] + "_disp1_SSD.png";
			rightResultPath = "results/" + root.split('/')[1] + "_disp5_SSD.png";
			leftResultImage = Image.open(leftResultPath).convert('L');
			rightResultImage = Image.open(rightResultPath).convert('L');
			pool.apply_async(computeBadPixel, (im[0], im[1], leftResultImage, rightResultImage, leftResultPath, rightResultPath))
	pool.close()
	pool.join()