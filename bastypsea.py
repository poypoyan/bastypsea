# Basic Type Search (bastypsea) for Apex language
# Python prototype
# By poypoyan
# 
# Distributed under the MIT software license. See the accompanying
# file LICENSE or https://opensource.org/license/mit/.

import re


class ApexCodeState:
    def __init__(self, obj: str):
        self.DELIMS = ['//', '/*', '*/', ';', '{', '}']
        self.line = 1
        self.vars = []
        self.types = [obj]
        self.is_comment = False
        self.is_test_class = False
        self._last_delim = -1
        self._curly_bracket_ctr = 0
        self._cand_inner_class = ''
        self._is_in_outer_class = False
        self._is_in_inner_class = False

    def upd_from_pline(self, pline: str, delim: int, input_obj: str, input_act: str, founds: list, ignore_test: bool) -> None:
        if self.is_comment:
            self._upd_from_delim(delim)

        # search for outer class init
        rgx_class = '^[a-z\s]+class\s+([a-z0-9_]+)'
        rgx_var_init = f'[a-z0-9_,<>\s]*{ input_obj }[a-z0-9_,<>\s]*\s+([a-z0-9_]+)'
        res = re.search(rgx_class, pline, re.I)
        if not self._is_in_outer_class:
            # check if test class
            if ignore_test and '@istest' in pline.casefold():
                self.is_test_class = True
            if res:
                self._is_in_outer_class = True
            self._upd_from_delim(delim)
            return

        # search for var in inner class
        if self._is_in_inner_class:
            if len(self.vars) == 0 or self.types[0] != self._cand_inner_class:
                res1 = self._check_var_init(pline)
                if res1:
                    self.types.insert(0, self._cand_inner_class)

            if delim == 4:
                self._curly_bracket_ctr += 1
            elif delim == 5:
                self._curly_bracket_ctr -= 1

            if self._curly_bracket_ctr == 0:
                self._is_in_inner_class = False
            self._upd_from_delim(delim)
            return

        # search for inner class init
        if res:
            self._is_in_inner_class = True
            self._curly_bracket_ctr = 1
            self._cand_inner_class = res.group(1)
            self._upd_from_delim(delim)
            return

        # search for var init
        res = self._check_var_init(pline)
        if res:
            # insert to self.vars as first element so that latest
            # added is checked first on self._res_from_action
            self.vars.insert(0, {
                'line_n': self.line,
                'name': res.group(1)
            })
            self._upd_from_delim(delim)
            return

        # search for action
        rgx_act_0 = f'[^.]{ input_act }\s+([a-z0-9_]+)'   # DML
        rgx_act_1 = f'Database.{ input_act }[a-z]*\s*\(\s*([a-z0-9_]+)'   # Database method
        for i in [rgx_act_0, rgx_act_1]:
            res = re.search(i, pline, re.I)
            if res:
                self._res_from_action(res, pline, founds)
                self._upd_from_delim(delim)
                return

    def _check_var_init(self, pline: str) -> re.Match:
        # print(self.types)
        for i in self.types:
            rgx_var_init = f'[a-z0-9_,<>\s]*{ i }[a-z0-9_,<>\s]*\s+([a-z0-9_]+)'
            res = re.search(rgx_var_init, pline, re.I)
            if res:
                return res
        return None

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


def bastypsea(fp, input_obj: str, input_act: str, ignore_test: bool=True) -> list:
    code_state = ApexCodeState(input_obj)
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
                i_plus = i + len(delim)
                if line[i: i_plus] == delim:
                    part_lines.append(line[part_start: i_plus])
                    part_delims.append(j)
                    part_start = i_plus
        part_lines.append(line[part_start: len(line)])
        part_delims.append(-1)

        # bastypsea proper
        # https://www.youtube.com/watch?v=mCeosicdJDI
        for i, pl in enumerate(part_lines):
            code_state.upd_from_pline(pl, part_delims[i], input_obj, input_act, founds, ignore_test)
            if ignore_test and code_state.is_test_class:
                return founds
        code_state.upd_from_newline()
    return founds


import time
from glob import glob
from os.path import isfile, basename
from pprint import pprint


if __name__ == '__main__':
    my_obj = 'OpportunityLineItem'
    my_act = 'Delete'
    my_path = r'.\classes\*.cls'

    founds = {}

    tic = time.perf_counter()
    classes = [f for f in glob(my_path) if isfile(f)]
    for i in classes:
        with open(i, 'r', encoding='utf-8') as fp:
            outputs = bastypsea(fp, my_obj, my_act)

        if len(outputs) > 0:
            founds[basename(i)] = outputs
    toc = time.perf_counter()

    print(f"Completed in {toc - tic:0.6f} seconds")
    pprint(founds)

