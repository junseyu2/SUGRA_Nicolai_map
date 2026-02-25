import z3
import re
import ansatz
import sympy as sp
from copy import deepcopy
from zero_one import zero_one_condition
from one_one import one_one_condition
from zero_two import zero_two_condition
from one_two import one_two_condition
from two_two import two_two_condition

equation_list_A=[]
equation_list_B=[]
for a,b in zero_one_condition.items():
    equation_list_A.append(b)
for a,b in one_one_condition.items():
    equation_list_A.append(b)
for a,b in zero_two_condition.items():
    equation_list_B.append(b)
for a,b in one_two_condition.items():
    equation_list_B.append(b)
for a,b in two_two_condition.items():
    equation_list_B.append(b)

def auxiliary_variable_0(equation_list,auxiliary_test):
    
    auxiliary_variable = set()
    
    for equation in equation_list:
        auxiliary_variable.update(symbol for symbol in equation.free_symbols if auxiliary_test(symbol))

    auxiliary_variable_0 = {symbol: sp.Integer(0) for symbol in auxiliary_variable}

    auxiliary_variable_0_equation_list=[]
    for equation in equation_list:
        auxiliary_variable_0_equation=sp.Integer(0)
        bucket=[]
        for term in sp.Add.make_args(equation.xreplace(auxiliary_variable_0)):
            bucket.append(sp.expand_mul(term))
            if len(bucket) >= 2000:
                auxiliary_variable_0_equation = sp.Add(auxiliary_variable_0_equation, sp.Add(*bucket))
                bucket.clear()
        if bucket:
            auxiliary_variable_0_equation = sp.Add(auxiliary_variable_0_equation, sp.Add(*bucket))
        auxiliary_variable_0_equation_list.append(auxiliary_variable_0_equation)

    return auxiliary_variable_0_equation_list

def _sympy_number_to_z3(n: sp.Expr):
    
    if isinstance(n, sp.Integer):
        return z3.RealVal(int(n))
    if isinstance(n, sp.Rational):
        return z3.RealVal(f"{int(n.p)}/{int(n.q)}")
    if n.is_Number:
        return z3.RealVal(str(n))
    raise ValueError(f"Not a numeric coefficient: {n} ({type(n)})")

def sympy_to_z3_poly(expr: sp.Expr, env: dict, memo: dict):
    
    if expr in memo:
        return memo[expr]

    if expr.is_Number:
        z = _sympy_number_to_z3(expr)
        memo[expr] = z
        return z

    if isinstance(expr, sp.Symbol):
        z = env.get(expr)
        if z is None:
            z = z3.Real(expr.name)
            env[expr] = z
        memo[expr] = z
        return z

    if isinstance(expr, sp.Add):
        acc = z3.RealVal("0")
        for a in expr.args:
            acc = acc + sympy_to_z3_poly(a, env, memo)
        memo[expr] = acc
        return acc

    if isinstance(expr, sp.Mul):
        acc = z3.RealVal("1")
        for a in expr.args:
            acc = acc * sympy_to_z3_poly(a, env, memo)
        memo[expr] = acc
        return acc

    if isinstance(expr, sp.Pow):
        base, exp = expr.as_base_exp()

        if not exp.is_Integer:
            raise ValueError(f"Non-polynomial exponent (not integer): {expr}")

        e = int(exp)

        if e < 0:
            if base.is_number:
                val = sp.Pow(base, exp)
                if val.is_Number:
                    z = _sympy_number_to_z3(val)
                    memo[expr] = z
                    return z
            raise ValueError(f"Non-polynomial negative power of non-number: {expr}")

        if e == 0:
            z = z3.RealVal("1")
            memo[expr] = z
            return z

        zb = sympy_to_z3_poly(base, env, memo)

        acc = z3.RealVal("1")
        for _ in range(e):
            acc = acc * zb

        memo[expr] = acc
        return acc

    raise ValueError(f"Unsupported Sympy node: {type(expr)} / {expr}")

def z3_poly_one_solution(equation_list):
    
    all_syms = set()
    for eq in equation_list:
        all_syms |= eq.free_symbols

    env = {s: z3.Real(s.name) for s in all_syms}
    memo = {}

    solver = z3.SolverFor("QF_NRA")

    for i, eq in enumerate(equation_list, 1):
        z_eq = sympy_to_z3_poly(eq, env, memo)
        solver.add(z_eq == 0)

    print("[z3] check() ...")
    r = solver.check()
    print("[z3] result =", r)

    if r == z3.unsat:
        raise ValueError("Z3: UNSAT")
    if r == z3.unknown:
        raise ValueError("Z3: UNKNOWN")

    m = solver.model()

    one_solution = {}

    for s in sorted(all_syms, key=lambda x: x.name):
        zv = env[s]
        val = m.eval(zv, model_completion=True)

        num = val.numerator_as_long()
        den = val.denominator_as_long()
        sval = sp.Rational(num, den)

        one_solution[s] = sval

    return one_solution

def gauss_jordan_one_solution(equation_list):

    RREF={}
    pivot_variable_list=[]
    reminder_equation_list=[]

    for eq_index,equation in enumerate(equation_list):

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
            '''
            for free_symbol in term.free_symbols:
                if main_test_A(free_symbol):
                    constant-=term
                    break
            else:
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
            '''
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
            print(eq_index)
            print(equation)
            print(constant)
            reminder_equation_list.append(constant)
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

    return solution

def substitute_equations(equation_list, sol):

    result = []
    for equation in equation_list:
        result_equation=sp.Integer(0)
        bucket=[]
        for term in sp.Add.make_args(equation.xreplace(sol)):
            bucket.append(sp.expand_mul(term))
            if len(bucket) >= 2000:
                result_equation = sp.Add(result_equation, sp.Add(*bucket))
                bucket.clear()
        if bucket:
            result_equation = sp.Add(result_equation, sp.Add(*bucket))
        result.append(result_equation)

    return result

MAIN_PREFIXES_A = ("zero_one","one_one")

_main_reA = re.compile(rf"^({'|'.join(map(re.escape, MAIN_PREFIXES_A))})_\d+_\d+$")

def main_test_A(symbol):    
    return _main_reA.match(symbol.name)

def full(symbol):    
    return True

solution={pv: val[0] for pv, val in gauss_jordan_one_solution(equation_list_A).items() if val[0]}

equation_list_B=substitute_equations(equation_list_B, solution)

equation_list_B=auxiliary_variable_0(equation_list_B,main_test_A)

solution.update({pv: val[0] for pv, val in gauss_jordan_one_solution(equation_list_B).items() if val[0]})

print('test_start')

for eq in auxiliary_variable_0(substitute_equations(equation_list_A+equation_list_B, solution),full):
    if eq:
        print(eq)

print('test_end')

zero_one_map_list=ansatz.map_ansatz('zero_one',[[0,0],[1,1],[1,1]],2)
one_one_map_list=ansatz.map_ansatz('one_one',[[0,0],[0,1]],2)
zero_two_A_map_list=ansatz.map_ansatz('zero_two_A',[[0,0],[1,1],[1,1],[1,1]],2)
zero_two_B_map_list=ansatz.map_ansatz('zero_two_B',[[0,0],[1,1],[0,2],[1,3],[1,3]],4)
one_two_A_map_list=ansatz.map_ansatz('one_two_A',[[0,0],[1,1],[0,2]],2)
one_two_B_map_list=ansatz.map_ansatz ('one_two_B',[[0,0],[1,1],[0,2],[0,3]],4)
one_two_C_map_list=ansatz.map_ansatz ('one_two_C',[[0,0],[0,1],[0,1],[1,2]],4)

word_solution=[]

def propagator_translate (cordinate,element):
    
    word_element=''
    
    global character_index_list
    global seen_index

    for index in element[1]:
        if index in seen_index:
            script="_"
        else:
            script="^"
            seen_index.add(index)
        character_index=script+'{'+character_index_list[index]+'}'
        word_element+=r'\partial'+character_index+" "
    
    word_element+=f'G({cordinate}) '

    return word_element

def Vielbein_translate (cordinate,element):
    
    word_element=''
    
    global character_index_list
    global seen_index

    for index in element[1]:
        if index in seen_index:
            script="_"
        else:
            script="^"
            seen_index.add(index)
        character_index=script+'{'+character_index_list[index]+'}'
        word_element+=r'\partial'+character_index+" "
    index1,index2=element[2]
    if index1 in seen_index:
        script1="_"
    else:
        script1="^"
        seen_index.add(index1)
    if index2 in seen_index:
        script2="_"
    else:
        script2="^"
        seen_index.add(index2)
    if script1==script2:
        word_element+='c'+script1+'{'+character_index_list[index1]+character_index_list[index2]+'}'+f'({cordinate})'+' '
    else:
        word_element+='c'+script1+'{'+character_index_list[index1]+'}'+script2+'{'+character_index_list[index2]+'}'+f'({cordinate})'+' '

    return word_element

for term,coeffeicent in solution.items():

    character_index_list=['',r'\mu',r'\nu',r"\rho",r"\sigma",r"\lambda",r"\kappa",r"\tau",r"\xi",r"\alpha",r"\beta",r"\gamma",r"\delta",r"\epsilon",r"\zeta",r"\theta",r"\pi",r"\phi",r"\chi",r"\psi",r"\omega"]

    seen_index=set()

    if coeffeicent>0:

        word_map=f'+{coeffeicent}*'

    elif coeffeicent<0:

        word_map=f'{coeffeicent}*'

    else:
        print('problem')
        continue

    if term.name.startswith('zero_one'):
        for zero_one_map in zero_one_map_list:
            if zero_one_map['id']==term.name:

                index_based=deepcopy(zero_one_map['index_based'])
                
                if zero_one_map['eta']==0:
                    word_map+=r'\int d^4 y '
                elif zero_one_map['eta']==1:
                    word_map+=r'\eta^{\mu\nu} \int d^4 y '
                    index_based=[[element[0]]+[[index+2 for index in index_list] for index_list in element[1:]]for element in index_based]

                word_map+=propagator_translate('x-y',index_based[0])
                word_map+=Vielbein_translate('y',index_based[1])
                word_map+=Vielbein_translate('y',index_based[2])
                break

    elif term.name.startswith('one_one'):
        for zero_one_map in zero_one_map_list:
            if zero_one_map['id']==term.name:

                index_based=deepcopy(zero_one_map['index_based'])
                
                if zero_one_map['eta']==0:
                    word_map+=r'\int d^4 y '
                elif zero_one_map['eta']==1:
                    word_map+=r'\eta^{\mu\nu} \int d^4 y '
                    index_based=[[element[0]]+[[index+2 for index in index_list] for index_list in element[1:]]for element in index_based]

                word_map+=propagator_translate('x-y',index_based[0])
                word_map+=Vielbein_translate('0',index_based[1])
        
    elif term.name.startswith('zero_two_A'):
        for zero_two_A_map in zero_two_A_map_list:
            if zero_two_A_map['id']==term.name:

                index_based=deepcopy(zero_two_A_map['index_based'])
                
                if zero_two_A_map['eta']==0:
                    word_map+=r'\int d^4 y '
                elif zero_two_A_map['eta']==1:
                    word_map+=r'\eta^{\mu\nu} \int d^4 y '
                    index_based=[[element[0]]+[[index+2 for index in index_list] for index_list in element[1:]]for element in index_based]

                word_map+=propagator_translate('x-y',index_based[0])
                word_map+=Vielbein_translate('y',index_based[1])
                word_map+=Vielbein_translate('y',index_based[2])
                word_map+=Vielbein_translate('y',index_based[3])
                break
        
    elif term.name.startswith('zero_two_B'):
        for zero_two_B_map in zero_two_B_map_list:
            if zero_two_B_map['id']==term.name:

                index_based=deepcopy(zero_two_B_map['index_based'])
                
                if zero_two_B_map['eta']==0:
                    word_map+=r'\int d^4 y d^4 z '
                elif zero_two_B_map['eta']==1:
                    word_map+=r'\eta^{\mu\nu} \int d^4 y d^4 z '
                    index_based=[[element[0]]+[[index+2 for index in index_list] for index_list in element[1:]]for element in index_based]

                word_map+=propagator_translate('x-y',index_based[0])
                word_map+=Vielbein_translate('y',index_based[1])
                word_map+=propagator_translate('y-z',index_based[2])
                word_map+=Vielbein_translate('z',index_based[3])
                word_map+=Vielbein_translate('z',index_based[4])
                break
        
    elif term.name.startswith('one_two_A'):
        for one_two_A_map in one_two_A_map_list:
            if one_two_A_map['id']==term.name:

                index_based=deepcopy(one_two_A_map['index_based'])
                
                if one_two_A_map['eta']==0:
                    word_map+=r'\int d^4 y '
                elif one_two_A_map['eta']==1:
                    word_map+=r'\eta^{\mu\nu} \int d^4 y '
                    index_based=[[element[0]]+[[index+2 for index in index_list] for index_list in element[1:]]for element in index_based]

                word_map+=propagator_translate('x-y',index_based[0])
                word_map+=Vielbein_translate('y',index_based[1])
                word_map+=propagator_translate('0',index_based[2])
                break
        
    elif term.name.startswith('one_two_B'):
        for one_two_B_map in one_two_B_map_list:
            if one_two_B_map['id']==term.name:

                index_based=deepcopy(one_two_B_map['index_based'])
                
                if one_two_B_map['eta']==0:
                    word_map+=r'\int d^4 y d^4 z '
                elif one_two_B_map['eta']==1:
                    word_map+=r'\eta^{\mu\nu} \int d^4 y d^4 z '
                    index_based=[[element[0]]+[[index+2 for index in index_list] for index_list in element[1:]]for element in index_based]

                word_map+=propagator_translate('x-y',index_based[0])
                word_map+=Vielbein_translate('y',index_based[1])
                word_map+=propagator_translate('y-z',index_based[2])
                word_map+=propagator_translate('0',index_based[3])
                break
        
    elif term.name.startswith('one_two_C'):
        for one_two_C_map in one_two_C_map_list:
            if one_two_C_map['id']==term.name:

                index_based=deepcopy(one_two_C_map['index_based'])
                
                if one_two_C_map['eta']==0:
                    word_map+=r'\int d^4 y d^4 z '
                elif one_two_C_map['eta']==1:
                    word_map+=r'\eta^{\mu\nu} \int d^4 y d^4 z '
                    index_based=[[element[0]]+[[index+2 for index in index_list] for index_list in element[1:]]for element in index_based]

                word_map+=propagator_translate('x-y',index_based[0])
                word_map+=propagator_translate('y-z',index_based[1])
                word_map+=propagator_translate('y-z',index_based[2])
                word_map+=Vielbein_translate('z',index_based[3])
                break
        
    else:
        print("problem")
        print(term)

    word_solution.append(word_map+'\n')

with open("tex_solution.txt", "w", encoding="utf-8") as f:
    f.writelines(word_solution)
