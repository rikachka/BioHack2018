import os
import sys
import pandas as pd
import numpy as np


encoding = { 
    'adaptor': 0, 'baseplate': 1, 'capsid': 2, 'capsid assembly protein': 3,
    'excisionase': 4, 'head assembly protein': 5, 'head protein': 6, 'integrase': 7,
    'integrase - transposase': 8, 'joining': 9, 'lysis protein': 10, 'nuclease': 11,
    'portal': 12, 'scaffolding protein': 13, 'tail assembly protein': 14,
    'tail protein': 15, 'tape measure protein': 16, 'terminase': 17, 'transposase': 18}


def get_model(in_size=19, classes_no=2):
    model = nn.LSTM(in_size, classes_no, 1)
    return model


if __name__ == '__main__':
    genome_path = sys.argv[1]
    data = pd.read_csv(genome_path, " ")
    bacteria = "bacterial_protein"
    model = get_model()
    model.load_state_dict(torch.load('model.h5'))
    position = 0
    putative_prophage_regions = []
    while position < len(data.query_name):
        if data.iat[position,2]==bacteria:
            position += 1
            continue
        else:
            start = position
            score = 10
            standard_length = 50
            while score > 0:
                position += 1
                if data.iat[position,2] == bacteria:
                    score-=1
                    standard_length-=1
                    if standard_length<0:
                        score-=2
                else:
                    score+=3
                    standard_length-=1
                    if standard_length<0:
                        score-=2
            end = position
            region_length = end-start
            if region_length > 15:
                putative_prophage_regions.append([start,end])
                

    sequences = []
    for region in putative_prophage_regions:
        sequence = data.values[region[0]:region[1]][:, 2]
        sequence[sequence == 'bacterial_protein'] = None
        matrix_sequence = np.zeros((len(sequence), 19))
        for index in range(len(sequence)):
            if sequence[index] is not None:
                matrix_sequence[index, encoding[sequence[index]]] = 1
        sequences.append(matrix_sequence)
        
    predictions = []
    for sequence in sequences:
        a, b = model.forward(Variable(torch.from_numpy(sequence[:, None, :].astype(np.float32))))
        predictions.append(a[-1].data.numpy()[0].argmax())
    
    np.save(sys.argv[2], np.array(predictions))
    np.save(sys.argv[3], np.array(putative_prophage_regions))