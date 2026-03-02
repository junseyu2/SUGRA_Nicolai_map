import ansatz
import sympy as sp
from copy import deepcopy
from itertools import product
from fractions import Fraction
from left import one_one_left

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

def one_one_action_integration_by_parts (one_one_action):

    number_partial_derivative_position=[]
    for element in one_one_action['index_based']:
        number_partial_derivative_position.append(len(element[1]))

    result=[]

    if number_partial_derivative_position==[0,2]:
        index_based_no_class_number=[indices for structure_element in one_one_action['index_based'] for indices in structure_element[1:]]
        position_based=[ [] for _ in range(2)]
        for position in range(len(index_based_no_class_number)):
            for index in index_based_no_class_number[position]:
                position_based[index-1].append(position)   
        one_one_action['position_based']=sorted(position_based)
        result.append(deepcopy(one_one_action))

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

result_operation=[]

condition_variable_index=1

for one_one_map_ansatz_term_first in deepcopy(map_ansatz_one_one):
    
    one_one_map_ansatz_term_first['coefficient']*=-2*((-1)**len(one_one_map_ansatz_term_first['index_based'][0][1]))
    
    if one_one_map_ansatz_term_first['eta']==0:

        one_one_map_ansatz_term_first['index_based'][0].append([1,2])

    elif one_one_map_ansatz_term_first['eta']==1:

        one_one_map_ansatz_term_first['index_based'][0].append([2,2])

    result_operation.append(deepcopy(one_one_map_ansatz_term_first))

for one_one_map_ansatz_term_second in deepcopy(map_ansatz_one_one):
    
    one_one_map_ansatz_term_second['coefficient']*=((-1)**len(one_one_map_ansatz_term_second['index_based'][0][1]))
    
    if one_one_map_ansatz_term_second['eta']==0:
        
        one_one_map_ansatz_term_second['index_based']=index_based_element_switch (one_one_map_ansatz_term_second['index_based'],[1],[2])
        one_one_map_ansatz_term_second['index_based'][0].append([1,1])

    elif one_one_map_ansatz_term_second['eta']==1:

        one_one_map_ansatz_term_second['index_based'][0].append([2,2])
        one_one_map_ansatz_term_second['coefficient']*=4

    result_operation.append(deepcopy(one_one_map_ansatz_term_second))

for zero_one_map_ansatz_term_first in ansatz.map_ansatz('zero_one',[[0,0],[1,1],[1,1]],2):

    zero_one_map_ansatz_term_first['coefficient']*=-1*Fraction(1,2)
    
    if zero_one_map_ansatz_term_first['eta']==0:
        for Leibniz_case in product([0,2],repeat=len(zero_one_map_ansatz_term_first['index_based'][1][1])):
            zero_one_map_ansatz_term_first_Leibniz_case=deepcopy(zero_one_map_ansatz_term_first)
            for destination in Leibniz_case:
                zero_one_map_ansatz_term_first_Leibniz_case['index_based'][destination][1].append(zero_one_map_ansatz_term_first_Leibniz_case['index_based'][1][1].pop(0))
            zero_one_map_ansatz_term_first_Leibniz_case['coefficient']*=(-1)**Leibniz_case.count(2)
            zero_one_map_ansatz_term_first_Leibniz_case['index_based'][1][2]+=[1,2]
            if zero_one_map_ansatz_term_first_Leibniz_case['index_based'][1][2][0]==zero_one_map_ansatz_term_first_Leibniz_case['index_based'][1][2][2]:
                zero_one_map_ansatz_term_first_Leibniz_case['coefficient']*=4
            else:
                zero_one_map_ansatz_term_first_Leibniz_case['index_based']=index_based_element_switch(zero_one_map_ansatz_term_first_Leibniz_case['index_based'],[zero_one_map_ansatz_term_first_Leibniz_case['index_based'][1][2][0]],[zero_one_map_ansatz_term_first_Leibniz_case['index_based'][1][2][2]])
            if zero_one_map_ansatz_term_first_Leibniz_case['index_based'][1][2][1]==zero_one_map_ansatz_term_first_Leibniz_case['index_based'][1][2][3]:
                zero_one_map_ansatz_term_first_Leibniz_case['coefficient']*=4
            else:
                zero_one_map_ansatz_term_first_Leibniz_case['index_based']=index_based_element_switch(zero_one_map_ansatz_term_first_Leibniz_case['index_based'],[zero_one_map_ansatz_term_first_Leibniz_case['index_based'][1][2][1]],[zero_one_map_ansatz_term_first_Leibniz_case['index_based'][1][2][3]])
            zero_one_map_ansatz_term_first_Leibniz_case['index_based'].pop(1)
            zero_one_map_ansatz_term_first_Leibniz_case['index_based'][0][0]=2
            zero_one_map_ansatz_term_first_Leibniz_case['index_based']=list(reversed(index_based_reorganize(zero_one_map_ansatz_term_first_Leibniz_case['index_based'])))
            result_operation.append(deepcopy(zero_one_map_ansatz_term_first_Leibniz_case))
        zero_one_map_ansatz_term_first['index_based']=index_based_element_switch(zero_one_map_ansatz_term_first['index_based'],[1,2],[2,1])
        for Leibniz_case in product([0,2],repeat=len(zero_one_map_ansatz_term_first['index_based'][1][1])):
            zero_one_map_ansatz_term_first_Leibniz_case=deepcopy(zero_one_map_ansatz_term_first)
            for destination in Leibniz_case:
                zero_one_map_ansatz_term_first_Leibniz_case['index_based'][destination][1].append(zero_one_map_ansatz_term_first_Leibniz_case['index_based'][1][1].pop(0))
            zero_one_map_ansatz_term_first_Leibniz_case['coefficient']*=(-1)**Leibniz_case.count(2)
            zero_one_map_ansatz_term_first_Leibniz_case['index_based'][1][2]+=[1,2]
            if zero_one_map_ansatz_term_first_Leibniz_case['index_based'][1][2][0]==zero_one_map_ansatz_term_first_Leibniz_case['index_based'][1][2][2]:
                zero_one_map_ansatz_term_first_Leibniz_case['coefficient']*=4
            else:
                zero_one_map_ansatz_term_first_Leibniz_case['index_based']=index_based_element_switch(zero_one_map_ansatz_term_first_Leibniz_case['index_based'],[zero_one_map_ansatz_term_first_Leibniz_case['index_based'][1][2][0]],[zero_one_map_ansatz_term_first_Leibniz_case['index_based'][1][2][2]])
            if zero_one_map_ansatz_term_first_Leibniz_case['index_based'][1][2][1]==zero_one_map_ansatz_term_first_Leibniz_case['index_based'][1][2][3]:
                zero_one_map_ansatz_term_first_Leibniz_case['coefficient']*=4
            else:
                zero_one_map_ansatz_term_first_Leibniz_case['index_based']=index_based_element_switch(zero_one_map_ansatz_term_first_Leibniz_case['index_based'],[zero_one_map_ansatz_term_first_Leibniz_case['index_based'][1][2][1]],[zero_one_map_ansatz_term_first_Leibniz_case['index_based'][1][2][3]])
            zero_one_map_ansatz_term_first_Leibniz_case['index_based'].pop(1)
            zero_one_map_ansatz_term_first_Leibniz_case['index_based'][0][0]=2
            zero_one_map_ansatz_term_first_Leibniz_case['index_based']=list(reversed(index_based_reorganize(zero_one_map_ansatz_term_first_Leibniz_case['index_based'])))
            result_operation.append(deepcopy(zero_one_map_ansatz_term_first_Leibniz_case))
    elif zero_one_map_ansatz_term_first['eta']==1:
        for Leibniz_case in product([0,2],repeat=len(zero_one_map_ansatz_term_first['index_based'][1][1])):
            zero_one_map_ansatz_term_first_Leibniz_case=deepcopy(zero_one_map_ansatz_term_first)
            zero_one_map_ansatz_term_first_Leibniz_case['coefficient']*=2
            for destination in Leibniz_case:
                zero_one_map_ansatz_term_first_Leibniz_case['index_based'][destination][1].append(zero_one_map_ansatz_term_first_Leibniz_case['index_based'][1][1].pop(0))
            zero_one_map_ansatz_term_first_Leibniz_case['coefficient']*=(-1)**Leibniz_case.count(2)
            if zero_one_map_ansatz_term_first_Leibniz_case['index_based'][1][2][1]==zero_one_map_ansatz_term_first_Leibniz_case['index_based'][1][2][0]:
                zero_one_map_ansatz_term_first_Leibniz_case['coefficient']*=4
            else:
                zero_one_map_ansatz_term_first_Leibniz_case['index_based']=index_based_element_switch(zero_one_map_ansatz_term_first_Leibniz_case['index_based'],[zero_one_map_ansatz_term_first_Leibniz_case['index_based'][1][2][1]],[zero_one_map_ansatz_term_first_Leibniz_case['index_based'][1][2][0]])
            zero_one_map_ansatz_term_first_Leibniz_case['index_based'].pop(1)
            zero_one_map_ansatz_term_first_Leibniz_case['index_based'][0][0]=2
            zero_one_map_ansatz_term_first_Leibniz_case['index_based']=list(reversed(index_based_reorganize(zero_one_map_ansatz_term_first_Leibniz_case['index_based'])))
            result_operation.append(deepcopy(zero_one_map_ansatz_term_first_Leibniz_case))

for zero_one_map_ansatz_term_second in ansatz.map_ansatz('zero_one',[[0,0],[1,1],[1,1]],2):

    zero_one_map_ansatz_term_second['coefficient']*=-1*Fraction(1,2)
    
    if zero_one_map_ansatz_term_second['eta']==0:
        for Leibniz_case in product([0,1],repeat=len(zero_one_map_ansatz_term_second['index_based'][2][1])):
            zero_one_map_ansatz_term_second_Leibniz_case=deepcopy(zero_one_map_ansatz_term_second)
            for destination in Leibniz_case:
                zero_one_map_ansatz_term_second_Leibniz_case['index_based'][destination][1].append(zero_one_map_ansatz_term_second_Leibniz_case['index_based'][2][1].pop(0))
            zero_one_map_ansatz_term_second_Leibniz_case['coefficient']*=(-1)**Leibniz_case.count(2)
            zero_one_map_ansatz_term_second_Leibniz_case['index_based'][2][2]+=[1,2]
            if zero_one_map_ansatz_term_second_Leibniz_case['index_based'][2][2][0]==zero_one_map_ansatz_term_second_Leibniz_case['index_based'][2][2][2]:
                zero_one_map_ansatz_term_second_Leibniz_case['coefficient']*=4
            else:
                zero_one_map_ansatz_term_second_Leibniz_case['index_based']=index_based_element_switch(zero_one_map_ansatz_term_second_Leibniz_case['index_based'],[zero_one_map_ansatz_term_second_Leibniz_case['index_based'][2][2][0]],[zero_one_map_ansatz_term_second_Leibniz_case['index_based'][2][2][2]])
            if zero_one_map_ansatz_term_second_Leibniz_case['index_based'][2][2][1]==zero_one_map_ansatz_term_second_Leibniz_case['index_based'][2][2][3]:
                zero_one_map_ansatz_term_second_Leibniz_case['coefficient']*=4
            else:
                zero_one_map_ansatz_term_second_Leibniz_case['index_based']=index_based_element_switch(zero_one_map_ansatz_term_second_Leibniz_case['index_based'],[zero_one_map_ansatz_term_second_Leibniz_case['index_based'][2][2][1]],[zero_one_map_ansatz_term_second_Leibniz_case['index_based'][2][2][3]])
            zero_one_map_ansatz_term_second_Leibniz_case['index_based'].pop(2)
            zero_one_map_ansatz_term_second_Leibniz_case['index_based'][0][0]=2
            zero_one_map_ansatz_term_second_Leibniz_case['index_based']=list(reversed(index_based_reorganize(zero_one_map_ansatz_term_second_Leibniz_case['index_based'])))
            result_operation.append(deepcopy(zero_one_map_ansatz_term_second_Leibniz_case))
        zero_one_map_ansatz_term_second['index_based']=index_based_element_switch(zero_one_map_ansatz_term_second['index_based'],[1,2],[2,1])
        for Leibniz_case in product([0,1],repeat=len(zero_one_map_ansatz_term_second['index_based'][2][1])):
            zero_one_map_ansatz_term_second_Leibniz_case=deepcopy(zero_one_map_ansatz_term_second)
            for destination in Leibniz_case:
                zero_one_map_ansatz_term_second_Leibniz_case['index_based'][destination][1].append(zero_one_map_ansatz_term_second_Leibniz_case['index_based'][2][1].pop(0))
            zero_one_map_ansatz_term_second_Leibniz_case['coefficient']*=(-1)**Leibniz_case.count(2)
            zero_one_map_ansatz_term_second_Leibniz_case['index_based'][2][2]+=[1,2]
            if zero_one_map_ansatz_term_second_Leibniz_case['index_based'][2][2][0]==zero_one_map_ansatz_term_second_Leibniz_case['index_based'][2][2][2]:
                zero_one_map_ansatz_term_second_Leibniz_case['coefficient']*=4
            else:
                zero_one_map_ansatz_term_second_Leibniz_case['index_based']=index_based_element_switch(zero_one_map_ansatz_term_second_Leibniz_case['index_based'],[zero_one_map_ansatz_term_second_Leibniz_case['index_based'][2][2][0]],[zero_one_map_ansatz_term_second_Leibniz_case['index_based'][2][2][2]])
            if zero_one_map_ansatz_term_second_Leibniz_case['index_based'][2][2][1]==zero_one_map_ansatz_term_second_Leibniz_case['index_based'][2][2][3]:
                zero_one_map_ansatz_term_second_Leibniz_case['coefficient']*=4
            else:
                zero_one_map_ansatz_term_second_Leibniz_case['index_based']=index_based_element_switch(zero_one_map_ansatz_term_second_Leibniz_case['index_based'],[zero_one_map_ansatz_term_second_Leibniz_case['index_based'][2][2][1]],[zero_one_map_ansatz_term_second_Leibniz_case['index_based'][2][2][3]])
            zero_one_map_ansatz_term_second_Leibniz_case['index_based'].pop(2)
            zero_one_map_ansatz_term_second_Leibniz_case['index_based'][0][0]=2
            zero_one_map_ansatz_term_second_Leibniz_case['index_based']=list(reversed(index_based_reorganize(zero_one_map_ansatz_term_second_Leibniz_case['index_based'])))
            result_operation.append(deepcopy(zero_one_map_ansatz_term_second_Leibniz_case))
    elif zero_one_map_ansatz_term_second['eta']==1:
        for Leibniz_case in product([0,1],repeat=len(zero_one_map_ansatz_term_second['index_based'][2][1])):
            zero_one_map_ansatz_term_second_Leibniz_case=deepcopy(zero_one_map_ansatz_term_second)
            zero_one_map_ansatz_term_second_Leibniz_case['coefficient']*=2
            for destination in Leibniz_case:
                zero_one_map_ansatz_term_second_Leibniz_case['index_based'][destination][1].append(zero_one_map_ansatz_term_second_Leibniz_case['index_based'][2][1].pop(0))
            zero_one_map_ansatz_term_second_Leibniz_case['coefficient']*=(-1)**Leibniz_case.count(2)
            if zero_one_map_ansatz_term_second_Leibniz_case['index_based'][2][2][1]==zero_one_map_ansatz_term_second_Leibniz_case['index_based'][2][2][0]:
                zero_one_map_ansatz_term_second_Leibniz_case['coefficient']*=4
            else:
                zero_one_map_ansatz_term_second_Leibniz_case['index_based']=index_based_element_switch(zero_one_map_ansatz_term_second_Leibniz_case['index_based'],[zero_one_map_ansatz_term_second_Leibniz_case['index_based'][2][2][1]],[zero_one_map_ansatz_term_second_Leibniz_case['index_based'][2][2][0]])
            zero_one_map_ansatz_term_second_Leibniz_case['index_based'].pop(2)
            zero_one_map_ansatz_term_second_Leibniz_case['index_based'][0][0]=2
            zero_one_map_ansatz_term_second_Leibniz_case['index_based']=list(reversed(index_based_reorganize(zero_one_map_ansatz_term_second_Leibniz_case['index_based'])))
            result_operation.append(deepcopy(zero_one_map_ansatz_term_second_Leibniz_case))
    
result_intergrated=[]

for term in result_operation:
    result_intergrated+=one_one_action_integration_by_parts(term)

one_one_action_class=ansatz.action_class('one_one',[[1,1],[2,2]],2)

one_one_condition_right=['']*len(one_one_action_class)

for term in result_intergrated:
    for action_class_index in range(len(one_one_action_class)):
        for position_based in one_one_action_class[action_class_index]['position_based']:
            if term['position_based']==position_based:
                coefficient=term['coefficient']
                variable=term['id']
                one_one_condition_right[action_class_index]+=(f'+({coefficient})*{variable}')
                break

for index,condition in enumerate(one_one_condition_right):
    if not condition:
        one_one_condition_right[index]="0"

for index in range(len(one_one_action_class)):
    one_one_condition_right[index]+="-action_"+one_one_action_class[index]['id']

one_one_condition={}

for index in range(len(one_one_condition_right)):
    one_one_condition.update({sp.Symbol(one_one_action_class[index]['id']):sp.simplify(sp.sympify(one_one_condition_right[index]))})

'''
one_one_condition_left=['-4','-1']

one_one_condition=[]

for index in range(len(one_one_condition_left)):
    one_one_condition.append(one_one_condition_left[index]+'='+one_one_condition_right[index])
'''
