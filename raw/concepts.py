import re

with open('00-Malagasy.Reference.txt') as f:
    data = [row for row in f]

with open('../etc/concepts.tsv', 'w') as f:
    f.write('NUMBER\tENGLISH\tITALIAN\tFRENCH\tMALAGASY\n')
    for row in data[4:]:
        print(row)
        number, english, italian, french, malagasy = re.split(
                r'\s\s+',
                re.sub(r'^\s+', '', row.strip()))
        f.write('\t'.join([number, english, italian, french, malagasy])+'\n')


