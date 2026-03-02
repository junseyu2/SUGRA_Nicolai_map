import ansatz
import linear_algebra
import sympy as sp
from itertools import product
from fractions import Fraction
from copy import deepcopy
import spl
from left import zero_two_A_left

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

for zero_two_A_map_ansatz_term_first in ansatz.map_ansatz('zero_two_A',[[0,0],[1,1],[1,1],[1,1]],2):
    
    zero_two_A_map_ansatz_term_first['coefficient']*=-2*((-1)**len(zero_two_A_map_ansatz_term_first['index_based'][0][1]))

    zero_two_A_map_ansatz_term_first['index_based'][0][0]=1
    
    if zero_two_A_map_ansatz_term_first['eta']==0:

        zero_two_A_map_ansatz_term_first['index_based'][0].append([1,2])

    elif zero_two_A_map_ansatz_term_first['eta']==1:

        zero_two_A_map_ansatz_term_first['index_based'][0].append([5,5])

    result_operation_A.append(deepcopy(zero_two_A_map_ansatz_term_first))

for zero_two_A_map_ansatz_term_second in ansatz.map_ansatz('zero_two_A',[[0,0],[1,1],[1,1],[1,1]],2):
    
    zero_two_A_map_ansatz_term_second['coefficient']*=((-1)**len(zero_two_A_map_ansatz_term_second['index_based'][0][1]))

    zero_two_A_map_ansatz_term_second['index_based'][0][0]=1
    
    if zero_two_A_map_ansatz_term_second['eta']==0:
        
        zero_two_A_map_ansatz_term_second['index_based']=index_based_element_switch (zero_two_A_map_ansatz_term_second['index_based'],[1],[2])
        zero_two_A_map_ansatz_term_second['index_based'][0].append([1,1])

    elif zero_two_A_map_ansatz_term_second['eta']==1:

        zero_two_A_map_ansatz_term_second['index_based'][0].append([5,5])
        zero_two_A_map_ansatz_term_second['coefficient']*=4

    result_operation_A.append(deepcopy(zero_two_A_map_ansatz_term_second))

for zero_two_B_map_ansatz_term_first in ansatz.map_ansatz('zero_two_B',[[0,0],[1,1],[0,2],[1,3],[1,3]],4):
    
    zero_two_B_map_ansatz_term_first['coefficient']*=-2*((-1)**len(zero_two_B_map_ansatz_term_first['index_based'][0][1]))

    zero_two_B_map_ansatz_term_first['index_based'][0][0]=1
    
    if zero_two_B_map_ansatz_term_first['eta']==0:

        zero_two_B_map_ansatz_term_first['index_based'][0].append([1,2])

    elif zero_two_B_map_ansatz_term_first['eta']==1:

        zero_two_B_map_ansatz_term_first['index_based'][0].append([6,6])

    result_operation_B.append(deepcopy(zero_two_B_map_ansatz_term_first))

for zero_two_B_map_ansatz_term_second in ansatz.map_ansatz('zero_two_B',[[0,0],[1,1],[0,2],[1,3],[1,3]],4):
    
    zero_two_B_map_ansatz_term_second['coefficient']*=((-1)**len(zero_two_B_map_ansatz_term_second['index_based'][0][1]))

    zero_two_B_map_ansatz_term_second['index_based'][0][0]=1
    
    if zero_two_B_map_ansatz_term_second['eta']==0:
        
        zero_two_B_map_ansatz_term_second['index_based']=index_based_element_switch (zero_two_B_map_ansatz_term_second['index_based'],[1],[2])
        zero_two_B_map_ansatz_term_second['index_based'][0].append([1,1])

    elif zero_two_B_map_ansatz_term_second['eta']==1:

        zero_two_B_map_ansatz_term_second['index_based'][0].append([6,6])
        zero_two_B_map_ansatz_term_second['coefficient']*=4

    result_operation_B.append(deepcopy(zero_two_B_map_ansatz_term_second))

for zero_one_map_ansatz_term_first in ansatz.map_ansatz('zero_one',[[0,0],[1,1],[1,1]],2):
    for zero_one_map_ansatz_term_second in ansatz.map_ansatz('zero_one',[[0,0],[1,1],[1,1]],2):
        first=deepcopy(zero_one_map_ansatz_term_first)
        second=deepcopy(zero_one_map_ansatz_term_second)
        first_id=first['id']
        second_id=second['id']
        map_product={'id':f"{first_id}*{second_id}",'coefficient':-1,'index_based':[],'position_based':[]}
        first['coefficient']*=(-1)**len(first['index_based'][0][1])
        map_product['coefficient']*=first['coefficient']*second['coefficient']
        first['index_based'][0][0]=2
        first['index_based'][1][0]=1
        first['index_based'][2][0]=1
        second['index_based'][1][0]=3
        second['index_based'][2][0]=3
        if first['eta']==0:
            if second['eta']==0:
                second['index_based']=index_based_element_switch(second['index_based'],[3,4],[5,6])
                map_product['coefficient']*=Fraction(1,2)
                for symmetrization in [[1,2],[2,1]]:
                    first_index_based=deepcopy(first['index_based'])
                    second_index_based=deepcopy(second['index_based'])
                    first_index_based=index_based_element_switch(first_index_based,[1,2],symmetrization)
                    first_index_based[0][1]+=second_index_based[0].pop(1)
                    map_product['index_based']=list(reversed(first_index_based))+second_index_based[1:]
                    result_operation_B.append(deepcopy(map_product))
                continue
            elif second['eta']==1:
                first['index_based']=index_based_element_switch(first['index_based'],[1,2,3,4],[1,1,2,3])
                second['index_based']=index_based_element_switch(second['index_based'],[1,2,3],[4,5,6])
        elif first['eta']==1:
            if second['eta']==0:
                second['index_based']=index_based_element_switch(second['index_based'],[1,2,3,4],[4,4,5,6])
            elif second['eta']==1:
                map_product['coefficient']*=4
                second['index_based']=index_based_element_switch(second['index_based'],[1,2,3],[4,5,6])                
        first['index_based'][0][1]+=second['index_based'][0].pop(1)
        map_product['index_based']=list(reversed(first['index_based']))+second['index_based'][1:]
        result_operation_B.append(deepcopy(map_product))

for zero_one_map_ansatz_term_third in ansatz.map_ansatz('zero_one',[[0,0],[1,1],[1,1]],2):
    for zero_one_map_ansatz_term_fourth in ansatz.map_ansatz('zero_one',[[0,0],[1,1],[1,1]],2):
        third=deepcopy(zero_one_map_ansatz_term_third)
        fourth=deepcopy(zero_one_map_ansatz_term_fourth)
        third_id=third['id']
        fourth_id=fourth['id']
        map_product={'id':f"{third_id}*{fourth_id}",'coefficient':Fraction(1,2),'index_based':[],'position_based':[]}
        third['coefficient']*=(-1)**len(third['index_based'][0][1])
        map_product['coefficient']*=third['coefficient']*fourth['coefficient']
        third['index_based'][0][0]=2
        third['index_based'][1][0]=1
        third['index_based'][2][0]=1
        fourth['index_based'][1][0]=3
        fourth['index_based'][2][0]=3
        if third['eta']==0:
            if fourth['eta']==0:
                third['index_based']=index_based_element_switch(third['index_based'],[1,2,3,4],[1,1,2,3])
                fourth['index_based']=index_based_element_switch(fourth['index_based'],[1,2,3,4],[4,4,5,6])
            elif fourth['eta']==1:
                map_product['coefficient']*=4
                third['index_based']=index_based_element_switch(third['index_based'],[1,2,3,4],[1,1,2,3])
                fourth['index_based']=index_based_element_switch(fourth['index_based'],[1,2,3],[4,5,6])
        elif third['eta']==1:
            if fourth['eta']==0:
                map_product['coefficient']*=4
                fourth['index_based']=index_based_element_switch(fourth['index_based'],[1,2,3,4],[4,4,5,6])
            elif fourth['eta']==1:
                map_product['coefficient']*=16
                fourth['index_based']=index_based_element_switch(fourth['index_based'],[1,2,3],[4,5,6])                
        third['index_based'][0][1]+=fourth['index_based'][0].pop(1)
        map_product['index_based']=list(reversed(third['index_based']))+fourth['index_based'][1:]
        result_operation_B.append(deepcopy(map_product))    

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

zero_two_A_action_class=ansatz.action_class('zero_two_A',[[1,1],[1,1],[1,1],[1,1]],2)

zero_two_B_action_class=ansatz.action_class('zero_two_B',[[1,1],[1,1],[0,2],[1,3],[1,3]],4,symmetry=True)

zero_two_condition={}

for term in result_operation_A:
    for action_class in zero_two_A_action_class:
        for position_based in action_class['position_based']:
            if term['position_based']==position_based:
                coefficient=term['coefficient']
                variable=term['id']
                zero_two_condition[action_class['id']]=zero_two_condition.get(action_class['id'],'')+f'+({coefficient})*{variable}'
                break

for term in result_operation_B:
    for action_class in zero_two_B_action_class:
        for position_based in action_class['position_based']:
            if term['position_based']==position_based:
                coefficient=term['coefficient']
                variable=term['id']
                zero_two_condition[action_class['id']]=zero_two_condition.get(action_class['id'],'')+f'+({coefficient})*{variable}'
                break

zero_two_condition_new={}      

for key,value in zero_two_condition.items():
    expr=sp.Integer(0)
    bucket=[]
    for term in spl._split_top_level_addsub(value):
        bucket.append(sp.expand_mul(sp.sympify(term)))
        if len(bucket) >= 2000:
            expr=sp.Add(expr,sp.Add(*bucket))
            bucket.clear()
    if bucket:
        expr=sp.Add(expr, sp.Add(*bucket))
    zero_two_condition_new.update({sp.Symbol(key):deepcopy(expr)})

zero_two_condition=zero_two_condition_new

#zero_two_condition={sp.Symbol(key):sp.simplify(sp.sympify(value)) for key,value in zero_two_condition.items()}

for left in zero_two_A_left:
    for action_class in zero_two_A_action_class:
        if position_based_of_(left['index_based']) in action_class['position_based']:
            zero_two_condition[sp.Symbol(action_class['id'])]-=sp.sympify(left['coefficient'])

BA_inear_combination=[]

for term in zero_two_B_action_class:
    if len(term['index_based'][2][1])==2:
        if term['index_based'][2][1][0]==term['index_based'][2][1][1]:
            term['index_based'].pop(2)
            term['index_based'][2][0]=1
            term['index_based'][3][0]=1
            for term2 in zero_two_A_action_class:
                if position_based_of_(index_based_reorganize(term['index_based'])) in term2['position_based']:
                    BA_inear_combination.append(sp.sympify(term['id']+'-'+term2['id']))

solution,pivot_variable_list=linear_algebra.gauss_jordan_solution(
    linear_algebra.linear_combination_of_(
    ansatz.action_class('zero_two_A',[[1,1],[1,1],[1,1],[1,1]],2),
    [[0,[2,'+'],[4,'+'],[6,'+']],
     [2,[0,'+'],[4,'+'],[6,'+']],
     [4,[0,'+'],[2,'+'],[6,'+']],
     [6,[0,'+'],[2,'+'],[4,'+']]]
    )
    +
    linear_algebra.linear_combination_of_(
    ansatz.action_class('zero_two_B',[[1,1],[1,1],[0,2],[1,3],[1,3]],4,symmetry=True),
    [[0,[2,'+'],[4,'+']],
     [2,[0,'+'],[4,'+']],
     [4,[0,'+'],[2,'+']],
     [4,[5,'-'],[7,'-']],
     [5,[4,'-'],[7,'+']],
     [7,[4,'-'],[5,'+']]],
    symmetry=True
    )
    +
    BA_inear_combination
    )

for pivot_variable in pivot_variable_list:
    for variable,coefficient in solution[pivot_variable][1].items():
        zero_two_condition[variable]=zero_two_condition.get(variable,sp.Integer(0))+coefficient*(zero_two_condition.get(pivot_variable,sp.Integer(0)))
    zero_two_condition.pop(pivot_variable, None)

#zero_two_A_condition_left=['-2','-1','-2','-4','2','4','1','2','(1/2)+z','4+2*z','(1/2)-z','2-2*z','3','-1*(1/2)+d','-4+2*d','-1*(1/2)-d','-2-2*d','-3','2+e','2+e','6+e','-e','4-e','2-e','4','-3-x','-2-x+y','-4-x-y','(1/2)+x','-1+x+y','-6+x-y','-1-y','-1*(7/2)+y','-1*(1/2)','-1','(1/2)','2','(1/2)','-2','-2','(5/2)','(1/2)','-1*(1/2)']
#zero_two_A_condition_left=['-2','-1','-2','-4','2','4','1','2','(1/2)','4','(1/2)','2','3','-1*(1/2)','-4','-1*(1/2)','-2','-3','2','2','6','0','4','2','4','-3','-2','-4','(1/2)','-1','-6','-1','-1*(7/2)','-1*(1/2)','-1','(1/2)','2','(1/2)','-2','-2','(5/2)','(1/2)','-1*(1/2)']
