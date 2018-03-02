import os
import sys
import pandas as pd
import numpy as np


def parse_line(line):
    splitted = line.split(' ')
    splitted = [value for value in splitted if value != '' and value != '-'][:3]
    return splitted


def soft_mkdir(dirname):
    try:
        os.mkdir(dirname)
    except Exception as e:
        print('directory has been created before')
        

if __name__ == '__main__':
    dirname = sys.argv[1]
    numpy_dir = 'numpy_dir'
    soft_mkdir(numpy_dir)
    filenames = [filename for filename in sorted(os.listdir(dirname)) if filename.endswith('.rep')]
    for filename in filenames:
        with open('{}/{}'.format(dirname, filename)) as f:
            lines = f.readlines()
            filtered = [parse_line(line) for line in lines if not line.startswith('#')]
            dataframe = pd.DataFrame(filtered, columns=['target_name', 'query_name', 'e_value'])
            dataframe['e_value'] = dataframe.e_value.astype(float)
            grouped = dataframe.groupby('query_name').first()
            grouped[grouped['e_value'] > 1e-5] = None
            sequence = grouped['target_name'].values
            np.save('{}/{}'.format(numpy_dir, filename), sequence)