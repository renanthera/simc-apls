#!/bin/python
import re
import uuid
import subprocess
import json
import shutil
import os
import itertools

def parse_strings_from_file(filename, search):
    data = []
    with open(filename) as file:
        contents = file.read()
    matches = re.findall(search, contents, re.MULTILINE)
    if matches:
        for match in matches:
            if match not in data:
                data.append(match)
    return data

class Sim:
    apl_header_match = '^(?![\s#]|\$\(name\)|html|output|target_error).*$'
    apl_match        = '^(?![\s#]|\$\(name\)|html|output|target_error).*$'
    fixed_match      = '.+'
    talents_match    = '^(?![\s#]).*talents=(.*)$'
    write_dir = 'cache/'
    uuid_index = 'uuid-index'

    def __init__(self, apl_components, index, target_error):
        self.apl_components = apl_components
        # self.apl_header = apl_header
        # self.apl = apl
        # self.fixed = fixed
        # self.talents = talents
        # self.names = combinations
        self.index = index
        self.target_error = target_error

        self.uuid = 'afc0ef8b-5a3e-4d2c-a320-4923e3eec676/'
        # self.uuid = str(uuid.uuid4()) + '/'
        # TODO: self.index is a str already
        self.file_path = self.write_dir + self.uuid + str(self.index) + '/'

        self.apl_header.append('output=/dev/null')

        self.generate_profilesets()
        self.write_sim()


    def write_sim(self):
        contents = ''
        names = ''
        data = []
        # name = ['$(name)=' + self.uuid[:-1] + '_' + str(self.index) + '\n']
        json = ['json2=' + self.file_path + 'output.json']
        target_error = ['target_error='+str(self.target_error)]
        data = self.apl_header + json + target_error + [''] + self.apl + [''] + self.profilesets
        for entry in self.apl_components:
            data += entry + ['']

        for line in data:
            contents += line + '\n'
        # TODO: intelligently format this file (json?)
        for name in self.names:
            for u in name:
                names += u + '_'
            names = names[:-1] + '\n'
        os.makedirs(self.file_path, exist_ok=True)
        with open(self.file_path + 'simulation.simc', 'w+') as file:
            file.write(contents)
        with open(self.file_path + 'names', 'w+') as file:
            file.write(names)
        with open(self.write_dir + self.uuid_index, 'a+') as file:
            file.write(self.uuid + '\n')
        for k,v in self.apl_components['files_to_copy']:
            shutil.copy(k, self.file_path)


    def generate_profilesets(self):
        self.profilesets = []
        # TODO: make this work with more fixed types
        prefix = 'profileset.'
        talents = 'talents='
        for combination in self.names:
            name = prefix + combination[0] + '+='
            self.profilesets.append(name + talents + combination[2] + '\n' + name + combination[1])

    # TODO: rework json parser
    def parse_json(self):
        data = []
        with open(self.file_path + 'output.json') as file:
            contents = json.load(file)
        for entry in contents['sim']['profilesets']['results']:
            data.append(entry)
        data.sort(key = lambda e: e['mean'])
        return data

    # TODO: rework json parser
    def compute_maximums(self, data):
        m = {}
        for entry in data:
            if m == {}:
                m = entry
            else:
                for key in entry:
                    m[key] = max(m[key], entry[key])
        return m

    def extract_profilesets(self):
        self.target_error /= 4

        data = self.parse_json()
        maximums = self.compute_maximums(data)
        self.generate_file_path()

        l = []
        for entry in data:
            if entry['mean'] >= maximums['mean'] - maximums['mean_error'] * 2:
                l.append(entry['name'])
        temp = []
        for entry in self.names:
            if entry[0] in l:
                print(entry)
                temp.append(entry)
        self.names = temp
        self.generate_profilesets()
        self.write_sim()

    def run_sim(self):
        subprocess.run(['./simc', self.file_path + 'simulation.simc'])

class SimSet:
    def __init__(self):
        self.sims = []
        self.sim_iter = iter(self.sims)
        self.create_sim()

    # def create_sim(self, fixed, talents):
    def create_sim(self):
        uuid = 'afc0ef8b-5a3e-4d2c-a320-4923e3eec676/'
        # uuid = str(uuid.uuid4()) + '/'
        index = 1
        count = itertools.count(1)
        fixed = parse_strings_from_file('fixed.simc', Sim.fixed_match)
        talents = parse_strings_from_file('talents.simc', Sim.talents_match)
        combinations = [(str(next(count)), u, v) for u in fixed for v in talents]
        apl_components = {
            'strings':    [ parse_strings_from_file('brim.simc', Sim.apl_header_match),
                            parse_strings_from_file('apl.simc', Sim.apl_match),
                            ]
            'parameters': { '':,
                            'target_error': 0.5,
                            'json2':
                           }
        }
        sim_components = {
            'files_to_copy': [ 'brm.simc',
                               'apl.simc',
                               'fixed.simc',
                               'talents.simc'
                              ],
            'parameters':     { 'uuid': uuid,
                                'index': index,
                                'file_path': Sim.write_dir + uuid + '/' + index + '/'
                               }
        }
        index = len(self.sims) + 1
        self.sims.append(Sim(apl_components, index, 0.5 / (2 ** index)))

    def run_sim(self):
        current = next(self.sim_iter)
        current.run_sim()
        current.extract_profilesets()



test = SimSet()
# # test.run_sim()
# test.extract_profilesets()
# # test.run_sim()
# test.extract_profilesets()
# test.run_sim()
# test.extract_profilesets()
