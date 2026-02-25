import ansatz
import linear_algebra
import sympy as sp
import spl
from itertools import product
from fractions import Fraction
from copy import deepcopy
from left import one_two_A_left
from left import one_two_C_left

def index_based_element_switch (index_based, old_elements, new_elements):
    
    mapping = dict(zip(old_elements, new_elements))
    
    result = []
    for element in index_based:
        new_element = [element[0]]
        for indexes in element[1:]:
            new_indexes=[]
            for index in indexes:
                if index in mapping:
                    new_indexes.append(mapping[index])
                else:
                    new_indexes.append(index)
            new_element.append(new_indexes)
        result.append(new_element)
    
    return result

def index_based_reorganize(index_based):

    all_index = []
    for element in index_based:
        for indexes in element[1:]:
            all_index+=indexes

    all_index = sorted(set(all_index))

    old_index=[]
    new_index=[]
    for new, old in enumerate(all_index, start=1):
        old_index.append(old)
        new_index.append(new)

    return index_based_element_switch (index_based, old_index, new_index)

def position_based_of_(index_based):
    index_based_no_class_number=[indices for structure_element in index_based for indices in structure_element[1:]]
    position_based=[ [] for _ in range(len(set(index for element in index_based_no_class_number for index in element)))]
    for position in range(len(index_based_no_class_number)):
        for index in index_based_no_class_number[position]:
            position_based[index-1].append(position)   
    return sorted(position_based)

result_operation_A=[]
result_operation_B=[]
result_operation_C=[]

for one_two_A_map_ansatz_term_first in ansatz.map_ansatz ('one_two_A',[[0,0],[1,1],[0,2]],2):
    
    one_two_A_map_ansatz_term_first['coefficient']*=-2*((-1)**len(one_two_A_map_ansatz_term_first['index_based'][0][1]))

    one_two_A_map_ansatz_term_first['index_based'][0][0]=1
    
    if one_two_A_map_ansatz_term_first['eta']==0:

        one_two_A_map_ansatz_term_first['index_based'][0].append([1,2])

    elif one_two_A_map_ansatz_term_first['eta']==1:

        one_two_A_map_ansatz_term_first['index_based'][0].append([3,3])

    result_operation_A.append(deepcopy(one_two_A_map_ansatz_term_first))

for one_two_A_map_ansatz_term_second in ansatz.map_ansatz ('one_two_A',[[0,0],[1,1],[0,2]],2):
    
    one_two_A_map_ansatz_term_second['coefficient']*=((-1)**len(one_two_A_map_ansatz_term_second['index_based'][0][1]))

    one_two_A_map_ansatz_term_second['index_based'][0][0]=1
    
    if one_two_A_map_ansatz_term_second['eta']==0:
        
        one_two_A_map_ansatz_term_second['index_based']=index_based_element_switch (one_two_A_map_ansatz_term_second['index_based'],[1],[2])
        one_two_A_map_ansatz_term_second['index_based'][0].append([1,1])

    elif one_two_A_map_ansatz_term_second['eta']==1:

        one_two_A_map_ansatz_term_second['index_based'][0].append([3,3])
        one_two_A_map_ansatz_term_second['coefficient']*=4

    result_operation_A.append(deepcopy(one_two_A_map_ansatz_term_second))

for one_two_B_map_ansatz_term_first in ansatz.map_ansatz ('one_two_B',[[0,0],[1,1],[0,2],[0,3]],4):
    
    one_two_B_map_ansatz_term_first['coefficient']*=-2*((-1)**len(one_two_B_map_ansatz_term_first['index_based'][0][1]))

    one_two_B_map_ansatz_term_first['index_based'][0][0]=1
    
    if one_two_B_map_ansatz_term_first['eta']==0:

        one_two_B_map_ansatz_term_first['index_based'][0].append([1,2])

    elif one_two_B_map_ansatz_term_first['eta']==1:

        one_two_B_map_ansatz_term_first['index_based'][0].append([4,4])

    result_operation_B.append(deepcopy(one_two_B_map_ansatz_term_first))

for one_two_B_map_ansatz_term_second in ansatz.map_ansatz ('one_two_B',[[0,0],[1,1],[0,2],[0,3]],4):
    
    one_two_B_map_ansatz_term_second['coefficient']*=((-1)**len(one_two_B_map_ansatz_term_second['index_based'][0][1]))

    one_two_B_map_ansatz_term_second['index_based'][0][0]=1
    
    if one_two_B_map_ansatz_term_second['eta']==0:
        
        one_two_B_map_ansatz_term_second['index_based']=index_based_element_switch (one_two_B_map_ansatz_term_second['index_based'],[1],[2])
        one_two_B_map_ansatz_term_second['index_based'][0].append([1,1])

    elif one_two_B_map_ansatz_term_second['eta']==1:

        one_two_B_map_ansatz_term_second['index_based'][0].append([4,4])
        one_two_B_map_ansatz_term_second['coefficient']*=4

    result_operation_B.append(deepcopy(one_two_B_map_ansatz_term_second))

for one_two_C_map_ansatz_term_first in ansatz.map_ansatz ('one_two_C',[[0,0],[0,1],[0,1],[1,2]],4):
    
    one_two_C_map_ansatz_term_first['coefficient']*=-2*((-1)**len(one_two_C_map_ansatz_term_first['index_based'][0][1]))

    one_two_C_map_ansatz_term_first['index_based'][0][0]=1
    one_two_C_map_ansatz_term_first['index_based'][1][0]=2
    one_two_C_map_ansatz_term_first['index_based'][2][0]=2
    one_two_C_map_ansatz_term_first['index_based'][3][0]=3
    
    if one_two_C_map_ansatz_term_first['eta']==0:

        one_two_C_map_ansatz_term_first['index_based'][0].append([1,2])

    elif one_two_C_map_ansatz_term_first['eta']==1:

        one_two_C_map_ansatz_term_first['index_based'][0].append([4,4])

    result_operation_C.append(deepcopy(one_two_C_map_ansatz_term_first))

for one_two_C_map_ansatz_term_second in ansatz.map_ansatz ('one_two_C',[[0,0],[0,1],[0,1],[1,2]],4):
    
    one_two_C_map_ansatz_term_second['coefficient']*=((-1)**len(one_two_C_map_ansatz_term_second['index_based'][0][1]))

    one_two_C_map_ansatz_term_second['index_based'][0][0]=1
    one_two_C_map_ansatz_term_second['index_based'][1][0]=2
    one_two_C_map_ansatz_term_second['index_based'][2][0]=2
    one_two_C_map_ansatz_term_second['index_based'][3][0]=3
    
    if one_two_C_map_ansatz_term_second['eta']==0:
        
        one_two_C_map_ansatz_term_second['index_based']=index_based_element_switch (one_two_C_map_ansatz_term_second['index_based'],[1],[2])
        one_two_C_map_ansatz_term_second['index_based'][0].append([1,1])

    elif one_two_C_map_ansatz_term_second['eta']==1:

        one_two_C_map_ansatz_term_second['index_based'][0].append([4,4])
        one_two_C_map_ansatz_term_second['coefficient']*=4

    result_operation_C.append(deepcopy(one_two_C_map_ansatz_term_second))

map_ansatz_one_one=[]
for term in ansatz.map_ansatz('one_one',[[0,0],[0,1]],2):
    if len(term['index_based'][0][1])==0:
        map_ansatz_one_one.append(term)

for zero_one_map_ansatz_term_first in ansatz.map_ansatz('zero_one',[[0,0],[1,1],[1,1]],2):
    for one_one_map_ansatz_term_first in map_ansatz_one_one:
        zero_one=deepcopy(zero_one_map_ansatz_term_first)
        one_one=deepcopy(one_one_map_ansatz_term_first)
        zero_one_id=zero_one['id']
        one_one_id=one_one['id']
        map_product={'id':f"{zero_one_id}*{one_one_id}",'coefficient':-2,'index_based':[],'position_based':[]}
        zero_one['coefficient']*=(-1)**len(zero_one['index_based'][0][1])
        map_product['coefficient']*=zero_one['coefficient']*one_one['coefficient']
        zero_one['index_based'][0][0]=2
        zero_one['index_based'][1][0]=1
        zero_one['index_based'][2][0]=1
        one_one['index_based'][1][0]=3
        if zero_one['eta']==0:
            if one_one['eta']==0:
                map_product['coefficient']*=Fraction(1,2)
                for symmetrization in [[1,2],[2,1]]:
                    zero_one_index_based=deepcopy(zero_one['index_based'])
                    one_one_index_based=deepcopy(one_one['index_based'])
                    zero_one_index_based=index_based_element_switch(zero_one_index_based,[1,2],symmetrization)
                    map_product['index_based']=list(reversed(zero_one_index_based))+one_one_index_based[1:]
                    result_operation_B.append(deepcopy(map_product))
                continue
            elif one_one['eta']==1:
                zero_one['index_based']=index_based_element_switch(zero_one['index_based'],[1,2,3,4],[1,1,2,3])
                one_one['index_based']=index_based_element_switch(one_one['index_based'],[1],[4])
        elif zero_one['eta']==1:
            if one_one['eta']==0:
                one_one['index_based']=index_based_element_switch(one_one['index_based'],[1,2],[4,4])
            elif one_one['eta']==1:
                map_product['coefficient']*=4
                one_one['index_based']=index_based_element_switch(one_one['index_based'],[1],[4])                
        map_product['index_based']=list(reversed(zero_one['index_based']))+one_one['index_based'][1:]
        result_operation_B.append(deepcopy(map_product))

for zero_one_map_ansatz_term_second in ansatz.map_ansatz('zero_one',[[0,0],[1,1],[1,1]],2):
    for one_one_map_ansatz_term_second in map_ansatz_one_one:
        zero_one=deepcopy(zero_one_map_ansatz_term_second)
        one_one=deepcopy(one_one_map_ansatz_term_second)
        zero_one_id=zero_one['id']
        one_one_id=one_one['id']
        map_product={'id':f"{zero_one_id}*{one_one_id}",'coefficient':1,'index_based':[],'position_based':[]}
        zero_one['coefficient']*=(-1)**len(zero_one['index_based'][0][1])
        map_product['coefficient']*=zero_one['coefficient']*one_one['coefficient']
        zero_one['index_based'][0][0]=2
        zero_one['index_based'][1][0]=1
        zero_one['index_based'][2][0]=1
        one_one['index_based'][1][0]=3
        if zero_one['eta']==0:
            if one_one['eta']==0:
                zero_one['index_based']=index_based_element_switch(zero_one['index_based'],[1,2,3,4],[1,1,2,3])
                one_one['index_based']=index_based_element_switch(one_one['index_based'],[1,2],[4,4])
            elif one_one['eta']==1:
                map_product['coefficient']*=4
                zero_one['index_based']=index_based_element_switch(zero_one['index_based'],[1,2,3,4],[1,1,2,3])
                one_one['index_based']=index_based_element_switch(one_one['index_based'],[1],[4])
        elif zero_one['eta']==1:
            if one_one['eta']==0:
                map_product['coefficient']*=4
                one_one['index_based']=index_based_element_switch(one_one['index_based'],[1,2],[4,4])
            elif one_one['eta']==1:
                map_product['coefficient']*=16
                one_one['index_based']=index_based_element_switch(one_one['index_based'],[1],[4])                
        map_product['index_based']=list(reversed(zero_one['index_based']))+one_one['index_based'][1:]
        result_operation_B.append(deepcopy(map_product))         

for zero_two_A_map_ansatz_term_first in ansatz.map_ansatz('zero_two_A',[[0,0],[1,1],[1,1],[1,1]],2):

    zero_two_A_map_ansatz_term_first['coefficient']*=-1*Fraction(1,2)
    
    if zero_two_A_map_ansatz_term_first['eta']==0:
        for Leibniz_case in product([0,2,3],repeat=len(zero_two_A_map_ansatz_term_first['index_based'][1][1])):
            zero_two_A_map_ansatz_term_first_Leibniz_case=deepcopy(zero_two_A_map_ansatz_term_first)
            for destination in Leibniz_case:
                zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'][destination][1].append(zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][1].pop(0))
            zero_two_A_map_ansatz_term_first_Leibniz_case['coefficient']*=(-1)**(Leibniz_case.count(2)+Leibniz_case.count(3))
            zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2]+=[1,2]
            if zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][0]==zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][2]:
                zero_two_A_map_ansatz_term_first_Leibniz_case['coefficient']*=4
            else:
                zero_two_A_map_ansatz_term_first_Leibniz_case['index_based']=index_based_element_switch(zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'],[zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][0]],[zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][2]])
            if zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][1]==zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][3]:
                zero_two_A_map_ansatz_term_first_Leibniz_case['coefficient']*=4
            else:
                zero_two_A_map_ansatz_term_first_Leibniz_case['index_based']=index_based_element_switch(zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'],[zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][1]],[zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][3]])
            zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'].pop(1)
            zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'][0][0]=2
            zero_two_A_map_ansatz_term_first_Leibniz_case['index_based']=list(reversed(index_based_reorganize(zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'])))
            result_operation_A.append(deepcopy(zero_two_A_map_ansatz_term_first_Leibniz_case))
        zero_two_A_map_ansatz_term_first['index_based']=index_based_element_switch(zero_two_A_map_ansatz_term_first['index_based'],[1,2],[2,1])
        for Leibniz_case in product([0,2,3],repeat=len(zero_two_A_map_ansatz_term_first['index_based'][1][1])):
            zero_two_A_map_ansatz_term_first_Leibniz_case=deepcopy(zero_two_A_map_ansatz_term_first)
            for destination in Leibniz_case:
                zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'][destination][1].append(zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][1].pop(0))
            zero_two_A_map_ansatz_term_first_Leibniz_case['coefficient']*=(-1)**(Leibniz_case.count(2)+Leibniz_case.count(3))
            zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2]+=[1,2]
            if zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][0]==zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][2]:
                zero_two_A_map_ansatz_term_first_Leibniz_case['coefficient']*=4
            else:
                zero_two_A_map_ansatz_term_first_Leibniz_case['index_based']=index_based_element_switch(zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'],[zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][0]],[zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][2]])
            if zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][1]==zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][3]:
                zero_two_A_map_ansatz_term_first_Leibniz_case['coefficient']*=4
            else:
                zero_two_A_map_ansatz_term_first_Leibniz_case['index_based']=index_based_element_switch(zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'],[zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][1]],[zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][3]])
            zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'].pop(1)
            zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'][0][0]=2
            zero_two_A_map_ansatz_term_first_Leibniz_case['index_based']=list(reversed(index_based_reorganize(zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'])))
            result_operation_A.append(deepcopy(zero_two_A_map_ansatz_term_first_Leibniz_case))
    elif zero_two_A_map_ansatz_term_first['eta']==1:
        for Leibniz_case in product([0,2,3],repeat=len(zero_two_A_map_ansatz_term_first['index_based'][1][1])):
            zero_two_A_map_ansatz_term_first_Leibniz_case=deepcopy(zero_two_A_map_ansatz_term_first)
            zero_two_A_map_ansatz_term_first_Leibniz_case['coefficient']*=2
            for destination in Leibniz_case:
                zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'][destination][1].append(zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][1].pop(0))
            zero_two_A_map_ansatz_term_first_Leibniz_case['coefficient']*=(-1)**(Leibniz_case.count(2)+Leibniz_case.count(3))
            if zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][1]==zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][0]:
                zero_two_A_map_ansatz_term_first_Leibniz_case['coefficient']*=4
            else:
                zero_two_A_map_ansatz_term_first_Leibniz_case['index_based']=index_based_element_switch(zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'],[zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][1]],[zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][0]])
            zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'].pop(1)
            zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'][0][0]=2
            zero_two_A_map_ansatz_term_first_Leibniz_case['index_based']=list(reversed(index_based_reorganize(zero_two_A_map_ansatz_term_first_Leibniz_case['index_based'])))
            result_operation_A.append(deepcopy(zero_two_A_map_ansatz_term_first_Leibniz_case))

for zero_two_A_map_ansatz_term_second in ansatz.map_ansatz('zero_two_A',[[0,0],[1,1],[1,1],[1,1]],2):

    zero_two_A_map_ansatz_term_second['coefficient']*=-1*Fraction(1,2)
    
    if zero_two_A_map_ansatz_term_second['eta']==0:
        for Leibniz_case in product([0,1,3],repeat=len(zero_two_A_map_ansatz_term_second['index_based'][2][1])):
            zero_two_A_map_ansatz_term_second_Leibniz_case=deepcopy(zero_two_A_map_ansatz_term_second)
            for destination in Leibniz_case:
                zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'][destination][1].append(zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'][2][1].pop(0))
            zero_two_A_map_ansatz_term_second_Leibniz_case['coefficient']*=(-1)**(Leibniz_case.count(1)+Leibniz_case.count(3))
            zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'][2][2]+=[1,2]
            if zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'][2][2][0]==zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'][2][2][2]:
                zero_two_A_map_ansatz_term_second_Leibniz_case['coefficient']*=4
            else:
                zero_two_A_map_ansatz_term_second_Leibniz_case['index_based']=index_based_element_switch(zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'],[zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'][2][2][0]],[zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'][2][2][2]])
            if zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'][2][2][1]==zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'][2][2][3]:
                zero_two_A_map_ansatz_term_second_Leibniz_case['coefficient']*=4
            else:
                zero_two_A_map_ansatz_term_second_Leibniz_case['index_based']=index_based_element_switch(zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'],[zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'][2][2][1]],[zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'][2][2][3]])
            zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'].pop(2)
            zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'][0][0]=2
            zero_two_A_map_ansatz_term_second_Leibniz_case['index_based']=list(reversed(index_based_reorganize(zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'])))
            result_operation_A.append(deepcopy(zero_two_A_map_ansatz_term_second_Leibniz_case))
        zero_two_A_map_ansatz_term_second['index_based']=index_based_element_switch(zero_two_A_map_ansatz_term_second['index_based'],[1,2],[2,1])
        for Leibniz_case in product([0,1,3],repeat=len(zero_two_A_map_ansatz_term_second['index_based'][2][1])):
            zero_two_A_map_ansatz_term_second_Leibniz_case=deepcopy(zero_two_A_map_ansatz_term_second)
            for destination in Leibniz_case:
                zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'][destination][1].append(zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'][2][1].pop(0))
            zero_two_A_map_ansatz_term_second_Leibniz_case['coefficient']*=(-1)**(Leibniz_case.count(1)+Leibniz_case.count(3))
            zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'][2][2]+=[1,2]
            if zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'][2][2][0]==zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'][2][2][2]:
                zero_two_A_map_ansatz_term_second_Leibniz_case['coefficient']*=4
            else:
                zero_two_A_map_ansatz_term_second_Leibniz_case['index_based']=index_based_element_switch(zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'],[zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'][2][2][0]],[zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'][2][2][2]])
            if zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'][2][2][1]==zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'][2][2][3]:
                zero_two_A_map_ansatz_term_second_Leibniz_case['coefficient']*=4
            else:
                zero_two_A_map_ansatz_term_second_Leibniz_case['index_based']=index_based_element_switch(zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'],[zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'][2][2][1]],[zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'][2][2][3]])
            zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'].pop(2)
            zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'][0][0]=2
            zero_two_A_map_ansatz_term_second_Leibniz_case['index_based']=list(reversed(index_based_reorganize(zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'])))
            result_operation_A.append(deepcopy(zero_two_A_map_ansatz_term_second_Leibniz_case))
    elif zero_two_A_map_ansatz_term_second['eta']==1:
        for Leibniz_case in product([0,1,3],repeat=len(zero_two_A_map_ansatz_term_second['index_based'][2][1])):
            zero_two_A_map_ansatz_term_second_Leibniz_case=deepcopy(zero_two_A_map_ansatz_term_second)
            zero_two_A_map_ansatz_term_second_Leibniz_case['coefficient']*=2
            for destination in Leibniz_case:
                zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'][destination][1].append(zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'][2][1].pop(0))
            zero_two_A_map_ansatz_term_second_Leibniz_case['coefficient']*=(-1)**(Leibniz_case.count(1)+Leibniz_case.count(3))
            if zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'][2][2][1]==zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'][2][2][0]:
                zero_two_A_map_ansatz_term_second_Leibniz_case['coefficient']*=4
            else:
                zero_two_A_map_ansatz_term_second_Leibniz_case['index_based']=index_based_element_switch(zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'],[zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'][2][2][1]],[zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'][2][2][0]])
            zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'].pop(2)
            zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'][0][0]=2
            zero_two_A_map_ansatz_term_second_Leibniz_case['index_based']=list(reversed(index_based_reorganize(zero_two_A_map_ansatz_term_second_Leibniz_case['index_based'])))
            result_operation_A.append(deepcopy(zero_two_A_map_ansatz_term_second_Leibniz_case))

for zero_two_A_map_ansatz_term_third in ansatz.map_ansatz('zero_two_A',[[0,0],[1,1],[1,1],[1,1]],2):

    zero_two_A_map_ansatz_term_third['coefficient']*=-1*Fraction(1,2)
    
    if zero_two_A_map_ansatz_term_third['eta']==0:
        for Leibniz_case in product([0,1,2],repeat=len(zero_two_A_map_ansatz_term_third['index_based'][3][1])):
            zero_two_A_map_ansatz_term_third_Leibniz_case=deepcopy(zero_two_A_map_ansatz_term_third)
            for destination in Leibniz_case:
                zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'][destination][1].append(zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'][3][1].pop(0))
            zero_two_A_map_ansatz_term_third_Leibniz_case['coefficient']*=(-1)**(Leibniz_case.count(1)+Leibniz_case.count(2))
            zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'][3][2]+=[1,2]
            if zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'][3][2][0]==zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'][3][2][2]:
                zero_two_A_map_ansatz_term_third_Leibniz_case['coefficient']*=4
            else:
                zero_two_A_map_ansatz_term_third_Leibniz_case['index_based']=index_based_element_switch(zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'],[zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'][3][2][0]],[zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'][3][2][2]])
            if zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'][3][2][1]==zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'][3][2][3]:
                zero_two_A_map_ansatz_term_third_Leibniz_case['coefficient']*=4
            else:
                zero_two_A_map_ansatz_term_third_Leibniz_case['index_based']=index_based_element_switch(zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'],[zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'][3][2][1]],[zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'][3][2][3]])
            zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'].pop(3)
            zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'][0][0]=2
            zero_two_A_map_ansatz_term_third_Leibniz_case['index_based']=list(reversed(index_based_reorganize(zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'])))
            result_operation_A.append(deepcopy(zero_two_A_map_ansatz_term_third_Leibniz_case))
        zero_two_A_map_ansatz_term_third['index_based']=index_based_element_switch(zero_two_A_map_ansatz_term_third['index_based'],[1,2],[2,1])
        for Leibniz_case in product([0,1,2],repeat=len(zero_two_A_map_ansatz_term_third['index_based'][3][1])):
            zero_two_A_map_ansatz_term_third_Leibniz_case=deepcopy(zero_two_A_map_ansatz_term_third)
            for destination in Leibniz_case:
                zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'][destination][1].append(zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'][3][1].pop(0))
            zero_two_A_map_ansatz_term_third_Leibniz_case['coefficient']*=(-1)**(Leibniz_case.count(1)+Leibniz_case.count(2))
            zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'][3][2]+=[1,2]
            if zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'][3][2][0]==zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'][3][2][2]:
                zero_two_A_map_ansatz_term_third_Leibniz_case['coefficient']*=4
            else:
                zero_two_A_map_ansatz_term_third_Leibniz_case['index_based']=index_based_element_switch(zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'],[zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'][3][2][0]],[zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'][3][2][2]])
            if zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'][3][2][1]==zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'][3][2][3]:
                zero_two_A_map_ansatz_term_third_Leibniz_case['coefficient']*=4
            else:
                zero_two_A_map_ansatz_term_third_Leibniz_case['index_based']=index_based_element_switch(zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'],[zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'][3][2][1]],[zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'][3][2][3]])
            zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'].pop(3)
            zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'][0][0]=2
            zero_two_A_map_ansatz_term_third_Leibniz_case['index_based']=list(reversed(index_based_reorganize(zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'])))
            result_operation_A.append(deepcopy(zero_two_A_map_ansatz_term_third_Leibniz_case))
    elif zero_two_A_map_ansatz_term_third['eta']==1:
        for Leibniz_case in product([0,1,2],repeat=len(zero_two_A_map_ansatz_term_third['index_based'][3][1])):
            zero_two_A_map_ansatz_term_third_Leibniz_case=deepcopy(zero_two_A_map_ansatz_term_third)
            zero_two_A_map_ansatz_term_third_Leibniz_case['coefficient']*=2
            for destination in Leibniz_case:
                zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'][destination][1].append(zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'][3][1].pop(0))
            zero_two_A_map_ansatz_term_third_Leibniz_case['coefficient']*=(-1)**(Leibniz_case.count(1)+Leibniz_case.count(2))
            if zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'][3][2][1]==zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'][3][2][0]:
                zero_two_A_map_ansatz_term_third_Leibniz_case['coefficient']*=4
            else:
                zero_two_A_map_ansatz_term_third_Leibniz_case['index_based']=index_based_element_switch(zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'],[zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'][3][2][1]],[zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'][3][2][0]])
            zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'].pop(3)
            zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'][0][0]=2
            zero_two_A_map_ansatz_term_third_Leibniz_case['index_based']=list(reversed(index_based_reorganize(zero_two_A_map_ansatz_term_third_Leibniz_case['index_based'])))
            result_operation_A.append(deepcopy(zero_two_A_map_ansatz_term_third_Leibniz_case))

for zero_two_B_map_ansatz_term_first in ansatz.map_ansatz('zero_two_B',[[0,0],[1,1],[0,2],[1,3],[1,3]],4):

    zero_two_B_map_ansatz_term_first['coefficient']*=-1*Fraction(1,2)
    
    if zero_two_B_map_ansatz_term_first['eta']==0:
        for Leibniz_case in product([0,2],repeat=len(zero_two_B_map_ansatz_term_first['index_based'][1][1])):
            zero_two_B_map_ansatz_term_first_Leibniz_case=deepcopy(zero_two_B_map_ansatz_term_first)
            for destination in Leibniz_case:
                zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][destination][1].append(zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][1].pop(0))
            zero_two_B_map_ansatz_term_first_Leibniz_case['coefficient']*=(-1)**(Leibniz_case.count(2))
            zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2]+=[1,2]
            if zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][0]==zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][2]:
                zero_two_B_map_ansatz_term_first_Leibniz_case['coefficient']*=4
            else:
                zero_two_B_map_ansatz_term_first_Leibniz_case['index_based']=index_based_element_switch(zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'],[zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][0]],[zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][2]])
            if zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][1]==zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][3]:
                zero_two_B_map_ansatz_term_first_Leibniz_case['coefficient']*=4
            else:
                zero_two_B_map_ansatz_term_first_Leibniz_case['index_based']=index_based_element_switch(zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'],[zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][1]],[zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][3]])
            zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'].pop(1)
            zero_two_B_map_ansatz_term_first_Leibniz_case['coefficient']*=(-1)**(len(zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][1]))
            zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][0][0]=3
            zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][2][0]=1
            zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][3][0]=1
            zero_two_B_map_ansatz_term_first_Leibniz_case['index_based']=list(reversed(index_based_reorganize(zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'])))
            result_operation_B.append(deepcopy(zero_two_B_map_ansatz_term_first_Leibniz_case))
        zero_two_B_map_ansatz_term_first['index_based']=index_based_element_switch(zero_two_B_map_ansatz_term_first['index_based'],[1,2],[2,1])
        for Leibniz_case in product([0,2],repeat=len(zero_two_B_map_ansatz_term_first['index_based'][1][1])):
            zero_two_B_map_ansatz_term_first_Leibniz_case=deepcopy(zero_two_B_map_ansatz_term_first)
            for destination in Leibniz_case:
                zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][destination][1].append(zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][1].pop(0))
            zero_two_B_map_ansatz_term_first_Leibniz_case['coefficient']*=(-1)**(Leibniz_case.count(2))
            zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2]+=[1,2]
            if zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][0]==zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][2]:
                zero_two_B_map_ansatz_term_first_Leibniz_case['coefficient']*=4
            else:
                zero_two_B_map_ansatz_term_first_Leibniz_case['index_based']=index_based_element_switch(zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'],[zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][0]],[zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][2]])
            if zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][1]==zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][3]:
                zero_two_B_map_ansatz_term_first_Leibniz_case['coefficient']*=4
            else:
                zero_two_B_map_ansatz_term_first_Leibniz_case['index_based']=index_based_element_switch(zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'],[zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][1]],[zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][3]])
            zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'].pop(1)
            zero_two_B_map_ansatz_term_first_Leibniz_case['coefficient']*=(-1)**(len(zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][1]))
            zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][0][0]=3
            zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][2][0]=1
            zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][3][0]=1
            zero_two_B_map_ansatz_term_first_Leibniz_case['index_based']=list(reversed(index_based_reorganize(zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'])))
            result_operation_B.append(deepcopy(zero_two_B_map_ansatz_term_first_Leibniz_case))
    elif zero_two_B_map_ansatz_term_first['eta']==1:
        for Leibniz_case in product([0,2],repeat=len(zero_two_B_map_ansatz_term_first['index_based'][1][1])):
            zero_two_B_map_ansatz_term_first_Leibniz_case=deepcopy(zero_two_B_map_ansatz_term_first)
            zero_two_B_map_ansatz_term_first_Leibniz_case['coefficient']*=2
            for destination in Leibniz_case:
                zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][destination][1].append(zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][1].pop(0))
            zero_two_B_map_ansatz_term_first_Leibniz_case['coefficient']*=(-1)**(Leibniz_case.count(2))
            if zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][1]==zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][0]:
                zero_two_B_map_ansatz_term_first_Leibniz_case['coefficient']*=4
            else:
                zero_two_B_map_ansatz_term_first_Leibniz_case['index_based']=index_based_element_switch(zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'],[zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][1]],[zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][0]])
            zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'].pop(1)
            zero_two_B_map_ansatz_term_first_Leibniz_case['coefficient']*=(-1)**(len(zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][1]))
            zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][0][0]=3
            zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][2][0]=1
            zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'][3][0]=1
            zero_two_B_map_ansatz_term_first_Leibniz_case['index_based']=list(reversed(index_based_reorganize(zero_two_B_map_ansatz_term_first_Leibniz_case['index_based'])))
            result_operation_B.append(deepcopy(zero_two_B_map_ansatz_term_first_Leibniz_case))

for zero_two_B_map_ansatz_term_second in ansatz.map_ansatz('zero_two_B',[[0,0],[1,1],[0,2],[1,3],[1,3]],4):

    zero_two_B_map_ansatz_term_second['coefficient']*=-1*Fraction(1,2)
    
    if zero_two_B_map_ansatz_term_second['eta']==0:
        for Leibniz_case in product([2,4],repeat=len(zero_two_B_map_ansatz_term_second['index_based'][3][1])):
            zero_two_B_map_ansatz_term_second_Leibniz_case=deepcopy(zero_two_B_map_ansatz_term_second)
            for destination in Leibniz_case:
                zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'][destination][1].append(zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'][3][1].pop(0))
            zero_two_B_map_ansatz_term_second_Leibniz_case['coefficient']*=(-1)**(Leibniz_case.count(4))
            zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'][3][2]+=[1,2]
            if zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'][3][2][0]==zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'][3][2][2]:
                zero_two_B_map_ansatz_term_second_Leibniz_case['coefficient']*=4
            else:
                zero_two_B_map_ansatz_term_second_Leibniz_case['index_based']=index_based_element_switch(zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'],[zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'][3][2][0]],[zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'][3][2][2]])
            if zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'][3][2][1]==zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'][3][2][3]:
                zero_two_B_map_ansatz_term_second_Leibniz_case['coefficient']*=4
            else:
                zero_two_B_map_ansatz_term_second_Leibniz_case['index_based']=index_based_element_switch(zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'],[zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'][3][2][1]],[zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'][3][2][3]])
            zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'].pop(3)
            zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'][0][0]=2
            zero_two_B_map_ansatz_term_second_Leibniz_case['coefficient']*=(-1)**(len(zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'][0][1]))
            zero_two_B_map_ansatz_term_second_Leibniz_case['index_based']=ansatz.list_position_switch (zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'], [0,1], [1,0])
            zero_two_B_map_ansatz_term_second_Leibniz_case['index_based']=index_based_reorganize(zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'])
            result_operation_C.append(deepcopy(zero_two_B_map_ansatz_term_second_Leibniz_case))
        zero_two_B_map_ansatz_term_second['index_based']=index_based_element_switch(zero_two_B_map_ansatz_term_second['index_based'],[1,2],[2,1])
        for Leibniz_case in product([2,4],repeat=len(zero_two_B_map_ansatz_term_second['index_based'][3][1])):
            zero_two_B_map_ansatz_term_second_Leibniz_case=deepcopy(zero_two_B_map_ansatz_term_second)
            for destination in Leibniz_case:
                zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'][destination][1].append(zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'][3][1].pop(0))
            zero_two_B_map_ansatz_term_second_Leibniz_case['coefficient']*=(-1)**(Leibniz_case.count(4))
            zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'][3][2]+=[1,2]
            if zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'][3][2][0]==zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'][3][2][2]:
                zero_two_B_map_ansatz_term_second_Leibniz_case['coefficient']*=4
            else:
                zero_two_B_map_ansatz_term_second_Leibniz_case['index_based']=index_based_element_switch(zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'],[zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'][3][2][0]],[zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'][3][2][2]])
            if zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'][3][2][1]==zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'][3][2][3]:
                zero_two_B_map_ansatz_term_second_Leibniz_case['coefficient']*=4
            else:
                zero_two_B_map_ansatz_term_second_Leibniz_case['index_based']=index_based_element_switch(zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'],[zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'][3][2][1]],[zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'][3][2][3]])
            zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'].pop(3)
            zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'][0][0]=2
            zero_two_B_map_ansatz_term_second_Leibniz_case['coefficient']*=(-1)**(len(zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'][0][1]))
            zero_two_B_map_ansatz_term_second_Leibniz_case['index_based']=ansatz.list_position_switch (zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'], [0,1], [1,0])
            zero_two_B_map_ansatz_term_second_Leibniz_case['index_based']=index_based_reorganize(zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'])
            result_operation_C.append(deepcopy(zero_two_B_map_ansatz_term_second_Leibniz_case))
    elif zero_two_B_map_ansatz_term_second['eta']==1:
        for Leibniz_case in product([2,4],repeat=len(zero_two_B_map_ansatz_term_second['index_based'][3][1])):
            zero_two_B_map_ansatz_term_second_Leibniz_case=deepcopy(zero_two_B_map_ansatz_term_second)
            zero_two_B_map_ansatz_term_second_Leibniz_case['coefficient']*=2
            for destination in Leibniz_case:
                zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'][destination][1].append(zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'][3][1].pop(0))
            zero_two_B_map_ansatz_term_second_Leibniz_case['coefficient']*=(-1)**(Leibniz_case.count(4))
            if zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'][3][2][1]==zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'][3][2][0]:
                zero_two_B_map_ansatz_term_second_Leibniz_case['coefficient']*=4
            else:
                zero_two_B_map_ansatz_term_second_Leibniz_case['index_based']=index_based_element_switch(zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'],[zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'][3][2][1]],[zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'][3][2][0]])
            zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'].pop(3)
            zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'][0][0]=2
            zero_two_B_map_ansatz_term_second_Leibniz_case['coefficient']*=(-1)**(len(zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'][0][1]))
            zero_two_B_map_ansatz_term_second_Leibniz_case['index_based']=ansatz.list_position_switch (zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'], [0,1], [1,0])
            zero_two_B_map_ansatz_term_second_Leibniz_case['index_based']=index_based_reorganize(zero_two_B_map_ansatz_term_second_Leibniz_case['index_based'])
            result_operation_C.append(deepcopy(zero_two_B_map_ansatz_term_second_Leibniz_case))

for zero_two_B_map_ansatz_term_third in ansatz.map_ansatz('zero_two_B',[[0,0],[1,1],[0,2],[1,3],[1,3]],4):

    zero_two_B_map_ansatz_term_third['coefficient']*=-1*Fraction(1,2)
    
    if zero_two_B_map_ansatz_term_third['eta']==0:
        for Leibniz_case in product([2,3],repeat=len(zero_two_B_map_ansatz_term_third['index_based'][4][1])):
            zero_two_B_map_ansatz_term_third_Leibniz_case=deepcopy(zero_two_B_map_ansatz_term_third)
            for destination in Leibniz_case:
                zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'][destination][1].append(zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'][4][1].pop(0))
            zero_two_B_map_ansatz_term_third_Leibniz_case['coefficient']*=(-1)**(Leibniz_case.count(3))
            zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'][4][2]+=[1,2]
            if zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'][4][2][0]==zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'][4][2][2]:
                zero_two_B_map_ansatz_term_third_Leibniz_case['coefficient']*=4
            else:
                zero_two_B_map_ansatz_term_third_Leibniz_case['index_based']=index_based_element_switch(zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'],[zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'][4][2][0]],[zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'][4][2][2]])
            if zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'][4][2][1]==zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'][4][2][3]:
                zero_two_B_map_ansatz_term_third_Leibniz_case['coefficient']*=4
            else:
                zero_two_B_map_ansatz_term_third_Leibniz_case['index_based']=index_based_element_switch(zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'],[zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'][4][2][1]],[zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'][4][2][3]])
            zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'].pop(4)
            zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'][0][0]=2
            zero_two_B_map_ansatz_term_third_Leibniz_case['coefficient']*=(-1)**(len(zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'][0][1]))
            zero_two_B_map_ansatz_term_third_Leibniz_case['index_based']=ansatz.list_position_switch (zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'], [0,1], [1,0])
            zero_two_B_map_ansatz_term_third_Leibniz_case['index_based']=index_based_reorganize(zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'])
            result_operation_C.append(deepcopy(zero_two_B_map_ansatz_term_third_Leibniz_case))
        zero_two_B_map_ansatz_term_third['index_based']=index_based_element_switch(zero_two_B_map_ansatz_term_third['index_based'],[1,2],[2,1])
        for Leibniz_case in product([2,3],repeat=len(zero_two_B_map_ansatz_term_third['index_based'][4][1])):
            zero_two_B_map_ansatz_term_third_Leibniz_case=deepcopy(zero_two_B_map_ansatz_term_third)
            for destination in Leibniz_case:
                zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'][destination][1].append(zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'][4][1].pop(0))
            zero_two_B_map_ansatz_term_third_Leibniz_case['coefficient']*=(-1)**(Leibniz_case.count(3))
            zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'][4][2]+=[1,2]
            if zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'][4][2][0]==zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'][4][2][2]:
                zero_two_B_map_ansatz_term_third_Leibniz_case['coefficient']*=4
            else:
                zero_two_B_map_ansatz_term_third_Leibniz_case['index_based']=index_based_element_switch(zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'],[zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'][4][2][0]],[zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'][4][2][2]])
            if zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'][4][2][1]==zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'][4][2][3]:
                zero_two_B_map_ansatz_term_third_Leibniz_case['coefficient']*=4
            else:
                zero_two_B_map_ansatz_term_third_Leibniz_case['index_based']=index_based_element_switch(zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'],[zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'][4][2][1]],[zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'][4][2][3]])
            zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'].pop(4)
            zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'][0][0]=2
            zero_two_B_map_ansatz_term_third_Leibniz_case['coefficient']*=(-1)**(len(zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'][0][1]))
            zero_two_B_map_ansatz_term_third_Leibniz_case['index_based']=ansatz.list_position_switch (zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'], [0,1], [1,0])
            zero_two_B_map_ansatz_term_third_Leibniz_case['index_based']=index_based_reorganize(zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'])
            result_operation_C.append(deepcopy(zero_two_B_map_ansatz_term_third_Leibniz_case))
    elif zero_two_B_map_ansatz_term_third['eta']==1:
        for Leibniz_case in product([2,3],repeat=len(zero_two_B_map_ansatz_term_third['index_based'][4][1])):
            zero_two_B_map_ansatz_term_third_Leibniz_case=deepcopy(zero_two_B_map_ansatz_term_third)
            zero_two_B_map_ansatz_term_third_Leibniz_case['coefficient']*=2
            for destination in Leibniz_case:
                zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'][destination][1].append(zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'][4][1].pop(0))
            zero_two_B_map_ansatz_term_third_Leibniz_case['coefficient']*=(-1)**(Leibniz_case.count(3))
            if zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'][4][2][1]==zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'][4][2][0]:
                zero_two_B_map_ansatz_term_third_Leibniz_case['coefficient']*=4
            else:
                zero_two_B_map_ansatz_term_third_Leibniz_case['index_based']=index_based_element_switch(zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'],[zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'][4][2][1]],[zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'][4][2][0]])
            zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'].pop(4)
            zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'][0][0]=2
            zero_two_B_map_ansatz_term_third_Leibniz_case['coefficient']*=(-1)**(len(zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'][0][1]))
            zero_two_B_map_ansatz_term_third_Leibniz_case['index_based']=ansatz.list_position_switch (zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'], [0,1], [1,0])
            zero_two_B_map_ansatz_term_third_Leibniz_case['index_based']=index_based_reorganize(zero_two_B_map_ansatz_term_third_Leibniz_case['index_based'])
            result_operation_C.append(deepcopy(zero_two_B_map_ansatz_term_third_Leibniz_case))

zero_one_map_ansatz_field_derivative=[]

for zero_one_map_ansatz_term in ansatz.map_ansatz('zero_one',[[0,0],[1,1],[1,1]],2):
    zero_one_map_ansatz_term['coefficient']*=Fraction(1,2)
    if zero_one_map_ansatz_term['eta']==0:
        for Leibniz_case in product([0,2],repeat=len(zero_one_map_ansatz_term['index_based'][1][1])):
            zero_one_map_ansatz_term_Leibniz_case=deepcopy(zero_one_map_ansatz_term)                                                                         
            for destination in Leibniz_case:
                zero_one_map_ansatz_term_Leibniz_case['index_based'][destination][1].append(zero_one_map_ansatz_term_Leibniz_case['index_based'][1][1].pop(0))                                                                       
            zero_one_map_ansatz_term_Leibniz_case['coefficient']*=(-1)**(Leibniz_case.count(2))
            zero_one_map_ansatz_term_Leibniz_case['index_based'][1][2]+=[5,6]
            zero_one_map_ansatz_field_derivative.append(deepcopy(zero_one_map_ansatz_term_Leibniz_case))
        for Leibniz_case in product([0,1],repeat=len(zero_one_map_ansatz_term['index_based'][2][1])):
            zero_one_map_ansatz_term_Leibniz_case=deepcopy(zero_one_map_ansatz_term)                                                                         
            for destination in Leibniz_case:
                zero_one_map_ansatz_term_Leibniz_case['index_based'][destination][1].append(zero_one_map_ansatz_term_Leibniz_case['index_based'][2][1].pop(0))                                                                       
            zero_one_map_ansatz_term_Leibniz_case['coefficient']*=(-1)**(Leibniz_case.count(1))
            zero_one_map_ansatz_term_Leibniz_case['index_based'][2][2]+=[5,6]
            zero_one_map_ansatz_field_derivative.append(deepcopy(zero_one_map_ansatz_term_Leibniz_case))
        zero_one_map_ansatz_term['index_based']=index_based_element_switch(zero_one_map_ansatz_term['index_based'],[1,2],[2,1])
        for Leibniz_case in product([0,2],repeat=len(zero_one_map_ansatz_term['index_based'][1][1])):
            zero_one_map_ansatz_term_Leibniz_case=deepcopy(zero_one_map_ansatz_term)                                                                         
            for destination in Leibniz_case:
                zero_one_map_ansatz_term_Leibniz_case['index_based'][destination][1].append(zero_one_map_ansatz_term_Leibniz_case['index_based'][1][1].pop(0))                                                                       
            zero_one_map_ansatz_term_Leibniz_case['coefficient']*=(-1)**(Leibniz_case.count(2))
            zero_one_map_ansatz_term_Leibniz_case['index_based'][1][2]+=[5,6]
            zero_one_map_ansatz_field_derivative.append(deepcopy(zero_one_map_ansatz_term_Leibniz_case))
        for Leibniz_case in product([0,1],repeat=len(zero_one_map_ansatz_term['index_based'][2][1])):
            zero_one_map_ansatz_term_Leibniz_case=deepcopy(zero_one_map_ansatz_term)                                                                         
            for destination in Leibniz_case:
                zero_one_map_ansatz_term_Leibniz_case['index_based'][destination][1].append(zero_one_map_ansatz_term_Leibniz_case['index_based'][2][1].pop(0))                                                                       
            zero_one_map_ansatz_term_Leibniz_case['coefficient']*=(-1)**(Leibniz_case.count(1))
            zero_one_map_ansatz_term_Leibniz_case['index_based'][2][2]+=[5,6]
            zero_one_map_ansatz_field_derivative.append(deepcopy(zero_one_map_ansatz_term_Leibniz_case))                                                    
    if zero_one_map_ansatz_term['eta']==1:
        for Leibniz_case in product([0,2],repeat=len(zero_one_map_ansatz_term['index_based'][1][1])):
            zero_one_map_ansatz_term_Leibniz_case=deepcopy(zero_one_map_ansatz_term)                                                                         
            for destination in Leibniz_case:
                zero_one_map_ansatz_term_Leibniz_case['index_based'][destination][1].append(zero_one_map_ansatz_term_Leibniz_case['index_based'][1][1].pop(0))                                                                       
            zero_one_map_ansatz_term_Leibniz_case['coefficient']*=2*(-1)**(Leibniz_case.count(2))
            zero_one_map_ansatz_term_Leibniz_case['index_based'][1][2]+=[5,6]
            zero_one_map_ansatz_field_derivative.append(deepcopy(zero_one_map_ansatz_term_Leibniz_case))
        for Leibniz_case in product([0,1],repeat=len(zero_one_map_ansatz_term['index_based'][2][1])):
            zero_one_map_ansatz_term_Leibniz_case=deepcopy(zero_one_map_ansatz_term)                                                                         
            for destination in Leibniz_case:
                zero_one_map_ansatz_term_Leibniz_case['index_based'][destination][1].append(zero_one_map_ansatz_term_Leibniz_case['index_based'][2][1].pop(0))                                                                       
            zero_one_map_ansatz_term_Leibniz_case['coefficient']*=2*(-1)**(Leibniz_case.count(1))
            zero_one_map_ansatz_term_Leibniz_case['index_based'][2][2]+=[5,6]
            zero_one_map_ansatz_field_derivative.append(deepcopy(zero_one_map_ansatz_term_Leibniz_case))

zero_one_map_ansatz_field_derivative_first=deepcopy(zero_one_map_ansatz_field_derivative)

for term in zero_one_map_ansatz_field_derivative_first:
     term['coefficient']*=(-1)**(len(term['index_based'][0][1]))
     term['index_based'][0][0]=2
     term['index_based'][1][0]=1
     term['index_based'][2][0]=1
     term['index_based']=list(reversed(term['index_based']))
                                                                                 
zero_one_map_ansatz_field_derivative_second=deepcopy(zero_one_map_ansatz_field_derivative)
                                                                                 
for term in zero_one_map_ansatz_field_derivative_second:
     term['index_based'][0][0]=2
     term['index_based'][1][0]=3
     term['index_based'][2][0]=3
     term['index_based']=index_based_element_switch (term['index_based'], [1,2,3,4,5,6], [7,8,9,10,11,12])

for first in zero_one_map_ansatz_field_derivative_first:
     for second in zero_one_map_ansatz_field_derivative_second:
        first=deepcopy(first)
        second=deepcopy(second)
        first_id=first['id']
        second_id=second['id']
        map_product={'id':f"{first_id}*{second_id}",'coefficient': Fraction(1,2),'index_based':[],'position_based':[]}
        map_product['coefficient']*=first['coefficient']*second['coefficient']
        map_product['index_based']=first['index_based']+second['index_based']                                                                         
        if first['eta']==0:
            map_product['index_based']=index_based_element_switch (map_product['index_based'], [11,12], [1,2])
        elif first['eta']==1:
            map_product['index_based']=index_based_element_switch (map_product['index_based'], [12], [11])
        if second['eta']==0:
            map_product['index_based']=index_based_element_switch (map_product['index_based'], [5,6], [7,8])
        elif second['eta']==1:
            map_product['index_based']=index_based_element_switch (map_product['index_based'], [6], [5])
        #print(map_product)
        kronecker_delta_position=[ position for position in range(len(map_product['index_based'])) if len(map_product['index_based'][position]) > 2 and len(map_product['index_based'][position][2]) == 4]
        #print(kronecker_delta_position)
        for position in kronecker_delta_position:
            for order in [0,1]:
                if map_product['index_based'][position][2][order]==map_product['index_based'][position][2][order+2]:
                    map_product['coefficient']*=4
                else:
                    map_product['index_based']=index_based_element_switch (map_product['index_based'], [map_product['index_based'][position][2][order]], [map_product['index_based'][position][2][order+2]])
        map_product['index_based']=index_based_reorganize([ element for element in map_product['index_based'] if len(element) == 2 or len(element[2]) != 4])
        result_operation_C.append(deepcopy(map_product))

for index, term in enumerate(result_operation_A):
    result_operation_A[index]['position_based']=position_based_of_(term['index_based'])
    '''
    print(result_operation[index])
    '''

for index, term in enumerate(result_operation_B):
    result_operation_B[index]['position_based']=position_based_of_(term['index_based'])
    '''
    print(result_operation[index])
    '''

for index, term in enumerate(result_operation_C):
    result_operation_C[index]['position_based']=position_based_of_(term['index_based'])
    '''
    print(result_operation[index])
    '''

one_two_A_action_class=ansatz.action_class('one_two_A',[[1,1],[1,1],[2,2]],2)

one_two_B_action_class=ansatz.action_class('one_two_B',[[1,1],[1,1],[0,2],[2,3]],4)

one_two_C_action_class=ansatz.action_class('one_two_C',[[1,1],[0,2],[0,2],[1,3]],4,symmetry=True)

one_two_condition={}

for term in result_operation_A:
    for action_class in one_two_A_action_class:
        for position_based in action_class['position_based']:
            if term['position_based']==position_based:
                coefficient=term['coefficient']
                variable=term['id']
                one_two_condition[action_class['id']]=one_two_condition.get(action_class['id'],'')+f'+({coefficient})*{variable}'
                break

for term in result_operation_C:
    for action_class in one_two_C_action_class:
        for position_based in action_class['position_based']:
            if term['position_based']==position_based:
                coefficient=term['coefficient']
                variable=term['id']
                one_two_condition[action_class['id']]=one_two_condition.get(action_class['id'],'')+f'+({coefficient})*{variable}'
                break

for key in one_two_condition:
    one_two_condition[key]+="-action_"+key

for term in result_operation_B:
    for action_class in one_two_B_action_class:
        for position_based in action_class['position_based']:
            if term['position_based']==position_based:
                coefficient=term['coefficient']
                variable=term['id']
                one_two_condition[action_class['id']]=one_two_condition.get(action_class['id'],'')+f'+({coefficient})*{variable}'
                break

one_two_condition_new={}      

for key,value in one_two_condition.items():
    expr=sp.Integer(0)
    bucket=[]
    for term in spl._split_top_level_addsub(value):
        bucket.append(sp.expand_mul(sp.sympify(term)))
        if len(bucket) >= 2000:
            expr=sp.Add(expr,sp.Add(*bucket))
            bucket.clear()
    if bucket:
        expr=sp.Add(expr, sp.Add(*bucket))
    one_two_condition_new.update({sp.Symbol(key):deepcopy(expr)})

one_two_condition=one_two_condition_new

BA_inear_combination=[]
CA_inear_combination=[]

for term in one_two_B_action_class:
    if len(term['index_based'][2][1])==2:
        if term['index_based'][2][1][0]==term['index_based'][2][1][1]:
            '''
            print("B")
            print(term['index_based'])
            '''
            term['index_based'].pop(2)
            term['index_based'][2][0] = 2
            for term2 in one_two_A_action_class:
                if position_based_of_(index_based_reorganize(term['index_based'])) in term2['position_based']:
                    '''
                    print("A")
                    print(term2['index_based'])
                    print(sp.sympify(term['id']+'-'+term2['id']))
                    '''
                    BA_inear_combination.append(sp.sympify(term['id']+'-'+term2['id']))

for term in one_two_C_action_class:
    
    if len(term['index_based'][1][1])==2:
        if term['index_based'][1][1][0]==term['index_based'][1][1][1]:
            '''
            print("C")
            print(term['index_based'])
            '''
            term['index_based'].pop(1)
            term['index_based'][2][0]=1
            term['index_based'] = ansatz.list_position_switch(term['index_based'], [1, 2], [2, 1])
            for term2 in one_two_A_action_class:
                if position_based_of_(index_based_reorganize(term['index_based'])) in term2['position_based']:
                    '''
                    print("A")
                    print(term2['index_based'])
                    print(sp.sympify(term['id']+'-'+term2['id']))
                    '''
                    CA_inear_combination.append(sp.sympify(term['id']+'-'+term2['id']))
            continue

    if len(term['index_based'][2][1])==2:
        if term['index_based'][2][1][0]==term['index_based'][2][1][1]:
            '''
            print("C")
            print(term['index_based'])
            '''
            term['index_based'].pop(2)
            term['index_based'][2][0]=1
            term['index_based'] = ansatz.list_position_switch(term['index_based'], [1, 2], [2, 1])
            for term2 in one_two_A_action_class:
                if position_based_of_(index_based_reorganize(term['index_based'])) in term2['position_based']:
                    '''
                    print("A")
                    print(term2['index_based'])
                    print(sp.sympify(term['id']+'-'+term2['id']))
                    '''
                    CA_inear_combination.append(sp.sympify(term['id']+'-'+term2['id']))

solution,pivot_variable_list=linear_algebra.gauss_jordan_solution(
    linear_algebra.linear_combination_of_(
    ansatz.action_class('one_two_A',[[1,1],[1,1],[2,2]],2),
    [[0,[2,'+']],
     [2,[0,'+']]]
    )
    +
    linear_algebra.linear_combination_of_(
    ansatz.action_class('one_two_B',[[1,1],[1,1],[0,2],[2,3]],4),
    [[0,[2,'+'],[4,'+']],
     [2,[0,'+'],[4,'+']],
     [4,[0,'+'],[2,'+']]]
    )
    +
    linear_algebra.linear_combination_of_(
    ansatz.action_class('one_two_C',[[1,1],[0,2],[0,2],[1,3]],4,symmetry=True),
    [[0,[2,'+'],[3,'+']],
     [2,[0,'+'],[3,'+']],
     [3,[0,'+'],[2,'+']],
     [2,[3,'+'],[4,'-']],
     [3,[2,'+'],[4,'-']],
     [4,[2,'-'],[3,'-']]],
    symmetry=True
    )
    +
    BA_inear_combination
    +
    CA_inear_combination
    )

for pivot_variable in pivot_variable_list:
    for variable,coefficient in solution[pivot_variable][1].items():
        one_two_condition[variable]=one_two_condition.get(variable,sp.Integer(0))+coefficient*(one_two_condition.get(pivot_variable,sp.Integer(0)))
    one_two_condition.pop(pivot_variable, None)

