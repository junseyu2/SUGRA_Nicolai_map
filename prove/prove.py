import z3
import re
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
            '''
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
            
        for pivot_variable_index, pivot_variable in enumerate(pivot_variable_list):
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
            for symbol in constant.free_symbols:
                if symbol.name.startswith("action"):
                    print("constant_problem")
                    print(symbol)
            reminder_equation_list.append(constant)
            continue
        
        pivot_variable=min(row.keys(), key=lambda symbol: symbol.name)

        factor=row[pivot_variable]
        constant=constant*(sp.Rational(1,1)/factor)
        for variable in list(row.keys()):
            row[variable]=row[variable]*(sp.Rational(1, 1)/factor)

        for old_pivot_variable_index,old_pivot_variable in enumerate(pivot_variable_list):
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

    return solution,pivot_variable_list,reminder_equation_list

def substitute_equations(equation_list, sol: dict):

    residuals = []
    for expr in equation_list:
        r = expr.subs(sol)
        r = sp.simplify(r)
        residuals.append(deepcopy(r))

    return residuals

MAIN_PREFIXES_A = ("zero_one","one_one","action_one_two_A","action_one_two_C","action_two_two_A","action_two_two_C")

_main_reA = re.compile(rf"^({'|'.join(map(re.escape, MAIN_PREFIXES_A))})_\d+_\d+$")

def main_test_A(symbol):    
    return _main_reA.match(symbol.name)

def full(symbol):    
    return True

def collect_symbols(exprs):

    syms=set()
    for e in exprs:
        if e is None:
            continue
        if not isinstance(e, sp.Basic):
            raise TypeError(f"Non-sympy object found: {e!r} (type={type(e)})")
        syms |= e.free_symbols

    out = list(syms)

    return out

_,_,reminder_equation_list_B=gauss_jordan_one_solution(equation_list_B)

equation_list_A_symbol=collect_symbols(equation_list_A)

print("solution_A")
i=0
for sol in sp.nonlinsolve(equation_list_A+reminder_equation_list_B,equation_list_A_symbol):
    print("solution")
    print(i)
    for symbol_index in range(len(equation_list_A_symbol)):
        print(equation_list_A_symbol[symbol_index])
        print(sol[symbol_index])
    i+=1


