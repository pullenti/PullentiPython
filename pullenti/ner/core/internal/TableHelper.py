# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import typing
from enum import IntEnum
from pullenti.ntopy.Utils import Utils
from pullenti.ntopy.Misc import RefOutArgWrapper




class TableHelper:
    """ Поддержка работы с таблицами, расположенными в текстах.
     Начало таблицы - символ 1Eh, конец - 1Fh, ячейки оканчиваются 07h,
     комбинация 0D 0A 07 - конец строки.
     Данную структуру формирует функция извлечения текстов (ExtractText), так что это - для
     обратного восстановления таблицы в случае необходимости. """
    
    class TableTypes(IntEnum):
        UNDEFINED = 0
        TABLESTART = 1
        TABLEEND = 2
        ROWEND = 3
        CELLEND = 4
    
    class TableInfo:
        
        def __str__(self) -> str:
            return "{0} ({1}-{2})".format(Utils.enumToString(self.typ), self.col_span, self.row_span)
        
        def __init__(self, t : 'Token') -> None:
            self.col_span = 0
            self.row_span = 0
            self.typ = TableHelper.TableTypes.UNDEFINED
            self.src = None
            self.src = t
            if (t is None): 
                return
            if (t.is_char(chr(0x1E))): 
                self.typ = TableHelper.TableTypes.TABLESTART
                return
            if (t.is_char(chr(0x1F))): 
                self.typ = TableHelper.TableTypes.TABLEEND
                return
            if (not t.is_char(chr(7))): 
                return
            txt = t.kit.sofa.text
            self.typ = TableHelper.TableTypes.CELLEND
            p = t.begin_char - 1
            if (p < 0): 
                return
            if (ord(txt[p]) == 0xD or ord(txt[p]) == 0xA): 
                self.typ = TableHelper.TableTypes.ROWEND
                return
            self.row_span = 1
            self.col_span = self.row_span
            while p >= 0: 
                if (not Utils.isWhitespace(txt[p])): 
                    break
                elif (txt[p] == '\t'): 
                    self.col_span += 1
                elif (txt[p] == '\f'): 
                    self.row_span += 1
                p -= 1
    
    @staticmethod
    def try_parse_rows(t : 'Token', max_char : int, must_be_start_of_table : bool) -> typing.List['TableRowToken']:
        """ Получить список строк таблицы
        
        Args:
            t(Token): начальная позиция
            max_char(int): максимальная позиция (0 - не ограничена)
            must_be_start_of_table(bool): при true первый символ должен быть 1Eh
        
        Returns:
            typing.List[TableRowToken]: список строк
        """
        from pullenti.ner.core.internal.TableRowToken import TableRowToken
        if (t is None): 
            return None
        is_tab = False
        if (must_be_start_of_table): 
            if (not t.is_char(chr(0x1E))): 
                return None
            is_tab = True
        inoutarg467 = RefOutArgWrapper(is_tab)
        rw = TableHelper.__parse(t, max_char, None, inoutarg467)
        is_tab = inoutarg467.value
        if (rw is None): 
            return None
        res = list()
        res.append(rw)
        t = rw.end_token.next0
        while t is not None: 
            inoutarg466 = RefOutArgWrapper(is_tab)
            rw0 = TableHelper.__parse(t, max_char, rw, inoutarg466)
            is_tab = inoutarg466.value
            if (rw0 is None): 
                break
            rw = rw0
            res.append(rw)
            t = rw0.end_token
            if (rw0._last_row): 
                break
            t = t.next0
        rla = res[len(res) - 1]
        if (((rla._last_row and len(rla.cells) == 2 and rla.cells[0].col_span == 1) and rla.cells[0].row_span == 1 and rla.cells[1].col_span == 1) and rla.cells[1].row_span == 1): 
            lines0 = rla.cells[0]._lines
            lines1 = rla.cells[1]._lines
            if (len(lines0) > 2 and len(lines1) == len(lines0)): 
                for ii in range(len(lines0)):
                    rw = TableRowToken((lines0[ii].begin_token if ii == 0 else lines1[ii].begin_token), (lines0[ii].end_token if ii == 0 else lines1[ii].end_token))
                    rw.cells.append(lines0[ii])
                    rw.cells.append(lines1[ii])
                    rw._eor = rla._eor
                    if (ii == (len(lines0) - 1)): 
                        rw._last_row = rla._last_row
                        rw.end_token = rla.end_token
                    res.append(rw)
                res.remove(rla)
        for re in res: 
            if (len(re.cells) > 1): 
                return res
        return None
    
    @staticmethod
    def __parse(t : 'Token', max_char : int, prev : 'TableRowToken', is_tab : bool) -> 'TableRowToken':
        from pullenti.ner.core.internal.TableRowToken import TableRowToken
        from pullenti.ner.core.internal.TableCellToken import TableCellToken
        if (t is None or ((t.end_char > max_char and max_char > 0))): 
            return None
        txt = t.kit.sofa.text
        t0 = t
        if (t.is_char(chr(0x1E)) and t.next0 is not None): 
            is_tab.value = True
            t = t.next0
        cell_info = None
        tt = t
        while tt is not None and ((tt.end_char <= max_char or max_char == 0)): 
            if (tt.is_table_control_char): 
                cell_info = TableHelper.TableInfo(tt)
                if (cell_info.typ != TableHelper.TableTypes.CELLEND): 
                    cell_info = None
                break
            elif (tt.is_newline_after): 
                if (not is_tab.value and prev is None): 
                    break
                if ((tt.end_char - t.begin_char) > 100): 
                    if ((tt.end_char - t.begin_char) > 10000): 
                        break
                    if (not is_tab.value): 
                        break
                if (tt.whitespaces_after_count > 15): 
                    if (not is_tab.value): 
                        break
            tt = tt.next0
        if (cell_info is None): 
            return None
        res = TableRowToken(t0, tt)
        res.cells.append(TableCellToken._new468(t, tt, cell_info.row_span, cell_info.col_span))
        tt = tt.next0
        while tt is not None and ((tt.end_char <= max_char or max_char == 0)): 
            t0 = tt
            cell_info = None
            while tt is not None and ((tt.end_char <= max_char or max_char == 0)): 
                if (tt.is_table_control_char): 
                    cell_info = TableHelper.TableInfo(tt)
                    break
                elif (tt.is_newline_after): 
                    if (not is_tab.value and prev is None): 
                        break
                    if ((tt.end_char - t0.begin_char) > 400): 
                        if ((tt.end_char - t0.begin_char) > 20000): 
                            break
                        if (not is_tab.value): 
                            break
                    if (tt.whitespaces_after_count > 15): 
                        if (not is_tab.value): 
                            break
                tt = tt.next0
            if (cell_info is None): 
                break
            if (cell_info.typ == TableHelper.TableTypes.ROWEND and tt == t0): 
                res.end_token = tt
                res._eor = True
                break
            if (cell_info.typ != TableHelper.TableTypes.CELLEND): 
                break
            res.cells.append(TableCellToken._new468(t0, tt, cell_info.row_span, cell_info.col_span))
            res.end_token = tt
            tt = tt.next0
        if ((len(res.cells) < 2) and not res._eor): 
            return None
        if (res.end_token.next0 is not None and res.end_token.next0.is_char(chr(0x1F))): 
            res._last_row = True
            res.end_token = res.end_token.next0
        return res
    
    @staticmethod
    def is_cell_end(t : 'Token') -> bool:
        if (t is not None and t.is_char(chr(7))): 
            return True
        return False
    
    @staticmethod
    def is_row_end(t : 'Token') -> bool:
        if (t is None or not t.is_char(chr(7))): 
            return False
        ti = TableHelper.TableInfo(t)
        return ti.typ == TableHelper.TableTypes.ROWEND