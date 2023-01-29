import requests
import json
import sys
import pickle

# def getSpec(talents, name):
#     for k in talents:
#         if k['specName'] == name:
#             return k

# def printJson(talents):
#     print(json.dumps(talents,indent=2))

# def getTalents(filename, url):
#     try:
#         print('loading from file', file=sys.stderr)
#         with open(filename, 'r') as f:
#             return json.load(f)
#     except:
#         print('loading from url', file=sys.stderr)
#         response = requests.get(url)
#         with open(filename, 'w') as f:
#             json.dump(response.json(), f)
#         return response.json()


# class Tree:
#     def __init__(self, specName, filename, url):
#         self.talents = getSpec(getTalents(filename, url), specName)
#         self.classNodes = self.talents.get('classNodes')
#         self.classMap = self.getMap(self.classNodes)
#         self.specNodes = self.talents.get('specNodes')
#         self.specMap = self.getMap(self.specNodes)
#         self.talentstring = json.dumps(self.talents, indent=2)

#     def printTalents(self, group):
#         for k in self.talents.get(group):
#             print(k['id'],k['index'],'\t',k['name'],k['next'],k['prev'])
#         print()

#     def getMap(self, obj):
#         t = []
#         id = 0
#         for talent in obj:
#             talent['index'] = id
#             t.append(talent.get('id'))
#             id += 1
#         return t

#     def findNodeByID(self, id):
#         for talent in self.specNodes:
#             if talent.get('id') == id:
#                 return talent
#         for talent in self.classNodes:
#             if talent.get('id') == id:
#                 return talent

# class Loadout:
#     def __init__(self, talents, parent, t):
#         self.talents = talents
#         self.parent = parent
#         self.type = t

#     def printSelectedTalents(self):
#         for k in range(len(self.talents)):
#             if self.talents[k] != 0:
#                 if self.type == 'classNodes':
#                     print(self.parent.classMap[k], self.talents[k], self.parent.findNodeByID(self.parent.classMap[k]).get('name'))
#                 if self.type == 'specNodes':
#                     print(self.parent.classMap[k], self.talents[k], self.parent.findNodeByID(self.parent.specMap[k]).get('name'))

#     def pathtoroot(self, node):
#         if node.get('entryNode') == True:
#             return 1
#         for prev in node.get('prev'):
#             prevnode = self.parent.findNodeByID(prev)
#             if self.talents[prevnode.get('index')] == prevnode.get('maxRanks'):
#                 return self.pathtoroot(prevnode)
#             if prevnode.get('freeNode') == True:
#                 return self.pathtoroot(prevnode)
#         return 0

#     def validate(self):
#         pts = 25
#         sum = 0
#         for talent in range(len(self.talents)):
#             if self.talents[talent] != 0:
#                 if self.type == 'classNodes':
#                     if self.parent.findNodeByID(self.parent.classMap[talent]).get('freeNode') != True:
#                         sum += self.talents[talent]
#                     if self.pathtoroot(self.parent.classNodes[talent]) == 0:
#                         return 0
#                 if self.type == 'specNodes':
#                     if self.parent.findNodeByID(self.parent.specMap[talent]).get('freeNode') != True:
#                         sum += self.talents[talent]
#                     if self.pathtoroot(self.parent.specNodes[talent]) == 0:
#                         return 0
#         if self.type == 'classNodes' and sum == 31:
#             return 1, sum
#         if self.type == 'specNodes' and sum == 30:
#             return 1, sum
#         return 0, sum


# def setBase(talent, a, b):
#     if talent.get('freeNode') == True:
#         return 0
#     elif talent.get('id') in a:
#         return talent.get('maxRank')
#     elif talent.get('id') in b:
#         return 0
#     else:
#         return None

# def generateLoadouts(tree, a, b, c, d, t):
#     # a = list of all mandatory talents
#     # b = list of all banned talents
#     # c = list of lists of talents that all must be allocated if one is allocated
#     # d = list of lists of mutually exclusive talents

#     # if a => set to max
#     # if b => set to 0
#     # if c => check others in group
#     # if d => check others in group
#     loadouts = []
#     arr = []
#     tr = []
#     if t == 'classNode':
#         for talent in tree.classNodes:
#             arr.append(setBase(talent, a, b))
#     if t == 'specNode':
#         for talent in tree.specNodes:
#             arr.append(setBase(talent, a, b))
#     while True:
#         loadouts.append(Loadout(talents, tree, t))

# # base string
# talents = "BwQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQhSLJJgkENCAAAQakSSkIhESSSSKJ4AAkWKA"
# filename = 'talents.json'
# url = 'https://www.raidbots.com/static/data/beta/new-talent-trees.json'

# te = Tree('Brewmaster', filename, url)
# printJson(te.classNodes)

# # te.printTalents('classNodes')
# # te.printTalents('specNodes')

# c = [1,1,0,0,1,0,0,1,0,0,1,2,0,2,1,0,1,1,1,1,0,1,2,1,1,1,1,0,1,1,1,2,0,0,2,0,0,2,0,0,1,0]
# lo = Loadout(c, te, 'classNodes')
# print(lo.validate())
# lo.printSelectedTalents()


# d = [1,1,1,1,1,2,0,0,1,0,1,0,0,1,0,1,1,1,1,0,1,1,0,1,1,1,0,1,1,2,0,2,0,0,1,0,1,0,1,1,0,1]
# ln = Loadout(d, te, 'specNodes')
# print(ln.validate())
# ln.printSelectedTalents()

# options:
# 1:
#   - rjw v sd
# 2:
#   - bob v bnw
#   - lb v ton
#   - clash v fp (clash used as a dead point)
# 3:
#   - dfb v chp
#   - 9 points spent on:
#     * if one point spent on wwto, 3 points spent on r2 niuzao
#     * non-fp: anything except ans or cs
#     * fp: anything except ans

# def tmp():
pairs = [
    '101549:0/101548:1',  # sd
    '101549:1/101548:0',  # rjw
    '101447:0/101448:1',  # lb
    '101447:1/101448:0',  # ton
    '101450:0/101449:1',  # bnw
    '101450:1/101449:0',  # bob
    '101465:0/101466:1',  # dfb
    '101465:1/101466:0',  # chp
    '101440:0/101442:1',  # fp
    '101440:1/101442:0'   # clash
]

m = {
    'ht1':{'p':['head'],'c':1,'id':0},
    'ht2':{'p':['ht1'],'c':1,'id':1},
    'wwto':{'p':['head'],'c':3,'id':2},
    'ef1':{'p':['head'],'c':1,'id':3},
    'ef2':{'p':['ef1'],'c':1,'id':4},
    'cs':{'p':['head'],'c':1,'id':5},
    'bdb':{'p':['head'],'c':1,'id':6},
    'ek':{'p':['wwto','ef2'],'c':1,'id':7},
    'boc':{'p':['ef2'],'c':1,'id':8},
    'woo':{'p':['ef2','cs'],'c':1,'id':9},
    'bb':{'p':['bdb'],'c':1,'id':10},
    'sslk':{'p':['wwto','ek','boc'],'c':1,'id':11},
    'cta':{'p':['woo'],'c':1,'id':12},
    'sur':{'p':['woo'],'c':1,'id':13}
}

arr2 = [
    '101469:1',
    '101469:2',
    '101543:2/101540:1',
    '101412:1',
    '101412:2',
    '101411:1',
    '101552:1',
    '101542:1',
    '101411:1',
    '101539:1',
    '101551:1',
    '101541:1',
    '101538:1',
    '101537:1',
]

def pathtoroot(node, str, tree):
    for k in tree[node]['p']:
        if k == 'head':
            return 1
        if str[tree[k]['id']] == '1':
            return pathtoroot(k, str, tree)
    return 0

def validatestring(str,tree):
    sum = 0
    valid = True
    for k in range(len(str)):
        if str[k] == '1':
            if k == 2:
                sum += 3
            else:
                sum += 1
            for u, v in tree.items():
                if v['id'] == k:
                    if pathtoroot(u,str,tree) != 1:
                        valid = False
    if sum == 9 and valid == True:
        return 1
    return 0

c = 5
d = 13
ct = 0
id = 0
for k in range(2**c):
    t = ''
    fmt = '{0:0'+f'{c}'+'b}'
    rts = fmt.format(k)
    for k in range(c):
        t += '/'
        if rts[k] == '1':
            t += pairs[2*k]
        else:
            t += pairs[2*k+1]
    for l in range(2**d):
        id += 1
        u = ''
        fmtb = '{0:0'+f'{d}'+'b}'
        strb = fmtb.format(l)
        if strb[5] == '1':
            if rts[4] != '1':
                continue
        if not validatestring(strb, m):
            continue
        if strb[11] == '1' and strb[12] == '1':
            continue
        ct += 1
        for l in range(d):
            if strb[l] == '1':
                u += '/'+arr2[l]
        print('#',id,ct,rts,strb)
        name = 'profileset.'+str(id)
        tal = 'spec_talents+='+t+'/'+u
        print(name+'+='+tal)
        # print('spec_talents+='+t+'/'+u)
        # print('spec_talents+='+u)

# print('#',ct)
# print(validatestring('11011000000000',m))

q = '11100011001100'
q = '11011011111000'
# print(validatestring(q,m))




# Given a set of required and banned nodes:
# Find all paths from the head of the tree to the next barrier where all paths contain:
# - All required nodes
# - No banned nodes
# - Contain at least k points, where k is the minimum requirement to proceed.
#
# Augment this set with all variants of those paths which fulfil all previous requirements to the next threshold
