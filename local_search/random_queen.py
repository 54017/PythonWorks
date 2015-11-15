import random
import getopt, sys
import re

def generate_random_queen():
	queen = range(0, 8)
	amount = 0
	opts, args = getopt.getopt(sys.argv[1:], "n:t:", [])
	for opt, value in opts:
		if opt == '-n':
			amount = value
	fileReader = open("data.txt", "w")
	reg = re.compile(r', |\[|\]')
	for i in range(int(amount)):
		random.shuffle(queen)
		fileReader.writelines(reg.sub('', str(queen)) + "\n")

	fileReader.close()

if __name__ == "__main__":
	generate_random_queen()
