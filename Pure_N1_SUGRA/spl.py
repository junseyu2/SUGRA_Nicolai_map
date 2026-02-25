import re
import sympy as sp

def _split_top_level_addsub(s):
    
    if not s:
        return []

    terms = []
    depth = 0
    start = 0

    for i, ch in enumerate(s):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif depth == 0 and ch in "+-":
            # 맨 앞 부호는 자르지 않음 (unary +/-)
            if i == start:
                continue
            terms.append(s[start:i])
            start = i

    terms.append(s[start:])
    
    return terms #[t for t in terms if t and t != "+"]

def split_single_parens(term):

    lpos = term.find("(")
    if lpos == -1:
        raise ValueError("괄호가 없습니다.")

    depth = 0
    rpos = -1
    for j in range(lpos, len(term)):
        ch = term[j]
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                rpos = j
                break

    if rpos == -1:
        raise ValueError("괄호가 닫히지 않았습니다.")

    inner = term[lpos + 1 : rpos]

    left = term[:lpos]
    right = term[rpos + 1 :]

    if left.endswith("*"):
        left = left[:-1]
    if right.startswith("*"):
        right = right[1:]

    if left and right:
        rest = left + "*" + right
    else:
        rest = left or right or "1"

    if rest in ("", "+"):
        rest = "1"
    elif rest == "-":
        rest = "-1"

    return rest, inner
