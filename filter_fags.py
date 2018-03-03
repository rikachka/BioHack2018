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
    
    clean_dir(result_dirname)
    filenames = [filename for filename in sorted(os.listdir(input_dirname)) if filename.endswith('csv')]
    for filename in filenames:
        input_file_path = '{}/{}'.format(input_dirname, filename)
        
        vog_anno = pd.read_csv(input_file_path, sep='\t')
        vog_anno['is_capsid'] = vog_anno.short_anno.apply(lambda cur_anno: int(cur_anno == 'capsid'))
        vog_anno['is_integrase'] = vog_anno.short_anno.apply(lambda cur_anno: int(cur_anno == 'integrase'))
        vog_anno['is_transposase'] = vog_anno.short_anno.apply(lambda cur_anno: int(cur_anno == 'transposase'))
        
        if (len(vog_anno) > 0 
            and (vog_anno.is_integrase.sum() == 1 or vog_anno.is_transposase.sum() == 1)
            and vog_anno.is_capsid.sum() >= 1
           ):
            result_file_path = '{}/{}'.format(result_dirname, filename)
            vog_anno.to_csv(result_file_path, sep='\t')