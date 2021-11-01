import extremals as xt
import pandas as pd
import numpy as np
from numpy import nan

def unpack(obj, name):
    diz = {}
    try:
        for x in obj.columns:
            diz[x] = list(obj[x].values)
    except:
        diz[obj.name] = list(obj.values)
        
    print('r=repack(%s,%s)' %(str(diz), str(list(obj.index))))
    print('if not AreEqual(r,%s): problem()' %name)
    return (diz, list(obj.index))


def repack(diz, index):
    if len(diz.keys()) == 1:
        for name in diz.keys():
            return pd.Series(diz[name], index = index, name = name)
    return pd.DataFrame(diz, index = index)
    
def round_list(l, digit = 10):
    return [round(x,digit) for x in l]

def round_obj(obj, digit = 10):
    if type(obj) == pd.Series:
        for x in obj.index: obj[x] = round(obj[x],digit)
    elif type(obj) == pd.DataFrame:
        [ round_obj(obj[c], digit) for c in  obj.columns]
            
def represent(obj, name):
    if type(obj) == pd.Series:
        print('index = %s' %list(obj.index))
        print('values = %s' %list(obj.values))
        print("if list(%s.index) != index or list(%s.values) != values: problem()" % (name, name))

def problem(): raise Exception('Problems here') 

def AreEqual(obj1,obj2):
    obj1 = obj1.round(10)
    obj2 = obj2.round(10)
    return obj1.equals(obj2)
    
    if type(obj1) == pd.Series:
        if list(obj1.index) != list(obj2.index) or round_list(obj1.values) != round_list(obj2.values):
            return False
        return True
    elif type(obj1) == pd.DataFrame:
        if list(obj1.columns) != list(obj2.columns): return False
        for c in obj1.columns:
            if not AreEqual(obj1[c], obj2[c]): return False
        return True
    
pd.set_option("display.precision", 6)

data = pd.DataFrame( 
    {'col1': [3, 100, 1, -3, None, 9, 22, 8, 9, 0],  
    'col2': [100, 200, -123, None, 7, -34.5, 95, 3, 12, -567], 
    'col3' : [0, 74, -13.4, 44, 21, 3, -4, None, None, 21]},
     index = list('abcdefghil')
     )


# ~ melb_data = pd.read_csv('/home/tonini/Downloads/melb_data.csv')
# ~ melb_data = melb_data[xt.Test.filter(melb_data)]

#### extremals.Test

test = xt.Test(function = lambda x : (x[1]-x[2])**2/x[0], name = 'custom' )
result = test.Apply(data)

"""
    # result is the series
    f    1.562500e+02
    b    1.587600e+02
    g    4.455000e+02
    a    3.333333e+03
    c    1.201216e+04
    l             inf
    Name: custom, dtype: float64
"""

test = xt.Test(function = lambda x : sum(x), name='Sum', normalized = True)
result = test.Apply(data)
values = [-0.762235122784632, -0.1683758367113834, -0.005086227851983096, 0.1764270220315841, 0.19089022919362134, 0.568379936122793]
index = ['l', 'c', 'f', 'a', 'g', 'b']
if list(result.index) != index or list(result.values) != values: problem()
    

    
### extremals.ColTest

ctest = xt.ColTest('col1')
result = ctest.Apply(data)
index = ['d', 'l', 'c', 'a', 'h', 'f', 'i', 'g', 'b']
values = [-3.0, 0.0, 1.0, 3.0, 8.0, 9.0, 9.0, 22.0, 100.0]
if list(result.index) != index or list(result.values) != values: problem()
   
if not AreEqual(result, data['col1'].dropna().sort_values()):  problem()

ctest.normalized = True # or ctest = extremal.ColTest('col1', normalized = True)
result_nor = ctest.Apply(data)
index = ['d', 'l', 'c', 'a', 'h', 'f', 'i', 'g', 'b']
values = [-0.21514027654772339, -0.18213580230460674, -0.17113431089023454, -0.1491313280614901, -0.094123870989629, -0.08312237957525678, -0.08312237957525678, 0.05989700881158206, 0.9180133391326151]
if list(result_nor.index) != index or list(result_nor.values) != values: problem()
    
if not AreEqual(xt.Normalize(result),result_nor): problem()

### extremals.ColDiffTest

cdtest = xt.ColDiffTest('col1','col2')
result = cdtest.Apply(data)
if not AreEqual(result, (data['col2']-data['col1']).dropna().sort_values()):  problem()
index = ['l', 'c', 'f', 'h', 'i', 'g', 'a', 'b']
values = [-567.0, -124.0, -43.5, -5.0, 3.0, 73.0, 97.0, 100.0]
if list(result.index) != index or list(result.values) != values: problem()

cdtest.normalized = True # or cdtest = extremal.ColDiffTest('col1','col2', normalized = True)
result_nor = cdtest.Apply(data)
index = ['l', 'c', 'f', 'h', 'i', 'g', 'a', 'b']
values = [-0.8771432832445585, -0.11326669009583867, 0.025541584731411764, 0.09192815095314023, 0.1057227621160968, 0.22642560979196674, 0.26780944328083645, 0.27298242246694515]
if list(result_nor.index) != index or list(result_nor.values) != values: problem()

if not AreEqual(xt.Normalize(result),result_nor): problem()

    
### extremals.TWDTest

twd = xt.TWDTest() # all columns will be used
result = twd.Apply(data)
index = ['e', 'h', 'i', 'f', 'd', 'g', 'a', 'c', 'l', 'b']
values = [0.10282733873740618, 0.1539047877881331, 0.15737939281824168, 0.28241265262150894, 0.5524992456406854, 0.5579414249442527, 0.6029143038582063, 0.7272181018081674, 1.075786928286798, 2.024296762680489]
if list(result.index) != index or list(result.values) != values: problem()

twd2 = xt.TWDTest(keys = ['col3'])
result2 = twd2.Apply(data)
index = ['e', 'l', 'f', 'a', 'g', 'd', 'c', 'b']
values = [0.03661260129691062, 0.03661260129691062, 0.1987541213260862, 0.23798190842991898, 0.2902856245683627, 0.3373589690929621, 0.41319935749370557, 0.72963684013129]
if list(result2.index) != index or list(result2.values) != values: problem()

result_2 = abs(xt.ColTest('col3', normalized = True).Apply(data)).sort_values()

if not AreEqual(result2, result_2): problem()

#### extremals.Extremals

tests = [
    xt.ColTest('col3', normalized = True),
    xt.Test(function = lambda x: x[2] - x[1] -x[0], name = 'custom'),
    xt.TWDTest(name = 'TWD on data')
]

extr = xt.Extremals(data, tests)
result = extr.Run()
r = repack(\
{'col3': [nan, nan, 0.03661260129691063, 0.3373589690929622, -0.19875412132608622, -0.23798190842991904, -0.4131993574937056, -0.29028562456836277, 0.03661260129691063, 0.7296368401312903], 'custom' : [nan, nan, nan, nan, 28.5, -103.0, 108.6, -121.0, 588.0, -226.0], 'TWD on data': [0.15737939281824168, 0.1539047877881331, 0.10282733873740618, 0.5524992456406854, 0.28241265262150894, 0.6029143038582063, 0.7272181018081674, 0.5579414249442527, 1.075786928286798, 2.024296762680489], 'TWD': [0.26867966365321205, 0.27068154706673736, 0.336722269595787, 0.3783914979306518, 0.42210236862515116, 0.4790865060192545, 0.5694190213972216, 0.5850078576187193, 1.1315794560109824, 1.9550233898131868]}, ['i', 'h', 'e', 'd', 'f', 'a', 'c', 'g', 'l', 'b'])
if not AreEqual(r, result): problem()


b_result = extr.OutOfBound(0, 0.2)
r=repack({'col3': [0.03661260129691063, 0.7296368401312903], 'custom': [588.0, -226.0], 'TWD on data': [1.075786928286798, 2.024296762680489], 'TWD': [1.1315794560109824, 1.9550233898131868]},['l', 'b'])
if not AreEqual(r,b_result): problem()
# ~ unpack(b_result,'b_result')

bb_result = extr.OutOfBound(0, 0.2, key = 'custom')
r=repack({'col3': [0.03661260129691063], 'custom': [588.0], 'TWD on data': [1.075786928286798], 'TWD': [1.1315794560109824]},['l'])
if not AreEqual(r,bb_result): problem()
# ~ unpack(bb_result,'bb_result')


r=xt.OutOfBound(extr.results, bound = [0, 0.2], key = 'custom')
if not AreEqual(r,bb_result): problem()

### extremals.ExtremalsCol

ecol = xt.ExtremalsCol(data)
result = ecol.Run()
r=repack({'col1': [nan, 8.0, 9.0, 9.0, -3.0, 22.0, 3.0, 1.0, 0.0, 100.0], 'col2': [7.0, 3.0, 12.0, -34.5, nan, 95.0, 100.0, -123.0, -567.0, 200.0], 'col3': [21.0, nan, nan, 3.0, 44.0, -4.0, 0.0, -13.4, 21.0, 74.0], 'TWD': [0.10282733873740618, 0.1539047877881331, 0.15737939281824168, 0.28241265262150894, 0.5524992456406856, 0.5579414249442527, 0.6029143038582064, 0.7272181018081674, 1.075786928286798, 2.024296762680489]},['e', 'h', 'i', 'f', 'd', 'g', 'a', 'c', 'l', 'b'])
if not AreEqual(r,result): problem()

r=result.drop('TWD', axis = 1).sort_index()
if not AreEqual(r, data): problem()

ecol.NormalizeTests(True)
# ~ ecol = xt.ExtremalsCol(data, normalized = True)
nor_result = ecol.Run()
r=repack({'col1': [nan, -0.094123870989629, -0.08312237957525678, -0.08312237957525678, -0.21514027654772339, 0.05989700881158206, -0.1491313280614901, -0.17113431089023454, -0.18213580230460674, 0.9180133391326151], 'col2': [0.06621473744049555, 0.059780916798504086, 0.07425701324298489, -0.0005361517201659598, nan, 0.2077587915643079, 0.21580106736679724, -0.14288443342422727, -0.8570385246852806, 0.376646583416584], 'col3': [0.03661260129691063, nan, nan, -0.19875412132608622, 0.3373589690929622, -0.29028562456836277, -0.23798190842991904, -0.4131993574937056, 0.03661260129691063, 0.7296368401312903], 'TWD': [0.10282733873740618, 0.15390478778813305, 0.15737939281824165, 0.28241265262150894, 0.5524992456406855, 0.5579414249442527, 0.6029143038582063, 0.7272181018081674, 1.0757869282867978, 2.024296762680489]},['e', 'h', 'i', 'f', 'd', 'g', 'a', 'c', 'l', 'b'])
if not AreEqual(r,nor_result): problem()
# ~ unpack(nor_result,'nor_result')

r=nor_result.drop('TWD', axis = 1).sort_index()
if not (AreEqual(r,xt.Normalize(data)) and AreEqual(nor_result['TWD'],result['TWD'])): problem()
if not AreEqual(abs(nor_result.drop('TWD', axis = 1)).sum(axis = 1), result['TWD']): problem()

if not AreEqual(xt.ExtremalsCol(xt.Normalize(data), keys = ['col1', 'col3']).Run(), xt.ExtremalsCol(data, keys = ['col1', 'col3'], normalized = True).Run()): problem()

### extremals.ExtremalsDiff

ediff = xt.ExtremalsDiff(data)
result = ediff.Run()
r=repack({'(col2 - col1)': [nan, -5.0, 3.0, -43.5, -124.0, 97.0, nan, 73.0, 100.0, -567.0], '(col3 - col1)': [nan, nan, nan, -6.0, -14.4, -3.0, 47.0, -26.0, -26.0, 21.0], '(col3 - col2)': [14.0, nan, nan, 37.5, 109.6, -100.0, nan, -99.0, -126.0, 588.0], 'TWD': [0.07665473619930256, 0.09192815095314023, 0.1057227621160968, 0.1393789834345731, 0.3986710515093698, 0.5618603634031968, 0.7374634208122243, 0.8717787873521854, 0.9627629080359592, 2.083459255462169]},['e', 'h', 'i', 'f', 'c', 'a', 'd', 'g', 'b', 'l'])
if not AreEqual(r,result): problem()
# ~ unpack(result,'result')

### extremals.Normalize

nor_data = xt.Normalize(data)
r=repack({'col1': [-0.1491313280614901, 0.9180133391326151, -0.17113431089023454, -0.21514027654772339, nan, -0.08312237957525678, 0.05989700881158206, -0.094123870989629, -0.08312237957525678, -0.18213580230460674], 'col2': [0.21580106736679724, 0.376646583416584, -0.14288443342422727, nan, 0.06621473744049555, -0.0005361517201659598, 0.2077587915643079, 0.059780916798504086, 0.07425701324298489, -0.8570385246852806], 'col3': [-0.23798190842991898, 0.72963684013129, -0.41319935749370557, 0.3373589690929621, 0.03661260129691062, -0.1987541213260862, -0.2902856245683627, nan, nan, 0.03661260129691062]},['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'l'])
if not AreEqual(r,nor_data): problem()

nor_col3 = xt.Normalize(data['col3'], dropna = True)
r=repack({'col3': [-0.23798190842991898, 0.72963684013129, -0.41319935749370557, 0.3373589690929621, 0.03661260129691062, -0.1987541213260862, -0.2902856245683627, 0.03661260129691062]},['a', 'b', 'c', 'd', 'e', 'f', 'g', 'l'])
if not AreEqual(r,nor_col3): problem()

### OutOfBound

s = data['col1']
if not type(s) == pd.Series:
    s = s.loc[:, ~s.columns.duplicated()]['col1']

t1 = xt.OutOfBound(s,2,3)
r=repack({'col1': [-3.0, 0.0, 9.0, 22.0, 100.0]},['d', 'l', 'i', 'g', 'b'])
if not AreEqual(r,t1): problem()

t2 = xt.OutOfBound(s, bound = [0,0.3])
r=repack({'col1': [22.0, 100.0]},['g', 'b'])
if not AreEqual(r,t2): problem()
if not AreEqual(xt.OutOfBound(s, -1), s.sort_values().dropna()): problem()

new_data = pd.DataFrame(
            {'col1' : [1, 2, 3, 4],
             'col2' : [None, 4 , None, 2]},
             index = ['a', 'b', 'c', 'd']
            )

d1 = xt.OutOfBound(new_data,0,0.5, key = 'col1')
r=repack({'col1': [3, 4], 'col2': [nan, 2.0]},['c', 'd'])
if not AreEqual(r,d1): problem()


d2 = xt.OutOfBound(new_data,0,0.5, key = 'col2')
r=repack({'col1': [2], 'col2': [4.0]},['b'])
if not AreEqual(r,d2): problem()

### TWDExtremals

keys = ['col1', 'col3']
twd_series = xt.TWDExtremals(data, keys = keys)


if not AreEqual(xt.TWDExtremals(data['col1']), xt.TWDExtremals(data[['col1']])): problem()
if not AreEqual(twd_series, xt.TWDTest(keys).Apply(data)): problem()
if not AreEqual(twd_series, xt.TWDTest().Apply(data[keys])): problem()
if not AreEqual(twd_series, xt.TWDExtremals(data[keys])): problem()
if not AreEqual(pd.concat([data[keys], twd_series], axis = 1), xt.ExtremalsCol(data[keys]).Run().sort_index()): problem()
if not AreEqual( xt.OutOfBound(twd_series, 0.2,0.5),  xt.TWDExtremals(data[keys], bound = [0.2,0.5])): problem()

### Purge
# ~ pd.options.display.float_format = "{:.2f}".format

# ~ keys =['Bathroom', 'Rooms']
# ~ purged, good = xt.PurgeTWD(melb_data, keys=keys, high = 0.1, steps = 10, verbose = True)
# ~ print(melb_data.mean())

purged, good = xt.PurgeTWD(data, high = 0.3, steps = 1)
if not AreEqual(pd.concat([purged, good], axis = 0).sort_index(),data): problem()

purged2, good2 = xt.PurgeTWD(data, high = 0.3, steps = 4)
if not AreEqual(pd.concat([purged2, good2], axis = 0).sort_index(),data): problem()

purged3, good3 = xt.PurgeTWD(data, high = 0.3, steps = 3, keys = ['col1'])
if not AreEqual(pd.concat([purged3, good3], axis = 0).sort_index(),data): problem()

r=repack({'col1': [100.0, 0.0, 1.0], 'col2': [200.0, -567.0, -123.0], 'col3': [74.0, 21.0, -13.4]},['b', 'l', 'c'])
if not AreEqual(r,purged): problem()
r=repack({'col1': [100.0, 0.0, 22.0], 'col2': [200.0, -567.0, 95.0], 'col3': [74.0, 21.0, -4.0]},['b', 'l', 'g'])
if not AreEqual(r,purged2): problem()
r=repack({'col1': [100.0, 22.0, -3.0], 'col2': [200.0, 95.0, nan], 'col3': [74.0, -4.0, 44.0]},['b', 'g', 'd'])
if not AreEqual(r,purged3): problem()

### AddTest
a = xt.AddTests(xt.AddTests(data, tests = xt.GetDiffTests(data)), tests = xt.GetColTests(data), normalized = True)
redata = xt.AddTWDTest(a)
r=repack({'col1': [nan, -0.094123870989629, -0.08312237957525678, -0.08312237957525678, -0.17113431089023454, -0.1491313280614901, -0.21514027654772339, 0.05989700881158206, 0.9180133391326151, -0.18213580230460674], 'col2': [0.06621473744049555, 0.059780916798504086, 0.07425701324298489, -0.0005361517201659598, -0.14288443342422727, 0.21580106736679724, nan, 0.2077587915643079, 0.376646583416584, -0.8570385246852806], 'col3': [0.03661260129691062, nan, nan, -0.1987541213260862, -0.41319935749370557, -0.23798190842991898, 0.3373589690929621, -0.2902856245683627, 0.72963684013129, 0.03661260129691062], '(col2 - col1)': [nan, 0.09192815095314023, 0.1057227621160968, 0.025541584731411764, -0.11326669009583867, 0.26780944328083645, nan, 0.22642560979196674, 0.27298242246694515, -0.8771432832445585], '(col3 - col1)': [nan, nan, nan, -0.07585087503003256, -0.20475351814465437, -0.02981421677481049, 0.737463420812224, -0.3827619300648464, -0.3827619300648464, 0.3384790492669661], '(col3 - col2)': [-0.07665473619930256, nan, nan, -0.037986523673128776, 0.08065084326887673, -0.26423670334754984, nan, -0.2625912474953722, -0.3070185555041676, 0.8678369229506442], 'TWD': [0.17948207493670876, 0.24583293874127332, 0.2631021549343385, 0.42179163605608205, 1.1258891533175373, 1.1647746672614032, 1.2899626664529098, 1.429720212296438, 2.9870596707164485, 3.1592461837489663]},['e', 'h', 'i', 'f', 'c', 'a', 'd', 'g', 'b', 'l'])
if not AreEqual(r,redata): problem()

if not AreEqual(xt.AddTWDTest(xt.Normalize(data)), xt.AddTWDTest(data, normalized = True)): problem()

