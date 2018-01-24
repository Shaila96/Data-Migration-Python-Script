from glob import iglob
import csv
from collections import OrderedDict

files = sorted(iglob('*.csv'))
header = OrderedDict()
data = []

for filename in files:
    with open(filename, 'rb') as fin:
        csvin = csv.DictReader(fin)
        try:
            header.update(OrderedDict.fromkeys(csvin.fieldnames))
            data.append(next(csvin))
        except TypeError:
            print('was empty')
            # print filename, 'was empty'
        except StopIteration:
            print("didn't contain a row")
            # print filename, "didn't contain a row"

with open('output_filename.csv', 'wb') as fout:
    csvout = csv.DictWriter(fout, fieldnames=list(header))
    csvout.writeheader()
    csvout.writerows(data)