import ansatz
import sympy as sp
from copy import deepcopy
from itertools import product
from fractions import Fraction
from left import two_two_C_left

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

def two_two_A_action_integration_by_parts(two_two_A_action):

    number_partial_derivative_position=[]
    for element in two_two_A_action['index_based']:
        number_partial_derivative_position.append(len(element[1]))

    result=[]

    if set(number_partial_derivative_position)=={0,2}:
        index_based_no_class_number=[indices for structure_element in two_two_A_action['index_based'] for indices in structure_element[1:]]
        position_based=[ [] for _ in range(1)]
        for position in range(len(index_based_no_class_number)):
            for index in index_based_no_class_number[position]:
                position_based[index-1].append(position)   
        two_two_A_action['position_based']=sorted(position_based)
        result.append(deepcopy(two_two_A_action))

    return result

def two_two_B_action_integration_by_parts(two_two_B_action):

    number_partial_derivative_position=[]
    for element in two_two_B_action['index_based']:
        number_partial_derivative_position.append(len(element[1]))

    result=[]

    if all(number_partial_derivative % 2 == 0 for number_partial_derivative in number_partial_derivative_position):
        index_based_no_class_number=[indices for structure_element in two_two_B_action['index_based'] for indices in structure_element[1:]]
        position_based=[ [] for _ in range(2)]
        for position in range(len(index_based_no_class_number)):
            for index in index_based_no_class_number[position]:
                position_based[index-1].append(position)   
        two_two_B_action['position_based']=sorted(position_based)
        result.append(deepcopy(two_two_B_action))

    return result

def two_two_C_action_integration_by_parts(two_two_C_action):

    number_partial_derivative_position=[]
    for element in two_two_C_action['index_based']:
        number_partial_derivative_position.append(len(element[1]))

    result=[]

    index_based_no_class_number=[indices for structure_element in two_two_C_action['index_based'] for indices in structure_element[1:]]
    position_based=[ [] for _ in range(2)]
    for position in range(len(index_based_no_class_number)):
        for index in index_based_no_class_number[position]:
            position_based[index-1].append(position)   
    two_two_C_action['position_based']=sorted(position_based)
    result.append(deepcopy(two_two_C_action))

    return result

def position_based_of_(index_based):
    index_based_no_class_number=[indices for structure_element in index_based for indices in structure_element[1:]]
    position_based=[ [] for _ in range(len(set(index for element in index_based_no_class_number for index in element)))]
    for position in range(len(index_based_no_class_number)):
        for index in index_based_no_class_number[position]:
            position_based[index-1].append(position)   
    return sorted(position_based)

map_ansatz_one_one=[]
for term in ansatz.map_ansatz('one_one',[[0,0],[0,1]],2):
    if len(term['index_based'][0][1])==0:
        map_ansatz_one_one.append(term)

result_operation_A=[]
result_operation_B=[]
result_operation_C=[]

condition_variable_index=1

for one_one_map_ansatz_term_first in map_ansatz_one_one:
    for one_one_map_ansatz_term_second in map_ansatz_one_one:
        first=deepcopy(one_one_map_ansatz_term_first)
        second=deepcopy(one_one_map_ansatz_term_second)
        first_id=first['id']
        second_id=second['id']
        map_product={'id':f"{first_id}*{second_id}",'coefficient':1,'index_based':[],'position_based':[]}
        first['index_based'][0][0]=1
        first['index_based'][1][0]=2
        second['index_based'][1][0]=2
        if first['eta']==0:
            if second['eta']==0:
                map_product['coefficient']*=Fraction(1,2)
                for symmetrization in [[1,2],[2,1]]:
                    first_index_based=deepcopy(first['index_based'])
                    second_index_based=deepcopy(second['index_based'])
                    first_index_based=index_based_element_switch(first_index_based,[1,2],symmetrization)
                    map_product['index_based']=first_index_based+second_index_based[1:]
                    result_operation_B.append(deepcopy(map_product))
                continue
            elif second['eta']==1:
                first['index_based']=index_based_element_switch(first['index_based'],[1,2],[1,1])
                second['index_based']=index_based_element_switch(second['index_based'],[1],[2])
        elif first['eta']==1:
            if second['eta']==0:
                second['index_based']=index_based_element_switch(second['index_based'],[1,2],[2,2])
            elif second['eta']==1:
                map_product['coefficient']*=4
                second['index_based']=index_based_element_switch(second['index_based'],[1],[2])                
        first['index_based'][0][1]+=second['index_based'][0].pop(1)
        map_product['index_based']=first['index_based']+second['index_based'][1:]
        result_operation_B.append(deepcopy(map_product))

for one_one_map_ansatz_term_third in map_ansatz_one_one:
    for one_one_map_ansatz_term_fourth in map_ansatz_one_one:
        third=deepcopy(one_one_map_ansatz_term_third)
        fourth=deepcopy(one_one_map_ansatz_term_fourth)
        third_id=third['id']
        fourth_id=fourth['id']
        map_product={'id':f"{third_id}*{fourth_id}",'coefficient':-1*Fraction(1,2),'index_based':[],'position_based':[]}
        third['index_based'][0][0]=1
        third['index_based'][1][0]=2
        fourth['index_based'][1][0]=2
        if third['eta']==0:
            if fourth['eta']==0:
                third['index_based']=index_based_element_switch(third['index_based'],[1,2],[1,1])
                fourth['index_based']=index_based_element_switch(fourth['index_based'],[1,2],[2,2])
            elif fourth['eta']==1:
                map_product['coefficient']*=4
                third['index_based']=index_based_element_switch(third['index_based'],[1,2],[1,1])
                fourth['index_based']=index_based_element_switch(fourth['index_based'],[1],[2])
        elif third['eta']==1:
            if fourth['eta']==0:
                map_product['coefficient']*=4
                fourth['index_based']=index_based_element_switch(fourth['index_based'],[1,2],[2,2])
            elif fourth['eta']==1:
                map_product['coefficient']*=16
                fourth['index_based']=index_based_element_switch(fourth['index_based'],[1],[2])                
        map_product['index_based']=third['index_based']+fourth['index_based'][1:]
        result_operation_B.append(deepcopy(map_product))

for one_two_A_map_ansatz_term_first in ansatz.map_ansatz ('one_two_A',[[0,0],[1,1],[0,2]],2):

    one_two_A_map_ansatz_term_first['coefficient']*=Fraction(1,2)
    
    if one_two_A_map_ansatz_term_first['eta']==0:
        one_two_A_map_ansatz_term_first_Leibniz_case=deepcopy(one_two_A_map_ansatz_term_first)
        one_two_A_map_ansatz_term_first_Leibniz_case['index_based'][0][1]+=deepcopy(one_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][1])
        one_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2]+=[1,2]
        if one_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][0]==one_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][2]:
            one_two_A_map_ansatz_term_first_Leibniz_case['coefficient']*=4
        else:
            one_two_A_map_ansatz_term_first_Leibniz_case['index_based']=index_based_element_switch(one_two_A_map_ansatz_term_first_Leibniz_case['index_based'],[one_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][0]],[one_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][2]])
        if one_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][1]==one_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][3]:
            one_two_A_map_ansatz_term_first_Leibniz_case['coefficient']*=4
        else:
            one_two_A_map_ansatz_term_first_Leibniz_case['index_based']=index_based_element_switch(one_two_A_map_ansatz_term_first_Leibniz_case['index_based'],[one_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][1]],[one_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][3]])
        one_two_A_map_ansatz_term_first_Leibniz_case['index_based'].pop(1)
        one_two_A_map_ansatz_term_first_Leibniz_case['index_based'][0][0]=1
        one_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][0]=1
        one_two_A_map_ansatz_term_first_Leibniz_case['index_based']=index_based_reorganize(one_two_A_map_ansatz_term_first_Leibniz_case['index_based'])
        result_operation_A.append(deepcopy(one_two_A_map_ansatz_term_first_Leibniz_case))
        one_two_A_map_ansatz_term_first['index_based']=index_based_element_switch(one_two_A_map_ansatz_term_first['index_based'],[1,2],[2,1])
        one_two_A_map_ansatz_term_first_Leibniz_case=deepcopy(one_two_A_map_ansatz_term_first)
        one_two_A_map_ansatz_term_first_Leibniz_case['index_based'][0][1]+=deepcopy(one_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][1])
        one_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2]+=[1,2]
        if one_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][0]==one_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][2]:
            one_two_A_map_ansatz_term_first_Leibniz_case['coefficient']*=4
        else:
            one_two_A_map_ansatz_term_first_Leibniz_case['index_based']=index_based_element_switch(one_two_A_map_ansatz_term_first_Leibniz_case['index_based'],[one_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][0]],[one_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][2]])
        if one_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][1]==one_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][3]:
            one_two_A_map_ansatz_term_first_Leibniz_case['coefficient']*=4
        else:
            one_two_A_map_ansatz_term_first_Leibniz_case['index_based']=index_based_element_switch(one_two_A_map_ansatz_term_first_Leibniz_case['index_based'],[one_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][1]],[one_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][3]])
        one_two_A_map_ansatz_term_first_Leibniz_case['index_based'].pop(1)
        one_two_A_map_ansatz_term_first_Leibniz_case['index_based'][0][0]=1
        one_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][0]=1
        one_two_A_map_ansatz_term_first_Leibniz_case['index_based']=index_based_reorganize(one_two_A_map_ansatz_term_first_Leibniz_case['index_based'])
        result_operation_A.append(deepcopy(one_two_A_map_ansatz_term_first_Leibniz_case))
    elif one_two_A_map_ansatz_term_first['eta']==1:
        one_two_A_map_ansatz_term_first_Leibniz_case=deepcopy(one_two_A_map_ansatz_term_first)
        one_two_A_map_ansatz_term_first_Leibniz_case['coefficient']*=2
        one_two_A_map_ansatz_term_first_Leibniz_case['index_based'][0][1]+=deepcopy(one_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][1])
        if one_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][1]==one_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][0]:
            one_two_A_map_ansatz_term_first_Leibniz_case['coefficient']*=4
        else:
            one_two_A_map_ansatz_term_first_Leibniz_case['index_based']=index_based_element_switch(one_two_A_map_ansatz_term_first_Leibniz_case['index_based'],[one_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][1]],[one_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][2][0]])
        one_two_A_map_ansatz_term_first_Leibniz_case['index_based'].pop(1)
        one_two_A_map_ansatz_term_first_Leibniz_case['index_based'][0][0]=1
        one_two_A_map_ansatz_term_first_Leibniz_case['index_based'][1][0]=1
        one_two_A_map_ansatz_term_first_Leibniz_case['index_based']=index_based_reorganize(one_two_A_map_ansatz_term_first_Leibniz_case['index_based'])
        result_operation_A.append(deepcopy(one_two_A_map_ansatz_term_first_Leibniz_case))

for one_two_B_map_ansatz_term_first in ansatz.map_ansatz ('one_two_B',[[0,0],[1,1],[0,2],[0,3]],4):

    one_two_B_map_ansatz_term_first['coefficient']*=Fraction(1,2)#ha
    
    if one_two_B_map_ansatz_term_first['eta']==0:
        for Leibniz_case in product([0,2],repeat=len(one_two_B_map_ansatz_term_first['index_based'][1][1])):
            one_two_B_map_ansatz_term_first_Leibniz_case=deepcopy(one_two_B_map_ansatz_term_first)
            for destination in Leibniz_case:
                one_two_B_map_ansatz_term_first_Leibniz_case['index_based'][destination][1].append(one_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][1].pop(0))
            one_two_B_map_ansatz_term_first_Leibniz_case['coefficient']*=(-1)**Leibniz_case.count(2)
            one_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2]+=[1,2]
            if one_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][0]==one_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][2]:
                one_two_B_map_ansatz_term_first_Leibniz_case['coefficient']*=4
            else:
                one_two_B_map_ansatz_term_first_Leibniz_case['index_based']=index_based_element_switch(one_two_B_map_ansatz_term_first_Leibniz_case['index_based'],[one_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][0]],[one_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][2]])
            if one_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][1]==one_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][3]:
                one_two_B_map_ansatz_term_first_Leibniz_case['coefficient']*=4
            else:
                one_two_B_map_ansatz_term_first_Leibniz_case['index_based']=index_based_element_switch(one_two_B_map_ansatz_term_first_Leibniz_case['index_based'],[one_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][1]],[one_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][3]])
            one_two_B_map_ansatz_term_first_Leibniz_case['index_based'].pop(1)
            one_two_B_map_ansatz_term_first_Leibniz_case['index_based'][2][0]=2
            one_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][0]=1
            one_two_B_map_ansatz_term_first_Leibniz_case['index_based'][0][0]=2
            one_two_B_map_ansatz_term_first_Leibniz_case['index_based'].append(one_two_B_map_ansatz_term_first_Leibniz_case['index_based'].pop(0))
            one_two_B_map_ansatz_term_first_Leibniz_case['index_based']=index_based_reorganize(one_two_B_map_ansatz_term_first_Leibniz_case['index_based'])
            result_operation_B.append(deepcopy(one_two_B_map_ansatz_term_first_Leibniz_case))
        one_two_B_map_ansatz_term_first['index_based']=index_based_element_switch(one_two_B_map_ansatz_term_first['index_based'],[1,2],[2,1])
        for Leibniz_case in product([0,2],repeat=len(one_two_B_map_ansatz_term_first['index_based'][1][1])):
            one_two_B_map_ansatz_term_first_Leibniz_case=deepcopy(one_two_B_map_ansatz_term_first)
            for destination in Leibniz_case:
                one_two_B_map_ansatz_term_first_Leibniz_case['index_based'][destination][1].append(one_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][1].pop(0))
            one_two_B_map_ansatz_term_first_Leibniz_case['coefficient']*=(-1)**Leibniz_case.count(2)
            one_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2]+=[1,2]
            if one_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][0]==one_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][2]:
                one_two_B_map_ansatz_term_first_Leibniz_case['coefficient']*=4
            else:
                one_two_B_map_ansatz_term_first_Leibniz_case['index_based']=index_based_element_switch(one_two_B_map_ansatz_term_first_Leibniz_case['index_based'],[one_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][0]],[one_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][2]])
            if one_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][1]==one_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][3]:
                one_two_B_map_ansatz_term_first_Leibniz_case['coefficient']*=4
            else:
                one_two_B_map_ansatz_term_first_Leibniz_case['index_based']=index_based_element_switch(one_two_B_map_ansatz_term_first_Leibniz_case['index_based'],[one_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][1]],[one_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][3]])
            one_two_B_map_ansatz_term_first_Leibniz_case['index_based'].pop(1)
            one_two_B_map_ansatz_term_first_Leibniz_case['index_based'][2][0]=2
            one_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][0]=1
            one_two_B_map_ansatz_term_first_Leibniz_case['index_based'][0][0]=2
            one_two_B_map_ansatz_term_first_Leibniz_case['index_based'].append(one_two_B_map_ansatz_term_first_Leibniz_case['index_based'].pop(0))
            one_two_B_map_ansatz_term_first_Leibniz_case['index_based']=index_based_reorganize(one_two_B_map_ansatz_term_first_Leibniz_case['index_based'])
            result_operation_B.append(deepcopy(one_two_B_map_ansatz_term_first_Leibniz_case))
    elif one_two_B_map_ansatz_term_first['eta']==1:
        for Leibniz_case in product([0,2],repeat=len(one_two_B_map_ansatz_term_first['index_based'][1][1])):
            one_two_B_map_ansatz_term_first_Leibniz_case=deepcopy(one_two_B_map_ansatz_term_first)
            one_two_B_map_ansatz_term_first_Leibniz_case['coefficient']*=2
            for destination in Leibniz_case:
                one_two_B_map_ansatz_term_first_Leibniz_case['index_based'][destination][1].append(one_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][1].pop(0))
            one_two_B_map_ansatz_term_first_Leibniz_case['coefficient']*=(-1)**Leibniz_case.count(2)
            if one_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][1]==one_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][0]:
                one_two_B_map_ansatz_term_first_Leibniz_case['coefficient']*=4
            else:
                one_two_B_map_ansatz_term_first_Leibniz_case['index_based']=index_based_element_switch(one_two_B_map_ansatz_term_first_Leibniz_case['index_based'],[one_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][1]],[one_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][2][0]])
            one_two_B_map_ansatz_term_first_Leibniz_case['index_based'].pop(1)
            one_two_B_map_ansatz_term_first_Leibniz_case['index_based'][2][0]=2
            one_two_B_map_ansatz_term_first_Leibniz_case['index_based'][1][0]=1
            one_two_B_map_ansatz_term_first_Leibniz_case['index_based'][0][0]=2
            one_two_B_map_ansatz_term_first_Leibniz_case['index_based'].append(one_two_B_map_ansatz_term_first_Leibniz_case['index_based'].pop(0))
            one_two_B_map_ansatz_term_first_Leibniz_case['index_based']=index_based_reorganize(one_two_B_map_ansatz_term_first_Leibniz_case['index_based'])
            result_operation_B.append(deepcopy(one_two_B_map_ansatz_term_first_Leibniz_case))

for one_two_C_map_ansatz_term_first in ansatz.map_ansatz ('one_two_C',[[0,0],[0,1],[0,1],[1,2]],4):

    one_two_C_map_ansatz_term_first['coefficient']*=Fraction(1,2)#ha
    
    if one_two_C_map_ansatz_term_first['eta']==0:
        for Leibniz_case in product([1,2],repeat=len(one_two_C_map_ansatz_term_first['index_based'][3][1])):
            one_two_C_map_ansatz_term_first_Leibniz_case=deepcopy(one_two_C_map_ansatz_term_first)
            one_two_C_map_ansatz_term_first_Leibniz_case['coefficient']*=(-1)**len(one_two_C_map_ansatz_term_first_Leibniz_case['index_based'][0][1])
            for destination in Leibniz_case:
                one_two_C_map_ansatz_term_first_Leibniz_case['index_based'][destination][1].append(one_two_C_map_ansatz_term_first_Leibniz_case['index_based'][3][1].pop(0))
            one_two_C_map_ansatz_term_first_Leibniz_case['index_based'][3][2]+=[1,2]
            if one_two_C_map_ansatz_term_first_Leibniz_case['index_based'][3][2][0]==one_two_C_map_ansatz_term_first_Leibniz_case['index_based'][3][2][2]:
                one_two_C_map_ansatz_term_first_Leibniz_case['coefficient']*=4
            else:
                one_two_C_map_ansatz_term_first_Leibniz_case['index_based']=index_based_element_switch(one_two_C_map_ansatz_term_first_Leibniz_case['index_based'],[one_two_C_map_ansatz_term_first_Leibniz_case['index_based'][3][2][0]],[one_two_C_map_ansatz_term_first_Leibniz_case['index_based'][3][2][2]])
            if one_two_C_map_ansatz_term_first_Leibniz_case['index_based'][3][2][1]==one_two_C_map_ansatz_term_first_Leibniz_case['index_based'][3][2][3]:
                one_two_C_map_ansatz_term_first_Leibniz_case['coefficient']*=4
            else:
                one_two_C_map_ansatz_term_first_Leibniz_case['index_based']=index_based_element_switch(one_two_C_map_ansatz_term_first_Leibniz_case['index_based'],[one_two_C_map_ansatz_term_first_Leibniz_case['index_based'][3][2][1]],[one_two_C_map_ansatz_term_first_Leibniz_case['index_based'][3][2][3]])
            one_two_C_map_ansatz_term_first_Leibniz_case['index_based'].pop(3)
            one_two_C_map_ansatz_term_first_Leibniz_case['index_based'][0][0]=1
            one_two_C_map_ansatz_term_first_Leibniz_case['index_based']=index_based_reorganize(one_two_C_map_ansatz_term_first_Leibniz_case['index_based'])
            result_operation_C.append(deepcopy(one_two_C_map_ansatz_term_first_Leibniz_case))
        one_two_C_map_ansatz_term_first['index_based']=index_based_element_switch(one_two_C_map_ansatz_term_first['index_based'],[1,2],[2,1])
        for Leibniz_case in product([1,2],repeat=len(one_two_C_map_ansatz_term_first['index_based'][3][1])):
            one_two_C_map_ansatz_term_first_Leibniz_case=deepcopy(one_two_C_map_ansatz_term_first)
            one_two_C_map_ansatz_term_first_Leibniz_case['coefficient']*=(-1)**len(one_two_C_map_ansatz_term_first_Leibniz_case['index_based'][0][1])
            for destination in Leibniz_case:
                one_two_C_map_ansatz_term_first_Leibniz_case['index_based'][destination][1].append(one_two_C_map_ansatz_term_first_Leibniz_case['index_based'][3][1].pop(0))
            one_two_C_map_ansatz_term_first_Leibniz_case['index_based'][3][2]+=[1,2]
            if one_two_C_map_ansatz_term_first_Leibniz_case['index_based'][3][2][0]==one_two_C_map_ansatz_term_first_Leibniz_case['index_based'][3][2][2]:
                one_two_C_map_ansatz_term_first_Leibniz_case['coefficient']*=4
            else:
                one_two_C_map_ansatz_term_first_Leibniz_case['index_based']=index_based_element_switch(one_two_C_map_ansatz_term_first_Leibniz_case['index_based'],[one_two_C_map_ansatz_term_first_Leibniz_case['index_based'][3][2][0]],[one_two_C_map_ansatz_term_first_Leibniz_case['index_based'][3][2][2]])
            if one_two_C_map_ansatz_term_first_Leibniz_case['index_based'][3][2][1]==one_two_C_map_ansatz_term_first_Leibniz_case['index_based'][3][2][3]:
                one_two_C_map_ansatz_term_first_Leibniz_case['coefficient']*=4
            else:
                one_two_C_map_ansatz_term_first_Leibniz_case['index_based']=index_based_element_switch(one_two_C_map_ansatz_term_first_Leibniz_case['index_based'],[one_two_C_map_ansatz_term_first_Leibniz_case['index_based'][3][2][1]],[one_two_C_map_ansatz_term_first_Leibniz_case['index_based'][3][2][3]])
            one_two_C_map_ansatz_term_first_Leibniz_case['index_based'].pop(3)
            one_two_C_map_ansatz_term_first_Leibniz_case['index_based'][0][0]=1
            one_two_C_map_ansatz_term_first_Leibniz_case['index_based']=index_based_reorganize(one_two_C_map_ansatz_term_first_Leibniz_case['index_based'])
            result_operation_C.append(deepcopy(one_two_C_map_ansatz_term_first_Leibniz_case))
    elif one_two_C_map_ansatz_term_first['eta']==1:
        for Leibniz_case in product([1,2],repeat=len(one_two_C_map_ansatz_term_first['index_based'][3][1])):
            one_two_C_map_ansatz_term_first_Leibniz_case=deepcopy(one_two_C_map_ansatz_term_first)
            one_two_C_map_ansatz_term_first_Leibniz_case['coefficient']*=2*(-1)**len(one_two_C_map_ansatz_term_first_Leibniz_case['index_based'][0][1])
            for destination in Leibniz_case:
                one_two_C_map_ansatz_term_first_Leibniz_case['index_based'][destination][1].append(one_two_C_map_ansatz_term_first_Leibniz_case['index_based'][3][1].pop(0))
            if one_two_C_map_ansatz_term_first_Leibniz_case['index_based'][3][2][1]==one_two_C_map_ansatz_term_first_Leibniz_case['index_based'][3][2][0]:
                one_two_C_map_ansatz_term_first_Leibniz_case['coefficient']*=4
            else:
                one_two_C_map_ansatz_term_first_Leibniz_case['index_based']=index_based_element_switch(one_two_C_map_ansatz_term_first_Leibniz_case['index_based'],[one_two_C_map_ansatz_term_first_Leibniz_case['index_based'][3][2][1]],[one_two_C_map_ansatz_term_first_Leibniz_case['index_based'][3][2][0]])
            one_two_C_map_ansatz_term_first_Leibniz_case['index_based'].pop(3)
            one_two_C_map_ansatz_term_first_Leibniz_case['index_based'][0][0]=1
            one_two_C_map_ansatz_term_first_Leibniz_case['index_based']=index_based_reorganize(one_two_C_map_ansatz_term_first_Leibniz_case['index_based'])
            result_operation_C.append(deepcopy(one_two_C_map_ansatz_term_first_Leibniz_case))           

result_intergrated_A=[]
result_intergrated_B=[]
result_intergrated_C=[]

for term in result_operation_B:
    for term in two_two_B_action_integration_by_parts(term):
        if len(term['index_based'][0][1])==2:
            if term['index_based'][0][1][0]==term['index_based'][0][1][1]:
                term['index_based'].pop(0)
                term['index_based'][0][0]=1
                term['index_based'][1][0]=1
                term['index_based']=index_based_reorganize(term['index_based'])
                result_operation_A+=[term]
            else:
                result_intergrated_B+=[term]
        else:
            result_intergrated_B+=[term]

for term in result_operation_C:
    for term in two_two_C_action_integration_by_parts(term):
        if len(term['index_based'][0][1]) == 2:
            if term['index_based'][0][1][0] == term['index_based'][0][1][1]:
                term['index_based'].pop(0)
                term['index_based'] = index_based_reorganize(term['index_based'])
                result_operation_A += [term]
            else:
                result_intergrated_C += [term]
        elif len(term['index_based'][1][1]) == 2:
            if term['index_based'][1][1][0] == term['index_based'][1][1][1]:
                term['index_based'].pop(1)
                term['index_based'] = index_based_reorganize(term['index_based'])
                result_operation_A += [term]
            else:
                result_intergrated_C += [term]
        elif len(term['index_based'][2][1]) == 2:
            if term['index_based'][2][1][0] == term['index_based'][2][1][1]:
                term['index_based'].pop(2)
                term['index_based'] = index_based_reorganize(term['index_based'])
                result_operation_A += [term]
            else:
                result_intergrated_C += [term]
        else:
            result_intergrated_C += [term]
'''
for ab in result_operation_A:
    position=[]
    partial=0
    index=[]
    for abc in ab['index_based']:
        position.append(abc[0])
        partial+=len(abc[1])
        if len(abc)==3:
            if len(abc[2])!=2:
                print('filed_index_problem')
        for abcd in abc[1:]:
            for abcde in abcd:
                index.append(abcde)
    if partial!=2:
        print('partial_problem')
    if sorted(index)!=[1,1]:
        print('index_problem')
    if position!=[1,1]:
        print('cordinate_problem')
'''       
for term in result_operation_A:
    result_intergrated_A+=two_two_A_action_integration_by_parts(term) 

two_two_A_action_class=ansatz.action_class('two_two_A',[[2,1],[2,1]],2)

two_two_A_condition_right=['']*len(two_two_A_action_class)

for term in result_intergrated_A:
    for action_class_index in range(len(two_two_A_action_class)):
        for position_based in two_two_A_action_class[action_class_index]['position_based']:
            if term['position_based']==position_based:
                coefficient=term['coefficient']
                variable=term['id']
                two_two_A_condition_right[action_class_index]+=(f'+({coefficient})*{variable}')
                break

for index,condition in enumerate(two_two_A_condition_right):
    if not condition:
        two_two_A_condition_right[index]="0"

two_two_B_action_class=ansatz.action_class('two_two_B',[[0,1],[2,2],[2,2]],4)

two_two_B_condition_right=['']*len(two_two_B_action_class)

for term in result_intergrated_B:
    for action_class_index in range(len(two_two_B_action_class)):
        for position_based in two_two_B_action_class[action_class_index]['position_based']:
            if term['position_based']==position_based:
                coefficient=term['coefficient']
                variable=term['id']
                two_two_B_condition_right[action_class_index]+=(f'+({coefficient})*{variable}')
                break

for index,condition in enumerate(two_two_B_condition_right):
    if not condition:
        two_two_B_condition_right[index]="0"

two_two_C_action_class=ansatz.action_class('two_two_C',[[0,1],[0,1],[0,1]],4)

two_two_C_condition_right=['']*len(two_two_C_action_class)

for term in result_intergrated_C:
    for action_class_index in range(len(two_two_C_action_class)):
        for position_based in two_two_C_action_class[action_class_index]['position_based']:
            if term['position_based']==position_based:
                coefficient=term['coefficient']
                variable=term['id']
                two_two_C_condition_right[action_class_index]+=(f'+({coefficient})*{variable}')
                break

for index,condition in enumerate(two_two_C_condition_right):
    if not condition:
        two_two_C_condition_right[index]="0"

two_two_condition={}

for index in range(len(two_two_A_action_class)):
    two_two_condition.update({sp.Symbol(two_two_A_action_class[index]['id']):sp.simplify(sp.sympify(two_two_A_condition_right[index]))})
for index in range(len(two_two_B_action_class)):
    two_two_condition.update({sp.Symbol(two_two_B_action_class[index]['id']):sp.simplify(sp.sympify(two_two_B_condition_right[index]))})
for index in range(len(two_two_C_action_class)):
    two_two_condition.update({sp.Symbol(two_two_C_action_class[index]['id']):sp.simplify(sp.sympify(two_two_C_condition_right[index]))})

for left in two_two_C_left:
    for action_class in two_two_C_action_class:
        if position_based_of_(left['index_based']) in action_class['position_based']:
            two_two_condition[sp.Symbol(action_class['id'])]-=sp.sympify(left['coefficient'])

'''
two_two_A_condition_left=['0']*len(two_two_A_action_class)

two_two_B_condition_left=['0']*len(two_two_B_action_class)

two_two_C_condition_left=['0','8','8','4']#ha

two_two_A_condition=[]

for index in range(len(two_two_A_condition_left)):
    two_two_A_condition.append(two_two_A_condition_left[index]+'='+two_two_A_condition_right[index])
    #print(two_two_A_condition[index])

two_two_B_condition=[]

for index in range(len(two_two_B_condition_left)):
    two_two_B_condition.append(two_two_B_condition_left[index]+'='+two_two_B_condition_right[index])
    #print(two_two_B_condition[index])

two_two_C_condition=[]

for index in range(len(two_two_C_condition_left)):
    two_two_C_condition.append(two_two_C_condition_left[index]+'='+two_two_C_condition_right[index])
    #print(two_two_C_condition[index])
'''

    
