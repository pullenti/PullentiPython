# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
import typing
from enum import IntEnum
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.instrument.InstrumentKind import InstrumentKind
from pullenti.ner.instrument.internal.NumberingHelper import NumberingHelper
from pullenti.morph.LanguageHelper import LanguageHelper


class PartToken(MetaToken):
    """ Примитив, из которых состоит часть декрета (статья, пункт и часть) """
    
    class ItemType(IntEnum):
        UNDEFINED = 0
        PREFIX = 0 + 1
        APPENDIX = (0 + 1) + 1
        DOCPART = ((0 + 1) + 1) + 1
        PART = (((0 + 1) + 1) + 1) + 1
        SECTION = ((((0 + 1) + 1) + 1) + 1) + 1
        SUBSECTION = (((((0 + 1) + 1) + 1) + 1) + 1) + 1
        CHAPTER = ((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1
        CLAUSE = (((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        PARAGRAPH = ((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        SUBPARAGRAPH = (((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        ITEM = ((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        SUBITEM = (((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        INDENTION = ((((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        SUBINDENTION = (((((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        PREAMBLE = ((((((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        NOTICE = (((((((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        SUBPROGRAM = ((((((((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        PAGE = (((((((((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        ADDAGREE = ((((((((((((((((((0 + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1) + 1
        
        @classmethod
        def has_value(cls, value):
            return any(value == item.value for item in cls)
    
    class PartValue(MetaToken):
        
        def __init__(self, begin : 'Token', end : 'Token') -> None:
            super().__init__(begin, end, None)
            self.value = None;
        
        @property
        def source_value(self) -> str:
            t0 = self.begin_token
            t1 = self.end_token
            if (t1.isChar('.')): 
                t1 = t1.previous
            elif (t1.isChar(')') and not t0.isChar('(')): 
                t1 = t1.previous
            return (MetaToken(t0, t1)).getSourceText()
        
        @property
        def int_value(self) -> int:
            if (Utils.isNullOrEmpty(self.value)): 
                return 0
            wrapnum1022 = RefOutArgWrapper(0)
            inoutres1023 = Utils.tryParseInt(self.value, wrapnum1022)
            num = wrapnum1022.value
            if (inoutres1023): 
                return num
            return 0
        
        def __str__(self) -> str:
            return self.value
        
        def correctValue(self) -> None:
            from pullenti.ner.TextToken import TextToken
            from pullenti.ner.core.BracketHelper import BracketHelper
            from pullenti.ner.NumberToken import NumberToken
            from pullenti.ner.decree.DecreeReferent import DecreeReferent
            if ((isinstance(self.end_token.next0_, TextToken)) and (Utils.asObjectOrNull(self.end_token.next0_, TextToken)).length_char == 1 and self.end_token.next0_.chars.is_letter): 
                if (not self.end_token.is_whitespace_after): 
                    self.value += (Utils.asObjectOrNull(self.end_token.next0_, TextToken)).term
                    self.end_token = self.end_token.next0_
                elif ((self.end_token.whitespaces_after_count < 2) and self.end_token.next0_.next0_ is not None and self.end_token.next0_.next0_.isChar(')')): 
                    self.value += (Utils.asObjectOrNull(self.end_token.next0_, TextToken)).term
                    self.end_token = self.end_token.next0_.next0_
            if ((BracketHelper.canBeStartOfSequence(self.end_token.next0_, False, False) and (isinstance(self.end_token.next0_.next0_, TextToken)) and self.end_token.next0_.next0_.length_char == 1) and BracketHelper.canBeEndOfSequence(self.end_token.next0_.next0_.next0_, False, self.end_token.next0_, False)): 
                self.value = "{0}.{1}".format(self.value, (Utils.asObjectOrNull(self.end_token.next0_.next0_, TextToken)).term)
                self.end_token = self.end_token.next0_.next0_.next0_
            t = self.end_token.next0_
            first_pass2863 = True
            while True:
                if first_pass2863: first_pass2863 = False
                else: t = t.next0_
                if (not (t is not None)): break
                if (t.is_whitespace_before): 
                    if (t.whitespaces_before_count > 1): 
                        break
                    if (((isinstance(t, TextToken)) and t.length_char == 1 and t.next0_ is not None) and t.next0_.isChar(')')): 
                        self.value = "{0}.{1}".format(Utils.ifNotNull(self.value, ""), (Utils.asObjectOrNull(t, TextToken)).term)
                        t = t.next0_
                        self.end_token = t
                    break
                if (t.isCharOf("_.") and not t.is_whitespace_after): 
                    if (isinstance(t.next0_, NumberToken)): 
                        self.value = "{0}.{1}".format(Utils.ifNotNull(self.value, ""), (Utils.asObjectOrNull(t.next0_, NumberToken)).value)
                        t = t.next0_
                        self.end_token = t
                        continue
                    if (((t.next0_ is not None and t.next0_.isChar('(') and (isinstance(t.next0_.next0_, NumberToken))) and not t.next0_.is_whitespace_after and t.next0_.next0_.next0_ is not None) and t.next0_.next0_.next0_.isChar(')')): 
                        self.value = "{0}.{1}".format(Utils.ifNotNull(self.value, ""), (Utils.asObjectOrNull(t.next0_.next0_, NumberToken)).value)
                        self.end_token = t.next0_.next0_.next0_
                        continue
                if (t.is_hiphen and not t.is_whitespace_after and (isinstance(t.next0_, NumberToken))): 
                    wrapn11024 = RefOutArgWrapper(0)
                    inoutres1025 = Utils.tryParseInt(self.value, wrapn11024)
                    n1 = wrapn11024.value
                    if (inoutres1025): 
                        if (n1 >= (Utils.asObjectOrNull(t.next0_, NumberToken)).value): 
                            self.value = "{0}.{1}".format(Utils.ifNotNull(self.value, ""), (Utils.asObjectOrNull(t.next0_, NumberToken)).value)
                            t = t.next0_
                            self.end_token = t
                            continue
                if ((t.isCharOf("(<") and (isinstance(t.next0_, NumberToken)) and t.next0_.next0_ is not None) and t.next0_.next0_.isCharOf(")>")): 
                    self.value = "{0}.{1}".format(Utils.ifNotNull(self.value, ""), (Utils.asObjectOrNull(t.next0_, NumberToken)).value)
                    t = t.next0_.next0_
                    self.end_token = t
                    if (t.next0_ is not None and t.next0_.isChar('.') and not t.is_whitespace_after): 
                        t = t.next0_
                    continue
                break
            if (self.end_token.next0_ is not None and self.end_token.next0_.isCharOf(".") and not self.end_token.is_whitespace_after): 
                if (self.end_token.next0_.next0_ is not None and (isinstance(self.end_token.next0_.next0_.getReferent(), DecreeReferent)) and not self.end_token.next0_.is_newline_after): 
                    self.end_token = self.end_token.next0_
            if (self.begin_token == self.end_token and self.end_token.next0_ is not None and self.end_token.next0_.isChar(')')): 
                ok = True
                lev = 0
                ttt = self.begin_token.previous
                while ttt is not None: 
                    if (ttt.is_newline_after): 
                        break
                    if (ttt.isChar(')')): 
                        lev += 1
                    elif (ttt.isChar('(')): 
                        lev -= 1
                        if (lev < 0): 
                            ok = False
                            break
                    ttt = ttt.previous
                if (ok): 
                    tt = self.end_token.next0_.next0_
                    if (tt is not None): 
                        if ((isinstance(tt.getReferent(), DecreeReferent)) or PartToken.tryAttach(tt, None, False, False) is not None): 
                            self.end_token = self.end_token.next0_
        
        @staticmethod
        def _new1026(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str) -> 'PartValue':
            res = PartToken.PartValue(_arg1, _arg2)
            res.value = _arg3
            return res
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.typ = PartToken.ItemType.UNDEFINED
        self.alt_typ = PartToken.ItemType.UNDEFINED
        self.values = list()
        self.name = None;
        self.ind = 0
        self.decree = None;
        self.is_doubt = False
        self.delim_after = False
        self.has_terminator = False
        self.anafor_ref = None;
    
    def __str__(self) -> str:
        res = Utils.newStringIO(Utils.enumToString(self.typ))
        for v in self.values: 
            print(" {0}".format(v), end="", file=res, flush=True)
        if (self.delim_after): 
            print(", DelimAfter", end="", file=res)
        if (self.is_doubt): 
            print(", Doubt", end="", file=res)
        if (self.has_terminator): 
            print(", Terminator", end="", file=res)
        if (self.anafor_ref is not None): 
            print(", Ref='{0}'".format(self.anafor_ref.term), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def tryAttach(t : 'Token', prev : 'PartToken', in_bracket : bool=False, ignore_number : bool=False) -> 'PartToken':
        """ Привязать с указанной позиции один примитив
        
        """
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.decree.DecreeReferent import DecreeReferent
        from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
        from pullenti.ner.decree.internal.DecreeToken import DecreeToken
        from pullenti.ner.decree.DecreeAnalyzer import DecreeAnalyzer
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.core.BracketHelper import BracketHelper
        if (t is None): 
            return None
        res = None
        if (t.morph.class0_.is_personal_pronoun and (t.whitespaces_after_count < 2)): 
            res = PartToken.tryAttach(t.next0_, prev, False, False)
            if (res is not None): 
                res.anafor_ref = (Utils.asObjectOrNull(t, TextToken))
                res.begin_token = t
                return res
        tt = Utils.asObjectOrNull(t, TextToken)
        if ((isinstance(t, NumberToken)) and t.next0_ is not None and (t.whitespaces_after_count < 3)): 
            re = PartToken.__createPartTyp0(t.next0_, prev)
            if (re is not None): 
                t11 = re.end_token.next0_
                ok1 = False
                if (t11 is not None and (isinstance(t11.getReferent(), DecreeReferent))): 
                    ok1 = True
                elif (prev is not None and t11 is not None and not ((isinstance(t11, NumberToken)))): 
                    ok1 = True
                if (not ok1): 
                    res1 = PartToken.tryAttach(t11, None, False, False)
                    if (res1 is not None): 
                        ok1 = True
                if (ok1 or in_bracket): 
                    re.begin_token = t
                    re.values.append(PartToken.PartValue._new1026(t, t, str((Utils.asObjectOrNull(t, NumberToken)).value)))
                    return re
        if (((isinstance(t, NumberToken)) and (Utils.asObjectOrNull(t, NumberToken)).typ == NumberSpellingType.DIGIT and prev is None) and t.previous is not None): 
            t0 = t.previous
            delim = False
            if (t0.isChar(',') or t0.morph.class0_.is_conjunction): 
                delim = True
                t0 = t0.previous
            if (t0 is None): 
                return None
            dr = Utils.asObjectOrNull(t0.getReferent(), DecreePartReferent)
            if (dr is None): 
                if (t0.isChar('(') and t.next0_ is not None): 
                    if (t.next0_.isValue("ЧАСТЬ", None) or t.next0_.isValue("Ч", None)): 
                        te = t.next0_
                        if (te.next0_ is not None and te.next0_.isChar('.')): 
                            te = te.next0_
                        res = PartToken._new797(t, te, PartToken.ItemType.PART)
                        res.values.append(PartToken.PartValue._new1026(t, t, str((Utils.asObjectOrNull(t, NumberToken)).value)))
                        return res
                return None
            if (dr.clause is None): 
                return None
            res = PartToken._new1029(t, t, PartToken.ItemType.CLAUSE, not delim)
            pv = PartToken.PartValue._new1026(t, t, str((Utils.asObjectOrNull(t, NumberToken)).value))
            res.values.append(pv)
            t = t.next0_
            while t is not None: 
                if (t.is_whitespace_before): 
                    break
                elif (t.isCharOf("._") and (isinstance(t.next0_, NumberToken))): 
                    t = t.next0_
                    pv.end_token = res.end_token = t
                    pv.value = "{0}.{1}".format(pv.value, (Utils.asObjectOrNull(t, NumberToken)).value)
                else: 
                    break
                t = t.next0_
            return res
        if (((isinstance(t, NumberToken)) and (Utils.asObjectOrNull(t, NumberToken)).typ == NumberSpellingType.DIGIT and prev is not None) and prev.typ == PartToken.ItemType.PREFIX and (t.whitespaces_before_count < 3)): 
            pv = PartToken.PartValue._new1026(t, t, str((Utils.asObjectOrNull(t, NumberToken)).value))
            pv.correctValue()
            ttt1 = pv.end_token.next0_
            ne = DecreeToken.tryAttach(ttt1, None, False)
            ok = False
            if (ne is not None and ne.typ == DecreeToken.ItemType.TYP): 
                ok = True
            elif (DecreeAnalyzer._checkOtherTyp(ttt1, True) is not None): 
                ok = True
            elif (DecreeAnalyzer._getDecree(ttt1) is not None): 
                ok = True
            if (ok): 
                res = PartToken._new797(t, pv.end_token, PartToken.ItemType.ITEM)
                res.values.append(pv)
                return res
        if (tt is None): 
            return None
        if (tt.length_char == 1 and not tt.chars.is_all_lower): 
            if (not MiscHelper.canBeStartOfSentence(tt)): 
                return None
        t1 = tt
        res = PartToken.__createPartTyp0(t1, prev)
        if (res is not None): 
            t1 = res.end_token
        elif ((t1.isValue("СИЛУ", None) or t1.isValue("СОГЛАСНО", None) or t1.isValue("СООТВЕТСТВИЕ", None)) or t1.isValue("ПОЛОЖЕНИЕ", None)): 
            if (t1.isValue("СИЛУ", None) and t1.previous is not None and t1.previous.morph.class0_.is_verb): 
                return None
            res = PartToken._new797(t1, t1, PartToken.ItemType.PREFIX)
            if (t1.next0_ is not None and t1.next0_.isValue("С", None)): 
                res.end_token = t1.next0_
            return res
        elif (((t1.isValue("УГОЛОВНОЕ", None) or t1.isValue("КРИМІНАЛЬНА", None))) and t1.next0_ is not None and ((t1.next0_.isValue("ДЕЛО", None) or t1.next0_.isValue("СПРАВА", None)))): 
            t1 = t1.next0_
            if (t1.next0_ is not None and t1.next0_.isValue("ПО", None)): 
                t1 = t1.next0_
            return PartToken._new797(t, t1, PartToken.ItemType.PREFIX)
        elif ((((t1.isValue("МОТИВИРОВОЧНЫЙ", None) or t1.isValue("МОТИВУВАЛЬНИЙ", None) or t1.isValue("РЕЗОЛЮТИВНЫЙ", None)) or t1.isValue("РЕЗОЛЮТИВНИЙ", None))) and t1.next0_ is not None and ((t1.next0_.isValue("ЧАСТЬ", None) or t1.next0_.isValue("ЧАСТИНА", None)))): 
            rr = PartToken._new797(t1, t1.next0_, PartToken.ItemType.PART)
            rr.values.append(PartToken.PartValue._new1026(t1, t1, ("мотивировочная" if t1.isValue("МОТИВИРОВОЧНЫЙ", None) or t1.isValue("МОТИВУВАЛЬНИЙ", None) else "резолютивная")))
            return rr
        if (res is None): 
            return None
        if (ignore_number): 
            return res
        if (res.is_newline_after): 
            if (res.chars.is_all_upper): 
                return None
        if (t1.next0_ is not None and t1.next0_.isChar('.')): 
            if (not t1.next0_.is_newline_after or (t1.length_char < 3)): 
                t1 = t1.next0_
        t1 = t1.next0_
        if (t1 is None): 
            return None
        if (res.typ == PartToken.ItemType.CLAUSE): 
            if (((isinstance(t1, NumberToken)) and (Utils.asObjectOrNull(t1, NumberToken)).value == (3) and not t1.is_whitespace_after) and t1.next0_ is not None and t1.next0_.length_char == 2): 
                return None
        if (res.typ == PartToken.ItemType.CLAUSE and t1.isValue("СТ", None)): 
            t1 = t1.next0_
            if (t1 is not None and t1.isChar('.')): 
                t1 = t1.next0_
        elif (res.typ == PartToken.ItemType.PART and t1.isValue("Ч", None)): 
            t1 = t1.next0_
            if (t1 is not None and t1.isChar('.')): 
                t1 = t1.next0_
        elif (res.typ == PartToken.ItemType.ITEM and t1.isValue("П", None)): 
            t1 = t1.next0_
            if (t1 is not None and t1.isChar('.')): 
                t1 = t1.next0_
            res.alt_typ = PartToken.ItemType.SUBITEM
        if (t1 is None): 
            return None
        if (res.typ == PartToken.ItemType.CLAUSE and (isinstance(t1.getReferent(), DecreeReferent)) and t1.next0_ is not None): 
            res.decree = (Utils.asObjectOrNull(t1.getReferent(), DecreeReferent))
            t1 = t1.next0_
        ttn = MiscHelper.checkNumberPrefix(t1)
        first_num_prefix = None
        if (ttn is not None): 
            first_num_prefix = (Utils.asObjectOrNull(t1, TextToken))
            t1 = ttn
        if (t1 is None): 
            return None
        res.end_token = t1
        and0_ = False
        ntyp = NumberSpellingType.DIGIT
        tt1 = t1
        while t1 is not None:
            if (t1.whitespaces_before_count > 15): 
                break
            if (t1 != tt1 and t1.is_newline_before): 
                break
            if (ttn is not None): 
                ttn = MiscHelper.checkNumberPrefix(t1)
                if (ttn is not None): 
                    t1 = ttn
            if (BracketHelper.canBeStartOfSequence(t1, False, False)): 
                br = BracketHelper.tryParse(t1, BracketParseAttr.NO, 100)
                if (br is None): 
                    break
                ok = True
                newp = None
                ttt = t1.next0_
                first_pass2864 = True
                while True:
                    if first_pass2864: first_pass2864 = False
                    else: ttt = ttt.next0_
                    if (not (ttt is not None)): break
                    if (ttt.end_char > br.end_token.previous.end_char): 
                        break
                    if (ttt.isChar(',')): 
                        continue
                    if (isinstance(ttt, NumberToken)): 
                        if ((Utils.asObjectOrNull(ttt, NumberToken)).value == (0)): 
                            ok = False
                            break
                        if (newp is None): 
                            newp = list()
                        newp.append(PartToken.PartValue._new1026(ttt, ttt, str((Utils.asObjectOrNull(ttt, NumberToken)).value)))
                        continue
                    to = Utils.asObjectOrNull(ttt, TextToken)
                    if (to is None): 
                        ok = False
                        break
                    if ((res.typ != PartToken.ItemType.ITEM and res.typ != PartToken.ItemType.SUBITEM and res.typ != PartToken.ItemType.INDENTION) and res.typ != PartToken.ItemType.SUBINDENTION): 
                        ok = False
                        break
                    if (not to.chars.is_letter or to.length_char != 1): 
                        ok = False
                        break
                    if (newp is None): 
                        newp = list()
                    pv = PartToken.PartValue._new1026(ttt, ttt, to.term)
                    if (BracketHelper.canBeStartOfSequence(ttt.previous, False, False)): 
                        pv.begin_token = ttt.previous
                    if (BracketHelper.canBeEndOfSequence(ttt.next0_, False, None, False)): 
                        pv.end_token = ttt.next0_
                    newp.append(pv)
                if (newp is None or not ok): 
                    break
                res.values.extend(newp)
                res.end_token = br.end_token
                t1 = br.end_token.next0_
                if (and0_): 
                    break
                if (t1 is not None and t1.is_hiphen and BracketHelper.canBeStartOfSequence(t1.next0_, False, False)): 
                    br1 = BracketHelper.tryParse(t1.next0_, BracketParseAttr.NO, 100)
                    if ((br1 is not None and (isinstance(t1.next0_.next0_, TextToken)) and t1.next0_.next0_.length_char == 1) and t1.next0_.next0_.next0_ == br1.end_token): 
                        res.values.append(PartToken.PartValue._new1026(br1.begin_token, br1.end_token, (Utils.asObjectOrNull(t1.next0_.next0_, TextToken)).term))
                        res.end_token = br1.end_token
                        t1 = br1.end_token.next0_
                continue
            if (((isinstance(t1, TextToken)) and t1.length_char == 1 and t1.chars.is_letter) and len(res.values) == 0): 
                if (t1.chars.is_all_upper and res.typ == PartToken.ItemType.SUBPROGRAM): 
                    res.values.append(PartToken.PartValue._new1026(t1, t1, (Utils.asObjectOrNull(t1, TextToken)).term))
                    res.end_token = t1
                    return res
                ok = True
                lev = 0
                ttt = t1.previous
                while ttt is not None: 
                    if (ttt.is_newline_after): 
                        break
                    if (ttt.isChar('(')): 
                        lev -= 1
                        if (lev < 0): 
                            ok = False
                            break
                    elif (ttt.isChar(')')): 
                        lev += 1
                    ttt = ttt.previous
                if (ok and t1.next0_ is not None and t1.next0_.isChar(')')): 
                    res.values.append(PartToken.PartValue._new1026(t1, t1.next0_, (Utils.asObjectOrNull(t1, TextToken)).term))
                    res.end_token = t1.next0_
                    t1 = t1.next0_.next0_
                    continue
                if (((ok and t1.next0_ is not None and t1.next0_.isChar('.')) and not t1.next0_.is_whitespace_after and (isinstance(t1.next0_.next0_, NumberToken))) and t1.next0_.next0_.next0_ is not None and t1.next0_.next0_.next0_.isChar(')')): 
                    res.values.append(PartToken.PartValue._new1026(t1, t1.next0_.next0_.next0_, "{0}.{1}".format((Utils.asObjectOrNull(t1, TextToken)).term, (Utils.asObjectOrNull(t1.next0_.next0_, NumberToken)).value)))
                    res.end_token = t1.next0_.next0_.next0_
                    t1 = res.end_token.next0_
                    continue
            pref_to = None
            if (len(res.values) > 0 and not ((isinstance(t1, NumberToken))) and first_num_prefix is not None): 
                ttn = MiscHelper.checkNumberPrefix(t1)
                if (ttn is not None): 
                    pref_to = t1
                    t1 = ttn
            if (isinstance(t1, NumberToken)): 
                tt0 = Utils.ifNotNull(pref_to, t1)
                if (len(res.values) > 0): 
                    if (res.values[0].int_value == 0 and not str.isdigit(res.values[0].value[0])): 
                        break
                    if ((Utils.asObjectOrNull(t1, NumberToken)).typ != ntyp): 
                        break
                ntyp = (Utils.asObjectOrNull(t1, NumberToken)).typ
                val = PartToken.PartValue._new1026(tt0, t1, str((Utils.asObjectOrNull(t1, NumberToken)).value))
                val.correctValue()
                res.values.append(val)
                res.end_token = val.end_token
                t1 = res.end_token.next0_
                if (and0_): 
                    break
                continue
            nt = NumberHelper.tryParseRoman(t1)
            if (nt is not None): 
                pv = PartToken.PartValue._new1026(t1, nt.end_token, str(nt.value))
                res.values.append(pv)
                pv.correctValue()
                res.end_token = pv.end_token
                t1 = res.end_token.next0_
                continue
            if ((t1 == tt1 and ((res.typ == PartToken.ItemType.APPENDIX or res.typ == PartToken.ItemType.ADDAGREE)) and t1.isValue("К", None)) and t1.next0_ is not None and (isinstance(t1.next0_.getReferent(), DecreeReferent))): 
                res.values.append(PartToken.PartValue._new1026(t1, t1, ""))
                break
            if (res.typ == PartToken.ItemType.ADDAGREE and first_num_prefix is not None and len(res.values) == 0): 
                ddd = DecreeToken.tryAttach(first_num_prefix, None, False)
                if (ddd is not None and ddd.typ == DecreeToken.ItemType.NUMBER and ddd.value is not None): 
                    res.values.append(PartToken.PartValue._new1026(t1, ddd.end_token, ddd.value))
                    res.end_token = ddd.end_token
                    t1 = res.end_token
                    break
            if (len(res.values) == 0): 
                break
            if (t1.isCharOf(",.")): 
                if (t1.is_newline_after and t1.isChar('.')): 
                    break
                t1 = t1.next0_
                continue
            if (t1.is_hiphen and res.values[len(res.values) - 1].value.find('.') > 0): 
                t1 = t1.next0_
                continue
            if (t1.is_and or t1.is_or): 
                t1 = t1.next0_
                and0_ = True
                continue
            if (t1.is_hiphen): 
                if (not ((isinstance(t1.next0_, NumberToken)))): 
                    break
                min0_ = res.values[len(res.values) - 1].int_value
                if (min0_ == 0): 
                    break
                max0_ = (Utils.asObjectOrNull(t1.next0_, NumberToken)).value
                if (max0_ < min0_): 
                    break
                if ((max0_ - min0_) > 200): 
                    break
                val = PartToken.PartValue._new1026(t1.next0_, t1.next0_, str(max0_))
                val.correctValue()
                res.values.append(val)
                res.end_token = val.end_token
                t1 = res.end_token.next0_
                continue
            break
        if (len(res.values) == 0 and not res.is_newline_after and BracketHelper.canBeStartOfSequence(res.end_token, True, False)): 
            lev = PartToken._getRank(res.typ)
            if (lev > 0 and (lev < PartToken._getRank(PartToken.ItemType.CLAUSE))): 
                br = BracketHelper.tryParse(res.end_token, BracketParseAttr.NO, 100)
                if (br is not None): 
                    res.name = MiscHelper.getTextValueOfMetaToken(br, GetTextAttr.NO)
                    res.end_token = br.end_token
        if (len(res.values) == 0 and res.name is None): 
            if (not ignore_number and res.typ != PartToken.ItemType.PREAMBLE and res.typ != PartToken.ItemType.SUBPROGRAM): 
                return None
            if (res.begin_token != res.end_token): 
                res.end_token = res.end_token.previous
        return res
    
    @staticmethod
    def __createPartTyp0(t1 : 'Token', prev : 'PartToken') -> 'PartToken':
        wrapis_short1048 = RefOutArgWrapper(False)
        pt = PartToken.__createPartTyp(t1, prev, wrapis_short1048)
        is_short = wrapis_short1048.value
        if (pt is None): 
            return None
        if ((is_short and not pt.end_token.is_whitespace_after and pt.end_token.next0_ is not None) and pt.end_token.next0_.isChar('.')): 
            if (not pt.end_token.next0_.is_newline_after): 
                pt.end_token = pt.end_token.next0_
        return pt
    
    @staticmethod
    def __createPartTyp(t1 : 'Token', prev : 'PartToken', is_short : bool) -> 'PartToken':
        is_short.value = False
        if (t1 is None): 
            return None
        if (t1.isValue("ЧАСТЬ", "ЧАСТИНА")): 
            return PartToken._new797(t1, t1, PartToken.ItemType.PART)
        if (t1.isValue("Ч", None)): 
            is_short.value = True
            return PartToken._new797(t1, t1, PartToken.ItemType.PART)
        if (t1.isValue("ГЛАВА", None) or t1.isValue("ГЛ", None)): 
            is_short.value = t1.length_char == 2
            return PartToken._new797(t1, t1, PartToken.ItemType.CHAPTER)
        if (t1.isValue("ПРИЛОЖЕНИЕ", "ДОДАТОК") or t1.isValue("ПРИЛ", None)): 
            if ((t1.is_newline_before and t1.length_char > 6 and t1.next0_ is not None) and t1.next0_.isChar(':')): 
                return None
            is_short.value = (t1.length_char < 5)
            return PartToken._new797(t1, t1, PartToken.ItemType.APPENDIX)
        if (t1.isValue("ПРИМЕЧАНИЕ", "ПРИМІТКА") or t1.isValue("ПРИМ", None)): 
            is_short.value = (t1.length_char < 5)
            return PartToken._new797(t1, t1, PartToken.ItemType.NOTICE)
        if (t1.isValue("СТАТЬЯ", "СТАТТЯ") or t1.isValue("СТ", None)): 
            is_short.value = (t1.length_char < 3)
            return PartToken._new797(t1, t1, PartToken.ItemType.CLAUSE)
        if (t1.isValue("ПУНКТ", None) or t1.isValue("П", None) or t1.isValue("ПП", None)): 
            is_short.value = (t1.length_char < 3)
            return PartToken._new1055(t1, t1, PartToken.ItemType.ITEM, (PartToken.ItemType.SUBITEM if t1.isValue("ПП", None) else PartToken.ItemType.UNDEFINED))
        if (t1.isValue("ПОДПУНКТ", "ПІДПУНКТ")): 
            return PartToken._new797(t1, t1, PartToken.ItemType.SUBITEM)
        if (t1.isValue("ПРЕАМБУЛА", None)): 
            return PartToken._new797(t1, t1, PartToken.ItemType.PREAMBLE)
        if (t1.isValue("ПОДП", None) or t1.isValue("ПІДП", None)): 
            is_short.value = True
            return PartToken._new797(t1, t1, PartToken.ItemType.SUBITEM)
        if (t1.isValue("РАЗДЕЛ", "РОЗДІЛ") or t1.isValue("РАЗД", None)): 
            is_short.value = (t1.length_char < 5)
            return PartToken._new797(t1, t1, PartToken.ItemType.SECTION)
        if (((t1.isValue("Р", None) or t1.isValue("P", None))) and t1.next0_ is not None and t1.next0_.isChar('.')): 
            if (prev is not None): 
                if (prev.typ == PartToken.ItemType.ITEM or prev.typ == PartToken.ItemType.SUBITEM): 
                    is_short.value = True
                    return PartToken._new797(t1, t1.next0_, PartToken.ItemType.SECTION)
        if (t1.isValue("ПОДРАЗДЕЛ", "ПІРОЗДІЛ")): 
            return PartToken._new797(t1, t1, PartToken.ItemType.SUBSECTION)
        if (t1.isValue("ПАРАГРАФ", None) or t1.isValue("§", None)): 
            return PartToken._new797(t1, t1, PartToken.ItemType.PARAGRAPH)
        if (t1.isValue("АБЗАЦ", None) or t1.isValue("АБЗ", None)): 
            is_short.value = (t1.length_char < 7)
            return PartToken._new797(t1, t1, PartToken.ItemType.INDENTION)
        if (t1.isValue("СТРАНИЦА", "СТОРІНКА") or t1.isValue("СТР", "СТОР")): 
            is_short.value = (t1.length_char < 7)
            return PartToken._new797(t1, t1, PartToken.ItemType.PAGE)
        if (t1.isValue("ПОДАБЗАЦ", "ПІДАБЗАЦ") or t1.isValue("ПОДАБЗ", "ПІДАБЗ")): 
            return PartToken._new797(t1, t1, PartToken.ItemType.SUBINDENTION)
        if (t1.isValue("ПОДПАРАГРАФ", "ПІДПАРАГРАФ")): 
            return PartToken._new797(t1, t1, PartToken.ItemType.SUBPARAGRAPH)
        if (t1.isValue("ПОДПРОГРАММА", "ПІДПРОГРАМА")): 
            return PartToken._new797(t1, t1, PartToken.ItemType.SUBPROGRAM)
        if (t1.isValue("ДОПСОГЛАШЕНИЕ", None)): 
            return PartToken._new797(t1, t1, PartToken.ItemType.ADDAGREE)
        if (((t1.isValue("ДОП", None) or t1.isValue("ДОПОЛНИТЕЛЬНЫЙ", "ДОДАТКОВА"))) and t1.next0_ is not None): 
            tt = t1.next0_
            if (tt.isChar('.') and tt.next0_ is not None): 
                tt = tt.next0_
            if (tt.isValue("СОГЛАШЕНИЕ", "УГОДА")): 
                return PartToken._new797(t1, tt, PartToken.ItemType.ADDAGREE)
        return None
    
    @staticmethod
    def tryAttachList(t : 'Token', in_bracket : bool=False, max_count : int=40) -> typing.List['PartToken']:
        """ Привязать примитивы в контейнере с указанной позиции
        
        Returns:
            typing.List[PartToken]: Список примитивов
        """
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.NumberToken import NumberToken
        p = PartToken.tryAttach(t, None, in_bracket, False)
        if (p is None): 
            return None
        res = list()
        res.append(p)
        if (p.is_newline_after and p.is_newline_before): 
            if (not p.begin_token.chars.is_all_lower): 
                return res
        tt = p.end_token.next0_
        while tt is not None:
            if (tt.whitespaces_before_count > 15): 
                if (tt.previous is not None and tt.previous.is_comma_and): 
                    pass
                else: 
                    break
            if (max_count > 0 and len(res) >= max_count): 
                break
            delim = False
            if (((tt.isCharOf(",;.") or tt.is_and or tt.is_or)) and tt.next0_ is not None): 
                if (tt.isCharOf(";.")): 
                    res[len(res) - 1].has_terminator = True
                else: 
                    res[len(res) - 1].delim_after = True
                    if ((tt.next0_ is not None and tt.next0_.isValue("А", None) and tt.next0_.next0_ is not None) and tt.next0_.next0_.isValue("ТАКЖЕ", "ТАКОЖ")): 
                        tt = tt.next0_.next0_
                tt = tt.next0_
                delim = True
            if (tt is None): 
                break
            if (tt.is_newline_before): 
                if (tt.chars.is_letter and not tt.chars.is_all_lower): 
                    break
            if (tt.isChar('(')): 
                br = BracketHelper.tryParse(tt, BracketParseAttr.NO, 100)
                if (br is not None): 
                    li = PartToken.tryAttachList(tt.next0_, True, 40)
                    if (li is not None and len(li) > 0): 
                        if (li[0].typ == PartToken.ItemType.PARAGRAPH or li[0].typ == PartToken.ItemType.PART or li[0].typ == PartToken.ItemType.ITEM): 
                            if (li[len(li) - 1].end_token.next0_ == br.end_token): 
                                if (len(p.values) > 1): 
                                    ii = 1
                                    while ii < len(p.values): 
                                        pp = PartToken._new797(p.values[ii].begin_token, (p.end_token if ii == (len(p.values) - 1) else p.values[ii].end_token), p.typ)
                                        pp.values.append(p.values[ii])
                                        res.append(pp)
                                        ii += 1
                                    if (p.values[1].begin_token.previous is not None and p.values[1].begin_token.previous.end_char >= p.begin_token.begin_char): 
                                        p.end_token = p.values[1].begin_token.previous
                                    del p.values[1:1+len(p.values) - 1]
                                res.extend(li)
                                li[len(li) - 1].end_token = br.end_token
                                tt = br.end_token.next0_
                                continue
            p0 = PartToken.tryAttach(tt, p, in_bracket, False)
            if (p0 is None and ((tt.isValue("В", None) or tt.isValue("К", None) or tt.isValue("ДО", None)))): 
                p0 = PartToken.tryAttach(tt.next0_, p, in_bracket, False)
            if (p0 is None): 
                if (BracketHelper.isBracket(tt, False)): 
                    br = BracketHelper.tryParse(tt, BracketParseAttr.NO, 100)
                    if (br is not None): 
                        p0 = PartToken.tryAttach(br.end_token.next0_, None, False, False)
                        if (p0 is not None and p0.typ != PartToken.ItemType.PREFIX and len(p0.values) > 0): 
                            res[len(res) - 1].end_token = br.end_token
                            res[len(res) - 1].name = MiscHelper.getTextValueOfMetaToken(br, GetTextAttr.NO)
                            p = p0
                            res.append(p)
                            tt = p.end_token.next0_
                            continue
                if (tt.is_newline_before): 
                    if (len(res) == 1 and res[0].is_newline_before): 
                        break
                    if (tt.previous is not None and tt.previous.is_comma_and): 
                        pass
                    else: 
                        break
                if ((isinstance(tt, NumberToken)) and delim): 
                    p0 = (None)
                    if (p.typ == PartToken.ItemType.CLAUSE or in_bracket): 
                        p0 = PartToken._new797(tt, tt, PartToken.ItemType.CLAUSE)
                    elif (len(res) > 1 and res[len(res) - 2].typ == PartToken.ItemType.CLAUSE and res[len(res) - 1].typ == PartToken.ItemType.PART): 
                        p0 = PartToken._new797(tt, tt, PartToken.ItemType.CLAUSE)
                    elif ((len(res) > 2 and res[len(res) - 3].typ == PartToken.ItemType.CLAUSE and res[len(res) - 2].typ == PartToken.ItemType.PART) and res[len(res) - 1].typ == PartToken.ItemType.ITEM): 
                        p0 = PartToken._new797(tt, tt, PartToken.ItemType.CLAUSE)
                    elif (len(res) > 0 and len(res[len(res) - 1].values) > 0 and "." in res[len(res) - 1].values[0].value): 
                        p0 = PartToken._new797(tt, tt, res[len(res) - 1].typ)
                    if (p0 is None): 
                        break
                    vv = PartToken.PartValue._new1026(tt, tt, str((Utils.asObjectOrNull(tt, NumberToken)).value))
                    p0.values.append(vv)
                    vv.correctValue()
                    p0.end_token = vv.end_token
                    tt = p0.end_token.next0_
                    if (tt is not None and tt.is_hiphen and ((isinstance(tt.next0_, NumberToken)))): 
                        tt = tt.next0_
                        vv = PartToken.PartValue._new1026(tt, tt, str((Utils.asObjectOrNull(tt, NumberToken)).value))
                        vv.correctValue()
                        p0.values.append(vv)
                        p0.end_token = vv.end_token
                        tt = p0.end_token.next0_
            if (tt.isChar(',') and not tt.is_newline_after): 
                p1 = PartToken.tryAttach(tt.next0_, p, False, False)
                if (p1 is not None and PartToken._getRank(p1.typ) > 0 and PartToken._getRank(p.typ) > 0): 
                    if (PartToken._getRank(p1.typ) < PartToken._getRank(p.typ)): 
                        p0 = p1
            if (p0 is None): 
                break
            if (p0.is_newline_before and len(res) == 1 and res[0].is_newline_before): 
                break
            if (p0.typ == PartToken.ItemType.ITEM and p.typ == PartToken.ItemType.ITEM): 
                if (p0.alt_typ == PartToken.ItemType.UNDEFINED and p.alt_typ == PartToken.ItemType.SUBITEM): 
                    p.typ = PartToken.ItemType.SUBITEM
                    p.alt_typ = PartToken.ItemType.UNDEFINED
                elif (p.alt_typ == PartToken.ItemType.UNDEFINED and p0.alt_typ == PartToken.ItemType.SUBITEM): 
                    p0.typ = PartToken.ItemType.SUBITEM
                    p0.alt_typ = PartToken.ItemType.UNDEFINED
            p = p0
            res.append(p)
            tt = p.end_token.next0_
        i = 0
        first_pass2865 = True
        while True:
            if first_pass2865: first_pass2865 = False
            else: i += 1
            if (not (i < (len(res) - 1))): break
            if (res[i].typ == PartToken.ItemType.PART and res[i + 1].typ == PartToken.ItemType.PART and len(res[i].values) > 1): 
                v1 = res[i].values[len(res[i].values) - 2].int_value
                v2 = res[i].values[len(res[i].values) - 1].int_value
                if (v1 == 0 or v2 == 0): 
                    continue
                if ((v2 - v1) < 10): 
                    continue
                pt = PartToken._new797(res[i].end_token, res[i].end_token, PartToken.ItemType.CLAUSE)
                pt.values.append(PartToken.PartValue._new1026(res[i].end_token, res[i].end_token, str(v2)))
                del res[i].values[len(res[i].values) - 1]
                if (res[i].end_token != res[i].begin_token): 
                    res[i].end_token = res[i].end_token.previous
                res.insert(i + 1, pt)
        if ((len(res) == 1 and res[0].typ == PartToken.ItemType.SUBPROGRAM and res[0].end_token.next0_ is not None) and res[0].end_token.next0_.isChar('.')): 
            res[0].end_token = res[0].end_token.next0_
        for i in range(len(res) - 1, -1, -1):
            p = res[i]
            if (p.is_newline_after and p.is_newline_before and p.typ != PartToken.ItemType.SUBPROGRAM): 
                del res[i:i+len(res) - i]
                continue
            if (((i == 0 and p.is_newline_before and p.has_terminator) and p.end_token.next0_ is not None and p.end_token.next0_.isChar('.')) and MiscHelper.canBeStartOfSentence(p.end_token.next0_.next0_)): 
                del res[i]
                continue
        return (None if len(res) == 0 else res)
    
    def canBeNextNarrow(self, p : 'PartToken') -> bool:
        if (self.typ == p.typ): 
            if (self.typ != PartToken.ItemType.SUBITEM): 
                return False
            if (p.values is not None and len(p.values) > 0 and p.values[0].int_value == 0): 
                if (self.values is not None and len(self.values) > 0 and self.values[0].int_value > 0): 
                    return True
            return False
        if (self.typ == PartToken.ItemType.PART or p.typ == PartToken.ItemType.PART): 
            return True
        i1 = PartToken._getRank(self.typ)
        i2 = PartToken._getRank(p.typ)
        if (i1 >= 0 and i2 >= 0): 
            return i1 < i2
        return False
    
    @staticmethod
    def isPartBefore(t0 : 'Token') -> bool:
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.TextToken import TextToken
        if (t0 is None): 
            return False
        i = 0
        tt = t0.previous
        while tt is not None: 
            if (tt.is_newline_after or ((isinstance(tt, ReferentToken)))): 
                break
            else: 
                st = PartToken.tryAttach(tt, None, False, False)
                if (st is not None): 
                    if (st.end_token.next0_ == t0): 
                        return True
                    break
                if ((isinstance(tt, TextToken)) and tt.chars.is_letter): 
                    i += 1
                    if ((i) > 2): 
                        break
            tt = tt.previous
        return False
    
    @staticmethod
    def _getRank(t : 'ItemType') -> int:
        if (t == PartToken.ItemType.DOCPART): 
            return 1
        if (t == PartToken.ItemType.APPENDIX): 
            return 1
        if (t == PartToken.ItemType.SECTION): 
            return 2
        if (t == PartToken.ItemType.SUBPROGRAM): 
            return 2
        if (t == PartToken.ItemType.SUBSECTION): 
            return 3
        if (t == PartToken.ItemType.CHAPTER): 
            return 4
        if (t == PartToken.ItemType.PREAMBLE): 
            return 5
        if (t == PartToken.ItemType.PARAGRAPH): 
            return 5
        if (t == PartToken.ItemType.SUBPARAGRAPH): 
            return 6
        if (t == PartToken.ItemType.PAGE): 
            return 6
        if (t == PartToken.ItemType.CLAUSE): 
            return 7
        if (t == PartToken.ItemType.PART): 
            return 8
        if (t == PartToken.ItemType.NOTICE): 
            return 8
        if (t == PartToken.ItemType.ITEM): 
            return 9
        if (t == PartToken.ItemType.SUBITEM): 
            return 10
        if (t == PartToken.ItemType.INDENTION): 
            return 11
        if (t == PartToken.ItemType.SUBINDENTION): 
            return 12
        return 0
    
    @staticmethod
    def _getAttrNameByTyp(typ_ : 'ItemType') -> str:
        from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
        if (typ_ == PartToken.ItemType.CHAPTER): 
            return DecreePartReferent.ATTR_CHAPTER
        if (typ_ == PartToken.ItemType.APPENDIX): 
            return DecreePartReferent.ATTR_APPENDIX
        if (typ_ == PartToken.ItemType.CLAUSE): 
            return DecreePartReferent.ATTR_CLAUSE
        if (typ_ == PartToken.ItemType.INDENTION): 
            return DecreePartReferent.ATTR_INDENTION
        if (typ_ == PartToken.ItemType.ITEM): 
            return DecreePartReferent.ATTR_ITEM
        if (typ_ == PartToken.ItemType.PARAGRAPH): 
            return DecreePartReferent.ATTR_PARAGRAPH
        if (typ_ == PartToken.ItemType.SUBPARAGRAPH): 
            return DecreePartReferent.ATTR_SUBPARAGRAPH
        if (typ_ == PartToken.ItemType.PART): 
            return DecreePartReferent.ATTR_PART
        if (typ_ == PartToken.ItemType.SECTION): 
            return DecreePartReferent.ATTR_SECTION
        if (typ_ == PartToken.ItemType.SUBSECTION): 
            return DecreePartReferent.ATTR_SUBSECTION
        if (typ_ == PartToken.ItemType.SUBINDENTION): 
            return DecreePartReferent.ATTR_SUBINDENTION
        if (typ_ == PartToken.ItemType.SUBITEM): 
            return DecreePartReferent.ATTR_SUBITEM
        if (typ_ == PartToken.ItemType.PREAMBLE): 
            return DecreePartReferent.ATTR_PREAMBLE
        if (typ_ == PartToken.ItemType.NOTICE): 
            return DecreePartReferent.ATTR_NOTICE
        if (typ_ == PartToken.ItemType.SUBPROGRAM): 
            return DecreePartReferent.ATTR_SUBPROGRAM
        if (typ_ == PartToken.ItemType.ADDAGREE): 
            return DecreePartReferent.ATTR_ADDAGREE
        if (typ_ == PartToken.ItemType.DOCPART): 
            return DecreePartReferent.ATTR_DOCPART
        if (typ_ == PartToken.ItemType.PAGE): 
            return DecreePartReferent.ATTR_PAGE
        return None
    
    @staticmethod
    def _getInstrKindByTyp(typ_ : 'ItemType') -> 'InstrumentKind':
        if (typ_ == PartToken.ItemType.CHAPTER): 
            return InstrumentKind.CHAPTER
        if (typ_ == PartToken.ItemType.APPENDIX): 
            return InstrumentKind.APPENDIX
        if (typ_ == PartToken.ItemType.CLAUSE): 
            return InstrumentKind.CLAUSE
        if (typ_ == PartToken.ItemType.INDENTION): 
            return InstrumentKind.INDENTION
        if (typ_ == PartToken.ItemType.ITEM): 
            return InstrumentKind.ITEM
        if (typ_ == PartToken.ItemType.PARAGRAPH): 
            return InstrumentKind.PARAGRAPH
        if (typ_ == PartToken.ItemType.SUBPARAGRAPH): 
            return InstrumentKind.SUBPARAGRAPH
        if (typ_ == PartToken.ItemType.PART): 
            return InstrumentKind.CLAUSEPART
        if (typ_ == PartToken.ItemType.SECTION): 
            return InstrumentKind.SECTION
        if (typ_ == PartToken.ItemType.SUBSECTION): 
            return InstrumentKind.SUBSECTION
        if (typ_ == PartToken.ItemType.SUBITEM): 
            return InstrumentKind.SUBITEM
        if (typ_ == PartToken.ItemType.PREAMBLE): 
            return InstrumentKind.PREAMBLE
        if (typ_ == PartToken.ItemType.NOTICE): 
            return InstrumentKind.NOTICE
        if (typ_ == PartToken.ItemType.DOCPART): 
            return InstrumentKind.DOCPART
        return InstrumentKind.UNDEFINED
    
    @staticmethod
    def _getTypeByAttrName(name_ : str) -> 'ItemType':
        from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
        if (name_ == DecreePartReferent.ATTR_CHAPTER): 
            return PartToken.ItemType.CHAPTER
        if (name_ == DecreePartReferent.ATTR_APPENDIX): 
            return PartToken.ItemType.APPENDIX
        if (name_ == DecreePartReferent.ATTR_CLAUSE): 
            return PartToken.ItemType.CLAUSE
        if (name_ == DecreePartReferent.ATTR_INDENTION): 
            return PartToken.ItemType.INDENTION
        if (name_ == DecreePartReferent.ATTR_ITEM): 
            return PartToken.ItemType.ITEM
        if (name_ == DecreePartReferent.ATTR_PARAGRAPH): 
            return PartToken.ItemType.PARAGRAPH
        if (name_ == DecreePartReferent.ATTR_SUBPARAGRAPH): 
            return PartToken.ItemType.SUBPARAGRAPH
        if (name_ == DecreePartReferent.ATTR_PART): 
            return PartToken.ItemType.PART
        if (name_ == DecreePartReferent.ATTR_SECTION): 
            return PartToken.ItemType.SECTION
        if (name_ == DecreePartReferent.ATTR_SUBSECTION): 
            return PartToken.ItemType.SUBSECTION
        if (name_ == DecreePartReferent.ATTR_SUBINDENTION): 
            return PartToken.ItemType.SUBINDENTION
        if (name_ == DecreePartReferent.ATTR_SUBITEM): 
            return PartToken.ItemType.SUBITEM
        if (name_ == DecreePartReferent.ATTR_NOTICE): 
            return PartToken.ItemType.NOTICE
        if (name_ == DecreePartReferent.ATTR_PREAMBLE): 
            return PartToken.ItemType.PREAMBLE
        if (name_ == DecreePartReferent.ATTR_SUBPROGRAM): 
            return PartToken.ItemType.SUBPROGRAM
        if (name_ == DecreePartReferent.ATTR_ADDAGREE): 
            return PartToken.ItemType.ADDAGREE
        if (name_ == DecreePartReferent.ATTR_DOCPART): 
            return PartToken.ItemType.DOCPART
        return PartToken.ItemType.PREFIX
    
    @staticmethod
    def tryCreateBetween(p1 : 'DecreePartReferent', p2 : 'DecreePartReferent') -> typing.List['DecreePartReferent']:
        from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
        not_eq_attr = None
        val1 = None
        val2 = None
        for s1 in p1.slots: 
            if (p2.findSlot(s1.type_name, s1.value, True) is not None): 
                continue
            else: 
                if (not_eq_attr is not None): 
                    return None
                val2 = p2.getStringValue(s1.type_name)
                if (val2 is None): 
                    return None
                not_eq_attr = s1.type_name
                val1 = (Utils.asObjectOrNull(s1.value, str))
        if (val1 is None or val2 is None): 
            return None
        diap = NumberingHelper.createDiap(val1, val2)
        if (diap is None or (len(diap) < 3)): 
            return None
        res = list()
        i = 1
        while i < (len(diap) - 1): 
            dpr = DecreePartReferent()
            for s in p1.slots: 
                val = s.value
                if (s.type_name == not_eq_attr): 
                    val = (diap[i])
                dpr.addSlot(s.type_name, val, False, 0)
            res.append(dpr)
            i += 1
        return res
    
    @staticmethod
    def getNumber(str0_ : str) -> int:
        if (Utils.isNullOrEmpty(str0_)): 
            return 0
        wrapi1083 = RefOutArgWrapper(0)
        inoutres1084 = Utils.tryParseInt(str0_, wrapi1083)
        i = wrapi1083.value
        if (inoutres1084): 
            return i
        if (not str.isalpha(str0_[0])): 
            return 0
        ch = str.upper(str0_[0])
        if ((ord(ch)) < 0x80): 
            i = (((ord(ch)) - (ord('A'))) + 1)
            if ((ch == 'Z' and len(str0_) > 2 and str0_[1] == '.') and str.isdigit(str0_[2])): 
                wrapn1079 = RefOutArgWrapper(0)
                inoutres1080 = Utils.tryParseInt(str0_[2:], wrapn1079)
                n = wrapn1079.value
                if (inoutres1080): 
                    i += n
        elif (LanguageHelper.isCyrillicChar(ch)): 
            i = PartToken.RU_NUMS.find(ch)
            if (i < 0): 
                return 0
            i += 1
            if ((ch == 'Я' and len(str0_) > 2 and str0_[1] == '.') and str.isdigit(str0_[2])): 
                wrapn1081 = RefOutArgWrapper(0)
                inoutres1082 = Utils.tryParseInt(str0_[2:], wrapn1081)
                n = wrapn1081.value
                if (inoutres1082): 
                    i += n
        if (i < 0): 
            return 0
        return i
    
    RU_NUMS = "АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЭЮЯ"
    
    @staticmethod
    def _new797(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType') -> 'PartToken':
        res = PartToken(_arg1, _arg2)
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new1029(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : bool) -> 'PartToken':
        res = PartToken(_arg1, _arg2)
        res.typ = _arg3
        res.is_doubt = _arg4
        return res
    
    @staticmethod
    def _new1055(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : 'ItemType') -> 'PartToken':
        res = PartToken(_arg1, _arg2)
        res.typ = _arg3
        res.alt_typ = _arg4
        return res