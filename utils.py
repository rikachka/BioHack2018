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