from enum import Enum
from typing import NamedTuple
import re

class PatternType(Enum):
    Normal = ''
    Start = 'start'
    End = 'end'
    Once = 'once'
    Return = 'return'

class Pattern(NamedTuple):
    string: str
    pattern_type: PatternType

class Rule:
    left: Pattern
    right: Pattern
    enabled: bool
    
    def __init__(self, left: Pattern, right: Pattern):
        self.left = left
        self.right = right
        self.enabled = True

    def disp(self) -> str:
        return f'\033[0;35m{"" if self.left.pattern_type == PatternType.Normal else f"({self.left.pattern_type.value})"}\033[0;31m{self.left.string}\033[0;33m=\033[0;35m{"" if self.right.pattern_type == PatternType.Normal else f"({self.right.pattern_type.value})"}\033[0;32m{self.right.string}\033[0m'

class Rules:

    class ApplyResult(Enum):
        Success = 0
        NoRuleMatch = 1
        Return = 2

    KEYWORD_PATTERN: re.Pattern = re.compile(r'^\((start|end|once|return)\)')
    rules: list[Rule]

    def __init__(self, rules: list[Rule]):
        self.rules = rules

    @classmethod
    def parse(cls, grammar_text: str) -> 'Rules':
        rules = []
        for line in grammar_text.splitlines():
            if line.startswith('#') or '=' not in line:
                continue
            left, right = line.split('=')
            if (kw := cls.KEYWORD_PATTERN.search(left)):
                left = Pattern(string=left[kw.end():], pattern_type=PatternType(kw.group(1)))
            else:
                left = Pattern(string=left, pattern_type=PatternType.Normal)

            if (kw := cls.KEYWORD_PATTERN.search(right)):
                right = Pattern(string=right[kw.end():], pattern_type=PatternType(kw.group(1)))
            else:
                right = Pattern(string=right, pattern_type=PatternType.Normal)

            rules.append(Rule(left=left, right=right))
        return Rules(rules)

    def apply_once(self, string: str) -> tuple[ApplyResult, str]:
        for rule in self.rules:
            if not rule.enabled:
                continue
            
            typ = rule.left.pattern_type
            left = rule.left.string

            # try match
            try:
                index = string.index(left)
                if typ == PatternType.Start and index != 0:
                    continue
                elif typ == PatternType.End:
                    index = string.rindex(left)
                    if index != len(string) - len(left):
                        continue
            except ValueError:
                continue

            begin = index
            end = index + len(left)

            print(rule.disp())

            # check once
            if typ == PatternType.Once:
                rule.enabled = False

            print(f'\033[0;31m-\033[0m   "\033[1m{string[:begin]}\033[1;31m{string[begin:end]}\033[0m\033[1m{string[end:]}\033[0m"')
            print(f'\033[0;32m+\033[0m   ', end='')
            # try replace
            typ = rule.right.pattern_type
            right = rule.right.string
            if typ == PatternType.Normal:
                print(f'"\033[1m{string[:begin]}\033[1;32m{right}\033[0m\033[1m{string[end:]}\033[0m"')
                string = string[:begin] + right + string[end:]
            elif typ == PatternType.Return:
                print(f'"\033[1;36m{right}\033[0m"')
                return self.ApplyResult.Return, right
            elif typ == PatternType.Start:
                print(f'"\033[1;32m{right}\033[0m\033[1m{string[:begin]}{string[end:]}\033[0m"')
                string = right + string[:begin] + string[end:]
            elif typ == PatternType.End:
                print(f'"\033[1m{string[:begin]}{string[end:]}\033[1;32m{right}\033[0m"')
                string = string[:begin] + string[end:] + right

            return self.ApplyResult.Success, string
        return self.ApplyResult.NoRuleMatch, string

    def apply(self, string: str) -> str:
        counter = 0
        while True:
            print(f'\033[0;33m#{counter}\033[0m: ', end='')
            counter += 1
            result, s = self.apply_once(string)
            if result == self.ApplyResult.Success:
                string = s
            elif result == self.ApplyResult.Return:
                return s
            elif result == self.ApplyResult.NoRuleMatch:
                print(f'\033[1;36m{string}\033[0m')
                return string


if __name__ == '__main__':
    rules_input = '''
aa=ononnoa
ab=ononnob
ac=ononnoc
oa=oononno
b=oonnoonnno
c=ooonnnooonnnno
noono=onnoo
nooonno=oonnnoo
noooonnno=ooonnnnoo
ononno=true
oonnoonnno=true
ooonnnooonnnno=true
trueo=o
on=
no=false
'''
    g = Rules.parse(rules_input)
    print(g.apply('abbabbabbabba'))
