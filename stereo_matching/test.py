from PIL import Image
import numpy as np

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
			print "X", X
			result[i][j] = float(round(X, 4)) / 95.047
			result[i][j + 1] = float(round(Y, 4)) / 100.0
			result[i][j + 2] = float(round(Z, 4)) / 108.883
			print "result", result[i][j]
	for i in xrange(0, height):
		for j in xrange(0, 3 * width):
			if result[i][j] > 0.008856:
				result[i][j] = result[i][j] ** (1.0/3)
				print "1/3", result[i][j]
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

if __name__ == '__main__':
	im = Image.open("test.jpg")
	a = np.asarray(list(im.getdata())).reshape(1, 3);
	print a
	print rgb2lab(a, 1, 1)


