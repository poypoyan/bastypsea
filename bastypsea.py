# Basic Type Search (bastypsea) for Apex language
# Python prototype
# By: poypoyan
#
# https://www.youtube.com/watch?v=7CMDMaBsqj0
#
# MIT License
#
# Copyright (c) 2023 poypoyan
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re


class ApexCodeState:
    def __init__(self):
        self.DELIMS = ['//', '/*', '*/']
        self.line = 1
        self.comment = False
        self.vars = []
        self._last_delim = -1

    def upd_from_pline(self, pline: str, delim: int, input: dict, founds: list) -> None:
        if self.comment:
            self._upd_from_delim(delim)
            return

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
                    'fr_line_n': var['line_n'],
                    'pline': pline
                })
                self.vars.pop(i)
                # print('xxx', self.vars)
                return True
        return False

    def _upd_from_delim(self, delim: int) -> None:
        if delim >= 0:
            self._last_delim = delim

        if delim == 0:
            self.comment = True
        elif delim == 1:
            self.comment = True
        elif delim == 2:
            self.comment = False

    def upd_from_newline(self) -> None:
        self.line += 1

        if self._last_delim == 0:
            self.comment = False


def bastypsea(fp, inputs: dict) -> list:
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
        for i, pl in enumerate(part_lines):
            code_state.upd_from_pline(pl, part_delims[i], inputs, founds)

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

    mypath = '.\\prod-classes'   # must contain the Apex classes
    
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
