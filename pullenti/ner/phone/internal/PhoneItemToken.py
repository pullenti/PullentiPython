# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
import typing
from enum import IntEnum
from pullenti.unisharp.Utils import Utils
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.phone.PhoneKind import PhoneKind
from pullenti.ner.phone.internal.PhoneHelper import PhoneHelper
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.morph.LanguageHelper import LanguageHelper


class PhoneItemToken(MetaToken):
    """ Примитив, из которых состоит телефонный номер """
    
    class PhoneItemType(IntEnum):
        NUMBER = 0
        CITYCODE = 0 + 1
        DELIM = (0 + 1) + 1
        PREFIX = ((0 + 1) + 1) + 1
        ADDNUMBER = (((0 + 1) + 1) + 1) + 1
        COUNTRYCODE = ((((0 + 1) + 1) + 1) + 1) + 1
        ALT = (((((0 + 1) + 1) + 1) + 1) + 1) + 1
        
        @classmethod
        def has_value(cls, value):
            return any(value == item.value for item in cls)
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.item_type = PhoneItemToken.PhoneItemType.NUMBER
        self.value = None;
        self.kind = PhoneKind.UNDEFINED
        self.is_in_brackets = False
    
    @property
    def can_be_country_prefix(self) -> bool:
        if (self.value is not None and PhoneHelper.getCountryPrefix(self.value) == self.value): 
            return True
        else: 
            return False
    
    def __str__(self) -> str:
        return (Utils.enumToString(self.item_type) + ": " + self.value) + ((("" if self.kind == PhoneKind.UNDEFINED else " ({0})".format(Utils.enumToString(self.kind)))))
    
    @staticmethod
    def tryAttach(t0 : 'Token') -> 'PhoneItemToken':
        """ Привязать с указанной позиции один примитив
        
        Args:
            cnt: 
            indFrom: 
        
        """
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
        res = PhoneItemToken.__TryAttach(t0)
        if (res is None): 
            return None
        if (res.item_type != PhoneItemToken.PhoneItemType.PREFIX): 
            return res
        t = res.end_token.next0_
        first_pass3128 = True
        while True:
            if first_pass3128: first_pass3128 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_table_control_char): 
                break
            if (t.is_newline_before): 
                break
            res2 = PhoneItemToken.__TryAttach(t)
            if (res2 is not None): 
                if (res2.item_type == PhoneItemToken.PhoneItemType.PREFIX): 
                    if (res.kind == PhoneKind.UNDEFINED): 
                        res.kind = res2.kind
                    res.end_token = res2.end_token
                    t = res.end_token
                    continue
                break
            if (t.isChar(':')): 
                res.end_token = t
                break
            if (not ((isinstance(t, TextToken)))): 
                break
            if (t0.length_char == 1): 
                break
            npt = NounPhraseHelper.tryParse(t, NounPhraseParseAttr.NO, 0)
            if (npt is not None): 
                t = npt.end_token
                if (t.isValue("ПОСЕЛЕНИЕ", None)): 
                    return None
                res.end_token = t
                continue
            if (t.morph.class0_.is_preposition): 
                continue
            break
        return res
    
    @staticmethod
    def __TryAttach(t0 : 'Token') -> 'PhoneItemToken':
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.core.NumberExToken import NumberExToken
        if (t0 is None): 
            return None
        if (isinstance(t0, NumberToken)): 
            if (NumberExToken.tryParseNumberWithPostfix(t0) is not None and not t0.is_whitespace_after): 
                rt = t0.kit.processReferent("PHONE", t0.next0_)
                if (rt is None): 
                    return None
            if ((Utils.asObjectOrNull(t0, NumberToken)).typ == NumberSpellingType.DIGIT and not t0.morph.class0_.is_adjective): 
                return PhoneItemToken._new2478(t0, t0, PhoneItemToken.PhoneItemType.NUMBER, t0.getSourceText())
            return None
        if (t0.isChar('.')): 
            return PhoneItemToken._new2478(t0, t0, PhoneItemToken.PhoneItemType.DELIM, ".")
        if (t0.is_hiphen): 
            return PhoneItemToken._new2478(t0, t0, PhoneItemToken.PhoneItemType.DELIM, "-")
        if (t0.isChar('+')): 
            if (not ((isinstance(t0.next0_, NumberToken))) or (Utils.asObjectOrNull(t0.next0_, NumberToken)).typ != NumberSpellingType.DIGIT): 
                return None
            else: 
                val = t0.next0_.getSourceText()
                i = 0
                while i < len(val): 
                    if (val[i] != '0'): 
                        break
                    i += 1
                if (i >= len(val)): 
                    return None
                if (i > 0): 
                    val = val[i:]
                return PhoneItemToken._new2478(t0, t0.next0_, PhoneItemToken.PhoneItemType.COUNTRYCODE, val)
        if (t0.isChar(chr(0x2011)) and (isinstance(t0.next0_, NumberToken)) and t0.next0_.length_char == 2): 
            return PhoneItemToken._new2478(t0, t0, PhoneItemToken.PhoneItemType.DELIM, "-")
        if (t0.isCharOf("(")): 
            if (isinstance(t0.next0_, NumberToken)): 
                et = t0.next0_
                val = io.StringIO()
                while et is not None: 
                    if (et.isChar(')')): 
                        break
                    if (((isinstance(et, NumberToken))) and (Utils.asObjectOrNull(et, NumberToken)).typ == NumberSpellingType.DIGIT): 
                        print(et.getSourceText(), end="", file=val)
                    elif (not et.is_hiphen and not et.isChar('.')): 
                        return None
                    et = et.next0_
                if (et is None or val.tell() == 0): 
                    return None
                else: 
                    return PhoneItemToken._new2483(t0, et, PhoneItemToken.PhoneItemType.CITYCODE, Utils.toStringStringIO(val), True)
            else: 
                tt1 = PhoneItemToken.M_PHONE_TERMINS.tryParse(t0.next0_, TerminParseAttr.NO)
                if (tt1 is None or tt1.termin.tag is not None): 
                    pass
                elif (tt1.end_token.next0_ is None or not tt1.end_token.next0_.isChar(')')): 
                    pass
                else: 
                    return PhoneItemToken._new2484(t0, tt1.end_token.next0_, PhoneItemToken.PhoneItemType.PREFIX, True, "")
                return None
        if ((t0.isChar('/') and (isinstance(t0.next0_, NumberToken)) and t0.next0_.next0_ is not None) and t0.next0_.next0_.isChar('/') and t0.next0_.length_char == 3): 
            return PhoneItemToken._new2483(t0, t0.next0_.next0_, PhoneItemToken.PhoneItemType.CITYCODE, str((Utils.asObjectOrNull(t0.next0_, NumberToken)).value), True)
        t1 = None
        ki = PhoneKind.UNDEFINED
        if ((t0.isValue("Т", None) and t0.next0_ is not None and t0.next0_.isCharOf("\\/")) and t0.next0_.next0_ is not None and ((t0.next0_.next0_.isValue("Р", None) or t0.next0_.next0_.isValue("М", None)))): 
            t1 = t0.next0_.next0_
            ki = (PhoneKind.WORK if t1.isValue("Р", None) else PhoneKind.MOBILE)
        else: 
            tt = PhoneItemToken.M_PHONE_TERMINS.tryParse(t0, TerminParseAttr.NO)
            if (tt is None or tt.termin.tag is not None): 
                if (t0.isValue("НОМЕР", None)): 
                    rr = PhoneItemToken.__TryAttach(t0.next0_)
                    if (rr is not None and rr.item_type == PhoneItemToken.PhoneItemType.PREFIX): 
                        rr.begin_token = t0
                        return rr
                return None
            if (isinstance(tt.termin.tag2, PhoneKind)): 
                ki = (Utils.valToEnum(tt.termin.tag2, PhoneKind))
            t1 = tt.end_token
        res = PhoneItemToken._new2486(t0, t1, PhoneItemToken.PhoneItemType.PREFIX, "", ki)
        while True:
            if (t1.next0_ is not None and t1.next0_.isCharOf(".:")): 
                t1 = t1.next0_
                res.end_token = t1
            elif (t1.next0_ is not None and t1.next0_.is_table_control_char): 
                t1 = t1.next0_
            else: 
                break
        if (t0 == t1 and ((t0.begin_char == t0.end_char or t0.chars.is_all_upper))): 
            if (not t0.is_whitespace_after): 
                return None
        return res
    
    @staticmethod
    def tryAttachAdditional(t0 : 'Token') -> 'PhoneItemToken':
        from pullenti.ner.NumberToken import NumberToken
        t = t0
        if (t is None): 
            return None
        if (t.isChar(',')): 
            t = t.next0_
        elif (t.isCharOf("*#") and (isinstance(t.next0_, NumberToken))): 
            val0 = (Utils.asObjectOrNull(t.next0_, NumberToken)).getSourceText()
            t1 = t.next0_
            if ((t1.next0_ is not None and t1.next0_.is_hiphen and not t1.is_whitespace_after) and (isinstance(t1.next0_.next0_, NumberToken)) and not t1.next0_.is_whitespace_after): 
                t1 = t1.next0_.next0_
                val0 += t1.getSourceText()
            if (len(val0) >= 3 and (len(val0) < 7)): 
                return PhoneItemToken._new2478(t, t1, PhoneItemToken.PhoneItemType.ADDNUMBER, val0)
        br = False
        if (t is not None and t.isChar('(')): 
            br = True
            t = t.next0_
        to = PhoneItemToken.M_PHONE_TERMINS.tryParse(t, TerminParseAttr.NO)
        if (to is None): 
            if (not br): 
                return None
            if (t0.whitespaces_before_count > 1): 
                return None
        elif (to.termin.tag is None): 
            return None
        else: 
            t = to.end_token.next0_
        if (t is None): 
            return None
        if (((t.isValue("НОМЕР", None) or t.isValue("N", None) or t.isValue("#", None)) or t.isValue("№", None) or t.isValue("NUMBER", None)) or ((t.isChar('+') and br))): 
            t = t.next0_
        elif (to is None and not br): 
            return None
        elif (t.isValue("НОМ", None) or t.isValue("ТЕЛ", None)): 
            t = t.next0_
            if (t is not None and t.isChar('.')): 
                t = t.next0_
        if (t is not None and t.isCharOf(":,") and not t.is_newline_after): 
            t = t.next0_
        if (not ((isinstance(t, NumberToken)))): 
            return None
        val = (Utils.asObjectOrNull(t, NumberToken)).getSourceText()
        if ((t.next0_ is not None and t.next0_.is_hiphen and not t.is_whitespace_after) and (isinstance(t.next0_.next0_, NumberToken))): 
            val += t.next0_.next0_.getSourceText()
            t = t.next0_.next0_
        if ((len(val) < 2) or len(val) > 7): 
            return None
        if (br): 
            if (t.next0_ is None or not t.next0_.isChar(')')): 
                return None
            t = t.next0_
        res = PhoneItemToken._new2478(t0, t, PhoneItemToken.PhoneItemType.ADDNUMBER, val)
        return res
    
    @staticmethod
    def tryAttachAll(t0 : 'Token') -> typing.List['PhoneItemToken']:
        """ Привязать примитивы в контейнере с указанной позиции
        
        Args:
            cnt: 
            indFrom: 
        
        Returns:
            typing.List[PhoneItemToken]: Список примитивов
        """
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.TextToken import TextToken
        if (t0 is None): 
            return None
        p = PhoneItemToken.tryAttach(t0)
        br = False
        if (p is None and t0.isChar('(')): 
            br = True
            p = PhoneItemToken.tryAttach(t0.next0_)
            if (p is not None): 
                p.begin_token = t0
                p.is_in_brackets = True
                if (p.item_type == PhoneItemToken.PhoneItemType.PREFIX): 
                    br = False
        if (p is None or p.item_type == PhoneItemToken.PhoneItemType.DELIM): 
            return None
        res = list()
        res.append(p)
        t = p.end_token.next0_
        first_pass3129 = True
        while True:
            if first_pass3129: first_pass3129 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_table_control_char): 
                if (len(res) == 1 and res[0].item_type == PhoneItemToken.PhoneItemType.PREFIX): 
                    continue
                else: 
                    break
            if (br and t.isChar(')')): 
                br = False
                continue
            p0 = PhoneItemToken.tryAttach(t)
            if (p0 is None): 
                if (t.is_newline_before): 
                    break
                if (p.item_type == PhoneItemToken.PhoneItemType.PREFIX and ((t.isCharOf("\\/") or t.is_hiphen))): 
                    p0 = PhoneItemToken.tryAttach(t.next0_)
                    if (p0 is not None and p0.item_type == PhoneItemToken.PhoneItemType.PREFIX): 
                        p.end_token = p0.end_token
                        t = p.end_token
                        continue
                if ((res[0].item_type == PhoneItemToken.PhoneItemType.PREFIX and t.isCharOf("\\/") and not t.is_whitespace_after) and not t.is_whitespace_before and (isinstance(t.next0_, NumberToken))): 
                    sum_num = 0
                    for pp in res: 
                        if (pp.item_type == PhoneItemToken.PhoneItemType.CITYCODE or pp.item_type == PhoneItemToken.PhoneItemType.COUNTRYCODE or pp.item_type == PhoneItemToken.PhoneItemType.NUMBER): 
                            sum_num += len(pp.value)
                    if (sum_num < 7): 
                        tt = t.next0_
                        while tt is not None: 
                            if (tt.is_whitespace_before): 
                                break
                            elif (isinstance(tt, NumberToken)): 
                                sum_num += tt.length_char
                            elif ((isinstance(tt, TextToken)) and not tt.chars.is_letter): 
                                pass
                            else: 
                                break
                            tt = tt.next0_
                        if (sum_num == 10 or sum_num == 11): 
                            continue
                if (p0 is None): 
                    break
            if (t.is_newline_before): 
                if (p.item_type == PhoneItemToken.PhoneItemType.PREFIX): 
                    pass
                else: 
                    break
            if (t.whitespaces_before_count > 1): 
                ok = False
                for pp in res: 
                    if (pp.item_type == PhoneItemToken.PhoneItemType.PREFIX or pp.item_type == PhoneItemToken.PhoneItemType.COUNTRYCODE): 
                        ok = True
                        break
                if (not ok): 
                    break
            if (br and p.item_type == PhoneItemToken.PhoneItemType.NUMBER): 
                p.item_type = PhoneItemToken.PhoneItemType.CITYCODE
            p = p0
            if (p.item_type == PhoneItemToken.PhoneItemType.NUMBER and res[len(res) - 1].item_type == PhoneItemToken.PhoneItemType.NUMBER): 
                res.append(PhoneItemToken._new2478(t, t, PhoneItemToken.PhoneItemType.DELIM, " "))
            if (br): 
                p.is_in_brackets = True
            res.append(p)
            t = p.end_token
        p = PhoneItemToken.tryAttachAdditional(t)
        if ((p) is not None): 
            res.append(p)
        i = 1
        while i < (len(res) - 1): 
            if (res[i].item_type == PhoneItemToken.PhoneItemType.DELIM and res[i + 1].is_in_brackets): 
                del res[i]
                break
            elif (res[i].item_type == PhoneItemToken.PhoneItemType.DELIM and res[i + 1].item_type == PhoneItemToken.PhoneItemType.DELIM): 
                res[i].end_token = res[i + 1].end_token
                del res[i + 1]
                i -= 1
            i += 1
        if ((len(res) > 1 and res[0].is_in_brackets and res[0].item_type == PhoneItemToken.PhoneItemType.PREFIX) and res[len(res) - 1].end_token.next0_ is not None and res[len(res) - 1].end_token.next0_.isChar(')')): 
            res[len(res) - 1].end_token = res[len(res) - 1].end_token.next0_
        if (res[0].item_type == PhoneItemToken.PhoneItemType.PREFIX): 
            i = 2
            while i < (len(res) - 1): 
                if (res[i].item_type == PhoneItemToken.PhoneItemType.PREFIX and res[i + 1].item_type != PhoneItemToken.PhoneItemType.PREFIX): 
                    del res[i:i+len(res) - i]
                    break
                i += 1
        return res
    
    @staticmethod
    def tryAttachAlternate(t0 : 'Token', ph0 : 'PhoneReferent', pli : typing.List['PhoneItemToken']) -> 'PhoneItemToken':
        from pullenti.ner.NumberToken import NumberToken
        if (t0 is None): 
            return None
        if (t0.isCharOf("\\/") and (isinstance(t0.next0_, NumberToken)) and (t0.next0_.end_char - t0.next0_.begin_char) <= 1): 
            pli1 = PhoneItemToken.tryAttachAll(t0.next0_)
            if (pli1 is not None and len(pli1) > 1): 
                if (pli1[len(pli1) - 1].item_type == PhoneItemToken.PhoneItemType.DELIM): 
                    del pli1[len(pli1) - 1]
                if (len(pli1) <= len(pli)): 
                    num = ""
                    ii = 0
                    while ii < len(pli1): 
                        p1 = pli1[ii]
                        p0 = pli[(len(pli) - len(pli1)) + ii]
                        if (p1.item_type != p0.item_type): 
                            break
                        if (p1.item_type != PhoneItemToken.PhoneItemType.NUMBER and p1.item_type != PhoneItemToken.PhoneItemType.DELIM): 
                            break
                        if (p1.item_type == PhoneItemToken.PhoneItemType.NUMBER): 
                            if (p1.length_char != p0.length_char): 
                                break
                            num += p1.value
                        ii += 1
                    if (ii >= len(pli1)): 
                        return PhoneItemToken._new2478(t0, pli1[len(pli1) - 1].end_token, PhoneItemToken.PhoneItemType.ALT, num)
            return PhoneItemToken._new2478(t0, t0.next0_, PhoneItemToken.PhoneItemType.ALT, t0.next0_.getSourceText())
        if (t0.is_hiphen and (isinstance(t0.next0_, NumberToken)) and (t0.next0_.end_char - t0.next0_.begin_char) <= 1): 
            t1 = t0.next0_.next0_
            ok = False
            if (t1 is None): 
                ok = True
            elif (t1.is_newline_before or t1.isCharOf(",.")): 
                ok = True
            if (ok): 
                return PhoneItemToken._new2478(t0, t0.next0_, PhoneItemToken.PhoneItemType.ALT, t0.next0_.getSourceText())
        if ((t0.isChar('(') and (isinstance(t0.next0_, NumberToken)) and (t0.next0_.end_char - t0.next0_.begin_char) == 1) and t0.next0_.next0_ is not None and t0.next0_.next0_.isChar(')')): 
            return PhoneItemToken._new2478(t0, t0.next0_.next0_, PhoneItemToken.PhoneItemType.ALT, t0.next0_.getSourceText())
        if ((t0.isCharOf("/-") and (isinstance(t0.next0_, NumberToken)) and ph0._m_template is not None) and LanguageHelper.endsWith(ph0._m_template, str(((t0.next0_.end_char - t0.next0_.begin_char) + 1)))): 
            return PhoneItemToken._new2478(t0, t0.next0_, PhoneItemToken.PhoneItemType.ALT, t0.next0_.getSourceText())
        return None
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.core.TerminCollection import TerminCollection
        from pullenti.ner.core.Termin import Termin
        from pullenti.morph.MorphLang import MorphLang
        if (PhoneItemToken.M_PHONE_TERMINS is not None): 
            return
        PhoneItemToken.M_PHONE_TERMINS = TerminCollection()
        t = Termin("ТЕЛЕФОН", MorphLang.RU, True)
        t.addAbridge("ТЕЛ.")
        t.addAbridge("TEL.")
        t.addAbridge("Т-Н")
        t.addAbridge("Т.")
        t.addAbridge("T.")
        t.addAbridge("TEL.EXT.")
        t.addVariant("ТЛФ", False)
        t.addVariant("ТЛФН", False)
        t.addAbridge("Т/Ф")
        PhoneItemToken.M_PHONE_TERMINS.add(t)
        t = Termin._new2495("МОБИЛЬНЫЙ", MorphLang.RU, True, PhoneKind.MOBILE)
        t.addAbridge("МОБ.")
        t.addAbridge("Т.М.")
        t.addAbridge("М.Т.")
        t.addAbridge("М.")
        PhoneItemToken.M_PHONE_TERMINS.add(t)
        t = Termin._new2495("СОТОВЫЙ", MorphLang.RU, True, PhoneKind.MOBILE)
        t.addAbridge("СОТ.")
        t.addAbridge("CELL.")
        PhoneItemToken.M_PHONE_TERMINS.add(t)
        t = Termin._new2495("РАБОЧИЙ", MorphLang.RU, True, PhoneKind.WORK)
        t.addAbridge("РАБ.")
        t.addAbridge("Т.Р.")
        t.addAbridge("Р.Т.")
        PhoneItemToken.M_PHONE_TERMINS.add(t)
        t = Termin("ГОРОДСКОЙ", MorphLang.RU, True)
        t.addAbridge("ГОР.")
        t.addAbridge("Г.Т.")
        PhoneItemToken.M_PHONE_TERMINS.add(t)
        t = Termin._new2495("ДОМАШНИЙ", MorphLang.RU, True, PhoneKind.HOME)
        t.addAbridge("ДОМ.")
        PhoneItemToken.M_PHONE_TERMINS.add(t)
        t = Termin("КОНТАКТНЫЙ", MorphLang.RU, True)
        PhoneItemToken.M_PHONE_TERMINS.add(t)
        t = Termin("МНОГОКАНАЛЬНЫЙ", MorphLang.RU, True)
        PhoneItemToken.M_PHONE_TERMINS.add(t)
        t = Termin._new2495("ФАКС", MorphLang.RU, True, PhoneKind.FAX)
        t.addAbridge("Ф.")
        t.addAbridge("Т/ФАКС")
        t.addAbridge("ТЕЛ/ФАКС")
        PhoneItemToken.M_PHONE_TERMINS.add(t)
        t = Termin("ЗВОНИТЬ", MorphLang.RU, True)
        PhoneItemToken.M_PHONE_TERMINS.add(t)
        t = Termin._new2495("ПРИЕМНАЯ", MorphLang.RU, True, PhoneKind.WORK)
        PhoneItemToken.M_PHONE_TERMINS.add(t)
        t = Termin("PHONE", MorphLang.EN, True)
        t.addAbridge("PH.")
        t.addVariant("TELEFON", True)
        PhoneItemToken.M_PHONE_TERMINS.add(t)
        t = Termin._new2495("DIRECT LINE", MorphLang.EN, True, PhoneKind.WORK)
        t.addVariant("DIRECT LINES", True)
        PhoneItemToken.M_PHONE_TERMINS.add(t)
        t = Termin._new2495("MOBILE", MorphLang.EN, True, PhoneKind.MOBILE)
        t.addAbridge("MOB.")
        t.addVariant("MOBIL", True)
        t.addAbridge("M.")
        PhoneItemToken.M_PHONE_TERMINS.add(t)
        t = Termin._new2495("FAX", MorphLang.EN, True, PhoneKind.FAX)
        t.addAbridge("F.")
        PhoneItemToken.M_PHONE_TERMINS.add(t)
        t = Termin._new2495("HOME", MorphLang.EN, True, PhoneKind.HOME)
        PhoneItemToken.M_PHONE_TERMINS.add(t)
        t = Termin("CALL", MorphLang.EN, True)
        t.addVariant("SEDIU", True)
        PhoneItemToken.M_PHONE_TERMINS.add(t)
        t = Termin("ДОПОЛНИТЕЛЬНЫЙ", MorphLang.RU, True)
        t.tag = (t)
        t.addAbridge("ДОП.")
        t.addAbridge("EXT.")
        PhoneItemToken.M_PHONE_TERMINS.add(t)
        t = Termin("ДОБАВОЧНЫЙ", MorphLang.RU, True)
        t.tag = (t)
        t.addAbridge("ДОБ.")
        t.addAbridge("Д.")
        PhoneItemToken.M_PHONE_TERMINS.add(t)
        t = Termin("ВНУТРЕННИЙ", MorphLang.RU, True)
        t.tag = (t)
        t.addAbridge("ВНУТР.")
        t.addAbridge("ВН.")
        t.addAbridge("ВНТ.")
        t.addAbridge("Т.ВН.")
        PhoneItemToken.M_PHONE_TERMINS.add(t)
        t = Termin("TONE MODE", MorphLang.EN, True)
        t.tag = (t)
        PhoneItemToken.M_PHONE_TERMINS.add(t)
        t = Termin("TONE", MorphLang.EN, True)
        t.tag = (t)
        PhoneItemToken.M_PHONE_TERMINS.add(t)
        t = Termin("ADDITIONAL", MorphLang.EN, True)
        t.addAbridge("ADD.")
        t.tag = (t)
        t.addVariant("INTERNAL", True)
        t.addAbridge("INT.")
        PhoneItemToken.M_PHONE_TERMINS.add(t)
    
    M_PHONE_TERMINS = None
    
    @staticmethod
    def _new2478(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'PhoneItemType', _arg4 : str) -> 'PhoneItemToken':
        res = PhoneItemToken(_arg1, _arg2)
        res.item_type = _arg3
        res.value = _arg4
        return res
    
    @staticmethod
    def _new2483(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'PhoneItemType', _arg4 : str, _arg5 : bool) -> 'PhoneItemToken':
        res = PhoneItemToken(_arg1, _arg2)
        res.item_type = _arg3
        res.value = _arg4
        res.is_in_brackets = _arg5
        return res
    
    @staticmethod
    def _new2484(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'PhoneItemType', _arg4 : bool, _arg5 : str) -> 'PhoneItemToken':
        res = PhoneItemToken(_arg1, _arg2)
        res.item_type = _arg3
        res.is_in_brackets = _arg4
        res.value = _arg5
        return res
    
    @staticmethod
    def _new2486(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'PhoneItemType', _arg4 : str, _arg5 : 'PhoneKind') -> 'PhoneItemToken':
        res = PhoneItemToken(_arg1, _arg2)
        res.item_type = _arg3
        res.value = _arg4
        res.kind = _arg5
        return res