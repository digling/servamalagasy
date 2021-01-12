from collections import defaultdict
from glob import glob
import re

files = glob('*.txt')
D = {}
idx = 1
for path in files:
    if not path.startswith('00'):
        with open(path) as f:
            data = [row for row in f]
        language_name = re.split(
                r'\s\s+', re.sub('^\s+', '', data[1]))[-1].strip()
        print(path, language_name)
        for row in data[4:]:
            number, french, malagasy, form  = re.split(
                    r'\s\s+', 
                    re.sub('^\s+', '', row)
                    )
            if form.strip():
                D[idx] = [language_name, path, number, french, malagasy,
                        form.strip()]
                idx += 1
with open('data.tsv', 'w') as f:
    f.write('ID\tLANGUAGE\tFILENAME\tNUMBER\tFRENCH\tMALAGASY\tFORM\n')
    for idx, vals in sorted(D.items()):
        f.write(str(idx)+'\t'+'\t'.join(vals)+'\n')
