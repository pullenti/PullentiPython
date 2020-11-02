# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing
import io
from enum import IntEnum
from pullenti.unisharp.Utils import Utils

from pullenti.ner.Token import Token
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.TextToken import TextToken
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper

class OrgItemEponymToken(MetaToken):
    
    class PersonItemType(IntEnum):
        SURNAME = 0
        NAME = 1
        INITIAL = 2
        AND = 3
        LOCASEWORD = 4
        
        @classmethod
        def has_value(cls, value):
            return any(value == item.value for item in cls)
    
    class PersonItemToken(MetaToken):
        
        def __init__(self, begin : 'Token', end : 'Token') -> None:
            super().__init__(begin, end, None)
            self.typ = OrgItemEponymToken.PersonItemType.SURNAME
            self.value = None;
        
        def __str__(self) -> str:
            return "{0} {1}".format(Utils.enumToString(self.typ), Utils.ifNotNull(self.value, ""))
        
        @staticmethod
        def try_attach(t : 'Token') -> typing.List['PersonItemToken']:
            from pullenti.ner.TextToken import TextToken
            res = list()
            first_pass3805 = True
            while True:
                if first_pass3805: first_pass3805 = False
                else: t = t.next0_
                if (not (t is not None)): break
                if (t.is_newline_before and len(res) > 0): 
                    break
                tt = Utils.asObjectOrNull(t, TextToken)
                if (tt is None): 
                    break
                s = tt.term
                if (not str.isalpha(s[0])): 
                    break
                if (((len(s) == 1 or s == "ДЖ")) and not tt.chars.is_all_lower): 
                    t1 = t
                    if (t1.next0_ is not None and t1.next0_.is_char('.')): 
                        t1 = t1.next0_
                    res.append(OrgItemEponymToken.PersonItemToken._new1797(t, t1, OrgItemEponymToken.PersonItemType.INITIAL, s))
                    t = t1
                    continue
                if (tt.is_and): 
                    res.append(OrgItemEponymToken.PersonItemToken._new1798(t, t, OrgItemEponymToken.PersonItemType.AND))
                    continue
                if (tt.morph.class0_.is_pronoun or tt.morph.class0_.is_personal_pronoun): 
                    break
                if (tt.chars.is_all_lower): 
                    mc = tt.get_morph_class_in_dictionary()
                    if (mc.is_preposition or mc.is_verb or mc.is_adverb): 
                        break
                    t1 = t
                    if (t1.next0_ is not None and not t1.is_whitespace_after and t1.next0_.is_char('.')): 
                        t1 = t1.next0_
                    res.append(OrgItemEponymToken.PersonItemToken._new1797(t, t1, OrgItemEponymToken.PersonItemType.LOCASEWORD, s))
                    t = t1
                    continue
                if (tt.morph.class0_.is_proper_name): 
                    res.append(OrgItemEponymToken.PersonItemToken._new1797(t, t, OrgItemEponymToken.PersonItemType.NAME, s))
                elif ((t.next0_ is not None and t.next0_.is_hiphen and (isinstance(t.next0_.next0_, TextToken))) and not t.next0_.is_whitespace_after): 
                    res.append(OrgItemEponymToken.PersonItemToken._new1797(t, t.next0_.next0_, OrgItemEponymToken.PersonItemType.SURNAME, "{0}-{1}".format(s, t.next0_.next0_.term)))
                    t = t.next0_.next0_
                else: 
                    res.append(OrgItemEponymToken.PersonItemToken._new1797(t, t, OrgItemEponymToken.PersonItemType.SURNAME, s))
            return (res if len(res) > 0 else None)
        
        @staticmethod
        def _new1797(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'PersonItemType', _arg4 : str) -> 'PersonItemToken':
            res = OrgItemEponymToken.PersonItemToken(_arg1, _arg2)
            res.typ = _arg3
            res.value = _arg4
            return res
        
        @staticmethod
        def _new1798(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'PersonItemType') -> 'PersonItemToken':
            res = OrgItemEponymToken.PersonItemToken(_arg1, _arg2)
            res.typ = _arg3
            return res
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.eponyms = list()
    
    def __str__(self) -> str:
        res = io.StringIO()
        print("имени", end="", file=res)
        for e0_ in self.eponyms: 
            print(" {0}".format(e0_), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def try_attach(t : 'Token', must_has_prefix : bool=False) -> 'OrgItemEponymToken':
        from pullenti.ner.org.internal.OrgItemNameToken import OrgItemNameToken
        tt = Utils.asObjectOrNull(t, TextToken)
        if (tt is None): 
            if (t is None): 
                return None
            r1 = t.get_referent()
            if (r1 is not None and r1.type_name == "DATE"): 
                str0_ = str(r1).upper()
                if ((str0_ == "1 МАЯ" or str0_ == "7 ОКТЯБРЯ" or str0_ == "9 МАЯ") or str0_ == "8 МАРТА"): 
                    dt = OrgItemEponymToken._new1793(t, t, list())
                    dt.eponyms.append(str0_)
                    return dt
            age = NumberHelper.try_parse_age(t)
            if ((age is not None and (((isinstance(age.end_token.next0_, TextToken)) or (isinstance(age.end_token.next0_, ReferentToken)))) and (age.whitespaces_after_count < 3)) and not age.end_token.next0_.chars.is_all_lower and age.end_token.next0_.chars.is_cyrillic_letter): 
                dt = OrgItemEponymToken._new1793(t, age.end_token.next0_, list())
                dt.eponyms.append("{0} {1}".format(age.value, dt.end_token.get_source_text().upper()))
                return dt
            return None
        t1 = None
        full = False
        has_name = False
        if (tt.term == "ИМЕНИ" or tt.term == "ІМЕНІ"): 
            t1 = t.next0_
            full = True
            has_name = True
        elif (((tt.term == "ИМ" or tt.term == "ІМ")) and tt.next0_ is not None): 
            if (tt.next0_.is_char('.')): 
                t1 = tt.next0_.next0_
                full = True
            elif ((isinstance(tt.next0_, TextToken)) and tt.chars.is_all_lower and not tt.next0_.chars.is_all_lower): 
                t1 = tt.next0_
            has_name = True
        elif (tt.previous is not None and ((tt.previous.is_value("ФОНД", None) or tt.previous.is_value("ХРАМ", None) or tt.previous.is_value("ЦЕРКОВЬ", "ЦЕРКВА")))): 
            if ((not tt.chars.is_cyrillic_letter or tt.morph.class0_.is_preposition or tt.morph.class0_.is_conjunction) or not tt.chars.is_letter): 
                return None
            if (tt.whitespaces_before_count != 1): 
                return None
            if (tt.chars.is_all_lower): 
                return None
            if (tt.morph.class0_.is_adjective): 
                npt = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.NO, 0, None)
                if (npt is not None and npt.begin_token != npt.end_token): 
                    return None
            na = OrgItemNameToken.try_attach(tt, None, False, True)
            if (na is not None): 
                if (na.is_empty_word or na.is_std_name or na.is_std_tail): 
                    return None
            t1 = (tt)
        if (t1 is None or ((t1.is_newline_before and not full))): 
            return None
        if (tt.previous is not None and tt.previous.morph.class0_.is_preposition): 
            return None
        if (must_has_prefix and not has_name): 
            return None
        r = t1.get_referent()
        if ((r is not None and r.type_name == "DATE" and full) and r.find_slot("DAY", None, True) is not None and r.find_slot("YEAR", None, True) is None): 
            dt = OrgItemEponymToken._new1793(t, t1, list())
            dt.eponyms.append(str(r).upper())
            return dt
        holy = False
        if ((t1.is_value("СВЯТОЙ", None) or t1.is_value("СВЯТИЙ", None) or t1.is_value("СВ", None)) or t1.is_value("СВЯТ", None)): 
            t1 = t1.next0_
            holy = True
            if (t1 is not None and t1.is_char('.')): 
                t1 = t1.next0_
        if (t1 is None): 
            return None
        cl = t1.get_morph_class_in_dictionary()
        if (cl.is_noun or cl.is_adjective): 
            rt = t1.kit.process_referent("PERSON", t1)
            if (rt is not None and rt.referent.type_name == "PERSON" and rt.begin_token != rt.end_token): 
                e0_ = rt.referent.get_string_value("LASTNAME")
                if (e0_ is not None): 
                    if (rt.end_token.is_value(e0_, None)): 
                        re = OrgItemEponymToken(t, rt.end_token)
                        re.eponyms.append(rt.end_token.get_source_text())
                        return re
        nt = NumberHelper.try_parse_anniversary(t1)
        if (nt is not None and nt.typ == NumberSpellingType.AGE): 
            npt = NounPhraseHelper.try_parse(nt.end_token.next0_, NounPhraseParseAttr.NO, 0, None)
            if (npt is not None): 
                s = "{0}-{1} {2}".format(nt.value, ("РОКІВ" if t.kit.base_language.is_ua else "ЛЕТ"), MiscHelper.get_text_value(npt.begin_token, npt.end_token, GetTextAttr.NO))
                res = OrgItemEponymToken(t, npt.end_token)
                res.eponyms.append(s)
                return res
        its = OrgItemEponymToken.PersonItemToken.try_attach(t1)
        if (its is None): 
            if ((isinstance(t1, ReferentToken)) and (isinstance(t1.get_referent(), GeoReferent))): 
                s = MiscHelper.get_text_value(t1, t1, GetTextAttr.NO)
                re = OrgItemEponymToken(t, t1)
                re.eponyms.append(s)
                return re
            return None
        eponims = list()
        i = 0
        if (its[i].typ == OrgItemEponymToken.PersonItemType.LOCASEWORD): 
            i += 1
        if (i >= len(its)): 
            return None
        if (not full): 
            if (its[i].begin_token.morph.class0_.is_adjective and not its[i].begin_token.morph.class0_.is_proper_surname): 
                return None
        if (its[i].typ == OrgItemEponymToken.PersonItemType.INITIAL): 
            i += 1
            while True:
                if ((i < len(its)) and its[i].typ == OrgItemEponymToken.PersonItemType.INITIAL): 
                    i += 1
                if (i >= len(its) or ((its[i].typ != OrgItemEponymToken.PersonItemType.SURNAME and its[i].typ != OrgItemEponymToken.PersonItemType.NAME))): 
                    break
                eponims.append(its[i].value)
                t1 = its[i].end_token
                if ((i + 2) >= len(its) or its[i + 1].typ != OrgItemEponymToken.PersonItemType.AND or its[i + 2].typ != OrgItemEponymToken.PersonItemType.INITIAL): 
                    break
                i += 3
        elif (((i + 1) < len(its)) and its[i].typ == OrgItemEponymToken.PersonItemType.NAME and its[i + 1].typ == OrgItemEponymToken.PersonItemType.SURNAME): 
            eponims.append(its[i + 1].value)
            t1 = its[i + 1].end_token
            i += 2
            if ((((i + 2) < len(its)) and its[i].typ == OrgItemEponymToken.PersonItemType.AND and its[i + 1].typ == OrgItemEponymToken.PersonItemType.NAME) and its[i + 2].typ == OrgItemEponymToken.PersonItemType.SURNAME): 
                eponims.append(its[i + 2].value)
                t1 = its[i + 2].end_token
        elif (its[i].typ == OrgItemEponymToken.PersonItemType.SURNAME): 
            if (len(its) == (i + 2) and its[i].chars == its[i + 1].chars): 
                its[i].value += (" " + its[i + 1].value)
                its[i].end_token = its[i + 1].end_token
                del its[i + 1]
            eponims.append(its[i].value)
            if (((i + 1) < len(its)) and its[i + 1].typ == OrgItemEponymToken.PersonItemType.NAME): 
                if ((i + 2) == len(its)): 
                    i += 1
                elif (its[i + 2].typ != OrgItemEponymToken.PersonItemType.SURNAME): 
                    i += 1
            elif (((i + 1) < len(its)) and its[i + 1].typ == OrgItemEponymToken.PersonItemType.INITIAL): 
                if ((i + 2) == len(its)): 
                    i += 1
                elif (its[i + 2].typ == OrgItemEponymToken.PersonItemType.INITIAL and (i + 3) == len(its)): 
                    i += 2
            elif (((i + 2) < len(its)) and its[i + 1].typ == OrgItemEponymToken.PersonItemType.AND and its[i + 2].typ == OrgItemEponymToken.PersonItemType.SURNAME): 
                ok = True
                npt = NounPhraseHelper.try_parse(its[i + 2].begin_token, NounPhraseParseAttr.NO, 0, None)
                if (npt is not None and not npt.morph.case_.is_genitive and not npt.morph.case_.is_undefined): 
                    ok = False
                if (ok): 
                    eponims.append(its[i + 2].value)
                    i += 2
            t1 = its[i].end_token
        elif (its[i].typ == OrgItemEponymToken.PersonItemType.NAME and holy): 
            t1 = its[i].end_token
            sec = False
            if (((i + 1) < len(its)) and its[i].chars == its[i + 1].chars and its[i + 1].typ != OrgItemEponymToken.PersonItemType.INITIAL): 
                sec = True
                t1 = its[i + 1].end_token
            if (sec): 
                eponims.append("СВЯТ.{0} {1}".format(its[i].value, its[i + 1].value))
            else: 
                eponims.append("СВЯТ.{0}".format(its[i].value))
        elif (full and (i + 1) == len(its) and ((its[i].typ == OrgItemEponymToken.PersonItemType.NAME or its[i].typ == OrgItemEponymToken.PersonItemType.SURNAME))): 
            t1 = its[i].end_token
            eponims.append(its[i].value)
        elif ((its[i].typ == OrgItemEponymToken.PersonItemType.NAME and len(its) == 3 and its[i + 1].typ == OrgItemEponymToken.PersonItemType.NAME) and its[i + 2].typ == OrgItemEponymToken.PersonItemType.SURNAME): 
            t1 = its[i + 2].end_token
            eponims.append("{0} {1} {2}".format(its[i].value, its[i + 1].value, its[i + 2].value))
            i += 2
        if (len(eponims) == 0): 
            return None
        return OrgItemEponymToken._new1793(t, t1, eponims)
    
    @staticmethod
    def _new1793(_arg1 : 'Token', _arg2 : 'Token', _arg3 : typing.List[str]) -> 'OrgItemEponymToken':
        res = OrgItemEponymToken(_arg1, _arg2)
        res.eponyms = _arg3
        return res