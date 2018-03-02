import sys
import os
import argparse

parser = argparse.ArgumentParser(description='hmmer genomes')

parser.add_argument(
	'--source_dir', 
	help='dir with genomes. all .faa files will be processed (default: genomes)', 
	default='genomes')

parser.add_argument(
	'--db_dir', 
	help='dir with db files for hmmscan processing (default: hmmDB)',
	default='hmmDB')

parser.add_argument(
	'--result_dir', 
	help='dir where will be saved .rep files (default: reps)',
	default='reps')

def soft_mkdir(dirname):
    try:
        os.mkdir(dirname)
    except Exception as e:
        print('directory has been created before')


if __name__ == '__main__':
	args = parser.parse_args()
	dirname = args.source_dir
	db_dir = args.db_dir
	result_dir = args.result_dir
	soft_mkdir(result_dir)
	files = sorted(os.listdir(dirname))
	for filename in files:
		command = 'hmmscan --tblout {0}/{2}.rep {1}/bdb {3}/{2}'.format(result_dir, db_dir, filename, dirname)
		print(command)
		os.system(command)
