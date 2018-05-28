# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the convertor N2JP from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import typing
from pullenti.ntopy.Utils import Utils
from pullenti.ntopy.Misc import RefOutArgWrapper
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.instrument.InstrumentKind import InstrumentKind
from pullenti.ner.decree.DecreeChangeKind import DecreeChangeKind

from pullenti.ner.instrument.internal.ContentAnalyzeWhapper import ContentAnalyzeWhapper

from pullenti.ner.instrument.internal.NumberTypes import NumberTypes


class ListHelper:
    
    class LineToken(MetaToken):
        
        def __init__(self, b : 'Token', e0 : 'Token') -> None:
            self.is_list_item = False
            self.is_list_head = False
            self.number = 0
            super().__init__(b, e0, None)
        
        def correct_begin_token(self) -> None:
            if (not self.is_list_item): 
                return
            if (self.begin_token.is_hiphen and self.begin_token.next0 is not None): 
                self.begin_token = self.begin_token.next0
            elif ((self.number > 0 and self.begin_token.next0 is not None and self.begin_token.next0.is_char(')')) and self.begin_token.next0.next0 is not None): 
                self.begin_token = self.begin_token.next0.next0
        
        def __str__(self) -> str:
            return "{0}: {1}".format(("LISTITEM" if self.is_list_item else "TEXT"), self.get_source_text())
        
        @staticmethod
        def parse(t : 'Token', max_char : int, prev : 'LineToken') -> 'LineToken':
            from pullenti.ner.decree.DecreeReferent import DecreeReferent
            from pullenti.ner.core.BracketHelper import BracketHelper
            from pullenti.ner.NumberToken import NumberToken
            from pullenti.ner.TextToken import TextToken
            if (t is None or t.end_char > max_char): 
                return None
            res = ListHelper.LineToken(t, t)
            first_pass2777 = True
            while True:
                if first_pass2777: first_pass2777 = False
                else: t = t.next0
                if (not (t is not None and t.end_char <= max_char)): break
                if (t.is_char(':')): 
                    if (res.is_newline_before and res.begin_token.is_value("ПРИЛОЖЕНИЕ", "ДОДАТОК")): 
                        res.is_list_head = True
                    res.end_token = t
                    break
                if (t.is_char(';')): 
                    if (not t.is_whitespace_after): 
                        pass
                    if (t.previous is not None and isinstance(t.previous.get_referent(), DecreeReferent)): 
                        if (not t.is_whitespace_after): 
                            continue
                        if (t.next0 is not None and isinstance(t.next0.get_referent(), DecreeReferent)): 
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
                    next0_ = True
                    if (t.previous.is_comma or t.previous.is_and or t.is_char_of("(")): 
                        next0_ = False
                    elif (t.chars.is_letter or isinstance(t, NumberToken)): 
                        if (t.chars.is_all_lower): 
                            next0_ = False
                        elif (t.previous.chars.is_letter): 
                            next0_ = False
                    if (next0_): 
                        break
                res.end_token = t
            if (res.begin_token.is_hiphen): 
                res.is_list_item = (res.begin_token.next0 is not None and not res.begin_token.next0.is_hiphen)
            elif (res.begin_token.is_char_of("·")): 
                res.is_list_item = True
                res.begin_token = res.begin_token.next0
            elif (res.begin_token.next0 is not None and ((res.begin_token.next0.is_char(')') or ((prev is not None and ((prev.is_list_item or prev.is_list_head))))))): 
                if (res.begin_token.length_char == 1 or isinstance(res.begin_token, NumberToken)): 
                    res.is_list_item = True
                    if (isinstance(res.begin_token, NumberToken)): 
                        res.number = (res.begin_token if isinstance(res.begin_token, NumberToken) else None).value
                    elif (isinstance(res.begin_token, TextToken) and res.begin_token.length_char == 1): 
                        te = (res.begin_token if isinstance(res.begin_token, TextToken) else None).term
                        if (LanguageHelper.is_cyrillic_char(te[0])): 
                            res.number = (ord(te[0]) - ord('А'))
                        elif (LanguageHelper.is_latin_char(te[0])): 
                            res.number = (ord(te[0]) - ord('A'))
            return res
        
        @staticmethod
        def parse_list(t : 'Token', max_char : int, prev : 'LineToken') -> typing.List['LineToken']:
            lt = ListHelper.LineToken.parse(t, max_char, prev)
            if (lt is None): 
                return None
            res = list()
            res.append(lt)
            ss = str(lt)
            t = lt.end_token.next0
            while t is not None: 
                lt0 = ListHelper.LineToken.parse(t, max_char, lt)
                if (lt0 is None): 
                    break
                lt = lt0
                res.append(lt)
                t = lt0.end_token
                t = t.next0
            if ((len(res) < 2) and not res[0].is_list_item): 
                if ((prev is not None and prev.is_list_item and res[0].end_token.is_char('.')) and not res[0].begin_token.chars.is_capital_upper): 
                    res[0].is_list_item = True
                    return res
                return None
            for i in range(len(res)):
                if (res[i].is_list_item): 
                    break
            else: i = len(res)
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
        
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.instrument.internal.FragToken import FragToken
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
        first_pass2778 = True
        while True:
            if first_pass2778: first_pass2778 = False
            else: i += 1
            if (not (i < len(res.children))): break
            if (res.children[i].kind == InstrumentKind.INDENTION and ((res.children[i].end_token.is_char_of(":;") or ((((i + 1) < len(res.children)) and res.children[i + 1].kind == InstrumentKind.EDITIONS and res.children[i + 1].end_token.is_char_of(":;")))))): 
                cou = 1
                list_bullet = chr(0)
                j = (i + 1)
                first_pass2779 = True
                while True:
                    if first_pass2779: first_pass2779 = False
                    else: j += 1
                    if (not (j < len(res.children))): break
                    ch = res.children[j]
                    if (ch.kind == InstrumentKind.COMMENT or ch.kind == InstrumentKind.EDITIONS): 
                        continue
                    if (ch.kind != InstrumentKind.INDENTION): 
                        break
                    if (ch.end_token.is_char_of(";") or ((((j + 1) < len(res.children)) and res.children[j + 1].kind == InstrumentKind.EDITIONS and res.children[j + 1].end_token.is_char(';')))): 
                        cou += 1
                        if (isinstance(ch.begin_token, TextToken) and not ch.chars.is_letter): 
                            list_bullet = ch.kit.get_text_character(ch.begin_char)
                        continue
                    if (ch.end_token.is_char_of(".")): 
                        cou += 1
                        j += 1
                        break
                    if (ch.end_token.is_char_of(":")): 
                        if (ord(list_bullet) != 0 and ch.begin_token.is_char(list_bullet)): 
                            tt = ch.begin_token.next0
                            while tt is not None and (tt.end_char < ch.end_char): 
                                if (tt.previous.is_char('.') and MiscHelper.can_be_start_of_sentence(tt)): 
                                    ch2 = FragToken._new1209(tt, ch.end_token, InstrumentKind.INDENTION, ch.number)
                                    ch.end_token = tt.previous
                                    res.children.insert(j + 1, ch2)
                                    for k in range(j + 1, len(res.children), 1):
                                        if (res.children[k].kind == InstrumentKind.INDENTION): 
                                            res.children[k].number += 1
                                    cou += 1
                                    j += 1
                                    break
                                tt = tt.next0
                        break
                    cou += 1
                    j += 1
                    break
                if (cou < 3): 
                    i = j
                    continue
                if ((i > 0 and not res.children[i].end_token.is_char(':') and res.children[i - 1].kind2 == InstrumentKind.UNDEFINED) and res.children[i - 1].end_token.is_char(':')): 
                    res.children[i - 1].kind2 = InstrumentKind.LISTHEAD
                first_pass2780 = True
                while True:
                    if first_pass2780: first_pass2780 = False
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
        from pullenti.ner.instrument.internal.FragToken import FragToken
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.decree.DecreeChangeReferent import DecreeChangeReferent
        from pullenti.ner.decree.internal.PartToken import PartToken
        from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
        from pullenti.ner.instrument.internal.InstrToken1 import InstrToken1
        
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
            cit = FragToken._new1193(ci.begin_token, ci.end_token, InstrumentKind.CITATION)
            res.children.append(cit)
            if (BracketHelper.is_bracket(cit.begin_token.previous, True)): 
                cit.begin_token = cit.begin_token.previous
            if (BracketHelper.is_bracket(cit.end_token.next0, True)): 
                cit.end_token = cit.end_token.next0
                if (cit.end_token.next0 is not None and cit.end_token.next0.is_char_of(";.")): 
                    cit.end_token = cit.end_token.next0
            res.fill_by_content_children()
            if (res.children[0].has_changes): 
                pass
            cit_kind = InstrumentKind.UNDEFINED
            if (isinstance(ci.tag, DecreeChangeReferent)): 
                dcr = (ci.tag if isinstance(ci.tag, DecreeChangeReferent) else None)
                if (dcr.value is not None and len(dcr.value.new_items) > 0): 
                    mnem = dcr.value.new_items[0]
                    i = mnem.find(' ')
                    if (((i)) > 0): 
                        mnem = mnem[0 : (i)]
                    cit_kind = PartToken._get_instr_kind_by_typ(PartToken._get_type_by_attr_name(mnem))
                elif (len(dcr.owners) > 0 and isinstance(dcr.owners[0], DecreePartReferent) and dcr.kind == DecreeChangeKind.NEW): 
                    pat = (dcr.owners[0] if isinstance(dcr.owners[0], DecreePartReferent) else None)
                    min0 = 0
                    for s in pat.slots: 
                        ty = PartToken._get_type_by_attr_name(s.type_name)
                        if (ty == PartToken.ItemType.UNDEFINED): 
                            continue
                        l_ = PartToken._get_rank(ty)
                        if (l_ == 0): 
                            continue
                        if (l_ > min0 or min0 == 0): 
                            min0 = l_
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
            res._itok = InstrToken1.parse(res.begin_token, True, None, 0, None, False, res.end_char, False)
        lines = ListHelper.LineToken.parse_list(res.begin_token, end_char, None)
        if (lines is None or (len(lines) < 1)): 
            return -1
        ret = 1
        if (res.kind == InstrumentKind.CONTENT): 
            for j in range(ind + 1, len(chi), 1):
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
        if (len(lines) < 2): 
            return -1
        if ((len(lines) > 1 and lines[0].is_list_item and lines[1].is_list_item) and lines[0].number != 1): 
            if (len(lines) == 2 or not lines[2].is_list_item): 
                lines[1].is_list_item = False
                lines[0].is_list_item = lines[1].is_list_item
        for i in range(len(lines)):
            if (lines[i].is_list_item): 
                if (i > 0 and lines[i - 1].is_list_item): 
                    continue
                if (((i + 1) < len(lines)) and lines[i + 1].is_list_item): 
                    pass
                else: 
                    lines[i].is_list_item = False
                    continue
                new_line = False
                for j in range(i + 1, len(lines), 1):
                    if (not lines[j].is_list_item): 
                        break
                    elif (lines[j].is_newline_before): 
                        new_line = True
                else: j = len(lines)
                if (new_line): 
                    continue
                if (i > 0 and lines[i - 1].end_token.is_char(':')): 
                    continue
                for j in range(i, len(lines), 1):
                    if (not lines[j].is_list_item): 
                        break
                    else: 
                        lines[j].is_list_item = False
                else: j = len(lines)
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
                    for j in range(i + 1, len(lines), 1):
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
                    if (not ok or nonum == 0 or (num < 2)): 
                        break
                    lt = lines[i]
                    j = i + 1
                    while j < len(lines): 
                        if (lines[j].number > 0): 
                            lt = lines[j]
                        else: 
                            chli = (lt.tag if isinstance(lt.tag, list) else None)
                            if (chli is None): 
                                chli = list()
                                lt.tag = chli
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
        first_pass2781 = True
        while True:
            if first_pass2781: first_pass2781 = False
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
                    for i in range(i0, len(lines), 1):
                        if (not lines[i].is_list_item): 
                            break
                        else: 
                            lines[i].number = 0
                    else: i = len(lines)
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
            ch = FragToken._new1209(li.begin_token, li.end_token, (InstrumentKind.LISTITEM if li.is_list_item else InstrumentKind.CONTENT), li.number)
            if (ch.kind == InstrumentKind.CONTENT and ch.end_token.is_char(':')): 
                ch.kind = InstrumentKind.LISTHEAD
            res.children.append(ch)
            chli = (li.tag if isinstance(li.tag, list) else None)
            if (chli is not None): 
                for lt in chli: 
                    ch.children.append(FragToken._new1193(lt.begin_token, lt.end_token, InstrumentKind.LISTITEM))
                if (ch.begin_char < ch.children[0].begin_char): 
                    ch.children.insert(0, FragToken._new1193(ch.begin_token, ch.children[0].begin_token.previous, InstrumentKind.CONTENT))
        return ret
    
    @staticmethod
    def correct_app_list(lines : typing.List['InstrToken1']) -> None:
        from pullenti.ner.instrument.internal.InstrToken1 import InstrToken1
        i = 0
        while i < (len(lines) - 1): 
            if ((lines[i].typ == InstrToken1.Types.LINE and len(lines[i].numbers) == 0 and lines[i].begin_token.is_value("ПРИЛОЖЕНИЯ", "ДОДАТОК")) and len(lines[i + 1].numbers) > 0 and lines[i].end_token.is_char(':')): 
                num = 1
                ++ i
                first_pass2782 = True
                while True:
                    if first_pass2782: first_pass2782 = False
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
                        inoutarg1385 = RefOutArgWrapper(None)
                        inoutres1386 = Utils.tryParseInt(lines[i].numbers[0], inoutarg1385)
                        nn = inoutarg1385.value
                        if (inoutres1386): 
                            num = (nn + 1)
                        lines[i].num_typ = NumberTypes.UNDEFINED
                        lines[i].numbers.clear()
            i += 1