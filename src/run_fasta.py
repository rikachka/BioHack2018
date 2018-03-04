import argparse

parser = argparse.ArgumentParser(description='hmmer genomes')

parser.add_argument(
	'--fasta', 
	help='filt with genome.', 
	default='genomes')

parser.add_argument(
	'--db_dir', 
	help='dir with db files for hmmscan processing (default: hmmDB)',
	default='hmmDB')

parser.add_argument(
	'--rep', 
	help='result file name',
	default='reps')

if __name__ == '__main__':
	args = parser.parse_args()
	fasta_path  = args.fasta
	db_dir = args.db_dir
	rep_path = args.rep
	command = 'hmmscan --tblout {0}.rep {1}/bdb {2}'.format(rep_path, db_dir, fasta_path)
	os.system(command)
