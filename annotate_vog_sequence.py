import os
import sys
import pandas as pd
import numpy as np


def clean_dir(to_dir):
    tree_dir = to_dir
    tree = os.walk(tree_dir)
    existed = False
    for dir, subdirs, files in tree:
        existed = True
        if dir == tree_dir:
            for file in files:
                os.remove(dir + '/' + file)
    if (not existed):
        os.makedirs(to_dir)
        

if __name__ == '__main__':
    input_dirname = sys.argv[1]
    result_dirname = sys.argv[2]
    
#    vog_anno = pd.read_table('VOG_with_short_anno.txt', sep='\t')
    vog_anno = pd.read_table('vogs_with_anno_and_vq.txt', sep='\t')
    vog_anno = vog_anno.filter(items=['VOG.number', 'Short.Annotations', 'Viral Quotient'])
    vog_anno = vog_anno.rename(index=str, columns={'VOG.number': 'vog_number', 'Short.Annotations': 'short_anno', 'Viral Quotient': 'viral_quotient'})
    vog_anno = vog_anno.dropna()
    vog_anno = vog_anno.set_index('vog_number')
    
    existing_anno = vog_anno.groupby('short_anno', as_index=False).first()
    
    clean_dir(result_dirname)
    filenames = [filename for filename in sorted(os.listdir(input_dirname)) if filename.endswith('.rep.npy')]
    for filename in filenames:
        input_file_path = '{}/{}'.format(input_dirname, filename)
        vog_sequence = np.load(input_file_path)
        vog_sequence_df = pd.DataFrame(vog_sequence, columns=['vog'])
        vog_seq_anno = vog_sequence_df.join(vog_anno, on='vog')
        
        vog_seq_matrix = vog_seq_anno.copy()
        for anno in existing_anno.values.flatten():
            vog_seq_matrix[anno] = vog_seq_matrix.short_anno.apply(lambda cur_anno: int(cur_anno == anno))
            vog_seq_matrix[anno] = vog_seq_matrix.short_anno.apply(lambda cur_anno: int(cur_anno == anno))
            
        
#        result_file_path = '{}/{}'.format(result_dirname, filename) + '.csv'
#        vog_seq_matrix.to_csv(result_file_path, sep='\t')
        
        result_file_path = '{}/{}'.format(result_dirname, filename) + '.xlsx'
        vog_seq_anno.to_excel(result_file_path)