# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import typing
import math
from pullenti.ntopy.Utils import Utils
from pullenti.ntopy.Misc import RefOutArgWrapper
from pullenti.ner.instrument.internal.NumberTypes import NumberTypes

from pullenti.ner.instrument.InstrumentKind import InstrumentKind
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.core.NumberHelper import NumberHelper


class NumberingHelper:
    """ Поддержка анализа нумерации """
    
    @staticmethod
    def calc_delta(prev : 'InstrToken1', next0 : 'InstrToken1', can_sub_numbers : bool) -> int:
        """ Разница между двумя номерами
        
        Args:
            prev(InstrToken1): 
            next0(InstrToken1): 
            can_sub_numbers(bool): может быть 1. - 1.1 - 2.
        
        Returns:
            int: больше 0 - отличаются на это число, 0 не стыкуются
        """
        n1 = prev.last_number
        n2 = next0.last_number
        if (next0.last_min_number > 0): 
            n2 = next0.last_min_number
        if (len(prev.numbers) == len(next0.numbers)): 
            if (prev.typ_container_rank > 0 and prev.typ_container_rank == next0.typ_container_rank): 
                pass
            elif (prev.num_typ == next0.num_typ): 
                pass
            else: 
                return 0
            if (len(prev.numbers) > 1): 
                i = 0
                while i < (len(prev.numbers) - 1): 
                    if (prev.numbers[i] != next0.numbers[i]): 
                        return 0
                    i += 1
            if (n1 >= n2): 
                return 0
            return n2 - n1
        if (not can_sub_numbers): 
            return 0
        if ((len(prev.numbers) + 1) == len(next0.numbers) and len(next0.numbers) > 0): 
            if (prev.typ_container_rank > 0 and prev.typ_container_rank == next0.typ_container_rank): 
                pass
            elif (prev.num_typ == NumberTypes.DIGIT and next0.num_typ == NumberTypes.TWODIGITS): 
                pass
            elif (prev.num_typ == NumberTypes.TWODIGITS and next0.num_typ == NumberTypes.THREEDIGITS): 
                pass
            elif (prev.num_typ == NumberTypes.THREEDIGITS and next0.num_typ == NumberTypes.FOURDIGITS): 
                pass
            elif (prev.num_typ == NumberTypes.LETTER and next0.num_typ == NumberTypes.TWODIGITS and next0.numbers[0][0].isalpha()): 
                pass
            else: 
                return 0
            for i in range(len(prev.numbers)):
                if (prev.numbers[i] != next0.numbers[i]): 
                    return 0
            return n2
        if ((len(prev.numbers) - 1) == len(next0.numbers) and len(prev.numbers) > 1): 
            if (prev.typ_container_rank > 0 and prev.typ_container_rank == next0.typ_container_rank): 
                pass
            elif (prev.num_typ == NumberTypes.TWODIGITS): 
                if (next0.num_typ == NumberTypes.DIGIT): 
                    pass
                elif (next0.num_typ == NumberTypes.LETTER and prev.numbers[0][0].isalpha()): 
                    pass
            elif (prev.num_typ == NumberTypes.THREEDIGITS and next0.num_typ == NumberTypes.TWODIGITS): 
                pass
            elif (prev.num_typ == NumberTypes.FOURDIGITS and next0.num_typ == NumberTypes.THREEDIGITS): 
                pass
            else: 
                return 0
            i = 0
            while i < (len(prev.numbers) - 2): 
                if (prev.numbers[i] != next0.numbers[i]): 
                    return 0
                i += 1
            inoutarg1387 = RefOutArgWrapper(None)
            inoutres1388 = Utils.tryParseInt(prev.numbers[len(prev.numbers) - 2], inoutarg1387)
            n1 = inoutarg1387.value
            if (not inoutres1388): 
                if (len(prev.numbers) == 2): 
                    n1 = prev.first_number
                else: 
                    return 0
            if ((n1 + 1) != n2): 
                return 0
            return n2 - n1
        if ((len(prev.numbers) - 2) == len(next0.numbers) and len(prev.numbers) > 2): 
            if (prev.typ_container_rank > 0 and prev.typ_container_rank == next0.typ_container_rank): 
                pass
            elif (prev.num_typ == NumberTypes.THREEDIGITS and next0.num_typ == NumberTypes.DIGIT): 
                pass
            elif (prev.num_typ == NumberTypes.FOURDIGITS and next0.num_typ == NumberTypes.TWODIGITS): 
                pass
            else: 
                return 0
            i = 0
            while i < (len(prev.numbers) - 3): 
                if (prev.numbers[i] != next0.numbers[i]): 
                    return 0
                i += 1
            inoutarg1389 = RefOutArgWrapper(None)
            inoutres1390 = Utils.tryParseInt(prev.numbers[len(prev.numbers) - 3], inoutarg1389)
            n1 = inoutarg1389.value
            if (not inoutres1390): 
                return 0
            if ((n1 + 1) != n2): 
                return 0
            return n2 - n1
        if ((len(prev.numbers) - 3) == len(next0.numbers) and len(prev.numbers) > 3): 
            if (prev.typ_container_rank > 0 and prev.typ_container_rank == next0.typ_container_rank): 
                pass
            elif (prev.num_typ == NumberTypes.FOURDIGITS and next0.num_typ == NumberTypes.DIGIT): 
                pass
            else: 
                return 0
            i = 0
            while i < (len(prev.numbers) - 4): 
                if (prev.numbers[i] != next0.numbers[i]): 
                    return 0
                i += 1
            inoutarg1391 = RefOutArgWrapper(None)
            inoutres1392 = Utils.tryParseInt(prev.numbers[len(prev.numbers) - 4], inoutarg1391)
            n1 = inoutarg1391.value
            if (not inoutres1392): 
                return 0
            if ((n1 + 1) != n2): 
                return 0
            return n2 - n1
        return 0
    
    @staticmethod
    def extract_main_sequence(lines : typing.List['InstrToken1'], check_spec_texts : bool, can_sub_numbers : bool) -> typing.List['InstrToken1']:
        """ Выделить базовую верхоуровневую последовательность номеров (строк, содержащих номера)
        
        Args:
            lines(typing.List[InstrToken1]): исходные строки
            check_spec_texts(bool): проверять ли строки на мусор
            can_sub_numbers(bool): могут ли быть подномера типа 1. - 1.1 - 2.
        
        Returns:
            typing.List[InstrToken1]: null если не нашли или последовательность строк с номерами
        """
        from pullenti.ner.instrument.internal.InstrToken1 import InstrToken1
        res = None
        many_spec_char_lines = 0
        for i in range(len(lines)):
            li = lines[i]
            if (li.all_upper and li.is_standard_title): 
                if (res is not None and len(res) > 0 and res[len(res) - 1].tag is None): 
                    res[len(res) - 1].tag = li
            if (len(li.numbers) == 0): 
                continue
            if (li.last_number == 901): 
                pass
            if (li.num_typ == NumberTypes.LETTER): 
                pass
            if (li.typ != InstrToken1.Types.LINE): 
                continue
            if (res is None): 
                res = list()
                if (len(li.numbers) == 1 and li.numbers[0] == "1" and li.num_typ == NumberTypes.DIGIT): 
                    if ((((i + 1) < len(lines)) and len(lines[i + 1].numbers) == 1 and lines[i + 1].numbers[0] == "1") and lines[i + 1].num_typ == NumberTypes.DIGIT): 
                        for ii in range(i + 2, len(lines), 1):
                            if (lines[ii].num_typ == NumberTypes.ROMAN and len(lines[ii].numbers) > 0): 
                                if (lines[ii].numbers[0] == "2"): 
                                    li.num_typ = NumberTypes.ROMAN
                                break
            else: 
                if (res[0].num_suffix is not None): 
                    if (li.num_suffix is not None and li.num_suffix != res[0].num_suffix): 
                        continue
                if (len(res[0].numbers) != len(li.numbers)): 
                    if (li.begin_token.previous is not None and li.begin_token.previous.is_char(':')): 
                        continue
                    if (res[0].num_suffix is None or NumberingHelper.calc_delta(res[len(res) - 1], li, True) != 1): 
                        continue
                    if (not can_sub_numbers): 
                        if (((i + 1) < len(lines)) and NumberingHelper.calc_delta(res[len(res) - 1], lines[i + 1], False) == 1 and NumberingHelper.calc_delta(li, lines[i + 1], True) == 1): 
                            pass
                        else: 
                            continue
                else: 
                    if (res[0].num_typ == NumberTypes.ROMAN and li.num_typ != NumberTypes.ROMAN): 
                        continue
                    if (res[0].num_typ != NumberTypes.ROMAN and li.num_typ == NumberTypes.ROMAN): 
                        continue
                    if (res[0].num_typ != NumberTypes.LETTER and li.num_typ == NumberTypes.LETTER): 
                        continue
            res.append(li)
            if (li.has_many_spec_chars): 
                many_spec_char_lines += 1
        if (res is None): 
            return None
        if (check_spec_texts): 
            if (many_spec_char_lines > (math.floor(len(res) / 2))): 
                return None
        i = 0
        while i < (len(res) - 1): 
            if (NumberingHelper.calc_delta(res[i], res[i + 1], False) == 2): 
                ii0 = Utils.indexOfList(lines, res[i], 0)
                ii1 = Utils.indexOfList(lines, res[i + 1], ii0)
                j = ii0 + 1
                while j < ii1: 
                    if (len(lines[j].numbers) > 0): 
                        if (NumberingHelper.calc_delta(res[i], lines[j], True) == 1 and NumberingHelper.calc_delta(lines[j], res[i + 1], True) == 1): 
                            res.insert(i + 1, lines[j])
                            break
                    j += 1
            i += 1
        ch = True
        while ch:
            ch = False
            i = 1
            first_pass2783 = True
            while True:
                if first_pass2783: first_pass2783 = False
                else: i += 1
                if (not (i < len(res))): break
                d = NumberingHelper.calc_delta(res[i - 1], res[i], False)
                if (res[i - 1].num_suffix == res[i].num_suffix): 
                    if (d == 1): 
                        continue
                    if (((d > 1 and (d < 20))) or ((d == 0 and res[i - 1].num_typ == res[i].num_typ and len(res[i - 1].numbers) == len(res[i].numbers)))): 
                        if (NumberingHelper.calc_delta(res[i], res[i - 1], False) > 0): 
                            if (res[i - 1].tag is not None and i > 2): 
                                del res[i:i+len(res) - i]
                                ch = True
                                i -= 1
                                continue
                        if ((i + 1) < len(res)): 
                            dd = NumberingHelper.calc_delta(res[i], res[i + 1], False)
                            if (dd == 1): 
                                continue
                            dd = NumberingHelper.calc_delta(res[i - 1], res[i + 1], False)
                            if (dd == 1): 
                                del res[i]
                                i -= 1
                                ch = True
                                continue
                        elif (d > 3): 
                            del res[i]
                            i -= 1
                            ch = True
                        continue
                for j in range(i + 1, len(res), 1):
                    dd = NumberingHelper.calc_delta(res[j - 1], res[j], False)
                    if (dd != 1 and dd != 2): 
                        break
                    if (res[j - 1].num_suffix != res[j].num_suffix): 
                        break
                else: j = len(res)
                if ((d == 0 and NumberingHelper.calc_delta(res[i - 1], res[i], True) == 1 and res[i - 1].num_suffix is not None) and res[i].num_suffix == res[i - 1].num_suffix): 
                    d = 1
                if (d != 1 and j > (i + 1)): 
                    del res[i:i+j - i]
                    i -= 1
                    ch = True
                    continue
                if (d == 1): 
                    if ((i + 1) >= len(res)): 
                        continue
                    dd = NumberingHelper.calc_delta(res[i], res[i + 1], False)
                    if (dd == 1 and res[i - 1].num_suffix == res[i + 1].num_suffix): 
                        if (res[i].num_suffix != res[i - 1].num_suffix): 
                            res[i].num_suffix = res[i - 1].num_suffix
                            res[i].is_num_doubt = False
                            ch = True
                        continue
                if ((i + 1) < len(res)): 
                    dd = NumberingHelper.calc_delta(res[i - 1], res[i + 1], False)
                    if (dd == 1 and res[i - 1].num_suffix == res[i + 1].num_suffix): 
                        if (d == 1 and NumberingHelper.calc_delta(res[i], res[i + 1], True) == 1): 
                            pass
                        else: 
                            del res[i]
                            ch = True
                            continue
                elif (d == 0 or d > 10 or res[i - 1].num_suffix != res[i].num_suffix): 
                    del res[i]
                    ch = True
                    continue
        has_suf = 0
        for r in res: 
            if ((r.num_suffix is not None or r.typ_container_rank > 0 or len(r.numbers) > 1) or r.all_upper or r.num_typ == NumberTypes.ROMAN): 
                has_suf += 1
        if (has_suf == 0): 
            if (len(res) < 5): 
                return None
        if (len(res) >= 2): 
            if (res[0] != lines[0]): 
                tot = res[0].begin_token.begin_char - lines[0].begin_token.begin_char
                tot += (lines[len(lines) - 1].end_token.end_char - res[len(res) - 1].end_token.end_char)
                blk = res[len(res) - 1].end_token.end_char - res[0].begin_token.begin_char
                i = Utils.indexOfList(lines, res[len(res) - 1], 0)
                if (i > 0): 
                    lines1 = list(lines)
                    del lines1[0:0+i + 1]
                    res1 = NumberingHelper.extract_main_sequence(lines1, check_spec_texts, can_sub_numbers)
                    if (res1 is not None and len(res1) > 2): 
                        blk += (res1[len(res1) - 1].end_char - res1[0].begin_char)
                if ((blk * 3) < tot): 
                    if ((blk * 5) < tot): 
                        return None
                    for r in res: 
                        if (not r.all_upper and not r.has_changes): 
                            return None
            if (res[0].last_number == 1 and len(res[0].numbers) == 1): 
                res0 = list()
                res0.append(res[0])
                i = 1
                while i < len(res): 
                    for j in range(i + 1, len(res), 1):
                        if (res[j].last_number == 1 and len(res[j].numbers) == 1): 
                            break
                    else: j = len(res)
                    if ((j - i) < 3): 
                        break
                    j -= 1
                    errs = 0
                    jj = (i + 1)
                    while jj < j: 
                        d = NumberingHelper.calc_delta(res[jj - 1], res[jj], False)
                        if (d == 1): 
                            pass
                        elif (d > 1 and (d < 3)): 
                            errs += 1
                        else: 
                            break
                        jj += 1
                    if ((jj < j) or errs > 1): 
                        break
                    if (j < (len(res) - 1)): 
                        if (NumberingHelper.calc_delta(res0[len(res0) - 1], res[j], False) != 1): 
                            break
                        res0.append(res[j])
                    i = j
                    i += 1
                if (i >= len(res) and len(res0) > 1): 
                    return res0
            if (len(res) > 500): 
                return None
            return res
        if (len(res) == 1 and lines[0] == res[0]): 
            if (has_suf > 0): 
                return res
            if (len(lines) > 1 and len(lines[1].numbers) == (len(lines[0].numbers) + 1)): 
                for i in range(len(lines[0].numbers)):
                    if (lines[1].numbers[i] != lines[0].numbers[i]): 
                        return None
                return res
        return None
    
    @staticmethod
    def create_number(owner : 'FragToken', itok : 'InstrToken1') -> None:
        """ Создать результирующий узел, представляющий номер
        
        Args:
            owner(FragToken): 
            itok(InstrToken1): 
        """
        from pullenti.ner.instrument.internal.FragToken import FragToken
        from pullenti.ner.decree.internal.PartToken import PartToken
        if (itok.num_begin_token is None or itok.num_end_token is None): 
            return
        num = FragToken._new1393(itok.num_begin_token, itok.num_end_token, InstrumentKind.NUMBER, True, itok)
        owner.children.append(num)
        if (itok.num_typ == NumberTypes.TWODIGITS): 
            owner.number = itok.first_number
            owner.sub_number = itok.last_number
        elif (itok.num_typ == NumberTypes.THREEDIGITS): 
            owner.number = itok.first_number
            owner.sub_number = itok.middle_number
            owner.sub_number2 = itok.last_number
        elif (itok.num_typ == NumberTypes.FOURDIGITS and len(itok.numbers) == 4): 
            owner.number = itok.first_number
            owner.sub_number = PartToken.get_number(itok.numbers[1])
            owner.sub_number2 = PartToken.get_number(itok.numbers[2])
            owner.sub_number3 = itok.last_number
        else: 
            owner.number = itok.last_number
        owner.min_number = itok.last_min_number
        owner._itok = itok
    
    @staticmethod
    def parse_number(t : 'Token', res : 'InstrToken1', prev : 'InstrToken1') -> None:
        """ Распарсить нумерацию
        
        Args:
            t(Token): 
            res(InstrToken1): 
        """
        from pullenti.ner.instrument.internal.InstrToken1 import InstrToken1
        from pullenti.ner.ReferentToken import ReferentToken
        NumberingHelper.__parse_number(t, res, prev)
        if ((len(res.numbers) > 0 and res.num_end_token is not None and not res.is_newline_after) and res.num_end_token.next0 is not None and res.num_end_token.next0.is_hiphen): 
            res1 = InstrToken1(res.num_end_token.next0.next0, res.num_end_token.next0.next0)
            NumberingHelper.__parse_number(res1.begin_token, res1, res)
            if (len(res1.numbers) == len(res.numbers)): 
                i = 0
                while i < (len(res.numbers) - 1): 
                    if (res.numbers[i] != res1.numbers[i]): 
                        break
                    i += 1
                if (i >= (len(res.numbers) - 1) and (res.last_number < res1.last_number) and res1.num_end_token is not None): 
                    res.min_number = res.numbers[len(res.numbers) - 1]
                    res.numbers[len(res.numbers) - 1] = res1.numbers[len(res.numbers) - 1]
                    res.num_suffix = res1.num_suffix
                    res.num_end_token = res1.num_end_token
                    res.end_token = res.num_end_token
        if (len(res.numbers) > 0 and res.num_end_token is not None and res.typ == InstrToken1.Types.LINE): 
            tt = res.num_end_token
            ok = True
            if (tt.next0 is not None and tt.next0.is_hiphen): 
                ok = False
            elif (not tt.is_whitespace_after): 
                if (tt.next0 is not None and ((tt.next0.chars.is_capital_upper or tt.next0.chars.is_all_upper or isinstance(tt.next0, ReferentToken)))): 
                    pass
                else: 
                    ok = False
            if (not ok): 
                res.numbers.clear()
                res.num_begin_token = None
                res.num_end_token = res.num_begin_token
    
    @staticmethod
    def __parse_number(t : 'Token', res : 'InstrToken1', prev : 'InstrToken1') -> None:
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.core.NumberExToken import NumberExToken
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.instrument.internal.InstrToken1 import InstrToken1
        if (isinstance(t, NumberToken) and (t if isinstance(t, NumberToken) else None).typ == NumberSpellingType.DIGIT and ((t if isinstance(t, NumberToken) else None).value < 3000)): 
            if (len(res.numbers) >= 4): 
                pass
            if (t.morph.class0.is_adjective and res.typ_container_rank == 0): 
                return
            if (NumberExToken.try_parse_number_with_postfix(t) is not None): 
                return
            if ((t.next0 is not None and (t.whitespaces_after_count < 3) and t.next0.chars.is_letter) and t.next0.chars.is_all_lower): 
                if (not t.is_whitespace_after and t.next0.length_char == 1): 
                    pass
                else: 
                    return
            if (res.num_typ == NumberTypes.UNDEFINED): 
                res.num_typ = NumberTypes.DIGIT
            else: 
                res.num_typ = NumberTypes.COMBO
            if (len(res.numbers) > 0 and t.is_whitespace_before): 
                return
            if (len(res.numbers) == 0): 
                res.num_begin_token = t
            if ((t.next0 is not None and t.next0.is_hiphen and isinstance(t.next0.next0, NumberToken)) and (t.next0.next0 if isinstance(t.next0.next0, NumberToken) else None).value > (t if isinstance(t, NumberToken) else None).value): 
                res.min_number = str((t if isinstance(t, NumberToken) else None).value)
                t = t.next0.next0
            elif (((t.next0 is not None and t.next0.is_char_of(")") and t.next0.next0 is not None) and t.next0.next0.is_hiphen and isinstance(t.next0.next0.next0, NumberToken)) and (t.next0.next0.next0 if isinstance(t.next0.next0.next0, NumberToken) else None).value > (t if isinstance(t, NumberToken) else None).value): 
                res.min_number = str((t if isinstance(t, NumberToken) else None).value)
                t = t.next0.next0.next0
            res.numbers.append(str((t if isinstance(t, NumberToken) else None).value))
            res.num_end_token = t
            res.end_token = res.num_end_token
            res.num_suffix = None
            ttt = t.next0
            first_pass2784 = True
            while True:
                if first_pass2784: first_pass2784 = False
                else: ttt = ttt.next0
                if (not (ttt is not None and (len(res.numbers) < 4))): break
                ok1 = False
                if ((ttt.is_char_of("._") and not ttt.is_whitespace_after and isinstance(ttt.next0, NumberToken)) and (((ttt.next0 if isinstance(ttt.next0, NumberToken) else None).typ == NumberSpellingType.DIGIT or ((((ttt.next0 if isinstance(ttt.next0, NumberToken) else None).typ == NumberSpellingType.WORDS)) and ttt.next0.chars.is_latin_letter and not ttt.is_whitespace_after)))): 
                    ok1 = True
                elif ((ttt.is_char_of("(<") and isinstance(ttt.next0, NumberToken) and ttt.next0.next0 is not None) and ttt.next0.next0.is_char_of(")>")): 
                    ok1 = True
                if (ok1): 
                    ttt = ttt.next0
                    res.numbers.append(str((ttt if isinstance(ttt, NumberToken) else None).value))
                    res.num_typ = (NumberTypes.TWODIGITS if len(res.numbers) == 2 else ((NumberTypes.THREEDIGITS if len(res.numbers) == 3 else NumberTypes.FOURDIGITS)))
                    if ((ttt.next0 is not None and ttt.next0.is_char_of(")>") and ttt.next0.next0 is not None) and ttt.next0.next0.is_char('.')): 
                        ttt = ttt.next0
                    res.num_end_token = ttt
                    res.end_token = res.num_end_token
                    t = res.end_token
                    continue
                if ((isinstance(ttt, TextToken) and ttt.length_char == 1 and ttt.chars.is_letter) and not ttt.is_whitespace_before and len(res.numbers) == 1): 
                    res.numbers.append((ttt if isinstance(ttt, TextToken) else None).term)
                    res.num_typ = NumberTypes.COMBO
                    res.num_end_token = ttt
                    res.end_token = res.num_end_token
                    t = res.end_token
                    continue
                break
            if (t.next0 is not None and t.next0.is_char_of(").")): 
                res.num_suffix = t.next0.get_source_text()
                res.num_end_token = t.next0
                res.end_token = res.num_end_token
                t = res.end_token
            return
        if ((isinstance(t, NumberToken) and (t if isinstance(t, NumberToken) else None).typ == NumberSpellingType.WORDS and res.typ_container_rank > 0) and len(res.numbers) == 0): 
            res.numbers.append(str((t if isinstance(t, NumberToken) else None).value))
            res.num_typ = NumberTypes.DIGIT
            res.num_begin_token = t
            if (t.next0 is not None and t.next0.is_char('.')): 
                t = t.next0
                res.num_suffix = "."
            res.num_end_token = t
            res.end_token = res.num_end_token
            return
        nt = NumberHelper.try_parse_roman(t)
        if ((nt is not None and nt.value == 10 and t.next0 is not None) and t.next0.is_char(')')): 
            nt = None
        if (nt is not None and nt.value == 100): 
            nt = None
        if (nt is not None and nt.typ == NumberSpellingType.ROMAN): 
            if (res.num_typ == NumberTypes.UNDEFINED): 
                res.num_typ = NumberTypes.ROMAN
            else: 
                res.num_typ = NumberTypes.COMBO
            if (len(res.numbers) > 0 and t.is_whitespace_before): 
                return
            if (len(res.numbers) == 0): 
                res.num_begin_token = t
            res.numbers.append(str(nt.value))
            res.num_end_token = nt.end_token
            res.end_token = res.num_end_token
            t = res.end_token
            if (res.num_typ == NumberTypes.ROMAN and ((res.typ == InstrToken1.Types.CHAPTER or res.typ == InstrToken1.Types.SECTION or res.typ == InstrToken1.Types.LINE))): 
                if ((t.next0 is not None and t.next0.is_char_of("._<") and isinstance(t.next0.next0, NumberToken)) and (t.next0.next0 if isinstance(t.next0.next0, NumberToken) else None).typ == NumberSpellingType.DIGIT): 
                    t = t.next0.next0
                    res.numbers.append(str((t if isinstance(t, NumberToken) else None).value))
                    res.num_typ = NumberTypes.TWODIGITS
                    if (t.next0 is not None and t.next0.is_char('>')): 
                        t = t.next0
                    res.num_end_token = t
                    res.end_token = res.num_end_token
                    if ((t.next0 is not None and t.next0.is_char_of("._<") and isinstance(t.next0.next0, NumberToken)) and (t.next0.next0 if isinstance(t.next0.next0, NumberToken) else None).typ == NumberSpellingType.DIGIT): 
                        t = t.next0.next0
                        res.numbers.append(str((t if isinstance(t, NumberToken) else None).value))
                        res.num_typ = NumberTypes.THREEDIGITS
                        if (t.next0 is not None and t.next0.is_char('>')): 
                            t = t.next0
                        res.num_end_token = t
                        res.end_token = res.num_end_token
            if (t.next0 is not None and t.next0.is_char_of(").")): 
                res.num_suffix = t.next0.get_source_text()
                res.num_end_token = t.next0
                res.end_token = res.num_end_token
                t = res.end_token
            return
        if ((isinstance(t, TextToken) and t.length_char == 1 and t.chars.is_letter) and t == res.begin_token): 
            if ((not t.is_whitespace_after and isinstance(t.next0, NumberToken) and t.next0.next0 is not None) and t.next0.next0.is_char('.')): 
                res.num_begin_token = t
                res.num_typ = NumberTypes.DIGIT
                res.numbers.append(str((t.next0 if isinstance(t.next0, NumberToken) else None).value))
                res.num_suffix = ((t if isinstance(t, TextToken) else None).term + ".")
                res.num_end_token = t.next0.next0
                res.end_token = res.num_end_token
                t = res.end_token
                return
            if (t.next0 is not None and t.next0.is_char_of(".)")): 
                if (((t.next0.is_char('.') and isinstance(t.next0.next0, NumberToken) and t.next0.next0.next0 is not None) and t.next0.next0.next0.is_char(')') and not t.next0.is_whitespace_after) and not t.next0.next0.is_whitespace_after): 
                    res.num_typ = NumberTypes.TWODIGITS
                    res.numbers.append((t if isinstance(t, TextToken) else None).term)
                    res.numbers.append(str((t.next0.next0 if isinstance(t.next0.next0, NumberToken) else None).value))
                    res.num_suffix = ")"
                    res.num_begin_token = t
                    res.num_end_token = t.next0.next0.next0
                    res.end_token = res.num_end_token
                    t = res.end_token
                    return
                if (t.next0.is_char('.') and ((t.chars.is_all_upper or isinstance(t.next0.next0, NumberToken)))): 
                    pass
                else: 
                    tmp1 = InstrToken1(t, t.next0)
                    tmp1.numbers.append((t if isinstance(t, TextToken) else None).term)
                    if (tmp1.last_number > 1 and t.next0.is_char_of(".") and ((prev is None or (prev.last_number + 1) != tmp1.last_number))): 
                        pass
                    else: 
                        if (len(res.numbers) == 0): 
                            res.num_begin_token = t
                        res.num_typ = NumberTypes.LETTER
                        res.numbers.append((t if isinstance(t, TextToken) else None).term)
                        res.num_begin_token = t
                        res.num_end_token = t.next0
                        res.end_token = res.num_end_token
                        t = res.end_token
                        res.num_suffix = t.get_source_text()
                        return
    
    @staticmethod
    def correct_child_numbers(root : 'FragToken', children : typing.List['FragToken']) -> bool:
        has_num = False
        if (root.number > 0): 
            for ch in root.children: 
                if (ch.kind == InstrumentKind.NUMBER): 
                    has_num = True
                    break
                elif (ch.kind != InstrumentKind.KEYWORD): 
                    break
        if (not has_num): 
            return False
        if (root.sub_number == 0): 
            ok = True
            for ch in children: 
                if (ch.number > 0): 
                    if (ch.number == root.number and ch.sub_number > 0): 
                        pass
                    else: 
                        ok = False
            if (ok): 
                for ch in children: 
                    if (ch.number > 0): 
                        ch.number = ch.sub_number
                        ch.sub_number = ch.sub_number2
                        ch.sub_number2 = ch.sub_number3
                        ch.sub_number3 = 0
            return ok
        if (root.sub_number > 0 and root.sub_number2 == 0): 
            ok = True
            for ch in children: 
                if (ch.number > 0): 
                    if (ch.number == root.number and ch.sub_number == root.sub_number and ch.sub_number2 > 0): 
                        pass
                    else: 
                        ok = False
            if (ok): 
                for ch in children: 
                    if (ch.number > 0): 
                        ch.number = ch.sub_number2
                        ch.sub_number = ch.sub_number3
                        ch.sub_number3 = 0
                        ch.sub_number2 = ch.sub_number3
            return ok
        if (root.sub_number > 0 and root.sub_number2 > 0 and root.sub_number3 == 0): 
            ok = True
            for ch in children: 
                if (ch.number > 0): 
                    if ((ch.number == root.number and ch.sub_number == root.sub_number and ch.sub_number2 == root.sub_number2) and ch.sub_number3 > 0): 
                        pass
                    else: 
                        ok = False
            if (ok): 
                for ch in children: 
                    if (ch.number > 0): 
                        ch.number = ch.sub_number3
                        ch.sub_number3 = 0
                        ch.sub_number2 = ch.sub_number3
                        ch.sub_number = ch.sub_number2
            return ok
        return False
    
    @staticmethod
    def create_diap(s1 : str, s2 : str) -> typing.List[str]:
        pref = None
        if (s2.startswith(s1)): 
            i = len(s1)
            if (((i + 1) < len(s2)) and s2[i] == '.' and s2[i + 1].isdigit()): 
                inoutarg1394 = RefOutArgWrapper(None)
                inoutres1395 = Utils.tryParseInt(s2[i + 1 : ], inoutarg1394)
                n2 = inoutarg1394.value
                if (inoutres1395): 
                    res0 = list()
                    res0.append(s1)
                    i = 1
                    while i <= n2: 
                        res0.append("{0}.{1}".format(s1, i))
                        i += 1
                    return res0
        i = s1.rfind('.')
        if (((i)) > 0): 
            pref = s1[0 : (i + 1)]
            inoutarg1398 = RefOutArgWrapper(None)
            inoutres1399 = Utils.tryParseInt(s1[i + 1 : ], inoutarg1398)
            n1 = inoutarg1398.value
            if (not inoutres1399): 
                return None
            if (not s2.startswith(pref)): 
                return None
            inoutarg1396 = RefOutArgWrapper(None)
            inoutres1397 = Utils.tryParseInt(s2[i + 1 : ], inoutarg1396)
            n2 = inoutarg1396.value
            if (not inoutres1397): 
                return None
        else: 
            inoutarg1402 = RefOutArgWrapper(None)
            inoutres1403 = Utils.tryParseInt(s1, inoutarg1402)
            n1 = inoutarg1402.value
            if (not inoutres1403): 
                return None
            inoutarg1400 = RefOutArgWrapper(None)
            inoutres1401 = Utils.tryParseInt(s2, inoutarg1400)
            n2 = inoutarg1400.value
            if (not inoutres1401): 
                return None
        if (n2 <= n1): 
            return None
        res = list()
        i = n1
        while i <= n2: 
            if (pref is None): 
                res.append(str(i))
            else: 
                res.append(pref + ((str(i))))
            i += 1
        return res