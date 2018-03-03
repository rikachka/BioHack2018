import os
import sys
import pandas as pd
import numpy as np


def parse_line(line):
    splitted = line.split(' ')
    splitted = [value for value in splitted if value != '' and value != '-'][:3]
    return splitted


def parse_enzymes_names(file_path):
    f = open(file_path)
    lines = f.readlines()
    enzymes = []
    enzyme_id = -1
    for line in lines:
        if line[0] == '>':
            enzymes.append(line[1:].split(' ', 1)[0])
            enzyme_id += 1
    f.close()
    return pd.DataFrame(enzymes)


def soft_mkdir(dirname):
    try:
        os.mkdir(dirname)
    except Exception as e:
        print('directory has been created before')
        

if __name__ == '__main__':
    dirname = sys.argv[1]
    source_fasta = sys.argv[2]
    numpy_dir = sys.argv[3]
    soft_mkdir(numpy_dir)
    fasta_names = [filename for filename in sorted(os.listdir(source_fasta))]
    filenames = [filename for filename in sorted(os.listdir(dirname)) if filename.endswith('.rep')]
    if len(fasta_names) != len(filenames):
        raise(Exception('Different number of files .rep and .faa'))
    for filename, fasta_name in zip(filenames, fasta_names):
        with open('{}/{}'.format(dirname, filename)) as f:
            lines = f.readlines()
            filtered = [parse_line(line) for line in lines if not line.startswith('#')]
            dataframe = pd.DataFrame(filtered, columns=['target_name', 'query_name', 'e_value'])
            dataframe['e_value'] = dataframe.e_value.astype(float)
            grouped = dataframe.groupby('query_name').first()
            grouped[grouped['e_value'] > 1e-5] = None
            names = parse_enzymes_names('{}/{}'.format(source_fasta, fasta_name))
            names = names.join(grouped, on=0)
            sequence = names['target_name'].values
            np.save('{}/{}'.format(numpy_dir, filename), sequence)
