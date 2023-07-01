# Basic Type Search (bastypsea) for Apex language
# Python prototype
# By: poypoyan
# 
# Distributed under the MIT software license. See the accompanying
# file LICENSE or https://opensource.org/license/mit/.

import re


class ApexCodeState:
    def __init__(self):
        self.DELIMS = ['//', '/*', '*/']
        self.line = 1
        self.vars = []
        self.is_comment = False
        self.is_test_class = False
        self._last_delim = -1
        self._is_in_class_decl = False

    def upd_from_pline(self, pline: str, delim: int, input: dict, founds: list, ignore_test: bool) -> None:
        if self.is_comment:
            self._upd_from_delim(delim)

        # check if test class
        if ignore_test and not self._is_in_class_decl:
            if '@istest' in pline.casefold():
                self.is_test_class = True
            rgx = '^[a-z\s]+class'
            if re.search(rgx, pline, re.I):
                self._is_in_class_decl = True

        # search for var init
        rgx = f'{ input["obj"] }[a-z0-9_,<>\s]*\s+([a-z0-9_]+)'
        res = re.search(rgx, pline, re.I)
        if res:
            # insert as first element so that latest added
            # is checked first on self._res_from_action
            self.vars.insert(0, {
                'line_n': self.line,
                'name': res.group(1)
            })

        # search for action
        rgx1 = f'[^.]{ input["act"] }\s+([a-z0-9_]+)'   # DML
        rgx2 = f'Database.{ input["act"] }[a-z]*\s*\(\s*([a-z0-9_]+)'   # Database method
        res1 = re.search(rgx1, pline, re.I)
        res2 = re.search(rgx2, pline, re.I)
        if res1:
            self._res_from_action(res1, pline, founds)
        if res2:
            self._res_from_action(res2, pline, founds)

        self._upd_from_delim(delim)

    def _res_from_action(self, res: re.Match, pline: str, founds: list) -> bool:
        for i, var in enumerate(self.vars):
            if res.group(1) == var['name']:
                founds.append({
                    'line_n': self.line,
                    'init_line_n': var['line_n'],
                    'pline': pline
                })
                self.vars.pop(i)
                return True
        return False

    def _upd_from_delim(self, delim: int) -> None:
        if delim >= 0:
            self._last_delim = delim

        if delim == 0:
            self.is_comment = True
        elif delim == 1:
            self.is_comment = True
        elif delim == 2:
            self.is_comment = False

    def upd_from_newline(self) -> None:
        self.line += 1

        if self._last_delim == 0:
            self.is_comment = False


def bastypsea(fp, inputs: dict, ignore_test: bool=True) -> list:
    code_state = ApexCodeState()
    founds = []

    while True:
        line = fp.readline()
        if not line:
            break

        # separate lines according to DELIMS
        part_lines = []
        part_delims = []
        part_start = 0
        for i in range(len(line)):
            for j, delim in enumerate(code_state.DELIMS):
                if line[i: i + len(delim)] == delim:
                    part_lines.append(line[part_start: i])
                    part_delims.append(j)
                    part_start = i
        part_lines.append(line[part_start: len(line)])
        part_delims.append(-1)

        # bastypsea proper
        # https://www.youtube.com/watch?v=mCeosicdJDI
        for i, pl in enumerate(part_lines):
            code_state.upd_from_pline(pl, part_delims[i], inputs, founds, ignore_test)
            if ignore_test and code_state.is_test_class:
                break
        if ignore_test and code_state.is_test_class:
            break
        code_state.upd_from_newline()
    return founds


import time
from os import listdir
from os.path import isfile, join, splitext
from pprint import pprint


if __name__ == '__main__':
    inputs = {
        'obj': 'OpportunityLineItem',
        'act': 'Delete'
    }
    mypath = '.\\classes'   # must contain the Apex classes

    founds = {}

    tic = time.perf_counter()
    classes = [f for f in listdir(mypath) if isfile(join(mypath, f)) and splitext(f)[1] == '.cls']
    for i in classes:
        with open(join(mypath, i), 'r', encoding='utf-8') as fp:
            outputs = bastypsea(fp, inputs)

        if len(outputs) > 0:
            founds[i] = outputs
    toc = time.perf_counter()

    print(f"Completed in {toc - tic:0.6f} seconds")
    pprint(founds)
