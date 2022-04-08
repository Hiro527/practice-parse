import re

"""
<expr> ::= <term>([+-]<term>)*
<term> ::= <factor>([*/]<factor>)
<factor> ::= <number> | ( <expr> )
<number> ::= [0-9]+\.?[0-9]*
"""


index = 0
tokenRegex = re.compile(
    '(?:\d+\.?\d*|\.\d+)|[\(\)\*/\^]|[\+\-]|[\(\)]')  # すべてのトークンのパターン
numberCharRegex = re.compile('[0-9\.]')
isFloatRegex = re.compile('[0-9]+\.[0-9]*')


def eval():
    # 入力した式から空白を削除
    formula = re.sub('\s', '', input())
    return expr(tokenize(formula))


# トークン化
def tokenize(f: str) -> list[str]:
    token = tokenRegex.match(f).group()
    f = f[len(token):]
    if (len(f)):
        return [token] + tokenize(f)
    return [token]


# 式
def expr(t: list[str]):
    global index
    v = term(t)
    while index < len(t) and (t[index] == '+' or t[index] == '-'):
        operator = t[index]
        index += 1
        match operator:
            case '+':
                v += term(t)
            case '-':
                v -= term(t)
    return v


# 項
def term(t: list[str]):
    global index
    v = factor(t)
    while index < len(t) and (t[index] == '*' or t[index] == '/'):
        operator = t[index]
        index += 1
        match operator:
            case '*':
                v *= factor(t)
            case '/':
                v /= factor(t)
    return v


# 因子
def factor(t: list[str]):
    global index
    v = None
    if t[index] == '(':
        index += 1
        v = expr(t)
        if t[index] != ')' or index == len(t):
            print('Parsing error at index {0}'.format(index))
            exit()
        index += 1
    else:
        v = number(t)
    return v


# 数
def number(t: list[str]):
    global index
    v = None
    if isFloatRegex.match(t[index]):
        v = float(t[index])
    else:
        v = int(t[index])
    index += 1
    return v



if __name__ == '__main__':
    print(eval())