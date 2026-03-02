import sympy as sp
from copy import deepcopy

def linear_combination_of_(action_class,method_of_integration_by_parts,symmetry=False):
    linear_combination_list=[]
    for term in action_class:
        for element_index, element in enumerate(term['position_based'][0]):
            for method in method_of_integration_by_parts:
                if method[0] in element:
                    linear_combination="+"+deepcopy(term['id'])
                    for position,sign in method[1:]:
                        element_copy=deepcopy(element)
                        element_copy.remove(method[0])
                        element_copy.append(position)
                        element_copy.sort()
                        position_based_copy=deepcopy(term['position_based'][0])
                        position_based_copy.remove(element)
                        position_based_copy.append(element_copy)
                        position_based_copy.sort()
                        for term2 in action_class:
                            if position_based_copy in term2['position_based']:
                                linear_combination+=sign+deepcopy(term2['id'])
                                if symmetry:
                                    if sum(len(element2[1]) for element2 in term2['index_based'] if element2[0] == 2) % 2:
                                        if term2['position_based'].index(position_based_copy)>=len(term2['position_based'])//2:
                                            linear_combination+="*(-1)"
                                    
                    linear_combination_list.append(sp.simplify(sp.sympify(linear_combination)))
                    
    return linear_combination_list

def gauss_jordan_solution(equation_list):

    RREF={}
    pivot_variable_list=[]

    for equation in equation_list:

        row={}
        constant=sp.Integer(0)

        for term in sp.Add.make_args(equation):
            coefficient,variable=term.as_coeff_Mul()
            if variable==1:
                constant-=coefficient
            elif isinstance(variable,sp.Symbol):
                if variable in row:
                    row[variable]+=coefficient
                    if row[variable] == 0:
                        del row[variable]
                    continue
                row[variable]=coefficient
            else:
                raise ValueError(f"Nonlinear term : {term}")
            
        for pivot_variable in pivot_variable_list:
            if pivot_variable in row:
                pivot_constant,pivot_row=RREF[pivot_variable]
                factor=row[pivot_variable]
                constant=constant-factor*pivot_constant
                for variable,coefficient in pivot_row.items():
                    row[variable]=row.get(variable,sp.Integer(0))-factor*coefficient
                    if row[variable]==0:
                        del row[variable]
                        
        if not row:
            if constant != 0:
                raise ValueError(f"Inconsistent equation: 0 = {constant}")
            continue
        
        pivot_variable=min(row.keys(), key=lambda symbol: symbol.name)

        factor=row[pivot_variable]
        constant=constant*(sp.Rational(1,1)/factor)
        for variable in list(row.keys()):
            row[variable]=row[variable]*(sp.Rational(1, 1)/factor)

        for old_pivot_variable in pivot_variable_list:
            old_pivot_constant,old_pivot_row=RREF[old_pivot_variable]
            if pivot_variable in old_pivot_row:
                factor=old_pivot_row[pivot_variable]
                RREF[old_pivot_variable]=[old_pivot_constant-factor*constant,old_pivot_row]
                for variable,coefficient in row.items(): 
                    old_pivot_row[variable]=old_pivot_row.get(variable,sp.Integer(0))-factor*coefficient
                    if old_pivot_row[variable]==0:
                        del old_pivot_row[variable]

        RREF[pivot_variable]=[constant,row]
        pivot_variable_list.append(pivot_variable)

    for constant,row in RREF.values():
        for coefficient in row.values():
            if coefficient==0:
                raise ValueError("eliminate problem")

    solution={}
    
    for pivot_variable in  pivot_variable_list:
        constant,row=RREF[pivot_variable]
        new_row = {}
        for variable,coefficient in row.items():
            if variable == pivot_variable:
                continue
            new_row[variable] = -coefficient
        solution[pivot_variable] = [constant, new_row]

    return solution,pivot_variable_list
