import altair as alt
import pandas as pd
from SimSet import *
import random

# from SimSet import parse_combinations_from_file

def print_subset(entry):
    t = {u: v for u, v in entry.items() if u in ['name', 'mean', 'mean_error', 'iterations']}
    print(t)

def print_data(data):
    for f in range(len(data)):
        for r in range(len(data[f])):
            print_subset(data[f][r])

def update_data(data, sim_data):
    for f in sim_data:
        for r in f:
            for u in range(len(data)):
                for v in range(len(data[u])):
                    if data[u][v]['name'] == r['name']:
                        data[u][v] = r

uuid_1 = 'afc0ef8b-5a3e-4d2c-a320-4923e3eec676-stricter'
# uuid = str(uuid.uuid4())
files = ['fixed.simc', 'talents.simc']
combinations_1 = [parse_combinations_from_file(filename, SimSet.fixed_match) for filename in files]

test = SimSet()
test.run_sims(uuid_1, combinations_1)

data = test.sims[0].parse_json()
for sim in test.sims[1:]:
    sim_data = sim.parse_json()
    # print_data(sim_data)
    update_data(data, sim_data)

# for e in data:
#     print(e)
# print_data(data)
# print(len(data))

selector = 0

dct = {'name': [e['name'] for e in data[selector]], 'mean': [e['mean'] for e in data[selector]]}
dct = {'name': [random.random() for e in data[selector]], 'mean': [e['mean'] for e in data[selector]]}
d = pd.DataFrame(data=dct)

# d = alt.Data(values=dct)
# tmp = alt.Chart(d).mark_circle(size=5).encode(x='name:N',y='mean:Q')
tmp = alt.Chart(d).mark_circle(size=5).encode(x='name:Q',y='mean:Q')

tmp.save('chart.png', scale_factor=3.0)
