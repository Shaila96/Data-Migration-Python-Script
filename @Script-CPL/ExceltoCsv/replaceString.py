with open("Text\\abc.tp", "rt") as fin:
    with open("Csv\\replaced_file.csv", "wt") as fout:
        for line in fin:
            fout.write(line.replace(':', ','))