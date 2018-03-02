import sys
import os
if __name__ == '__main__':
	dirname = sys.argv[1]
	result_dir = sys.argv[2]
	files = sorted(os.listdir(dirname))
	for filename in files:
		os.system('hmmscan --tblout {0}/{1} ./hmmDB/bdb {2}/{1}'.format(result_dir, filename, dirname))