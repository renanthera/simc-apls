import re

#########
# USAGE #
#########

# configure inputfilename
# run script
# redirect stdout to target file
# ???
# profit

inputfilename = 'brm.simc'

with open(inputfilename, 'r') as inputfile:
    i = inputfile.readlines()

templates = {}

for k in i:
    if (k[0] == '$'):
        temp = k[:-1].split('=', 1)
        temp[0] = "\\" + temp[0][0] + "\\" + temp[0][1:-1] + "\\" + temp[0][-1:]
        templates[temp[0]] = temp[1]

# print()

# for k in templates:
#     print(k, templates[k])

# print()

def recurseTemplates():
    c = 0
    for k in templates:
        for l in templates:
            s = re.sub('('+l+')', templates[l], templates[k])
            if (s != templates[k]):
                c += 1
                templates[k] = s
    return c

t = 1
while (t != 0):
    t = recurseTemplates()

# for k in templates:
#     print(k, templates[k])

arr = []
for k in range(len(i)-1):
    if (i[k][0] == '$'):
        arr.append(k)
for k in arr:
    i[k] = '# '+i[k]

# print()

for k in range(len(i)-1):
    if (i[k][0] == '#'):
        continue
    # print(i[k],end='')
    for l in templates:
        s = re.sub('('+l+')', templates[l], i[k])
        if (s != i[k]):
            i[k] = s

for k in i:
   print(k, end='')
