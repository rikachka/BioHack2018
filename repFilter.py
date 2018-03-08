import sys
import pandas as pd

#Аргументы: fasta_file.faa re_file.rep limit_VQ limit_E-value
#Пример запуска:  
#python repFilter.py Salmonella_CT18.faa Salmonella_CT18.rep 0.85 1e-3

if __name__ == '__main__':
    input_faa = sys.argv[1]
    input_rep = sys.argv[2]
    input_lim_VQ = float(sys.argv[3])
    input_lim_E_value = float(sys.argv[4])

def extract_func_from_rep(query_name):
    sub_rep = rep_w_anno[rep_w_anno['query_name'] == query_name]
    if (sub_rep.empty):
        return 'bacterial_protein'
    else: 
        if (sub_rep[sub_rep['short_anno'].notna()].empty):
            return 'bacterial_protein'
        func_groups = sub_rep[sub_rep['short_anno'].notna()]
        min_E_value = func_groups['e-value'].min()
        if (min_E_value > input_lim_E_value):
            return 'bacterial_protein'
        return func_groups[func_groups['e-value'] == min_E_value].iloc[0, 3]

dict_vog_anno_and_vq = {}
with open('vogs_with_anno_and_vq.txt') as ann:
    ann.readline()
    for line in ann:
        temp_split = line.replace('"', '').split('\t')
        vq = float(temp_split[12].strip())
        vog = temp_split[1]
        short_anno = temp_split[9]
        if vq > input_lim_VQ:
            dict_vog_anno_and_vq[vog] = [short_anno, vq]

protein_list = []
with open(input_faa) as fasta:
    for line in fasta:
        if line.startswith('>'):
            protein_list.append(line.split('\t')[0].strip('>'))

rep = pd.read_csv(input_rep, sep='\s+', header=None,
                  skiprows=3, skipfooter=10, usecols=[0, 2, 4], 
                  names=['vog', 'query_name', 'e-value'], engine='python')
rep['e-value'] = rep['e-value'].astype(float)

rep['short_anno'] = rep['vog'].apply(lambda x: dict_vog_anno_and_vq[x][0] if x in dict_vog_anno_and_vq else None)
rep['vq'] = rep['vog'].apply(lambda x: dict_vog_anno_and_vq[x][1] if x in dict_vog_anno_and_vq else None)
rep_w_anno = rep

seq_with_functional_anno = pd.DataFrame(protein_list, columns=['query_name'])
seq_with_functional_anno['ID'] = range(1, seq_with_functional_anno.shape[0]+1)
seq_with_functional_anno['target_name'] = seq_with_functional_anno['query_name'].apply(extract_func_from_rep)
seq_func = seq_with_functional_anno

seq_func.to_csv('repFilter_result.txt', sep='\t')



