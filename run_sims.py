#!/bin/python
import re
import uuid
import subprocess

def parse_talent_strings(filename):
    data = []
    match_str = 'talents=(.*)'
    with open(filename) as file:
        for line in file:
            match = re.search(match_str, line)
            if match and match.group(1) not in data:
                data.append(match.group(1))
    return data

def format_talent_strings(filename, uuid):
    data = []
    a = 'profileset.\''
    b = '\'+=talents='
    suffix = '_' + str(uuid)
    talent_strings = parse_talent_strings(filename)

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

def write_file(filename, data):
    filename = str(filename)
    string = ''
    for line in data:
        string += line
    with open('cache/' + filename + '.simc', 'w') as file:
        file.write(string)
    with open('cache/uuid-index', 'a') as file:
        file.write(filename + '\n')

suffixes = ['json2=cache/$(name).json', 'html=/dev/null', 'output=/dev/null', '']
uuid = uuid.uuid4()

talent_strs = format_talent_strings('talents.simc', uuid)
apl_header = parse_apl('brm.simc', uuid=uuid, lines=suffixes)
apl = parse_apl('apl.simc')

f = apl_header + apl + talent_strs

write_file(uuid, f)

# subprocess.run(['./simc', 'cache/' + str(uuid) + '.simc'])
