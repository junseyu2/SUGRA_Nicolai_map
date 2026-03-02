import ansatz
import linear_algebra
import sympy as sp
from itertools import product
from copy import deepcopy
from left import zero_one_left

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

def position_based_of_(index_based):
    index_based_no_class_number=[indices for structure_element in index_based for indices in structure_element[1:]]
    position_based=[ [] for _ in range(len(set(index for element in index_based_no_class_number for index in element)))]
    for position in range(len(index_based_no_class_number)):
        for index in index_based_no_class_number[position]:
            position_based[index-1].append(position)   
    return sorted(position_based)

result_operation=[]

for zero_one_map_ansatz_term_first in ansatz.map_ansatz('zero_one',[[0,0],[1,1],[1,1]],2):
    
    zero_one_map_ansatz_term_first['coefficient']*=-2*((-1)**len(zero_one_map_ansatz_term_first['index_based'][0][1]))

    zero_one_map_ansatz_term_first['index_based'][0][0]=1
    
    if zero_one_map_ansatz_term_first['eta']==0:

        zero_one_map_ansatz_term_first['index_based'][0].append([1,2])

    elif zero_one_map_ansatz_term_first['eta']==1:

        zero_one_map_ansatz_term_first['index_based'][0].append([4,4])

    result_operation.append(deepcopy(zero_one_map_ansatz_term_first))

for zero_one_map_ansatz_term_second in ansatz.map_ansatz('zero_one',[[0,0],[1,1],[1,1]],2):
    
    zero_one_map_ansatz_term_second['coefficient']*=((-1)**len(zero_one_map_ansatz_term_second['index_based'][0][1]))

    zero_one_map_ansatz_term_second['index_based'][0][0]=1
    
    if zero_one_map_ansatz_term_second['eta']==0:
        
        zero_one_map_ansatz_term_second['index_based']=index_based_element_switch (zero_one_map_ansatz_term_second['index_based'],[1],[2])
        zero_one_map_ansatz_term_second['index_based'][0].append([1,1])

    elif zero_one_map_ansatz_term_second['eta']==1:

        zero_one_map_ansatz_term_second['index_based'][0].append([4,4])
        zero_one_map_ansatz_term_second['coefficient']*=4

    result_operation.append(deepcopy(zero_one_map_ansatz_term_second))

for index, term in enumerate(result_operation):
    result_operation[index]['position_based']=position_based_of_(term['index_based'])
    '''
    print(result_operation[index])
    '''
zero_one_action_class=ansatz.action_class('zero_one',[[1,1],[1,1],[1,1]],2)

zero_one_condition={}

for term in result_operation:
    for action_class in zero_one_action_class:
        for position_based in action_class['position_based']:
            if term['position_based']==position_based:
                coefficient=term['coefficient']
                variable=term['id']
                zero_one_condition[action_class['id']]=zero_one_condition.get(action_class['id'],'')+f'+({coefficient})*{variable}'
                break

zero_one_condition={sp.Symbol(key):sp.simplify(sp.sympify(value)) for key,value in zero_one_condition.items()}

for left in zero_one_left:
    for action_class in zero_one_action_class:
        if position_based_of_(left['index_based']) in action_class['position_based']:
            zero_one_condition[sp.Symbol(action_class['id'])]-=sp.sympify(left['coefficient'])

#zero_one_condition_left=['-2','-2','2','2','-1+a','-4+a','-1-a','-2-a','2+b','2+b','-b','4-b','1','2','-2','-1']
#zero_one_condition_left=['-2','-2','2','2','-1','-4','-1','-2','2','2','0','4','1','2','-2','-1']            

solution,pivot_variable_list=linear_algebra.gauss_jordan_solution(linear_algebra.linear_combination_of_(
    ansatz.action_class('zero_one',[[1,1],[1,1],[1,1]],2),
    [[0,[2,'+'],[4,'+']],
     [2,[0,'+'],[4,'+']],
     [4,[0,'+'],[2,'+']]]
    ))

for pivot_variable in pivot_variable_list:
    for variable,coefficient in solution[pivot_variable][1].items():
        zero_one_condition[variable]+=coefficient*zero_one_condition[pivot_variable]
    del zero_one_condition[pivot_variable]

