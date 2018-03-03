def parse_enzymes(file_path):
    f = open(file_path)
    enzymes = []
    enzyme_id = -1
    for line in lines:
        if line[0] == '>':
            enzymes.append([line])
            enzyme_id += 1
        else:
            enzymes[enzyme_id].append(line)
    f.close()
    return enzymes


# unique_sequences = [set(sequence) for sequence in sequences]
# sequences = [np.load('numpy_dir/{}'.format(filename)) for filename in sorted(os.listdir('numpy_dir/'))]
def get_frequency(sequences):
    copyness = {}
    total = 0
    for sequence in sequences:
        for wog in sequence:
            if wog is not None:
                total += 1
                if wog in copyness:
                    copyness[wog] += 1
                else:
                    copyness[wog] = 1
    for key, value in copyness.items():
        copyness[key] = value / total
    return copyness

