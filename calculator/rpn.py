from collections import deque
import re

regexAll = re.compile(
    '(?:\d+\.?\d*|\.\d+)|[\(\)\*/\^]|[\+\-]|[\(\)]')  # すべてのトークンのパターン
regexNumber = re.compile('(?:\d+\.?\d*|\.\d+)')  # 値
regexSymbol = re.compile('[\+\-\*/\^]')  # 演算記号
regexBracket = re.compile('[\(\)]')  # カッコ
regexSpace = re.compile('\s+')  # 空白文字

# 優先度(値が1)
priorities = {
    '+': 2,
    '-': 2,
    '*': 3,
    '/': 3,
    '^': 4,
    '(': 0,
    ')': 0
}

# 結合性(0: R, 1:L)
connectDirection = {
    '+': 1,
    '-': 1,
    '*': 1,
    '/': 1,
    '^': 0
}


formula = regexSpace.sub('', input())


# 与えられた文字列の属性を返す
def getType(v: str):
    if (regexNumber.match(v)):
        return 'Number'
    if (regexSymbol.match(v)):
        return 'Symbol'
    return 'Unknown'


# 数式→トークン配列の変換
def tokenize(formula: str) -> list[str]:
    token = regexAll.match(formula).group()
    formula = formula[len(token):]
    if (len(formula)):
        return [token] + tokenize(formula)
    return [token]


# トークン配列→RPN配列
def makeRpn(tokens: list[str]) -> list[str]:
    symbols = deque()  # 記号のスタック
    outputs = []       # 出力キュー
    for token in tokens:
        # 値の場合は出力キューへ追加
        if getType(token) == 'Number':
            outputs.append(token)
            continue
        # 演算子の場合の処理
        if not(regexBracket.match(token)):
            if len(symbols):
                priority1 = priorities[token]
                for symbol in reversed(symbols.copy()):
                    priority2 = priorities[symbol]
                    if (connectDirection[token] and priority1 <= priority2) or priority1 < priority2:
                        outputs.append(symbols.pop())
                    else:
                        break
            symbols.append(token)
            continue
        # カッコの処理
        if token == '(':
            symbols.append(token)
            continue
        if token == ')':
            for symbol in reversed(symbols.copy()):
                if symbol == '(':
                    symbols.pop()
                    break
                else:
                    outputs.append(symbols.pop())
            continue
    # 最後まで残った記号たちを出力キューへ追加
    if len(symbols):
        for symbol in reversed(symbols):
            outputs.append(symbol)
    return outputs


def runRpn(formula: list[str]):
    # 値のスタック
    values = deque()
    for token in formula:
        match getType(token):
            case 'Number':
                # 値ならそのままスタック
                values.append(float(token))
            case 'Symbol':
                # 最新の2つの値
                value1 = values.pop()
                value2 = values.pop()
                # 演算してスタック
                match token:
                    case '+':
                        values.append(value2 + value1)
                    case '-':
                        values.append(value2 - value1)
                    case '*':
                        values.append(value2 * value1)
                    case '/':
                        values.append(value2 / value1)
                    case '^':
                        values.append(value2 ** value1)
                    case _:
                        print('Error in formula')
                        exit()
    return values.pop()


def calc(formula):
    # 数式をトークンにして
    tokenizedFormula = tokenize(formula)
    # RPNにして
    rpn = makeRpn(tokenizedFormula)
    # RPNを計算する
    return runRpn(rpn)


print(calc(formula))


"""
参考: https://ja.wikipedia.org/wiki/操車場アルゴリズム
"""
