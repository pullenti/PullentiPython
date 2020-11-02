# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.decree.DecreeReferent import DecreeReferent
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.instrument.internal.InstrToken1 import InstrToken1
from pullenti.ner.instrument.internal.ContentAnalyzeWhapper import ContentAnalyzeWhapper
from pullenti.ner.core.CanBeEqualsAttr import CanBeEqualsAttr
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.instrument.internal.NumberTypes import NumberTypes
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.instrument.InstrumentKind import InstrumentKind
from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
from pullenti.ner.decree.DecreeChangeReferent import DecreeChangeReferent
from pullenti.ner.decree.internal.PartToken import PartToken
from pullenti.ner.decree.DecreeChangeKind import DecreeChangeKind
from pullenti.ner.instrument.internal.FragToken import FragToken

class ListHelper:
    
    class LineToken(MetaToken):
        
        def __init__(self, b : 'Token', e0_ : 'Token') -> None:
            super().__init__(b, e0_, None)
            self.is_list_item = False
            self.is_list_head = False
            self.number = 0
        
        def correct_begin_token(self) -> None:
            if (not self.is_list_item): 
                return
            if (self.begin_token.is_hiphen and self.begin_token.next0_ is not None): 
                self.begin_token = self.begin_token.next0_
            elif ((self.number > 0 and self.begin_token.next0_ is not None and self.begin_token.next0_.is_char(')')) and self.begin_token.next0_.next0_ is not None): 
                self.begin_token = self.begin_token.next0_.next0_
        
        def __str__(self) -> str:
            return "{0}: {1}".format(("LISTITEM" if self.is_list_item else "TEXT"), self.get_source_text())
        
        @staticmethod
        def parse(t : 'Token', max_char : int, prev : 'LineToken') -> 'LineToken':
            from pullenti.morph.LanguageHelper import LanguageHelper
            from pullenti.ner.NumberToken import NumberToken
            from pullenti.ner.TextToken import TextToken
            from pullenti.ner.core.BracketHelper import BracketHelper
            from pullenti.ner.core.BracketParseAttr import BracketParseAttr
            from pullenti.ner.decree.DecreeReferent import DecreeReferent
            if (t is None or t.end_char > max_char): 
                return None
            res = ListHelper.LineToken(t, t)
            first_pass3764 = True
            while True:
                if first_pass3764: first_pass3764 = False
                else: t = t.next0_
                if (not (t is not None and t.end_char <= max_char)): break
                if (t.is_char(':')): 
                    if (res.is_newline_before and res.begin_token.is_value("ПРИЛОЖЕНИЕ", "ДОДАТОК")): 
                        res.is_list_head = True
                    res.end_token = t
                    break
                if (t.is_char(';')): 
                    if (not t.is_whitespace_after): 
                        pass
                    if (t.previous is not None and (isinstance(t.previous.get_referent(), DecreeReferent))): 
                        if (not t.is_whitespace_after): 
                            continue
                        if (t.next0_ is not None and (isinstance(t.next0_.get_referent(), DecreeReferent))): 
                            continue
                    res.is_list_item = True
                    res.end_token = t
                    break
                if (t.is_char('(')): 
                    br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                    if (br is not None): 
                        t = br.end_token
                        res.end_token = t
                        continue
                if (t.is_newline_before and t != res.begin_token): 
                    next0__ = True
                    if (t.previous.is_comma or t.previous.is_and or t.is_char_of("(")): 
                        next0__ = False
                    elif (t.chars.is_letter or (isinstance(t, NumberToken))): 
                        if (t.chars.is_all_lower): 
                            next0__ = False
                        elif (t.previous.chars.is_letter): 
                            next0__ = False
                    if (next0__): 
                        break
                res.end_token = t
            if (res.begin_token.is_hiphen): 
                res.is_list_item = (res.begin_token.next0_ is not None and not res.begin_token.next0_.is_hiphen)
            elif (res.begin_token.is_char_of("·")): 
                res.is_list_item = True
                res.begin_token = res.begin_token.next0_
            elif (res.begin_token.next0_ is not None and ((res.begin_token.next0_.is_char(')') or ((prev is not None and ((prev.is_list_item or prev.is_list_head))))))): 
                if (res.begin_token.length_char == 1 or (isinstance(res.begin_token, NumberToken))): 
                    res.is_list_item = True
                    if ((isinstance(res.begin_token, NumberToken)) and res.begin_token.int_value is not None): 
                        res.number = res.begin_token.int_value
                    elif ((isinstance(res.begin_token, TextToken)) and res.begin_token.length_char == 1): 
                        te = res.begin_token.term
                        if (LanguageHelper.is_cyrillic_char(te[0])): 
                            res.number = ((ord(te[0])) - (ord('А')))
                        elif (LanguageHelper.is_latin_char(te[0])): 
                            res.number = ((ord(te[0])) - (ord('A')))
            return res
        
        @staticmethod
        def parse_list(t : 'Token', max_char : int, prev : 'LineToken') -> typing.List['LineToken']:
            lt = ListHelper.LineToken.parse(t, max_char, prev)
            if (lt is None): 
                return None
            res = list()
            res.append(lt)
            ss = str(lt)
            t = lt.end_token.next0_
            while t is not None: 
                lt0 = ListHelper.LineToken.parse(t, max_char, lt)
                if (lt0 is None): 
                    break
                lt = lt0
                res.append(lt)
                t = lt0.end_token
                t = t.next0_
            if ((len(res) < 2) and not res[0].is_list_item): 
                if ((prev is not None and prev.is_list_item and res[0].end_token.is_char('.')) and not res[0].begin_token.chars.is_capital_upper): 
                    res[0].is_list_item = True
                    return res
                return None
            i = 0
            while i < len(res): 
                if (res[i].is_list_item): 
                    break
                i += 1
            if (i >= len(res)): 
                return None
            cou = 0
            j = i
            while j < len(res): 
                if (not res[j].is_list_item): 
                    if (res[j - 1].is_list_item and res[j].end_token.is_char('.')): 
                        if (res[j].begin_token.get_source_text() == res[i].begin_token.get_source_text() or res[j].begin_token.chars.is_all_lower): 
                            res[j].is_list_item = True
                            j += 1
                            cou += 1
                else: 
                    cou += 1
                j += 1
            return res
    
    @staticmethod
    def analyze(res : 'FragToken') -> None:
        if (res.number == 4): 
            pass
        if (len(res.children) == 0): 
            ki = res.kind
            if (((ki == InstrumentKind.CHAPTER or ki == InstrumentKind.CLAUSE or ki == InstrumentKind.CONTENT) or ki == InstrumentKind.ITEM or ki == InstrumentKind.SUBITEM) or ki == InstrumentKind.CLAUSEPART or ki == InstrumentKind.INDENTION): 
                tmp = list()
                tmp.append(res)
                ListHelper.__analize_list_items(tmp, 0)
            return
        if (res.kind == InstrumentKind.CLAUSE and res.number == 12): 
            pass
        i = 0
        first_pass3765 = True
        while True:
            if first_pass3765: first_pass3765 = False
            else: i += 1
            if (not (i < len(res.children))): break
            if (res.children[i].kind == InstrumentKind.INDENTION and ((res.children[i].end_token.is_char_of(":;") or ((((i + 1) < len(res.children)) and res.children[i + 1].kind == InstrumentKind.EDITIONS and res.children[i + 1].end_token.is_char_of(":;")))))): 
                cou = 1
                list_bullet = chr(0)
                j = (i + 1)
                first_pass3766 = True
                while True:
                    if first_pass3766: first_pass3766 = False
                    else: j += 1
                    if (not (j < len(res.children))): break
                    ch = res.children[j]
                    if (ch.kind == InstrumentKind.COMMENT or ch.kind == InstrumentKind.EDITIONS): 
                        continue
                    if (ch.kind != InstrumentKind.INDENTION): 
                        break
                    if (ch.end_token.is_char_of(";") or ((((j + 1) < len(res.children)) and res.children[j + 1].kind == InstrumentKind.EDITIONS and res.children[j + 1].end_token.is_char(';')))): 
                        cou += 1
                        if ((isinstance(ch.begin_token, TextToken)) and not ch.chars.is_letter): 
                            list_bullet = ch.kit.get_text_character(ch.begin_char)
                        continue
                    if (ch.end_token.is_char_of(".")): 
                        cou += 1
                        j += 1
                        break
                    if (ch.end_token.is_char_of(":")): 
                        if ((ord(list_bullet)) != 0 and ch.begin_token.is_char(list_bullet)): 
                            tt = ch.begin_token.next0_
                            while tt is not None and (tt.end_char < ch.end_char): 
                                if (tt.previous.is_char('.') and MiscHelper.can_be_start_of_sentence(tt)): 
                                    ch2 = FragToken._new1357(tt, ch.end_token, InstrumentKind.INDENTION, ch.number)
                                    ch.end_token = tt.previous
                                    res.children.insert(j + 1, ch2)
                                    k = j + 1
                                    while k < len(res.children): 
                                        if (res.children[k].kind == InstrumentKind.INDENTION): 
                                            res.children[k].number += 1
                                        k += 1
                                    cou += 1
                                    j += 1
                                    break
                                tt = tt.next0_
                        break
                    cou += 1
                    j += 1
                    break
                if (cou < 3): 
                    i = j
                    continue
                if ((i > 0 and not res.children[i].end_token.is_char(':') and res.children[i - 1].kind2 == InstrumentKind.UNDEFINED) and res.children[i - 1].end_token.is_char(':')): 
                    res.children[i - 1].kind2 = InstrumentKind.LISTHEAD
                first_pass3767 = True
                while True:
                    if first_pass3767: first_pass3767 = False
                    else: i += 1
                    if (not (i < j)): break
                    ch = res.children[i]
                    if (ch.kind != InstrumentKind.INDENTION): 
                        continue
                    if (ch.end_token.is_char(':')): 
                        ch.kind2 = InstrumentKind.LISTHEAD
                    elif (((i + 1) < j) and res.children[i + 1].kind == InstrumentKind.EDITIONS and res.children[i + 1].end_token.is_char(':')): 
                        ch.kind2 = InstrumentKind.LISTHEAD
                    else: 
                        ch.kind2 = InstrumentKind.LISTITEM
        changed = list()
        i = 0
        while i < len(res.children): 
            if (res.number == 7): 
                pass
            if (len(res.children[i].children) > 0): 
                ListHelper.analyze(res.children[i])
            else: 
                co = ListHelper.__analize_list_items(res.children, i)
                if (co > 0): 
                    changed.append(res.children[i])
                    if (co > 1): 
                        del res.children[i + 1:i + 1+co - 1]
                    i += (co - 1)
            i += 1
        for i in range(len(changed) - 1, -1, -1):
            if (changed[i].kind == InstrumentKind.CONTENT): 
                j = Utils.indexOfList(res.children, changed[i], 0)
                if (j < 0): 
                    continue
                del res.children[j]
                res.children[j:j] = changed[i].children
    
    @staticmethod
    def __analize_list_items(chi : typing.List['FragToken'], ind : int) -> int:
        if (ind >= len(chi)): 
            return -1
        res = chi[ind]
        ki = res.kind
        if (((ki == InstrumentKind.CHAPTER or ki == InstrumentKind.CLAUSE or ki == InstrumentKind.CONTENT) or ki == InstrumentKind.ITEM or ki == InstrumentKind.SUBITEM) or ki == InstrumentKind.CLAUSEPART or ki == InstrumentKind.INDENTION): 
            pass
        else: 
            return -1
        if (res.has_changes and res.multiline_changes_value is not None): 
            ci = res.multiline_changes_value
            cit = FragToken._new1340(ci.begin_token, ci.end_token, InstrumentKind.CITATION)
            res.children.append(cit)
            if (BracketHelper.is_bracket(cit.begin_token.previous, True)): 
                cit.begin_token = cit.begin_token.previous
            if (BracketHelper.is_bracket(cit.end_token.next0_, True)): 
                cit.end_token = cit.end_token.next0_
                if (cit.end_token.next0_ is not None and cit.end_token.next0_.is_char_of(";.")): 
                    cit.end_token = cit.end_token.next0_
            res.fill_by_content_children()
            if (res.children[0].has_changes): 
                pass
            cit_kind = InstrumentKind.UNDEFINED
            if (isinstance(ci.tag, DecreeChangeReferent)): 
                dcr = Utils.asObjectOrNull(ci.tag, DecreeChangeReferent)
                if (dcr.value is not None and len(dcr.value.new_items) > 0): 
                    mnem = dcr.value.new_items[0]
                    i = mnem.find(' ')
                    if (((i)) > 0): 
                        mnem = mnem[0:0+i]
                    cit_kind = PartToken._get_instr_kind_by_typ(PartToken._get_type_by_attr_name(mnem))
                elif (len(dcr.owners) > 0 and (isinstance(dcr.owners[0], DecreePartReferent)) and dcr.kind == DecreeChangeKind.NEW): 
                    pat = Utils.asObjectOrNull(dcr.owners[0], DecreePartReferent)
                    min0_ = 0
                    for s in pat.slots: 
                        ty = PartToken._get_type_by_attr_name(s.type_name)
                        if (ty == PartToken.ItemType.UNDEFINED): 
                            continue
                        l_ = PartToken._get_rank(ty)
                        if (l_ == 0): 
                            continue
                        if (l_ > min0_ or min0_ == 0): 
                            min0_ = l_
                            cit_kind = PartToken._get_instr_kind_by_typ(ty)
            sub = None
            if (cit_kind != InstrumentKind.UNDEFINED and cit_kind != InstrumentKind.APPENDIX): 
                sub = FragToken(ci.begin_token, ci.end_token)
                wr = ContentAnalyzeWhapper()
                wr.analyze(sub, None, True, cit_kind)
                sub.kind = InstrumentKind.CONTENT
            else: 
                sub = FragToken.create_document(ci.begin_token, ci.end_char, cit_kind)
            if (sub is None or len(sub.children) == 0): 
                pass
            elif ((sub.kind == InstrumentKind.CONTENT and len(sub.children) > 0 and sub.children[0].begin_token == sub.begin_token) and sub.children[len(sub.children) - 1].end_token == sub.end_token): 
                cit.children.extend(sub.children)
            else: 
                cit.children.append(sub)
            return 1
        end_char = res.end_char
        if (res._itok is None): 
            res._itok = InstrToken1.parse(res.begin_token, True, None, 0, None, False, res.end_char, False, False)
        lines = ListHelper.LineToken.parse_list(res.begin_token, end_char, None)
        if (lines is None or (len(lines) < 1)): 
            return -1
        ret = 1
        if (res.kind == InstrumentKind.CONTENT): 
            j = ind + 1
            while j < len(chi): 
                if (chi[j].kind == InstrumentKind.CONTENT): 
                    lines2 = ListHelper.LineToken.parse_list(chi[j].begin_token, chi[j].end_char, lines[len(lines) - 1])
                    if (lines2 is None or (len(lines2) < 1)): 
                        break
                    if (not lines2[0].is_list_item): 
                        if ((len(lines2) > 1 and lines2[1].is_list_item and lines2[0].end_token.is_char_of(":")) and not lines2[0].begin_token.chars.is_capital_upper): 
                            lines2[0].is_list_item = True
                        else: 
                            break
                    lines.extend(lines2)
                    ret = ((j - ind) + 1)
                elif (chi[j].kind != InstrumentKind.EDITIONS and chi[j].kind != InstrumentKind.COMMENT): 
                    break
                j += 1
        if (len(lines) < 2): 
            return -1
        if ((len(lines) > 1 and lines[0].is_list_item and lines[1].is_list_item) and lines[0].number != 1): 
            if (len(lines) == 2 or not lines[2].is_list_item): 
                lines[1].is_list_item = False
                lines[0].is_list_item = lines[1].is_list_item
        i = 0
        first_pass3768 = True
        while True:
            if first_pass3768: first_pass3768 = False
            else: i += 1
            if (not (i < len(lines))): break
            if (lines[i].is_list_item): 
                if (i > 0 and lines[i - 1].is_list_item): 
                    continue
                if (((i + 1) < len(lines)) and lines[i + 1].is_list_item): 
                    pass
                else: 
                    lines[i].is_list_item = False
                    continue
                new_line = False
                j = (i + 1)
                while j < len(lines): 
                    if (not lines[j].is_list_item): 
                        break
                    elif (lines[j].is_newline_before): 
                        new_line = True
                    j += 1
                if (new_line): 
                    continue
                if (i > 0 and lines[i - 1].end_token.is_char(':')): 
                    continue
                j = i
                while j < len(lines): 
                    if (not lines[j].is_list_item): 
                        break
                    else: 
                        lines[j].is_list_item = False
                    j += 1
        if (len(lines) > 2): 
            last = lines[len(lines) - 1]
            last2 = lines[len(lines) - 2]
            if ((not last.is_list_item and last.end_token.is_char('.') and last2.is_list_item) and last2.end_token.is_char(';')): 
                if ((last.length_char < (last2.length_char * 2)) or last.begin_token.chars.is_all_lower): 
                    last.is_list_item = True
        i = 0
        while i < (len(lines) - 1): 
            if (not lines[i].is_list_item and not lines[i + 1].is_list_item): 
                if (((i + 2) < len(lines)) and lines[i + 2].is_list_item and lines[i + 1].end_token.is_char(':')): 
                    pass
                else: 
                    lines[i].end_token = lines[i + 1].end_token
                    del lines[i + 1]
                    i -= 1
            i += 1
        i = 0
        while i < (len(lines) - 1): 
            if (lines[i].is_list_item): 
                if (lines[i].number == 1): 
                    ok = True
                    num = 1
                    nonum = 0
                    j = i + 1
                    while j < len(lines): 
                        if (not lines[j].is_list_item): 
                            ok = False
                            break
                        elif (lines[j].number > 0): 
                            num += 1
                            if (lines[j].number != num): 
                                ok = False
                                break
                        else: 
                            nonum += 1
                        j += 1
                    if (not ok or nonum == 0 or (num < 2)): 
                        break
                    lt = lines[i]
                    j = i + 1
                    while j < len(lines): 
                        if (lines[j].number > 0): 
                            lt = lines[j]
                        else: 
                            chli = Utils.asObjectOrNull(lt.tag, list)
                            if (chli is None): 
                                chli = list()
                                lt.tag = (chli)
                            lt.end_token = lines[j].end_token
                            chli.append(lines[j])
                            del lines[j]
                            j -= 1
                        j += 1
            i += 1
        cou = 0
        for li in lines: 
            if (li.is_list_item): 
                cou += 1
        if (cou < 2): 
            return -1
        i = 0
        first_pass3769 = True
        while True:
            if first_pass3769: first_pass3769 = False
            else: i += 1
            if (not (i < len(lines))): break
            if (lines[i].is_list_item): 
                i0 = i
                ok = True
                cou = 1
                while i < len(lines): 
                    if (not lines[i].is_list_item): 
                        break
                    elif (lines[i].number != cou): 
                        ok = False
                    i += 1; cou += 1
                if (not ok): 
                    i = i0
                    while i < len(lines): 
                        if (not lines[i].is_list_item): 
                            break
                        else: 
                            lines[i].number = 0
                        i += 1
                if (cou > 3 and lines[i0].begin_token.get_source_text() != lines[i0 + 1].begin_token.get_source_text() and lines[i0 + 1].begin_token.get_source_text() == lines[i0 + 2].begin_token.get_source_text()): 
                    pref = lines[i0 + 1].begin_token.get_source_text()
                    ok = True
                    j = i0 + 2
                    while j < i: 
                        if (pref != lines[j].begin_token.get_source_text()): 
                            ok = False
                            break
                        j += 1
                    if (not ok): 
                        continue
                    tt = None
                    ok = False
                    tt = lines[i0].end_token.previous
                    while tt is not None and tt != lines[i0].begin_token: 
                        if (tt.get_source_text() == pref): 
                            ok = True
                            break
                        tt = tt.previous
                    if (ok): 
                        li0 = ListHelper.LineToken(lines[i0].begin_token, tt.previous)
                        lines[i0].begin_token = tt
                        lines.insert(i0, li0)
                        i += 1
        for li in lines: 
            li.correct_begin_token()
            ch = FragToken._new1357(li.begin_token, li.end_token, (InstrumentKind.LISTITEM if li.is_list_item else InstrumentKind.CONTENT), li.number)
            if (ch.kind == InstrumentKind.CONTENT and ch.end_token.is_char(':')): 
                ch.kind = InstrumentKind.LISTHEAD
            res.children.append(ch)
            chli = Utils.asObjectOrNull(li.tag, list)
            if (chli is not None): 
                for lt in chli: 
                    ch.children.append(FragToken._new1340(lt.begin_token, lt.end_token, InstrumentKind.LISTITEM))
                if (ch.begin_char < ch.children[0].begin_char): 
                    ch.children.insert(0, FragToken._new1340(ch.begin_token, ch.children[0].begin_token.previous, InstrumentKind.CONTENT))
        return ret
    
    @staticmethod
    def correct_app_list(lines : typing.List['InstrToken1']) -> None:
        i = 0
        while i < (len(lines) - 1): 
            if ((lines[i].typ == InstrToken1.Types.LINE and len(lines[i].numbers) == 0 and lines[i].begin_token.is_value("ПРИЛОЖЕНИЯ", "ДОДАТОК")) and len(lines[i + 1].numbers) > 0 and lines[i].end_token.is_char(':')): 
                num = 1
                i += 1
                first_pass3770 = True
                while True:
                    if first_pass3770: first_pass3770 = False
                    else: i += 1
                    if (not (i < len(lines))): break
                    if (len(lines[i].numbers) == 0): 
                        if (((i + 1) < len(lines)) and len(lines[i + 1].numbers) == 1 and lines[i + 1].numbers[0] == str(num)): 
                            lines[i - 1].end_token = lines[i].end_token
                            del lines[i]
                            i -= 1
                            continue
                        break
                    else: 
                        wrapnn1549 = RefOutArgWrapper(0)
                        inoutres1550 = Utils.tryParseInt(lines[i].numbers[0], wrapnn1549)
                        nn = wrapnn1549.value
                        if (inoutres1550): 
                            num = (nn + 1)
                        lines[i].num_typ = NumberTypes.UNDEFINED
                        lines[i].numbers.clear()
            i += 1
    
    @staticmethod
    def correct_index(lines : typing.List['InstrToken1']) -> None:
        if (len(lines) < 10): 
            return
        if (lines[0].typ == InstrToken1.Types.CLAUSE or lines[0].typ == InstrToken1.Types.CHAPTER): 
            pass
        else: 
            return
        index = list()
        index.append(lines[0])
        content = list()
        ind_text = 0
        con_text = 0
        i = 1
        while i < len(lines): 
            if (lines[i].typ == lines[0].typ): 
                if (ListHelper.__can_be_equals(lines[i], lines[0])): 
                    break
                else: 
                    index.append(lines[i])
            else: 
                ind_text += lines[i].length_char
            i += 1
        cind = i
        while i < len(lines): 
            if (lines[i].typ == lines[0].typ): 
                content.append(lines[i])
            else: 
                con_text += lines[i].length_char
            i += 1
        if (len(index) == len(content) and len(index) > 2): 
            if ((ind_text * 10) < con_text): 
                lines[0] = InstrToken1._new1551(lines[0].begin_token, lines[cind - 1].end_token, True, InstrToken1.Types.INDEX)
                del lines[1:1+cind - 1]
    
    @staticmethod
    def __can_be_equals(i1 : 'InstrToken1', i2 : 'InstrToken1') -> bool:
        if (i1.typ != i2.typ): 
            return False
        if (len(i1.numbers) > 0 and len(i2.numbers) > 0): 
            if (len(i1.numbers) != len(i2.numbers)): 
                return False
            i = 0
            while i < len(i1.numbers): 
                if (i1.numbers[i] != i2.numbers[i]): 
                    return False
                i += 1
        if (not MiscHelper.can_be_equals_ex(i1.value, i2.value, Utils.valToEnum((CanBeEqualsAttr.IGNORENONLETTERS) | (CanBeEqualsAttr.IGNOREUPPERCASE), CanBeEqualsAttr))): 
            return False
        return True