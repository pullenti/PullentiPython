# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing

from pullenti.ner.MetaToken import MetaToken

class TableCellToken(MetaToken):
    """ Токен - ячейка таблицы """
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        super().__init__(b, e0_, None)
        self.col_span = 1
        self.row_span = 1
        self._eoc = False
    
    @property
    def _lines(self) -> typing.List['TableCellToken']:
        res = list()
        t = self.begin_token
        while t is not None and t.end_char <= self.end_char: 
            t0 = t
            t1 = t
            first_pass3653 = True
            while True:
                if first_pass3653: first_pass3653 = False
                else: t = t.next0_
                if (not (t is not None and t.end_char <= self.end_char)): break
                t1 = t
                if (t.is_newline_after): 
                    if ((t.next0_ is not None and t.next0_.end_char <= self.end_char and t.next0_.chars.is_letter) and t.next0_.chars.is_all_lower and not t0.chars.is_all_lower): 
                        continue
                    break
            res.append(TableCellToken(t0, t1))
            t = t1
            t = t.next0_
        return res
    
    @staticmethod
    def _new534(_arg1 : 'Token', _arg2 : 'Token', _arg3 : int, _arg4 : int) -> 'TableCellToken':
        res = TableCellToken(_arg1, _arg2)
        res.row_span = _arg3
        res.col_span = _arg4
        return res