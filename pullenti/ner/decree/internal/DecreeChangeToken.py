# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.decree.internal.DecreeChangeTokenTyp import DecreeChangeTokenTyp
from pullenti.ner.decree.DecreeChangeKind import DecreeChangeKind
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.decree.DecreeChangeValueKind import DecreeChangeValueKind
from pullenti.ner.instrument.internal.NumberingHelper import NumberingHelper
from pullenti.ner.decree.DecreeChangeReferent import DecreeChangeReferent


class DecreeChangeToken(MetaToken):
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        from pullenti.ner.decree.internal.PartToken import PartToken
        super().__init__(b, e0_, None)
        self.typ = DecreeChangeTokenTyp.UNDEFINED
        self.decree = None;
        self.decree_tok = None;
        self.parts = None;
        self.new_parts = None;
        self.real_part = None;
        self.change_val = None;
        self.has_name = False
        self.has_text = False
        self.act_kind = DecreeChangeKind.UNDEFINED
        self.part_typ = PartToken.ItemType.UNDEFINED
    
    def __str__(self) -> str:
        from pullenti.ner.decree.internal.PartToken import PartToken
        from pullenti.morph.MorphLang import MorphLang
        tmp = io.StringIO()
        print(Utils.enumToString(self.typ), end="", file=tmp)
        if (self.act_kind != DecreeChangeKind.UNDEFINED): 
            print(" Kind={0}".format(Utils.enumToString(self.act_kind)), end="", file=tmp, flush=True)
        if (self.has_name): 
            print(" HasName", end="", file=tmp)
        if (self.has_text): 
            print(" HasText", end="", file=tmp)
        if (self.parts is not None): 
            for p in self.parts: 
                print(" {0}".format(p), end="", file=tmp, flush=True)
        if (self.real_part is not None): 
            print(" RealPart={0}".format(str(self.real_part)), end="", file=tmp, flush=True)
        if (self.new_parts is not None): 
            for p in self.new_parts: 
                print(" New={0}".format(p), end="", file=tmp, flush=True)
        if (self.part_typ != PartToken.ItemType.UNDEFINED): 
            print(" PTyp={0}".format(Utils.enumToString(self.part_typ)), end="", file=tmp, flush=True)
        if (self.decree_tok is not None): 
            print(" DecTok={0}".format(str(self.decree_tok)), end="", file=tmp, flush=True)
        if (self.decree is not None): 
            print(" Ref={0}".format(self.decree.toString(True, MorphLang(), 0)), end="", file=tmp, flush=True)
        if (self.change_val is not None): 
            print(" ChangeVal={0}".format(self.change_val.toString(True, MorphLang(), 0)), end="", file=tmp, flush=True)
        return Utils.toStringStringIO(tmp)
    
    @property
    def is_start(self) -> bool:
        return self.typ == DecreeChangeTokenTyp.STARTSINGLE or self.typ == DecreeChangeTokenTyp.STARTMULTU or self.typ == DecreeChangeTokenTyp.SINGLE
    
    @staticmethod
    def tryAttach(t : 'Token', main : 'DecreeChangeReferent'=None, ignore_newlines : bool=False, change_stack : typing.List['Referent']=None, is_in_edition : bool=False) -> 'DecreeChangeToken':
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.decree.internal.PartToken import PartToken
        from pullenti.ner.decree.DecreeReferent import DecreeReferent
        from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
        from pullenti.ner.decree.internal.DecreeToken import DecreeToken
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        from pullenti.morph.MorphClass import MorphClass
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.decree.DecreeChangeValueReferent import DecreeChangeValueReferent
        from pullenti.ner.instrument.internal.InstrToken1 import InstrToken1
        if (t is None): 
            return None
        tt = t
        if (t.is_newline_before and not ignore_newlines): 
            tt = t
            first_pass2837 = True
            while True:
                if first_pass2837: first_pass2837 = False
                else: tt = tt.next0_
                if (not (tt is not None)): break
                if (tt == t and BracketHelper.isBracket(tt, False) and not tt.isChar('(')): 
                    break
                elif ((tt == t and (isinstance(tt, TextToken)) and (((Utils.asObjectOrNull(tt, TextToken)).term == "СТАТЬЯ" or (Utils.asObjectOrNull(tt, TextToken)).term == "СТАТТЯ"))) and (isinstance(tt.next0_, NumberToken))): 
                    tt1 = tt.next0_.next0_
                    if (tt1 is not None and tt1.isChar('.')): 
                        tt1 = tt1.next0_
                        if (tt1 is not None and not tt1.is_newline_before and tt1.isValue("ВНЕСТИ", "УНЕСТИ")): 
                            continue
                        if (tt1 is not None and tt1.is_newline_before): 
                            return None
                        tt = tt1
                    break
                elif (tt == t and PartToken.tryAttach(tt, None, False, False) is not None): 
                    break
                elif ((isinstance(tt, NumberToken)) and (Utils.asObjectOrNull(tt, NumberToken)).typ == NumberSpellingType.DIGIT): 
                    if ((Utils.asObjectOrNull(tt, NumberToken)).value == (98)): 
                        pass
                elif (tt.is_hiphen): 
                    pass
                elif ((isinstance(tt, TextToken)) and not tt.chars.is_letter and not tt.is_whitespace_before): 
                    pass
                elif (((isinstance(tt, TextToken)) and tt.length_char == 1 and (isinstance(tt.next0_, TextToken))) and not tt.next0_.chars.is_letter): 
                    pass
                else: 
                    break
        if (tt is None): 
            return None
        res = None
        if (((isinstance(tt, TextToken)) and t.is_newline_before and not ignore_newlines) and tt.isValue("ВНЕСТИ", "УНЕСТИ") and ((((tt.next0_ is not None and tt.next0_.isValue("В", "ДО"))) or (Utils.asObjectOrNull(tt, TextToken)).term == "ВНЕСТИ" or (Utils.asObjectOrNull(tt, TextToken)).term == "УНЕСТИ"))): 
            res = DecreeChangeToken._new793(tt, tt, DecreeChangeTokenTyp.STARTMULTU)
            if (tt.next0_ is not None and tt.next0_.isValue("В", "ДО")): 
                tt = tt.next0_
                res.end_token = tt
            has_change = False
            tt = tt.next0_
            first_pass2838 = True
            while True:
                if first_pass2838: first_pass2838 = False
                else: tt = tt.next0_
                if (not (tt is not None)): break
                if (tt.is_newline_before): 
                    break
                if (isinstance(tt.getReferent(), DecreeReferent)): 
                    if (res.decree is not None and tt.getReferent() != res.decree): 
                        break
                    res.decree = (Utils.asObjectOrNull(tt.getReferent(), DecreeReferent))
                    res.end_token = tt
                    continue
                li = PartToken.tryAttachList(tt, False, 40)
                if (li is not None and len(li) > 0): 
                    res.parts = li
                    res.end_token = li[len(li) - 1].end_token
                    tt = res.end_token
                    continue
                if (tt.isChar('(')): 
                    br = BracketHelper.tryParse(tt, BracketParseAttr.NO, 100)
                    if (br is not None): 
                        tt = br.end_token
                        continue
                if (tt.is_newline_before): 
                    break
                res.end_token = tt
                if (tt.isChar(',') and has_change): 
                    res.typ = DecreeChangeTokenTyp.STARTSINGLE
                    break
                if (tt.isValue("ИЗМЕНЕНИЕ", "ЗМІНА") or tt.isValue("ДОПОЛНЕНИЕ", "ДОДАТОК")): 
                    has_change = True
                elif (tt.isValue("СЛЕДУЮЩИЙ", "НАСТУПНИЙ")): 
                    pass
                elif (tt.isValue("ТАКОЙ", "ТАКИЙ")): 
                    pass
            if (not has_change): 
                return None
            if (res.decree is None): 
                return None
            tt = res.end_token.next0_
            if (res.typ == DecreeChangeTokenTyp.STARTSINGLE and res.parts is None and tt is not None): 
                if ((tt.isValue("ИЗЛОЖИВ", "ВИКЛАВШИ") or tt.isValue("ДОПОЛНИВ", "ДОПОВНИВШИ") or tt.isValue("ИСКЛЮЧИВ", "ВИКЛЮЧИВШИ")) or tt.isValue("ЗАМЕНИВ", "ЗАМІНИВШИ")): 
                    tt = tt.next0_
                    if (tt is not None and tt.morph.class0_.is_preposition): 
                        tt = tt.next0_
                    res.parts = PartToken.tryAttachList(tt, False, 40)
                    if (res.parts is not None): 
                        tt = res.end_token.next0_
                        if (tt.isValue("ДОПОЛНИВ", "ДОПОВНИВШИ")): 
                            res.act_kind = DecreeChangeKind.APPEND
                        elif (tt.isValue("ИСКЛЮЧИВ", "ВИКЛЮЧИВШИ")): 
                            res.act_kind = DecreeChangeKind.REMOVE
                        elif (tt.isValue("ИЗЛОЖИВ", "ВИКЛАВШИ")): 
                            res.act_kind = DecreeChangeKind.NEW
                        elif (tt.isValue("ЗАМЕНИВ", "ЗАМІНИВШИ")): 
                            res.act_kind = DecreeChangeKind.EXCHANGE
                        res.end_token = res.parts[len(res.parts) - 1]
            return res
        if (((not ignore_newlines and t.is_newline_before and ((tt.isValue("ПРИЗНАТЬ", "ВИЗНАТИ") or tt.isValue("СЧИТАТЬ", "ВВАЖАТИ")))) and tt.next0_ is not None and tt.next0_.isValue("УТРАТИТЬ", "ВТРАТИТИ")) and tt.next0_.next0_ is not None and tt.next0_.next0_.isValue("СИЛА", "ЧИННІСТЬ")): 
            res = DecreeChangeToken._new794(tt, tt.next0_.next0_, DecreeChangeTokenTyp.ACTION, DecreeChangeKind.EXPIRE)
            tt = tt.next0_.next0_.next0_
            first_pass2839 = True
            while True:
                if first_pass2839: first_pass2839 = False
                else: tt = tt.next0_
                if (not (tt is not None)): break
                if (tt.isChar(':')): 
                    res.typ = DecreeChangeTokenTyp.STARTMULTU
                    res.end_token = tt
                    break
                if (isinstance(tt.getReferent(), DecreeReferent)): 
                    if (res.decree is not None): 
                        break
                    res.typ = DecreeChangeTokenTyp.STARTSINGLE
                    res.decree = (Utils.asObjectOrNull(tt.getReferent(), DecreeReferent))
                    res.end_token = tt
                    continue
                li = PartToken.tryAttachList(tt, False, 40)
                if (li is not None and len(li) > 0): 
                    if (res.parts is not None): 
                        break
                    res.typ = DecreeChangeTokenTyp.STARTSINGLE
                    res.parts = li
                    res.end_token = li[len(li) - 1].end_token
                    tt = res.end_token
                    continue
                if (tt.isChar('(')): 
                    br = BracketHelper.tryParse(tt, BracketParseAttr.NO, 100)
                    if (br is not None): 
                        tt = br.end_token
                        continue
                if (tt.is_newline_before): 
                    break
            return res
        if ((not ignore_newlines and ((t.is_newline_before or tt == t)) and tt.isValue("УТРАТИТЬ", "ВТРАТИТИ")) and tt.next0_ is not None and tt.next0_.isValue("СИЛА", "ЧИННІСТЬ")): 
            res = DecreeChangeToken._new793(tt, tt.next0_, DecreeChangeTokenTyp.UNDEFINED)
            tt = tt.next0_
            while tt is not None: 
                res.end_token = tt
                if (tt.is_newline_after): 
                    break
                tt = tt.next0_
            return res
        if (not ignore_newlines and t.is_newline_before): 
            if (tt.isValue("СЛОВО", None)): 
                pass
            res = DecreeChangeToken._new793(tt, tt, DecreeChangeTokenTyp.STARTSINGLE)
            first_pass2840 = True
            while True:
                if first_pass2840: first_pass2840 = False
                else: tt = tt.next0_
                if (not (tt is not None)): break
                if (tt != t and tt.is_newline_before): 
                    break
                if (tt.isValue("К", None) or tt.isValue("В", None) or tt.isValue("ИЗ", None)): 
                    continue
                if (tt.isValue("ПЕРЕЧЕНЬ", "ПЕРЕЛІК") and tt.next0_ is not None and tt.next0_.isValue("ИЗМЕНЕНИЕ", "ЗМІНА")): 
                    if (tt == t): 
                        res.begin_token = res.end_token = tt.next0_
                    tt = tt.next0_.next0_
                    res.typ = DecreeChangeTokenTyp.STARTMULTU
                    if (tt is not None and tt.isChar(',')): 
                        tt = tt.next0_
                    if (tt is not None and tt.isValue("ВНОСИМЫЙ", "ВНЕСЕНИЙ")): 
                        tt = tt.next0_
                    if (tt is None): 
                        break
                    continue
                if (tt.isValue("НАИМЕНОВАНИЕ", "НАЙМЕНУВАННЯ") or tt.isValue("НАЗВАНИЕ", "НАЗВА")): 
                    res.end_token = tt
                    if ((tt.next0_ is not None and tt.next0_.is_and and tt.next0_.next0_ is not None) and tt.next0_.next0_.isValue("ТЕКСТ", None)): 
                        res.has_text = True
                        tt = tt.next0_.next0_
                        res.end_token = tt
                    res.has_name = True
                    continue
                if (tt.isValue("ТЕКСТ", None)): 
                    pt = PartToken.tryAttach(tt.next0_, None, False, True)
                    if (pt is not None and pt.end_token.next0_ is not None and pt.end_token.next0_.isValue("СЧИТАТЬ", "ВВАЖАТИ")): 
                        res.end_token = pt.end_token
                        if (change_stack is not None and len(change_stack) > 0 and (isinstance(change_stack[0], DecreePartReferent))): 
                            res.real_part = (Utils.asObjectOrNull(change_stack[0], DecreePartReferent))
                        res.act_kind = DecreeChangeKind.CONSIDER
                        res.part_typ = pt.typ
                        res.has_text = True
                        return res
                if ((res.parts is None and not res.has_name and tt.isValue("ДОПОЛНИТЬ", "ДОПОВНИТИ")) and tt.next0_ is not None): 
                    res.act_kind = DecreeChangeKind.APPEND
                    tt1 = DecreeToken.isKeyword(tt.next0_, False)
                    if (tt1 is None or tt1.morph.case_.is_instrumental): 
                        tt1 = tt.next0_
                    else: 
                        tt1 = tt1.next0_
                    if (tt1 is not None and tt1.isValue("НОВЫЙ", "НОВИЙ")): 
                        tt1 = tt1.next0_
                    if (tt1 is not None and tt1.morph.case_.is_instrumental): 
                        pt = PartToken.tryAttach(tt1, None, False, False)
                        if (pt is None): 
                            pt = PartToken.tryAttach(tt1, None, False, True)
                        if (pt is not None and pt.typ != PartToken.ItemType.PREFIX): 
                            res.part_typ = pt.typ
                            res.end_token = pt.end_token
                            tt = res.end_token
                            if (res.new_parts is None): 
                                res.new_parts = list()
                            res.new_parts.append(pt)
                            if (tt.next0_ is not None and tt.next0_.is_and): 
                                pt = PartToken.tryAttach(tt.next0_.next0_, None, False, False)
                                if (pt is None): 
                                    pt = PartToken.tryAttach(tt.next0_.next0_, None, False, True)
                                if (pt is not None): 
                                    res.new_parts.append(pt)
                                    res.end_token = pt.end_token
                                    tt = res.end_token
                        continue
                li = PartToken.tryAttachList(tt, False, 40)
                if (li is None and tt.isValue("ПРИМЕЧАНИЕ", "ПРИМІТКА")): 
                    li = list()
                    li.append(PartToken._new797(tt, tt, PartToken.ItemType.NOTICE))
                if (li is not None and len(li) > 0 and li[0].typ == PartToken.ItemType.PREFIX): 
                    li = (None)
                if (li is not None and len(li) > 0): 
                    if (len(li) == 1 and PartToken._getRank(li[0].typ) > 0 and tt == t): 
                        if (li[0].is_newline_after): 
                            return None
                        if (li[0].end_token.next0_ is not None and li[0].end_token.next0_.isChar('.')): 
                            return None
                    if (res.act_kind != DecreeChangeKind.APPEND): 
                        if (res.parts is not None): 
                            break
                        res.parts = li
                    res.end_token = li[len(li) - 1].end_token
                    tt = res.end_token
                    continue
                if ((tt.morph.class0_.is_noun and change_stack is not None and len(change_stack) > 0) and (isinstance(change_stack[0], DecreePartReferent))): 
                    pa = PartToken.tryAttach(tt, None, False, True)
                    if (pa is not None): 
                        if (change_stack[0].getStringValue(PartToken._getAttrNameByTyp(pa.typ)) is not None): 
                            res.real_part = (Utils.asObjectOrNull(change_stack[0], DecreePartReferent))
                            res.end_token = tt
                            continue
                if (res.act_kind == DecreeChangeKind.APPEND): 
                    pa = PartToken.tryAttach(tt, None, False, True)
                    if (pa is not None): 
                        if (res.new_parts is None): 
                            res.new_parts = list()
                        res.new_parts.append(pa)
                        res.end_token = pa.end_token
                        continue
                if (isinstance(tt.getReferent(), DecreeReferent)): 
                    res.decree = (Utils.asObjectOrNull(tt.getReferent(), DecreeReferent))
                    res.end_token = tt
                    if (tt.next0_ is not None and tt.next0_.isChar('(')): 
                        br = BracketHelper.tryParse(tt.next0_, BracketParseAttr.NO, 100)
                        if (br is not None): 
                            tt = br.end_token
                            res.end_token = tt
                    continue
                pt0 = PartToken.tryAttach(tt, None, False, True)
                if (pt0 is not None and ((res.has_name or pt0.typ == PartToken.ItemType.APPENDIX)) and pt0.typ != PartToken.ItemType.PREFIX): 
                    res.end_token = pt0.end_token
                    tt = res.end_token
                    res.part_typ = pt0.typ
                    if (pt0.typ == PartToken.ItemType.APPENDIX and res.parts is None): 
                        res.parts = list()
                        res.parts.append(pt0)
                    continue
                if (res.change_val is None and not is_in_edition): 
                    res1 = None
                    if (tt == res.begin_token and BracketHelper.canBeStartOfSequence(tt, False, False)): 
                        pass
                    else: 
                        res1 = DecreeChangeToken.tryAttach(tt, main, True, None, False)
                    if (res1 is not None and res1.typ == DecreeChangeTokenTyp.VALUE and res1.change_val is not None): 
                        res.change_val = res1.change_val
                        if (res.act_kind == DecreeChangeKind.UNDEFINED): 
                            res.act_kind = res1.act_kind
                        res.end_token = res1.end_token
                        tt = res.end_token
                        if (tt.next0_ is not None and tt.next0_.isValue("К", None)): 
                            tt = tt.next0_
                        continue
                    if (tt.isValue("ПОСЛЕ", "ПІСЛЯ")): 
                        pt0 = PartToken.tryAttach(tt.next0_, None, True, False)
                        if (pt0 is not None and pt0.typ != PartToken.ItemType.PREFIX): 
                            if (res.parts is None): 
                                res.parts = list()
                                res.parts.append(pt0)
                            res.end_token = pt0.end_token
                            tt = res.end_token
                            continue
                    if (tt.isValue("ТЕКСТ", None) and tt.previous is not None and tt.previous.isValue("В", "У")): 
                        continue
                    if (tt.isValue("ИЗМЕНЕНИЕ", "ЗМІНА")): 
                        res.end_token = tt
                        continue
                if (tt != t and ((res.has_name or res.parts is not None)) and res.decree is None): 
                    dts = DecreeToken.tryAttachList(tt, None, 10, False)
                    if (dts is not None and len(dts) > 0 and dts[0].typ == DecreeToken.ItemType.TYP): 
                        res.end_token = dts[len(dts) - 1].end_token
                        tt = res.end_token
                        if (main is not None and res.decree is None and res.decree_tok is None): 
                            dec = None
                            for v in main.owners: 
                                if (isinstance(v, DecreeReferent)): 
                                    dec = (Utils.asObjectOrNull(v, DecreeReferent))
                                    break
                                elif (isinstance(v, DecreePartReferent)): 
                                    dec = (Utils.asObjectOrNull(v, DecreePartReferent)).owner
                                    if (dec is not None): 
                                        break
                            if (dec is not None and dec.typ0 == dts[0].value): 
                                res.decree = dec
                                res.decree_tok = dts[0]
                        continue
                if (tt == res.begin_token and main is not None): 
                    npt = NounPhraseHelper.tryParse(tt, NounPhraseParseAttr.NO, 0)
                    if (npt is not None): 
                        tt1 = npt.end_token.next0_
                        if ((tt1 is not None and tt1.isValue("ИЗЛОЖИТЬ", "ВИКЛАСТИ") and tt1.next0_ is not None) and tt1.next0_.isValue("В", None)): 
                            pt = PartToken._new797(tt, npt.end_token, PartToken.ItemType.APPENDIX)
                            pt.name = npt.getNormalCaseText(MorphClass(), False, MorphGender.UNDEFINED, False)
                            res.parts = list()
                            res.parts.append(pt)
                            res.end_token = pt.end_token
                            break
                ttt = DecreeToken.isKeyword(tt, False)
                if (ttt is not None and res.parts is None): 
                    ttt0 = ttt
                    while ttt is not None: 
                        if (MiscHelper.canBeStartOfSentence(ttt)): 
                            break
                        if (ttt.isChar('(') and ttt.next0_ is not None and ttt.next0_.isValue("ПРИЛОЖЕНИЕ", "ДОДАТОК")): 
                            if (ttt.is_newline_before): 
                                break
                            br = BracketHelper.tryParse(ttt, BracketParseAttr.NO, 100)
                            if (br is None): 
                                break
                            pt = PartToken.tryAttach(ttt.next0_, None, False, False)
                            if (pt is None): 
                                PartToken.tryAttach(ttt.next0_, None, False, True)
                            if (pt is not None): 
                                res.parts = list()
                                res.parts.append(pt)
                                res.end_token = br.end_token
                                tt = res.end_token
                                break
                        ttt = ttt.next0_
                    if (res.parts is not None): 
                        continue
                    if (res.act_kind == DecreeChangeKind.APPEND): 
                        res.end_token = ttt0
                        tt = res.end_token
                        continue
                    tt = ttt0
                    continue
                break
            if (((res.has_name or res.parts is not None or res.decree is not None) or res.real_part is not None or res.act_kind != DecreeChangeKind.UNDEFINED) or res.change_val is not None): 
                if (res.end_token.next0_ is not None and res.end_token.next0_.isChar(':') and res.end_token.next0_.is_newline_after): 
                    res.typ = DecreeChangeTokenTyp.SINGLE
                    res.end_token = res.end_token.next0_
                return res
            if (res.begin_token == tt): 
                tok1 = DecreeChangeToken.__m_terms.tryParse(tt, TerminParseAttr.NO)
                if (tok1 is not None): 
                    pass
                else: 
                    return None
            else: 
                return None
        tok = DecreeChangeToken.__m_terms.tryParse(tt, TerminParseAttr.NO)
        if (tt.morph.class0_.is_adjective and (((isinstance(tt, NumberToken)) or tt.isValue("ПОСЛЕДНИЙ", "ОСТАННІЙ") or tt.isValue("ПРЕДПОСЛЕДНИЙ", "ПЕРЕДОСТАННІЙ")))): 
            tok = DecreeChangeToken.__m_terms.tryParse(tt.next0_, TerminParseAttr.NO)
            if (tok is not None and (isinstance(tok.termin.tag, DecreeChangeValueKind))): 
                pass
            else: 
                tok = (None)
        if (tok is not None): 
            if (isinstance(tok.termin.tag, DecreeChangeKind)): 
                res = DecreeChangeToken._new794(tt, tok.end_token, DecreeChangeTokenTyp.ACTION, Utils.valToEnum(tok.termin.tag, DecreeChangeKind))
                if (((res.act_kind == DecreeChangeKind.APPEND or res.act_kind == DecreeChangeKind.CONSIDER)) and tok.end_token.next0_ is not None and tok.end_token.next0_.morph.case_.is_instrumental): 
                    pt = PartToken.tryAttach(tok.end_token.next0_, None, False, False)
                    if (pt is None): 
                        pt = PartToken.tryAttach(tok.end_token.next0_, None, False, True)
                    if (pt is not None and pt.typ != PartToken.ItemType.PREFIX): 
                        if (res.act_kind == DecreeChangeKind.APPEND): 
                            res.part_typ = pt.typ
                            if (res.new_parts is None): 
                                res.new_parts = list()
                            res.new_parts.append(pt)
                        elif (res.act_kind == DecreeChangeKind.CONSIDER): 
                            res.change_val = DecreeChangeValueReferent()
                            res.change_val.value = pt.getSourceText()
                        res.end_token = pt.end_token
                        tt = res.end_token
                        if (tt.next0_ is not None and tt.next0_.is_and and res.act_kind == DecreeChangeKind.APPEND): 
                            pt = PartToken.tryAttach(tt.next0_.next0_, None, False, False)
                            if (pt is None): 
                                pt = PartToken.tryAttach(tt.next0_.next0_, None, False, True)
                            if (pt is not None): 
                                res.new_parts.append(pt)
                                res.end_token = pt.end_token
                                tt = res.end_token
                return res
            if (isinstance(tok.termin.tag, DecreeChangeValueKind)): 
                res = DecreeChangeToken._new793(tt, tok.end_token, DecreeChangeTokenTyp.VALUE)
                res.change_val = DecreeChangeValueReferent()
                res.change_val.kind = Utils.valToEnum(tok.termin.tag, DecreeChangeValueKind)
                tt = tok.end_token.next0_
                if (tt is None): 
                    return None
                if (res.change_val.kind == DecreeChangeValueKind.SEQUENCE or res.change_val.kind == DecreeChangeValueKind.FOOTNOTE): 
                    if (isinstance(tt, NumberToken)): 
                        res.change_val.number = str((Utils.asObjectOrNull(tt, NumberToken)).value)
                        res.end_token = tt
                        tt = tt.next0_
                    elif (isinstance(res.begin_token, NumberToken)): 
                        res.change_val.number = str((Utils.asObjectOrNull(res.begin_token, NumberToken)).value)
                    elif (res.begin_token.morph.class0_.is_adjective): 
                        res.change_val.number = res.begin_token.getNormalCaseText(MorphClass(), False, MorphGender.UNDEFINED, False)
                    elif (BracketHelper.canBeStartOfSequence(tt, False, False) and (isinstance(tt.next0_, NumberToken)) and BracketHelper.canBeEndOfSequence(tt.next0_.next0_, False, None, False)): 
                        res.change_val.number = str((Utils.asObjectOrNull(tt.next0_, NumberToken)).value)
                        tt = tt.next0_.next0_
                        res.end_token = tt
                        tt = tt.next0_
                if (tt is not None and tt.isValue("ИЗЛОЖИТЬ", "ВИКЛАСТИ") and res.act_kind == DecreeChangeKind.UNDEFINED): 
                    res.act_kind = DecreeChangeKind.NEW
                    tt = tt.next0_
                    if (tt is not None and tt.isValue("В", None)): 
                        tt = tt.next0_
                if ((tt is not None and ((tt.isValue("СЛЕДУЮЩИЙ", "НАСТУПНИЙ") or tt.isValue("ТАКОЙ", "ТАКИЙ"))) and tt.next0_ is not None) and ((tt.next0_.isValue("СОДЕРЖАНИЕ", "ЗМІСТ") or tt.next0_.isValue("СОДЕРЖИМОЕ", "ВМІСТ") or tt.next0_.isValue("РЕДАКЦИЯ", "РЕДАКЦІЯ")))): 
                    tt = tt.next0_.next0_
                elif (tt is not None and tt.isValue("РЕДАКЦИЯ", "РЕДАКЦІЯ")): 
                    tt = tt.next0_
                if (tt is not None and tt.isChar(':')): 
                    tt = tt.next0_
                can_be_start = False
                if (BracketHelper.canBeStartOfSequence(tt, True, False)): 
                    can_be_start = True
                elif ((isinstance(tt, MetaToken)) and BracketHelper.canBeStartOfSequence((Utils.asObjectOrNull(tt, MetaToken)).begin_token, True, False)): 
                    can_be_start = True
                elif (tt is not None and tt.is_newline_before and tt.isValue("ПРИЛОЖЕНИЕ", "ДОДАТОК")): 
                    if ((tt.previous is not None and tt.previous.isChar(':') and tt.previous.previous is not None) and tt.previous.previous.isValue("РЕДАКЦИЯ", "РЕДАКЦІЯ")): 
                        can_be_start = True
                if (can_be_start): 
                    ttt = (tt.next0_ if BracketHelper.canBeStartOfSequence(tt, True, False) else tt)
                    first_pass2841 = True
                    while True:
                        if first_pass2841: first_pass2841 = False
                        else: ttt = ttt.next0_
                        if (not (ttt is not None)): break
                        if (ttt.isCharOf(".;") and ttt.is_newline_after): 
                            res.change_val.value = (MetaToken(tt.next0_, ttt.previous)).getSourceText()
                            res.end_token = ttt
                            break
                        if (BracketHelper.isBracket(ttt, True)): 
                            pass
                        elif (((isinstance(ttt, MetaToken))) and BracketHelper.isBracket((Utils.asObjectOrNull(ttt, MetaToken)).end_token, True)): 
                            pass
                        else: 
                            continue
                        if (ttt.next0_ is None or ttt.is_newline_after): 
                            pass
                        elif (ttt.next0_.isCharOf(".;") and ttt.next0_.is_newline_after): 
                            pass
                        elif (ttt.next0_.is_comma_and and DecreeChangeToken.tryAttach(ttt.next0_.next0_, main, False, change_stack, True) is not None): 
                            pass
                        elif (DecreeChangeToken.tryAttach(ttt.next0_, main, False, change_stack, True) is not None or DecreeChangeToken.__m_terms.tryParse(ttt.next0_, TerminParseAttr.NO) is not None): 
                            pass
                        else: 
                            continue
                        val = (MetaToken((tt.next0_ if BracketHelper.isBracket(tt, True) else tt), (ttt.previous if BracketHelper.isBracket(ttt, True) else ttt))).getSourceText()
                        res.end_token = ttt
                        if (not BracketHelper.canBeStartOfSequence(tt, True, False)): 
                            val = val[1:]
                        if (not BracketHelper.isBracket(ttt, True)): 
                            val = val[0:0+len(val) - 1]
                        res.change_val.value = val
                        break
                    if (res.change_val.value is None): 
                        return None
                    if (res.change_val.kind == DecreeChangeValueKind.WORDS): 
                        tok = DecreeChangeToken.__m_terms.tryParse(res.end_token.next0_, TerminParseAttr.NO)
                        if (tok is not None and (isinstance(tok.termin.tag, DecreeChangeValueKind)) and (Utils.valToEnum(tok.termin.tag, DecreeChangeValueKind)) == DecreeChangeValueKind.ROBUSTWORDS): 
                            res.change_val.kind = DecreeChangeValueKind.ROBUSTWORDS
                            res.end_token = tok.end_token
                return res
        is_nex_change = 0
        if (t is not None and t.isValue("В", "У") and t.next0_ is not None): 
            t = t.next0_
            if (t.isValue("РЕДАКЦИЯ", "РЕДАКЦІЯ") and t.next0_ is not None): 
                is_nex_change = 1
                t = t.next0_
        if (((t.isValue("СЛЕДУЮЩИЙ", "НАСТУПНИЙ") or tt.isValue("ТАКОЙ", "ТАКИЙ"))) and t.next0_ is not None and ((t.next0_.isValue("СОДЕРЖАНИЕ", "ЗМІСТ") or t.next0_.isValue("СОДЕРЖИМОЕ", "ВМІСТ") or t.next0_.isValue("РЕДАКЦИЯ", "РЕДАКЦІЯ")))): 
            is_nex_change = 2
            t = t.next0_.next0_
        if (t.isChar(':') and t.next0_ is not None): 
            if (t.previous is not None and t.previous.isValue("РЕДАКЦИЯ", "РЕДАКЦІЯ")): 
                is_nex_change += 1
            t = t.next0_
            tt = t
            if (is_nex_change > 0): 
                is_nex_change += 1
        if ((t == tt and t.previous is not None and t.previous.isChar(':')) and BracketHelper.isBracket(t, False) and not t.isChar('(')): 
            is_nex_change = 1
        if (((is_nex_change > 0 and BracketHelper.isBracket(t, True))) or ((is_nex_change > 1 and t.isValue("ПРИЛОЖЕНИЕ", "ДОДАТОК")))): 
            res = DecreeChangeToken._new793(t, t, DecreeChangeTokenTyp.VALUE)
            res.change_val = DecreeChangeValueReferent._new802(DecreeChangeValueKind.TEXT)
            if (is_in_edition): 
                return res
            t0 = (t.next0_ if BracketHelper.isBracket(t, True) else t)
            doubt1 = None
            clause_last = None
            tt = t.next0_
            first_pass2842 = True
            while True:
                if first_pass2842: first_pass2842 = False
                else: tt = tt.next0_
                if (not (tt is not None)): break
                if (not tt.is_newline_after): 
                    continue
                is_doubt = False
                instr = InstrToken1.parse(tt.next0_, True, None, 0, None, False, 0, False)
                dc_next = DecreeChangeToken.tryAttach(tt.next0_, None, False, None, True)
                if (dc_next is None): 
                    dc_next = DecreeChangeToken.tryAttach(tt.next0_, None, True, None, True)
                if (tt.next0_ is None): 
                    pass
                elif (dc_next is not None and ((dc_next.is_start or dc_next.change_val is not None or dc_next.typ == DecreeChangeTokenTyp.UNDEFINED))): 
                    pass
                else: 
                    is_doubt = True
                    pt = PartToken.tryAttach(tt.next0_, None, False, False)
                    if (pt is not None and pt.typ == PartToken.ItemType.CLAUSE and ((pt.is_newline_after or ((pt.end_token.next0_ is not None and pt.end_token.next0_.isChar('.')))))): 
                        is_doubt = False
                        if (clause_last is not None and instr is not None and NumberingHelper.calcDelta(clause_last, instr, True) == 1): 
                            is_doubt = True
                if (instr is not None and instr.typ == InstrToken1.Types.CLAUSE): 
                    clause_last = instr
                if (is_doubt and instr is not None): 
                    ttt = tt
                    while ttt is not None and ttt.end_char <= instr.end_char: 
                        if (ttt.isValue("УТРАТИТЬ", "ВТРАТИТИ") and ttt.next0_ is not None and ttt.next0_.isValue("СИЛА", "ЧИННІСТЬ")): 
                            is_doubt = False
                            break
                        ttt = ttt.next0_
                res.end_token = tt
                tt1 = tt
                if (tt1.isCharOf(";.")): 
                    res.end_token = tt1.previous
                    tt1 = res.end_token
                if (BracketHelper.isBracket(tt1, True)): 
                    tt1 = tt1.previous
                elif ((isinstance(tt1, MetaToken)) and BracketHelper.isBracket((Utils.asObjectOrNull(tt1, MetaToken)).end_token, True)): 
                    pass
                else: 
                    continue
                if (is_doubt): 
                    if (doubt1 is None): 
                        doubt1 = tt1
                    continue
                if (tt1.begin_char > t.end_char): 
                    res.change_val.value = (MetaToken(t0, tt1)).getSourceText()
                    return res
                break
            if (doubt1 is not None): 
                res.change_val.value = (MetaToken(t0, doubt1)).getSourceText()
                res.end_token = doubt1
                if (BracketHelper.isBracket(doubt1.next0_, True)): 
                    res.end_token = doubt1.next0_
                return res
            return None
        if (t.isValue("ПОСЛЕ", "ПІСЛЯ")): 
            res = DecreeChangeToken.tryAttach(t.next0_, None, False, None, False)
            if (res is not None and res.typ == DecreeChangeTokenTyp.VALUE): 
                res.typ = DecreeChangeTokenTyp.AFTERVALUE
                res.begin_token = t
                return res
        return None
    
    @staticmethod
    def __tryAttachList(t : 'Token') -> typing.List['DecreeChangeToken']:
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.decree.internal.PartToken import PartToken
        if (t is None or t.is_newline_before): 
            return None
        d0 = DecreeChangeToken.tryAttach(t, None, False, None, False)
        if (d0 is None): 
            return None
        res = list()
        res.append(d0)
        t = d0.end_token.next0_
        first_pass2843 = True
        while True:
            if first_pass2843: first_pass2843 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_newline_before): 
                if ((t.isValue("ПРИЛОЖЕНИЕ", "ДОДАТОК") and t.previous is not None and t.previous.isChar(':')) and t.previous.previous is not None and t.previous.previous.isValue("РЕДАКЦИЯ", "РЕДАКЦІЯ")): 
                    pass
                else: 
                    break
            d = DecreeChangeToken.tryAttach(t, None, False, None, False)
            if (d is None and t.isChar('.') and not t.is_newline_after): 
                continue
            if (d is None): 
                if (t.isValue("НОВЫЙ", "НОВИЙ")): 
                    continue
                if (t.isValue("НА", None)): 
                    continue
                if (t.isChar(':') and ((not t.is_newline_after or res[len(res) - 1].act_kind == DecreeChangeKind.NEW))): 
                    continue
                if ((isinstance(t, TextToken)) and (Utils.asObjectOrNull(t, TextToken)).term == "ТЕКСТОМ"): 
                    continue
                pts = PartToken.tryAttachList(t, False, 40)
                if (pts is not None): 
                    d = DecreeChangeToken._new803(pts[0].begin_token, pts[len(pts) - 1].end_token, DecreeChangeTokenTyp.UNDEFINED, pts)
                else: 
                    pt = PartToken.tryAttach(t, None, True, False)
                    if (pt is None): 
                        pt = PartToken.tryAttach(t, None, True, True)
                    if (pt is not None): 
                        d = DecreeChangeToken(pt.begin_token, pt.end_token)
                        if (t.previous is not None and t.previous.isValue("НОВЫЙ", "НОВИЙ")): 
                            d.new_parts = list()
                            d.new_parts.append(pt)
                        else: 
                            d.part_typ = pt.typ
            if (d is None): 
                break
            if (d.typ == DecreeChangeTokenTyp.SINGLE or d.typ == DecreeChangeTokenTyp.STARTMULTU or d.typ == DecreeChangeTokenTyp.STARTSINGLE): 
                break
            res.append(d)
            t = d.end_token
        return res
    
    __m_terms = None
    
    @staticmethod
    def _initialize() -> None:
        from pullenti.ner.core.TerminCollection import TerminCollection
        from pullenti.ner.core.Termin import Termin
        from pullenti.morph.MorphLang import MorphLang
        if (DecreeChangeToken.__m_terms is not None): 
            return
        DecreeChangeToken.__m_terms = TerminCollection()
        t = Termin._new118("ИЗЛОЖИТЬ В СЛЕДУЮЩЕЙ РЕДАКЦИИ", DecreeChangeKind.NEW)
        t.addVariant("ИЗЛОЖИВ ЕГО В СЛЕДУЮЩЕЙ РЕДАКЦИИ", False)
        t.addVariant("ИЗЛОЖИТЬ В РЕДАКЦИИ", False)
        DecreeChangeToken.__m_terms.add(t)
        t = Termin._new477("ВИКЛАСТИ В НАСТУПНІЙ РЕДАКЦІЇ", MorphLang.UA, DecreeChangeKind.NEW)
        t.addVariant("ВИКЛАВШИ В ТАКІЙ РЕДАКЦІЇ", False)
        t.addVariant("ВИКЛАВШИ ЙОГО В НАСТУПНІЙ РЕДАКЦІЇ", False)
        t.addVariant("ВИКЛАСТИ В РЕДАКЦІЇ", False)
        DecreeChangeToken.__m_terms.add(t)
        t = Termin._new118("ПРИЗНАТЬ УТРАТИВШИМ СИЛУ", DecreeChangeKind.EXPIRE)
        t.addVariant("СЧИТАТЬ УТРАТИВШИМ СИЛУ", False)
        DecreeChangeToken.__m_terms.add(t)
        t = Termin._new477("ВИЗНАТИ таким, що ВТРАТИВ ЧИННІСТЬ", MorphLang.UA, DecreeChangeKind.EXPIRE)
        t.addVariant("ВВАЖАТИ таким, що ВТРАТИВ ЧИННІСТЬ", False)
        DecreeChangeToken.__m_terms.add(t)
        t = Termin._new118("ИСКЛЮЧИТЬ", DecreeChangeKind.REMOVE)
        t.addVariant("ИСКЛЮЧИВ ИЗ НЕГО", False)
        DecreeChangeToken.__m_terms.add(t)
        t = Termin._new477("ВИКЛЮЧИТИ", MorphLang.UA, DecreeChangeKind.REMOVE)
        t.addVariant("ВИКЛЮЧИВШИ З НЬОГО", False)
        DecreeChangeToken.__m_terms.add(t)
        t = Termin._new118("СЧИТАТЬ", DecreeChangeKind.CONSIDER)
        t.addVariant("СЧИТАТЬ СООТВЕТСТВЕННО", False)
        DecreeChangeToken.__m_terms.add(t)
        t = Termin._new477("ВВАЖАТИ", MorphLang.UA, DecreeChangeKind.CONSIDER)
        t.addVariant("ВВАЖАТИ ВІДПОВІДНО", False)
        DecreeChangeToken.__m_terms.add(t)
        t = Termin._new118("ЗАМЕНИТЬ", DecreeChangeKind.EXCHANGE)
        t.addVariant("ЗАМЕНИВ В НЕМ", False)
        DecreeChangeToken.__m_terms.add(t)
        t = Termin._new477("ЗАМІНИТИ", MorphLang.UA, DecreeChangeKind.EXCHANGE)
        t.addVariant("ЗАМІНИВШИ В НЬОМУ", False)
        DecreeChangeToken.__m_terms.add(t)
        t = Termin._new118("ДОПОЛНИТЬ", DecreeChangeKind.APPEND)
        t.addVariant("ДОПОЛНИВ ЕГО", False)
        DecreeChangeToken.__m_terms.add(t)
        t = Termin._new477("ДОПОВНИТИ", MorphLang.UA, DecreeChangeKind.APPEND)
        t.addVariant("ДОПОВНИВШИ ЙОГО", False)
        DecreeChangeToken.__m_terms.add(t)
        t = Termin._new118("СЛОВО", DecreeChangeValueKind.WORDS)
        t.addVariant("АББРЕВИАТУРА", False)
        t.addVariant("АБРЕВІАТУРА", False)
        DecreeChangeToken.__m_terms.add(t)
        t = Termin._new118("ЦИФРА", DecreeChangeValueKind.NUMBERS)
        t.addVariant("ЧИСЛО", False)
        DecreeChangeToken.__m_terms.add(t)
        t = Termin._new118("ПРЕДЛОЖЕНИЕ", DecreeChangeValueKind.SEQUENCE)
        DecreeChangeToken.__m_terms.add(t)
        t = Termin._new477("ПРОПОЗИЦІЯ", MorphLang.UA, DecreeChangeValueKind.SEQUENCE)
        DecreeChangeToken.__m_terms.add(t)
        t = Termin._new118("СНОСКА", DecreeChangeValueKind.FOOTNOTE)
        DecreeChangeToken.__m_terms.add(t)
        t = Termin._new477("ВИНОСКА", MorphLang.UA, DecreeChangeValueKind.FOOTNOTE)
        DecreeChangeToken.__m_terms.add(t)
        t = Termin._new118("БЛОК", DecreeChangeValueKind.BLOCK)
        t.addVariant("БЛОК СО СЛОВАМИ", False)
        DecreeChangeToken.__m_terms.add(t)
        t = Termin._new477("БЛОК", MorphLang.UA, DecreeChangeValueKind.BLOCK)
        t.addVariant("БЛОК ЗІ СЛОВАМИ", False)
        DecreeChangeToken.__m_terms.add(t)
        t = Termin._new118("В СООТВЕТСТВУЮЩИХ ЧИСЛЕ И ПАДЕЖЕ", DecreeChangeValueKind.ROBUSTWORDS)
        t.addVariant("В СООТВЕТСТВУЮЩЕМ ПАДЕЖЕ", False)
        t.addVariant("В СООТВЕТСТВУЮЩЕМ ЧИСЛЕ", False)
        DecreeChangeToken.__m_terms.add(t)
        t = Termin._new477("У ВІДПОВІДНОМУ ЧИСЛІ ТА ВІДМІНКУ", MorphLang.UA, DecreeChangeValueKind.ROBUSTWORDS)
        t.addVariant("У ВІДПОВІДНОМУ ВІДМІНКУ", False)
        t.addVariant("У ВІДПОВІДНОМУ ЧИСЛІ", False)
        DecreeChangeToken.__m_terms.add(t)
    
    @staticmethod
    def attachReferents(dpr : 'Referent', tok0 : 'DecreeChangeToken') -> typing.List['ReferentToken']:
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.decree.internal.PartToken import PartToken
        from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
        from pullenti.ner.decree.DecreeChangeValueReferent import DecreeChangeValueReferent
        if (dpr is None or tok0 is None): 
            return None
        tt0 = tok0.end_token.next0_
        if (tt0 is not None and tt0.is_comma_and and tok0.act_kind == DecreeChangeKind.UNDEFINED): 
            tt0 = tt0.next0_
        if (tt0 is not None and tt0.isChar(':')): 
            tt0 = tt0.next0_
        toks = DecreeChangeToken.__tryAttachList(tt0)
        if (toks is None): 
            toks = list()
        toks.insert(0, tok0)
        res = list()
        dcr = DecreeChangeReferent()
        dcr.addSlot(DecreeChangeReferent.ATTR_OWNER, dpr, False, 0)
        rt = ReferentToken(dcr, tok0.begin_token, tok0.end_token)
        res.append(rt)
        new_items = None
        while True:
            i = 0
            first_pass2844 = True
            while True:
                if first_pass2844: first_pass2844 = False
                else: i += 1
                if (not (i < len(toks))): break
                tok = toks[i]
                if (tok.has_text and tok.has_name): 
                    dcr.is_owner_name_and_text = True
                elif (tok.has_name): 
                    dcr.is_owner_name = True
                elif (tok.has_text): 
                    dcr.is_only_text = True
                rt.end_token = tok.end_token
                if (tok.typ == DecreeChangeTokenTyp.AFTERVALUE): 
                    if (tok.change_val is not None): 
                        dcr.param = tok.change_val
                        if (tok.end_char > rt.end_char): 
                            rt.end_token = tok.end_token
                        res.insert(len(res) - 1, ReferentToken(tok.change_val, tok.begin_token, tok.end_token))
                    continue
                if (tok.act_kind != DecreeChangeKind.UNDEFINED): 
                    dcr.kind = tok.act_kind
                    if (tok.act_kind == DecreeChangeKind.EXPIRE): 
                        break
                if (tok.change_val is not None): 
                    if (((i + 2) < len(toks)) and ((toks[i + 1].act_kind == DecreeChangeKind.EXCHANGE or toks[i + 1].act_kind == DecreeChangeKind.NEW)) and toks[i + 2].change_val is not None): 
                        dcr.param = tok.change_val
                        rt11 = ReferentToken(tok.change_val, tok.begin_token, tok.end_token)
                        if (tok.parts is not None and len(tok.parts) > 0): 
                            rt11.begin_token = tok.parts[len(tok.parts) - 1].end_token.next0_
                        res.insert(len(res) - 1, rt11)
                        dcr.value = toks[i + 2].change_val
                        dcr.kind = toks[i + 1].act_kind
                        i += 2
                        tok = toks[i]
                    elif (((i + 1) < len(toks)) and toks[i + 1].change_val is not None and dcr.kind == DecreeChangeKind.EXCHANGE): 
                        dcr.param = tok.change_val
                        res.insert(len(res) - 1, ReferentToken(tok.change_val, tok.begin_token, tok.end_token))
                        dcr.value = toks[i + 1].change_val
                        i += 1
                        tok = toks[i]
                    elif (dcr.value is None): 
                        dcr.value = tok.change_val
                    elif ((dcr.value.kind != DecreeChangeValueKind.TEXT and tok.change_val.kind == DecreeChangeValueKind.TEXT and tok.change_val.value is not None) and dcr.value.value is None): 
                        dcr.value.value = tok.change_val.value
                    else: 
                        dcr.value = tok.change_val
                    if (tok.end_char > rt.end_char): 
                        rt.end_token = tok.end_token
                    res.insert(len(res) - 1, ReferentToken(tok.change_val, tok.begin_token, tok.end_token))
                    if (dcr.kind == DecreeChangeKind.CONSIDER or dcr.kind == DecreeChangeKind.NEW): 
                        break
                if (dcr.kind == DecreeChangeKind.APPEND and tok.new_parts is not None): 
                    for np in tok.new_parts: 
                        rank = PartToken._getRank(np.typ)
                        if (rank == 0): 
                            continue
                        eq_lev_val = None
                        if (isinstance(dpr, DecreePartReferent)): 
                            if (not (Utils.asObjectOrNull(dpr, DecreePartReferent))._isAllItemsOverThisLevel(np.typ)): 
                                eq_lev_val = dpr.getStringValue(PartToken._getAttrNameByTyp(np.typ))
                                if (eq_lev_val is None): 
                                    continue
                        dcr.kind = DecreeChangeKind.APPEND
                        if (new_items is None): 
                            new_items = list()
                        nam = PartToken._getAttrNameByTyp(np.typ)
                        if (nam is None): 
                            continue
                        if (len(np.values) == 0): 
                            if (eq_lev_val is None): 
                                new_items.append(nam)
                            else: 
                                wrapn826 = RefOutArgWrapper(0)
                                inoutres827 = Utils.tryParseInt(eq_lev_val, wrapn826)
                                n = wrapn826.value
                                if (inoutres827): 
                                    new_items.append("{0} {1}".format(nam, n + 1))
                                else: 
                                    new_items.append(nam)
                        elif (len(np.values) == 2 and np.values[0].end_token.next0_.is_hiphen): 
                            vv = NumberingHelper.createDiap(np.values[0].value, np.values[1].value)
                            if (vv is not None): 
                                for v in vv: 
                                    new_items.append("{0} {1}".format(nam, v))
                        if (len(new_items) == 0): 
                            for v in np.values: 
                                new_items.append("{0} {1}".format(nam, v.value))
            if (not dcr._checkCorrect()): 
                return None
            if (new_items is not None and dcr.value is not None and dcr.kind == DecreeChangeKind.APPEND): 
                for v in new_items: 
                    dcr.value.addSlot(DecreeChangeValueReferent.ATTR_NEWITEM, v, False, 0)
            new_items = (None)
            if (rt.end_token.next0_ is None or not rt.end_token.next0_.is_comma): 
                break
            toks = DecreeChangeToken.__tryAttachList(rt.end_token.next0_.next0_)
            if (toks is None): 
                break
            dts1 = DecreeChangeReferent()
            for o in dcr.owners: 
                dts1.addSlot(DecreeChangeReferent.ATTR_OWNER, o, False, 0)
            rt = ReferentToken(dts1, toks[0].begin_token, toks[0].end_token)
            res.append(rt)
            dcr = dts1
        return res
    
    @staticmethod
    def _new793(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'DecreeChangeTokenTyp') -> 'DecreeChangeToken':
        res = DecreeChangeToken(_arg1, _arg2)
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new794(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'DecreeChangeTokenTyp', _arg4 : 'DecreeChangeKind') -> 'DecreeChangeToken':
        res = DecreeChangeToken(_arg1, _arg2)
        res.typ = _arg3
        res.act_kind = _arg4
        return res
    
    @staticmethod
    def _new803(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'DecreeChangeTokenTyp', _arg4 : typing.List['PartToken']) -> 'DecreeChangeToken':
        res = DecreeChangeToken(_arg1, _arg2)
        res.typ = _arg3
        res.parts = _arg4
        return res