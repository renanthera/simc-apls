#!/bin/python
import re
import uuid
import subprocess
import json

def parse_talent_strings(filename):
    data = []
    match_str = 'talents=(.*)'
    with open(filename) as file:
        for line in file:
            match = re.search(match_str, line)
            if match and match.group(1) not in data:
                data.append(match.group(1))
    return data

def format_talent_strings(talent_strings, uuid):
    data = []
    a = 'profileset.\''
    b = '\'+=talents='
    suffix = '_' + str(uuid)

    for talents in talent_strings:
        data.append(a + talents + suffix + b + talents + '\n')
    return data

def parse_apl(filename, uuid='', lines=['']):
    data = []
    blacklist = ['\n', '#']
    fragments = ['name', 'html', 'output']
    uuid = str(uuid)
    with open(filename) as file:
        for line in file:
            if line[0] not in blacklist and line[0:7] != '$(name)':
                data.append(line)
            elif line[0:7] == '$(name)':
                data.append('$(name)=' + uuid + '\n')
    for line in lines:
        data.append(line + '\n')
    return data

def parse_json(filename):
    l = []
    # select = ['name', 'mean', 'mean_error']
    with open('cache/'+filename+'.json') as file:
        data = json.load(file)
    for entry in data['sim']['profilesets']['results']:
        l.append(entry)
        # l.append({k:entry[k] for k in select})
    l.sort(key=lambda e: e['mean'])
    return l

def compute_maximums(data):
    m = {}
    for entry in data:
        if m == {}:
            m = entry
        else:
            for key in entry:
                m[key] = max(m[key], entry[key])
    return m

def reduce_sims(uuid):
    l = []
    data = parse_json(str(uuid))
    maximums = compute_maximums(data)
    for entry in data:
        if entry['mean'] >= maximums['mean'] - maximums['mean_error'] * 2:
            l.append(entry['name'].split('_')[0])
    return l

def write_file(filename, data):
    string = ''
    filename = str(filename)
    for line in data:
        string += line
    with open('cache/' + filename + '.simc', 'w') as file:
        file.write(string)
    with open('cache/uuid-index', 'a') as file:
        file.write(filename + '\n')

def generate_sim(uuid):
    suffixes = ['json2=cache/$(name).json', 'html=/dev/null', 'output=/dev/null', '']

    talent_strings = parse_talent_strings('talents.simc')
    talent_strings_formatted = format_talent_strings(talent_strings, uuid)
    apl_header = parse_apl('brm.simc', uuid=uuid, lines=suffixes)
    apl = parse_apl('apl.simc')

    f = apl_header + apl + talent_strings_formatted

    write_file(uuid, f)

def run_sim(uuid):
    subprocess.run(['./simc', 'cache/' + str(uuid) + '.simc'])

def generate_child(configurations):


# def prune_cache(age=current_simc_version(?)):
# remove all files older than (age), remove all `.simc` without matching `.json`, clean up abandoned uuids from index
# possibly instead use simc build data of a date

# def improved(value)
# display which configurations have improved over the past (value) generations
# this possibly gets spun off elsewhere w/ helpers to better display what is improving/worsening graphically

# uuid = uuid.uuid4()
# generate_sim(uuid)
# run_sim(uuid)


d = reduce_sims('cac4151a-3121-433f-9c4d-10988a955b27')
for k in d:
    print(k)
# maximums = compute_maximums(d)
# ct = 1
# for e in d:
#     if e['mean'] >= maximums['mean'] - maximums['mean_error']*2:
#         print(ct, e)
#         ct += 1

# print(maximums)
