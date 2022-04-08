import re

"""
<expr> ::= <term>([+-]<term>)*
<term> ::= <factor>([*/]<factor>)
<factor> ::= <number> | ( <expr> )
<number> ::= [0-9]+\.?[0-9]*
"""


index = 0
nest = 0
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
    global index, nest
    print('\033[32m{0}<expr>: {1}\033[0m'.format(' ' * nest, ''.join(t[index:])))
    nest += 1
    v = term(t)
    while index < len(t) and (t[index] == '+' or t[index] == '-'):
        operator = t[index]
        index += 1
        print('\033[35m{0}<operator>: {1}\033[0m'.format(' ' * nest, operator))
        match operator:
            case '+':
                v += term(t)
            case '-':
                v -= term(t)
    nest -= 1
    return v


# 項
def term(t: list[str]):
    global index, nest
    print('\033[34m{0}<term>: {1}\033[0m'.format(' ' * nest, ''.join(t[index:])))
    nest += 1
    v = factor(t)
    while index < len(t) and (t[index] == '*' or t[index] == '/'):
        operator = t[index]
        index += 1
        print('\033[35m{0}<operator>: {1}\033[0m'.format(' ' * nest, operator))
        match operator:
            case '*':
                v *= factor(t)
            case '/':
                v /= factor(t)
    nest -= 1
    return v


# 因子
def factor(t: list[str]):
    global index, nest
    print('\033[33m{0}<factor>: {1}\033[0m'.format(' ' * nest, ''.join(t[index:])))
    nest += 1
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
    nest -= 1
    return v


# 数
def number(t: list[str]):
    global index, nest
    print('\033[31m{0}<number>: {1}\033[0m'.format(' ' * nest, t[index]))
    nest += 1
    v = None
    if isFloatRegex.match(t[index]):
        v = float(t[index])
    else:
        v = int(t[index])
    index += 1
    nest -= 1
    return v


if __name__ == '__main__':
    print('\033[32mAnswer: {0}\033[0m'.format(eval()))

"""
参考: https://qiita.com/thtitech/items/91e2456c989ca969850d
"""