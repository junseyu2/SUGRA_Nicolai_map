from itertools import combinations
from itertools import permutations
from itertools import product
from collections import Counter
from copy import deepcopy

def choose_possible_n_rest (lst, n):

    contrast_list = set()
    results = []

    for combination in combinations(range(len(lst)), n):
        choose_value = [lst[index] for index in combination]
        choose_n = tuple(sorted(choose_value))
        if choose_n in contrast_list:
            continue
        contrast_list.add(choose_n)

        combination_set = set(combination)
        rest = [value for index, value in enumerate(lst) if index not in combination_set]

        results.append([list(choose_n), rest])
        
    return results

def double_list_element_switch (double_list, old_elements, new_elements):
    
    mapping = dict(zip(old_elements, new_elements))
    
    result = []
    for sublist in double_list:
        new_sublist = []
        for element in sublist:
            if element in mapping:
                new_sublist.append(mapping[element])
            else:
                new_sublist.append(element)
        result.append(new_sublist)
    
    return result

def list_position_switch (lst, old_positions, new_positions):
    
    mapping = dict(zip(old_positions, new_positions))
    
    result = lst[:]

    for old_position, new_position in mapping.items():
        result[new_position] = lst[old_position]

    return result

def map_ansatz (ansatz_name,ansatz_structure,number_partial_derivative):

    def pairing(lst):

        if len(lst)==0:
            return [[]]
        
        if len(lst)==2:
            return [[lst]]

        result=[]

        first_element_number=lst.count(lst[0])

        for first_element_pair_number in range(first_element_number//2+1):
            result_head=[[lst[0],lst[0]]]*first_element_pair_number
            for choose, rest in choose_possible_n_rest (lst[first_element_number:], first_element_number-2*first_element_pair_number):
                result_middle=[]
                for index in choose:
                    result_middle.append([lst[0],index])
                for pairs in pairing(rest):
                    result.append(result_head+result_middle+pairs)

        '''

        if len(lst)==0:
            return [[]]
        
        if len(lst)==2:
            return [[lst]]
            
        paring_seed=lst.pop(0)
        result=[]
        for choose, rest in choose_possible_n_rest (lst, 1):
            result_seed=[paring_seed,*choose]
            for pairs in paring(rest):
                result.append([result_seed]+pairs)

        '''
                
        return result

    derivative_arrangement_list=list(product(range(len(ansatz_structure)),repeat=number_partial_derivative))
    
    if ansatz_structure[-1][0]==0:
        
        propagator_class_size=Counter([structure_element[1] for structure_element in ansatz_structure if structure_element[0]==0])
        propagator_class_size=list(propagator_class_size.values())
        minus_number_single_propagator=-1*propagator_class_size[-1]
        
        for propagator_field_position in range(len(ansatz_structure)-propagator_class_size[-1],len(ansatz_structure)):
            derivative_arrangement_list=[derivative_arrangement for derivative_arrangement in derivative_arrangement_list if derivative_arrangement.count(propagator_field_position) % 2 == 0]
    else:
        minus_number_single_propagator=None

    number_field=len([structure_element[1] for structure_element in ansatz_structure if structure_element[0]==1])
    
    position_based_eta_no_index_assignment_list=[]

    # mu : 0 nu : 0

    for pairs in pairing([0]*(number_partial_derivative-2)+[position for position in range(1,number_field+1) for _ in (0, 1)]):
        position_based_eta_no_index_assignment_list.append([[0,0]]+pairs)

    # mu : 0 nu : x

    for x, rest in choose_possible_n_rest([position for position in range(1,number_field+1) for _ in (0, 1)],1):
        for pairs in pairing([0]*(number_partial_derivative-1)+rest):
            position_based_eta_no_index_assignment_list.append([[0,*x]]+pairs)     

    # mu : x nu : x

    for x, rest in choose_possible_n_rest([position for position in range(1,number_field+1) for _ in (0, 1)],2):
        for pairs in pairing([0]*number_partial_derivative+rest):
            position_based_eta_no_index_assignment_list.append([x]+pairs)

    position_based_eta_yes_index_assignment_list=pairing([0]*number_partial_derivative+[position for position in range(1,number_field+1) for _ in (0, 1)])

    #position_based_eta_no_index_assignment_list=[[sorted(cd) for cd in ab] for ab in  position_based_eta_no_index_assignment_list]
    #position_based_eta_no_index_assignment_list=[ [ab[0]]+sorted(ab[1:]) for ab in position_based_eta_no_index_assignment_list]
    #position_based_eta_yes_index_assignment_list=[sorted([cd for cd in ab]) for ab in  position_based_eta_yes_index_assignment_list]
        
    field_class_size=Counter([structure_element[1] for structure_element in ansatz_structure if structure_element[0]==1])
    field_class_size=list(field_class_size.values())

    field_position_index_list=[index for index in range(1,sum(field_class_size)+1) for _ in range(2)]

    class_start_index=1
    field_position_index_split_list=[]
    for size in field_class_size:
        field_position_index_split_list.append(range(class_start_index,class_start_index+size))
        class_start_index=class_start_index+size

    possible_split_field_position_index_arrangement_list_list=[permutations(field_position_indexs) for field_position_indexs in field_position_index_split_list]
    
    possible_field_position_index_arrangement_list=[]
    
    for split_field_position_indexs in product(*possible_split_field_position_index_arrangement_list_list):
        possible_field_position_index_arrangement_list.append([position_index for split in split_field_position_indexs for position_index in split])

    assignment_index=0
    index_based_eta_no_index_assignment_list=[]
    
    for position_based_eta_no_index_assignment in position_based_eta_no_index_assignment_list:
        for field_position_index_arrangement in possible_field_position_index_arrangement_list:
            position_based_eta_no_index_assignment_switched=double_list_element_switch(position_based_eta_no_index_assignment,range(1,number_field+1),field_position_index_arrangement)
            position_based_eta_no_index_assignment_switched_sorted=[sorted(sublist) for sublist in position_based_eta_no_index_assignment_switched]
            position_based_eta_no_index_assignment_switched_sorted[1:]=sorted(position_based_eta_no_index_assignment_switched_sorted[1:])
            next_index = assignment_index + 1
            while next_index < len(position_based_eta_no_index_assignment_list):
                if position_based_eta_no_index_assignment_list[next_index] == position_based_eta_no_index_assignment_switched_sorted:
                    del position_based_eta_no_index_assignment_list[next_index]
                else:
                     next_index += 1
        index_based_eta_no_index_assignment=[[]for _ in range(number_field+1)]
        index_based_eta_no_index_assignment[position_based_eta_no_index_assignment[0][0]].append(1)
        index_based_eta_no_index_assignment[position_based_eta_no_index_assignment[0][1]].append(2)
        for index in range(1,number_field+number_partial_derivative//2):
            for position in position_based_eta_no_index_assignment[index]:
                index_based_eta_no_index_assignment[position].append(index+2)
        index_based_eta_no_index_assignment_list.append(index_based_eta_no_index_assignment)
        assignment_index+=1        

    assignment_index=0
    index_based_eta_yes_index_assignment_list=[]
    
    for position_based_eta_yes_index_assignment in position_based_eta_yes_index_assignment_list:
        for field_position_index_arrangement in possible_field_position_index_arrangement_list:
            position_based_eta_yes_index_assignment_switched=double_list_element_switch(position_based_eta_yes_index_assignment,range(1,number_field+1),field_position_index_arrangement)
            position_based_eta_yes_index_assignment_switched_sorted=[sorted(sublist) for sublist in position_based_eta_yes_index_assignment_switched]
            position_based_eta_yes_index_assignment_switched_sorted=sorted(position_based_eta_yes_index_assignment_switched_sorted)
            next_index = assignment_index + 1
            while next_index < len(position_based_eta_yes_index_assignment_list):
                if position_based_eta_yes_index_assignment_list[next_index] == position_based_eta_yes_index_assignment_switched_sorted:
                    del position_based_eta_yes_index_assignment_list[next_index]
                else:
                    next_index += 1
        index_based_eta_yes_index_assignment=[[]for _ in range(number_field+1)]
        for index in range(number_field+number_partial_derivative//2):
            for position in position_based_eta_yes_index_assignment[index]:
                index_based_eta_yes_index_assignment[position].append(index+1)
        index_based_eta_yes_index_assignment_list.append(index_based_eta_yes_index_assignment)
        assignment_index+=1

    class_size=Counter([structure_element[1] for structure_element in ansatz_structure])
    class_size=list(class_size.values())

    class_start_position=0
    class_position_split_list=[]
    for size in class_size:
        class_position_split_list.append(range(class_start_position,class_start_position+size))
        class_start_position=class_start_position+size

    possible_split_class_position_arrangement_list_list=[permutations(class_positions) for class_positions in class_position_split_list]
    
    possible_position_arrangement_list=[]
    
    for split_class_position_arrangement in product(*possible_split_class_position_arrangement_list_list):
        possible_position_arrangement_list.append([position for split_class in split_class_position_arrangement for position in split_class])

    result=[]
    
    for index_based_eta_no_index_assignment_index in range(len(index_based_eta_no_index_assignment_list)):
        index_based_eta_no_index_assignment_class=[]
        for derivative_arrangement_index in range(len(derivative_arrangement_list)):
            ansatz_term={'id':f"{ansatz_name}_{derivative_arrangement_index+1}_{index_based_eta_no_index_assignment_index+1}",'coefficient':1,'eta':0,'index_based':[],'position_based':[]}
            index_based=[[] for _ in range(len(ansatz_structure))]
            field_position=1
            for position in range(len(ansatz_structure)):
                index_based[position]+=[ansatz_structure[position][1],[]]
                if ansatz_structure[position][0]==1:
                    index_based[position].append(index_based_eta_no_index_assignment_list[index_based_eta_no_index_assignment_index][field_position])
                    field_position+=1
            for partial_derivative_order in range(number_partial_derivative):
                index_based[derivative_arrangement_list[derivative_arrangement_index][partial_derivative_order]][1].append(index_based_eta_no_index_assignment_list[index_based_eta_no_index_assignment_index][0][partial_derivative_order])
            index_based_no_class_number=[indices for structure_element in index_based for indices in structure_element[1:]]
            position_based=[ [] for _ in range((number_partial_derivative+2*number_field)//2)]
            for position in range(len(index_based_no_class_number)):
                for index in index_based_no_class_number[position]:
                    if index==1 or index==2:
                        position_based[0].append(position)
                    else:
                        position_based[index-2].append(position)
            position_based[1:]=sorted(position_based[1:])
            ansatz_term['index_based']=index_based
            ansatz_term['position_based']=position_based
            index_based_eta_no_index_assignment_class.append(ansatz_term)

        ansatz_term_index=0
        for ansatz_term in index_based_eta_no_index_assignment_class:
            for position_arrangement in possible_position_arrangement_list:
                index_based_switched=list_position_switch (ansatz_term['index_based'], range(len(ansatz_structure)), position_arrangement)
                index_based_switched_no_class_number=[indices for structure_element in index_based_switched for indices in structure_element[1:]]
                position_based_switched=[ [] for _ in range((number_partial_derivative+2*number_field)//2)]
                for position in range(len(index_based_switched_no_class_number)):
                    for index in index_based_switched_no_class_number[position]:
                        if index==1 or index==2:
                            position_based_switched[0].append(position)
                        else:
                            position_based_switched[index-2].append(position)
                position_based_switched[1:]=sorted(position_based_switched[1:])
                next_index = ansatz_term_index + 1
                while next_index < len(index_based_eta_no_index_assignment_class):
                    if index_based_eta_no_index_assignment_class[next_index]['position_based'] == position_based_switched:
                        del index_based_eta_no_index_assignment_class[next_index]
                    else:
                        next_index += 1
            ansatz_term_index += 1
        result+=index_based_eta_no_index_assignment_class

    for index_based_eta_yes_index_assignment_index in range(len(index_based_eta_yes_index_assignment_list)):
        index_based_eta_yes_index_assignment_class=[]
        for derivative_arrangement_index in range(len(derivative_arrangement_list)):
            ansatz_term={'id':f"{ansatz_name}_{derivative_arrangement_index+1}_{index_based_eta_yes_index_assignment_index+len(index_based_eta_no_index_assignment_list)+1}",'coefficient':1,'eta':1,'index_based':[],'position_based':[]}
            index_based=[[] for _ in range(len(ansatz_structure))]
            field_position=1
            for position in range(len(ansatz_structure)):
                index_based[position]+=[ansatz_structure[position][1],[]]
                if ansatz_structure[position][0]==1:
                    index_based[position].append(index_based_eta_yes_index_assignment_list[index_based_eta_yes_index_assignment_index][field_position])
                    field_position+=1
            for partial_derivative_order in range(number_partial_derivative):
                index_based[derivative_arrangement_list[derivative_arrangement_index][partial_derivative_order]][1].append(index_based_eta_yes_index_assignment_list[index_based_eta_yes_index_assignment_index][0][partial_derivative_order])
            index_based_no_class_number=[indices for structure_element in index_based for indices in structure_element[1:]]
            position_based=[ [] for _ in range((number_partial_derivative+2*number_field)//2)]
            for position in range(len(index_based_no_class_number)):
                for index in index_based_no_class_number[position]:
                    position_based[index-1].append(position)                        
            position_based=sorted(position_based)
            ansatz_term['index_based']=index_based
            ansatz_term['position_based']=position_based
            index_based_eta_yes_index_assignment_class.append(ansatz_term)

        ansatz_term_index=0
        for ansatz_term in index_based_eta_yes_index_assignment_class:
            for position_arrangement in possible_position_arrangement_list:
                index_based_switched=list_position_switch (ansatz_term['index_based'], range(len(ansatz_structure)), position_arrangement)
                index_based_switched_no_class_number=[indices for structure_element in index_based_switched for indices in structure_element[1:]]
                position_based_switched=[ [] for _ in range((number_partial_derivative+2*number_field)//2)]
                for position in range(len(index_based_switched_no_class_number)):
                    for index in index_based_switched_no_class_number[position]:
                        position_based_switched[index-1].append(position)   
                position_based_switched=sorted(position_based_switched)
                next_index = ansatz_term_index + 1
                while next_index < len(index_based_eta_yes_index_assignment_class):
                    if index_based_eta_yes_index_assignment_class[next_index]['position_based'] == position_based_switched:
                        del index_based_eta_yes_index_assignment_class[next_index]
                    else:
                        next_index+= 1
            ansatz_term_index+= 1
        result+=index_based_eta_yes_index_assignment_class

    result_index=0
    while result_index < len(result):
        for element in result[result_index]['index_based'][1:minus_number_single_propagator]:
            if (len(element)==2 and len(element[1])==2 and element[1][0]==element[1][1]):
                del result[result_index]
                result_index-=1
                break
        result_index+=1

    print(len(result))

    return result

def action_class (class_name,class_structure,number_partial_derivative,symmetry=False):

    def pairing(lst):

        if len(lst)==0:
            return [[]]
        
        if len(lst)==2:
            return [[lst]]

        result=[]

        first_element_number=lst.count(lst[0])

        for first_element_pair_number in range(first_element_number//2+1):
            result_head=[[lst[0],lst[0]]]*first_element_pair_number
            for choose, rest in choose_possible_n_rest (lst[first_element_number:], first_element_number-2*first_element_pair_number):
                result_middle=[]
                for index in choose:
                    result_middle.append([lst[0],index])
                for pairs in pairing(rest):
                    result.append(result_head+result_middle+pairs)
                    
        return result

    derivative_arrangement_list=list(product(range(len(class_structure)),repeat=number_partial_derivative))
    '''
    for derivative_arrangement in list(product(range(len(class_structure)),repeat=number_partial_derivative)):
        derivative_arrangement_list.append(derivative_arrangement)
    '''
    
    if class_structure[-1][0]==2:

        number_single_propagator_loop=len([structure_element[1] for structure_element in class_structure if structure_element[0]==2])
        minus_number_single_propagator_loop=-1*number_single_propagator_loop
        
        for single_propagator_loop_reverse_position in range(number_single_propagator_loop):
            class_structure[-1*(single_propagator_loop_reverse_position+1)][0]=0
        
        for single_propagator_loop_position in range(len(class_structure)-number_single_propagator_loop,len(class_structure)):
            derivative_arrangement_list=[derivative_arrangement for derivative_arrangement in derivative_arrangement_list if derivative_arrangement.count(single_propagator_loop_position) % 2 == 0]
    else:
        minus_number_single_propagator_loop=None

    number_field=len([structure_element[1] for structure_element in class_structure if structure_element[0]==1])

    position_based_index_assignment_list=pairing([0]*number_partial_derivative+[position for position in range(1,number_field+1) for _ in (0, 1)])

    field_class_size=Counter([structure_element[1] for structure_element in class_structure if structure_element[0]==1])
    field_class_size=list(field_class_size.values())

    field_position_index_list=[index for index in range(1,sum(field_class_size)+1) for _ in range(2)]

    class_start_index=1
    field_position_index_split_list=[]
    for size in field_class_size:
        field_position_index_split_list.append(range(class_start_index,class_start_index+size))
        class_start_index=class_start_index+size

    possible_split_field_position_index_arrangement_list_list=[permutations(field_position_indexs) for field_position_indexs in field_position_index_split_list]
    
    possible_field_position_index_arrangement_list=[]
    
    for split_field_position_indexs in product(*possible_split_field_position_index_arrangement_list_list):
        possible_field_position_index_arrangement_list.append([position_index for split in split_field_position_indexs for position_index in split])

    if symmetry:
        possible_reverse_field_position_index_arrangement_list=[]
        for field_position_index_arrangement in possible_field_position_index_arrangement_list:
            possible_reverse_field_position_index_arrangement_list.append(list(reversed(field_position_index_arrangement)))
        possible_field_position_index_arrangement_list+=possible_reverse_field_position_index_arrangement_list
            

    assignment_index=0
    index_based_index_assignment_list=[]
    
    for position_based_index_assignment in position_based_index_assignment_list:
        for field_position_index_arrangement in possible_field_position_index_arrangement_list:
            position_based_index_assignment_switched=double_list_element_switch(position_based_index_assignment,range(1,number_field+1),field_position_index_arrangement)
            position_based_index_assignment_switched_sorted=[sorted(sublist) for sublist in position_based_index_assignment_switched]
            position_based_index_assignment_switched_sorted=sorted(position_based_index_assignment_switched_sorted)
            next_index = assignment_index + 1
            while next_index < len(position_based_index_assignment_list):
                if position_based_index_assignment_list[next_index] == position_based_index_assignment_switched_sorted:
                    del position_based_index_assignment_list[next_index]
                else:
                    next_index += 1
        index_based_index_assignment=[[]for _ in range(number_field+1)]
        for index in range(number_field+number_partial_derivative//2):
            for position in position_based_index_assignment[index]:
                index_based_index_assignment[position].append(index+1)
        index_based_index_assignment_list.append(index_based_index_assignment)
        assignment_index+=1

    class_size=Counter([structure_element[1] for structure_element in class_structure])
    class_size=list(class_size.values())

    class_start_position=0
    class_position_split_list=[]
    for size in class_size:
        class_position_split_list.append(range(class_start_position,class_start_position+size))
        class_start_position=class_start_position+size

    possible_split_class_position_arrangement_list_list=[permutations(class_positions) for class_positions in class_position_split_list]
    
    possible_position_arrangement_list=[]
    
    for split_class_position_arrangement in product(*possible_split_class_position_arrangement_list_list):
        possible_position_arrangement_list.append([position for split_class in split_class_position_arrangement for position in split_class])

    if symmetry:
        possible_reverse_position_arrangement_list=[]
        for position_arrangement in possible_position_arrangement_list:
            possible_reverse_position_arrangement_list.append(list(reversed(position_arrangement)))
        possible_position_arrangement_list+=possible_reverse_position_arrangement_list

    result=[]

    for index_based_index_assignment_index in range(len(index_based_index_assignment_list)):
        index_based_index_assignment_class=[]
        for derivative_arrangement_index in range(len(derivative_arrangement_list)):
            term={'id':f"{class_name}_{derivative_arrangement_index+1}_{index_based_index_assignment_index+1}",'index_based':[],'position_based':[]}
            index_based=[[] for _ in range(len(class_structure))]
            field_position=1
            for position in range(len(class_structure)):
                index_based[position]+=[class_structure[position][1],[]]
                if class_structure[position][0]==1:
                    index_based[position].append(index_based_index_assignment_list[index_based_index_assignment_index][field_position])
                    field_position+=1
            for partial_derivative_order in range(number_partial_derivative):
                index_based[derivative_arrangement_list[derivative_arrangement_index][partial_derivative_order]][1].append(index_based_index_assignment_list[index_based_index_assignment_index][0][partial_derivative_order])
            for position_arrangement in possible_position_arrangement_list:
                index_based_switched=list_position_switch (index_based, range(len(class_structure)), position_arrangement)
                index_based_switched_no_class_number=[indices for structure_element in index_based_switched for indices in structure_element[1:]]
                position_based_switched=[ [] for _ in range((number_partial_derivative+2*number_field)//2)]
                for position in range(len(index_based_switched_no_class_number)):
                    for index in index_based_switched_no_class_number[position]:
                        position_based_switched[index-1].append(position)   
                position_based_switched=sorted(position_based_switched)
                term['position_based'].append(deepcopy(position_based_switched))
            term['index_based']=index_based
            index_based_index_assignment_class.append(term)

        term_index=0
        for term in index_based_index_assignment_class:
            next_index = term_index + 1
            while next_index < len(index_based_index_assignment_class):
                if term['position_based'][0] in index_based_index_assignment_class[next_index]['position_based']:
                    del index_based_index_assignment_class[next_index]
                else:
                    next_index+= 1
            term_index+= 1
        result+=index_based_index_assignment_class
    '''
    result_index=0
    while result_index < len(result):
        for element in result[result_index]['index_based'][:minus_number_single_propagator_loop]:
            if (len(element)==2 and len(element[1])==2 and element[1][0]==element[1][1]):
                del result[result_index]
                result_index-=1
                break
        result_index+=1
    '''
    print(len(result))

    return result

'''
for ab in map_ansatz('zero_one',[[0,0],[1,1],[1,1]],2):
    print(ab)
    
map_ansatz('zero_two_A',[[0,0],[1,1],[1,1],[1,1]],2)

map_ansatz('zero_two_B',[[0,0],[1,1],[0,2],[1,3],[1,3]],4)

for ab in map_ansatz ('one_one',[[0,0],[0,1]],2):
    print(ab)

for ab in map_ansatz ('one_two_A',[[0,0],[1,1],[0,2]],2):
    print(ab)

for ab in map_ansatz ('one_two_B',[[0,0],[1,1],[0,2],[0,3]],4):
    print(ab)

map_ansatz ('one_two_C',[[0,0],[0,1],[0,1],[1,2]],4)
'''

'''
for ab in action_class('zero_one',[[1,1],[1,1],[1,1]],2):
    print(ab)

for ab in action_class('one_one',[[1,1],[2,2]],2):
    print(ab)

action_class('zero_two_A',[[1,1],[1,1],[1,1],[1,1]],2)
#    print(ab)
action_class('zero_two_B',[[1,1],[1,1],[0,2],[1,3],[1,3]],4,symmetry=True)
#    print(ab)

for ab in action_class('one_two_A',[[1,1],[1,1],[2,2]],2):
    print(ab['index_based'])

action_class('one_two_B',[[1,1],[1,1],[0,2],[2,3]],4)
#    print(ab['index_based'])

index=0
for ab in action_class('one_two_C',[[1,1],[0,2],[0,2],[1,3]],4,symmetry=True):
    #print(index)
    print(ab['index_based'])
    index+=1

for ab in action_class('two_two_A',[[2,1],[2,1]],2):
    print(ab)

for ab in action_class('two_two_B',[[0,1],[2,2],[2,2]],4):
    print(ab)

for ab in action_class('two_two_C',[[0,1],[0,1],[0,1]],4):
    print(ab)
'''






        
        
        




    
