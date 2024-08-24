import re


class Recognise:
    def __init__(self, v, t, p, s, w):
        self.v = v  # str set
        self.t = t  # terminal str set
        self.p = p  # en_expr set
        self.s = s  # s
        self.w = w  # str
        self.len = len(self.w)
        self.v_list = []
        for i in range(self.len):
            v = []
            self.v_list.append(v)

    '''
    THE CORE CODES ARE AS FOLLOWS
    '''

    def recognise(self):
        for i in range(self.len):
            v_now = set()
            for gen_expr in self.p:
                if gen_expr.single_gen_ante(self.w[i]) is not None:
                    v_now.add(gen_expr.single_gen_ante(self.w[i]))
            self.v_list[i].append(v_now)
            print(f"v_{i + 1}_1={[item.__str__() for item in v_now]}")

        for j in range(2, self.len + 1):
            for i in range(1, self.len - j + 2):
                v_now = set()
                for k in range(1, j):
                    for gen_expr in self.p:
                        if gen_expr.double_ele() is None:
                            continue
                        a, (b, c) = gen_expr.double_ele()
                        if b in self.v_list[i - 1][k - 1] and c in self.v_list[i + k - 1][j - k - 1]:
                            v_now.add(a)
                self.v_list[i - 1].append(v_now)
                print(f"v_{i}_{j}={[item.__str__() for item in v_now]}")

        return self.s in self.v_list[0][self.len - 1]


class Expr:
    def __str__(self):
        return ''


class SingleExpr(Expr):
    def __init__(self, terminal: str):
        self.terminal = terminal

    def can_gen(self, x: str):
        return x == self.terminal

    def __str__(self):
        return self.terminal


class DoubleExpr(Expr):
    def __init__(self, first: str, second: str):
        self.first = first
        self.second = second

    def get_value(self):
        return self.first, self.second

    def __str__(self):
        return self.first + self.second


class GenExpr:
    def __init__(self, antecedent: str, consequence: Expr):
        self.antecedent = antecedent
        self.consequence = consequence

    def single_gen_ante(self, x: str):
        if isinstance(self.consequence, SingleExpr) \
                and self.consequence.can_gen(x):
            return self.antecedent
        return None

    def double_ele(self):
        if isinstance(self.consequence, DoubleExpr):
            return self.antecedent, self.consequence.get_value()
        return None

    def __str__(self):
        return self.antecedent + '->' + self.consequence.__str__()


def parse_gen_expr(str_item: str) -> GenExpr:
    str_list = str_item.split("->")
    if len(str_list) != 2:
        raise RuntimeError(f"Wrong Generation Format:{str_item}")
    antecedent = str_list[0]
    consequence = DoubleExpr(str_list[1][0], str_list[1][1]) if len(str_list[1]) > 1 \
        else SingleExpr(str_list[1])
    return GenExpr(antecedent, consequence)


def pre_process(input_str: str):
    return re.sub('[ \t\n]', '', input_str).split(',')


def main():
    v = set(pre_process(
        input("1.The start symbol is 'S' all the time.\n  "
              "Please enter the non-terminal set, use ',' to separate items:")))
    v.add('S')
    t = set(pre_process(
        input("2.Please enter the terminal set; use ',' to separate items:")))
    p_str = pre_process(input("3.Please enter the generation set, use ',' to separate items\n"
                              "  (Use '->' to separate the antecedent and the consequence):"))
    p = set()
    for str_item in p_str:
        p.add(parse_gen_expr(str_item))
    print(f"Your V set:{list(v)}")
    print(f"Your T set:{list(t)}")
    print(f"Your P set:{[item.__str__() for item in p]}")
    s = 'S'
    w = input("4.Please enter the words to be recognized:")
    recognise = Recognise(v, t, p, s, w)
    print(recognise.recognise())


main()
