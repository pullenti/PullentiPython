# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing
import io
from enum import IntEnum
from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.MetaToken import MetaToken
from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.Termin import Termin
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.measure.internal.NumbersWithUnitToken import NumbersWithUnitToken
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.transport.internal.TransItemToken import TransItemToken
from pullenti.ner.org.OrganizationReferent import OrganizationReferent

class WeaponItemToken(MetaToken):
    
    class Typs(IntEnum):
        NOUN = 0
        BRAND = 1
        MODEL = 2
        NUMBER = 3
        NAME = 4
        CLASS = 5
        DATE = 6
        CALIBER = 7
        DEVELOPER = 8
        
        @classmethod
        def has_value(cls, value):
            return any(value == item.value for item in cls)
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.typ = WeaponItemToken.Typs.NOUN
        self.value = None;
        self.alt_value = None;
        self.is_doubt = False
        self.is_after_conjunction = False
        self.is_internal = False
        self.__inner_tokens = list()
        self.ref = None;
    
    def __str__(self) -> str:
        return "{0}: {1} {2}{3}".format(Utils.enumToString(self.typ), Utils.ifNotNull(self.value, (("" if self.ref is None else str(self.ref)))), Utils.ifNotNull(self.alt_value, ""), ("[int]" if self.is_internal else ""))
    
    @staticmethod
    def try_parse_list(t : 'Token', max_count : int=10) -> typing.List['WeaponItemToken']:
        tr = WeaponItemToken.try_parse(t, None, False, False)
        if (tr is None): 
            return None
        if (tr.typ == WeaponItemToken.Typs.CLASS or tr.typ == WeaponItemToken.Typs.DATE): 
            return None
        tr0 = tr
        res = list()
        if (len(tr.__inner_tokens) > 0): 
            res.extend(tr.__inner_tokens)
            if (res[0].begin_char > tr.begin_char): 
                res[0].begin_token = tr.begin_token
        res.append(tr)
        t = tr.end_token.next0_
        if (tr.typ == WeaponItemToken.Typs.NOUN): 
            while t is not None: 
                if (t.is_char(':') or t.is_hiphen): 
                    pass
                else: 
                    break
                t = t.next0_
        and_conj = False
        first_pass3917 = True
        while True:
            if first_pass3917: first_pass3917 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (max_count > 0 and len(res) >= max_count): 
                break
            if (t.is_char(':')): 
                continue
            if (tr0.typ == WeaponItemToken.Typs.NOUN): 
                if (t.is_hiphen and t.next0_ is not None): 
                    t = t.next0_
            tr = WeaponItemToken.try_parse(t, tr0, False, False)
            if (tr is None): 
                if (BracketHelper.can_be_end_of_sequence(t, True, None, False) and t.next0_ is not None): 
                    if (tr0.typ == WeaponItemToken.Typs.MODEL or tr0.typ == WeaponItemToken.Typs.BRAND): 
                        tt1 = t.next0_
                        if (tt1 is not None and tt1.is_comma): 
                            tt1 = tt1.next0_
                        tr = WeaponItemToken.try_parse(tt1, tr0, False, False)
            if (tr is None and (isinstance(t, ReferentToken))): 
                rt = Utils.asObjectOrNull(t, ReferentToken)
                if (rt.begin_token == rt.end_token and (isinstance(rt.begin_token, TextToken))): 
                    tr = WeaponItemToken.try_parse(rt.begin_token, tr0, False, False)
                    if (tr is not None and tr.begin_token == tr.end_token): 
                        tr.begin_token = tr.end_token = t
            if (tr is None and t.is_char('(')): 
                br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                if (br is not None): 
                    tt = br.end_token.next0_
                    if (tt is not None and tt.is_comma): 
                        tt = tt.next0_
                    tr = WeaponItemToken.try_parse(tt, tr0, False, False)
                    if (tr is not None and tr.typ == WeaponItemToken.Typs.NUMBER): 
                        pass
                    else: 
                        tr = (None)
            if (tr is None and t.is_hiphen): 
                if (tr0.typ == WeaponItemToken.Typs.BRAND or tr0.typ == WeaponItemToken.Typs.MODEL): 
                    tr = WeaponItemToken.try_parse(t.next0_, tr0, False, False)
            if (tr is None and t.is_comma): 
                if ((tr0.typ == WeaponItemToken.Typs.NAME or tr0.typ == WeaponItemToken.Typs.BRAND or tr0.typ == WeaponItemToken.Typs.MODEL) or tr0.typ == WeaponItemToken.Typs.CLASS or tr0.typ == WeaponItemToken.Typs.DATE): 
                    tr = WeaponItemToken.try_parse(t.next0_, tr0, True, False)
                    if (tr is not None): 
                        if (tr.typ == WeaponItemToken.Typs.NUMBER): 
                            pass
                        else: 
                            tr = (None)
            if (tr is None): 
                break
            if (t.is_newline_before): 
                if (tr.typ != WeaponItemToken.Typs.NUMBER): 
                    break
            if (len(tr.__inner_tokens) > 0): 
                res.extend(tr.__inner_tokens)
            res.append(tr)
            tr0 = tr
            t = tr.end_token
            if (and_conj): 
                break
        i = 0
        while i < (len(res) - 1): 
            if (res[i].typ == WeaponItemToken.Typs.MODEL and res[i + 1].typ == WeaponItemToken.Typs.MODEL): 
                res[i].end_token = res[i + 1].end_token
                res[i].value = "{0}{1}{2}".format(res[i].value, ('-' if res[i].end_token.next0_ is not None and res[i].end_token.next0_.is_hiphen else ' '), res[i + 1].value)
                del res[i + 1]
                i -= 1
            i += 1
        return res
    
    @staticmethod
    def try_parse(t : 'Token', prev : 'WeaponItemToken', after_conj : bool, attach_high : bool=False) -> 'WeaponItemToken':
        res = WeaponItemToken.__try_parse(t, prev, after_conj, attach_high)
        if (res is None): 
            npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0, None)
            if (npt is not None and npt.noun.begin_char > npt.begin_char): 
                res = WeaponItemToken.__try_parse(npt.noun.begin_token, prev, after_conj, attach_high)
                if (res is not None): 
                    if (res.typ == WeaponItemToken.Typs.NOUN): 
                        str0_ = npt.get_normal_case_text(None, MorphNumber.SINGULAR, MorphGender.UNDEFINED, False)
                        if (str0_ == "РУЧНОЙ ГРАНАТ"): 
                            str0_ = "РУЧНАЯ ГРАНАТА"
                        if ((Utils.ifNotNull(str0_, "")).endswith(res.value)): 
                            if (res.alt_value is None): 
                                res.alt_value = str0_
                            else: 
                                str0_ = str0_[0:0+len(str0_) - len(res.value)].strip()
                                res.alt_value = "{0} {1}".format(str0_, res.alt_value)
                            res.begin_token = t
                            return res
            return None
        if (res.typ == WeaponItemToken.Typs.NAME): 
            br = BracketHelper.try_parse(res.end_token.next0_, BracketParseAttr.NO, 100)
            if (br is not None and br.is_char('(')): 
                alt = MiscHelper.get_text_value_of_meta_token(br, GetTextAttr.NO)
                if (MiscHelper.can_be_equal_cyr_and_latss(res.value, alt)): 
                    res.alt_value = alt
                    res.end_token = br.end_token
        return res
    
    @staticmethod
    def __try_parse(t : 'Token', prev : 'WeaponItemToken', after_conj : bool, attach_high : bool=False) -> 'WeaponItemToken':
        if (t is None): 
            return None
        if (BracketHelper.is_bracket(t, True)): 
            wit = WeaponItemToken.__try_parse(t.next0_, prev, after_conj, attach_high)
            if (wit is not None): 
                if (wit.end_token.next0_ is None): 
                    wit.begin_token = t
                    return wit
                if (BracketHelper.is_bracket(wit.end_token.next0_, True)): 
                    wit.begin_token = t
                    wit.end_token = wit.end_token.next0_
                    return wit
        tok = WeaponItemToken.M_ONTOLOGY.try_parse(t, TerminParseAttr.NO)
        if (tok is not None): 
            res = WeaponItemToken(t, tok.end_token)
            res.typ = (Utils.valToEnum(tok.termin.tag, WeaponItemToken.Typs))
            if (res.typ == WeaponItemToken.Typs.NOUN): 
                res.value = tok.termin.canonic_text
                if (tok.termin.tag2 is not None): 
                    res.is_doubt = True
                tt = res.end_token.next0_
                first_pass3918 = True
                while True:
                    if first_pass3918: first_pass3918 = False
                    else: tt = tt.next0_
                    if (not (tt is not None)): break
                    if (tt.whitespaces_before_count > 2): 
                        break
                    wit = WeaponItemToken.__try_parse(tt, None, False, False)
                    if (wit is not None): 
                        if (wit.typ == WeaponItemToken.Typs.BRAND): 
                            res.__inner_tokens.append(wit)
                            tt = wit.end_token
                            res.end_token = tt
                            continue
                        break
                    if (not (isinstance(tt, TextToken))): 
                        break
                    mc = tt.get_morph_class_in_dictionary()
                    if (mc == MorphClass.ADJECTIVE): 
                        if (res.alt_value is None): 
                            res.alt_value = res.value
                        if (res.alt_value.endswith(res.value)): 
                            res.alt_value = res.alt_value[0:0+len(res.alt_value) - len(res.value)]
                        res.alt_value = "{0}{1} {2}".format(res.alt_value, tt.term, res.value)
                        res.end_token = tt
                        continue
                    break
                return res
            if (res.typ == WeaponItemToken.Typs.BRAND or res.typ == WeaponItemToken.Typs.NAME): 
                res.value = tok.termin.canonic_text
                return res
            if (res.typ == WeaponItemToken.Typs.MODEL): 
                res.value = tok.termin.canonic_text
                if (isinstance(tok.termin.tag2, list)): 
                    li = Utils.asObjectOrNull(tok.termin.tag2, list)
                    for to in li: 
                        wit = WeaponItemToken._new2754(t, tok.end_token, Utils.valToEnum(to.tag, WeaponItemToken.Typs), to.canonic_text, tok.begin_token == tok.end_token)
                        res.__inner_tokens.append(wit)
                        if (to.additional_vars is not None and len(to.additional_vars) > 0): 
                            wit.alt_value = to.additional_vars[0].canonic_text
                res.__correct_model()
                return res
        nnn = MiscHelper.check_number_prefix(t)
        if (nnn is not None): 
            tit = TransItemToken._attach_number(nnn, True)
            if (tit is not None): 
                res = WeaponItemToken._new2755(t, tit.end_token, WeaponItemToken.Typs.NUMBER)
                res.value = tit.value
                res.alt_value = tit.alt_value
                return res
        if (((isinstance(t, TextToken)) and t.chars.is_letter and t.chars.is_all_upper) and (t.length_char < 4)): 
            if ((t.next0_ is not None and ((t.next0_.is_hiphen or t.next0_.is_char('.'))) and (t.next0_.whitespaces_after_count < 2)) and (isinstance(t.next0_.next0_, NumberToken))): 
                res = WeaponItemToken._new2756(t, t.next0_, WeaponItemToken.Typs.MODEL, True)
                res.value = t.term
                res.__correct_model()
                return res
            if ((isinstance(t.next0_, NumberToken)) and not t.is_whitespace_after): 
                res = WeaponItemToken._new2756(t, t, WeaponItemToken.Typs.MODEL, True)
                res.value = t.term
                res.__correct_model()
                return res
            if (t.term == "СП" and (t.whitespaces_after_count < 3) and (isinstance(t.next0_, TextToken))): 
                pp = WeaponItemToken.__try_parse(t.next0_, None, False, False)
                if (pp is not None and ((pp.typ == WeaponItemToken.Typs.MODEL or pp.typ == WeaponItemToken.Typs.BRAND))): 
                    res = WeaponItemToken._new2755(t, t, WeaponItemToken.Typs.NOUN)
                    res.value = "ПИСТОЛЕТ"
                    res.alt_value = "СЛУЖЕБНЫЙ ПИСТОЛЕТ"
                    return res
        if (((isinstance(t, TextToken)) and t.chars.is_letter and not t.chars.is_all_lower) and t.length_char > 2): 
            ok = False
            if (prev is not None and ((prev.typ == WeaponItemToken.Typs.NOUN or prev.typ == WeaponItemToken.Typs.MODEL or prev.typ == WeaponItemToken.Typs.BRAND))): 
                ok = True
            elif (prev is None and t.previous is not None and t.previous.is_comma_and): 
                ok = True
            if (ok): 
                res = WeaponItemToken._new2756(t, t, WeaponItemToken.Typs.NAME, True)
                res.value = t.term
                if ((t.next0_ is not None and t.next0_.is_hiphen and (isinstance(t.next0_.next0_, TextToken))) and t.next0_.next0_.chars == t.chars): 
                    res.value = "{0}-{1}".format(res.value, t.next0_.next0_.term)
                    res.end_token = t.next0_.next0_
                if (prev is not None and prev.typ == WeaponItemToken.Typs.NOUN): 
                    res.typ = WeaponItemToken.Typs.BRAND
                if (res.end_token.next0_ is not None and res.end_token.next0_.is_hiphen and (isinstance(res.end_token.next0_.next0_, NumberToken))): 
                    res.typ = WeaponItemToken.Typs.MODEL
                    res.__correct_model()
                elif (not res.end_token.is_whitespace_after and (isinstance(res.end_token.next0_, NumberToken))): 
                    res.typ = WeaponItemToken.Typs.MODEL
                    res.__correct_model()
                return res
        if (t.is_value("МАРКА", None)): 
            res = WeaponItemToken.__try_parse(t.next0_, prev, after_conj, False)
            if (res is not None and res.typ == WeaponItemToken.Typs.BRAND): 
                res.begin_token = t
                return res
            if (BracketHelper.can_be_start_of_sequence(t.next0_, True, False)): 
                br = BracketHelper.try_parse(t.next0_, BracketParseAttr.NO, 100)
                if (br is not None): 
                    return WeaponItemToken._new2760(t, br.end_token, WeaponItemToken.Typs.BRAND, MiscHelper.get_text_value(br.begin_token, br.end_token, GetTextAttr.NO))
            if (((isinstance(t, TextToken)) and (isinstance(t.next0_, TextToken)) and t.next0_.length_char > 1) and not t.next0_.chars.is_all_lower): 
                return WeaponItemToken._new2760(t, t.next0_, WeaponItemToken.Typs.BRAND, t.term)
        if (t.is_value("КАЛИБР", "КАЛІБР")): 
            tt1 = t.next0_
            if (tt1 is not None and ((tt1.is_hiphen or tt1.is_char(':')))): 
                tt1 = tt1.next0_
            num = NumbersWithUnitToken.try_parse(tt1, None, False, False, False, False)
            if (num is not None and num.single_val is not None): 
                return WeaponItemToken._new2760(t, num.end_token, WeaponItemToken.Typs.CALIBER, NumberHelper.double_to_string(num.single_val))
        if (isinstance(t, NumberToken)): 
            num = NumbersWithUnitToken.try_parse(t, None, False, False, False, False)
            if (num is not None and num.single_val is not None): 
                if (len(num.units) == 1 and num.units[0].unit is not None and num.units[0].unit.name_cyr == "мм"): 
                    return WeaponItemToken._new2760(t, num.end_token, WeaponItemToken.Typs.CALIBER, NumberHelper.double_to_string(num.single_val))
                if (num.end_token.next0_ is not None and num.end_token.next0_.is_value("КАЛИБР", "КАЛІБР")): 
                    return WeaponItemToken._new2760(t, num.end_token.next0_, WeaponItemToken.Typs.CALIBER, NumberHelper.double_to_string(num.single_val))
        if (t.is_value("ПРОИЗВОДСТВО", "ВИРОБНИЦТВО")): 
            tt1 = t.next0_
            if (tt1 is not None and ((tt1.is_hiphen or tt1.is_char(':')))): 
                tt1 = tt1.next0_
            if (isinstance(tt1, ReferentToken)): 
                if ((isinstance(tt1.get_referent(), OrganizationReferent)) or (isinstance(tt1.get_referent(), GeoReferent))): 
                    return WeaponItemToken._new2765(t, tt1, WeaponItemToken.Typs.DEVELOPER, tt1.get_referent())
        return None
    
    def __correct_model(self) -> None:
        tt = self.end_token.next0_
        if (tt is None or tt.whitespaces_before_count > 2): 
            return
        if (tt.is_value(":\\/.", None) or tt.is_hiphen): 
            tt = tt.next0_
        if (isinstance(tt, NumberToken)): 
            tmp = io.StringIO()
            print(tt.value, end="", file=tmp)
            is_lat = LanguageHelper.is_latin_char(self.value[0])
            self.end_token = tt
            tt = tt.next0_
            first_pass3919 = True
            while True:
                if first_pass3919: first_pass3919 = False
                else: tt = tt.next0_
                if (not (tt is not None)): break
                if ((isinstance(tt, TextToken)) and tt.length_char == 1 and tt.chars.is_letter): 
                    if (not tt.is_whitespace_before or ((tt.previous is not None and tt.previous.is_hiphen))): 
                        ch = tt.term[0]
                        self.end_token = tt
                        ch2 = chr(0)
                        if (LanguageHelper.is_latin_char(ch) and not is_lat): 
                            ch2 = LanguageHelper.get_cyr_for_lat(ch)
                            if (ch2 != (chr(0))): 
                                ch = ch2
                        elif (LanguageHelper.is_cyrillic_char(ch) and is_lat): 
                            ch2 = LanguageHelper.get_lat_for_cyr(ch)
                            if (ch2 != (chr(0))): 
                                ch = ch2
                        print(ch, end="", file=tmp)
                        continue
                break
            self.value = "{0}-{1}".format(self.value, Utils.toStringStringIO(tmp))
            self.alt_value = MiscHelper.create_cyr_lat_alternative(self.value)
        if (not self.end_token.is_whitespace_after and self.end_token.next0_ is not None and ((self.end_token.next0_.is_hiphen or self.end_token.next0_.is_char_of("\\/")))): 
            if (not self.end_token.next0_.is_whitespace_after and (isinstance(self.end_token.next0_.next0_, NumberToken))): 
                self.end_token = self.end_token.next0_.next0_
                self.value = "{0}-{1}".format(self.value, self.end_token.value)
                if (self.alt_value is not None): 
                    self.alt_value = "{0}-{1}".format(self.alt_value, self.end_token.value)
    
    M_ONTOLOGY = None
    
    @staticmethod
    def initialize() -> None:
        if (WeaponItemToken.M_ONTOLOGY is not None): 
            return
        WeaponItemToken.M_ONTOLOGY = TerminCollection()
        li = [ ]
        t = Termin._new100("ПИСТОЛЕТ", WeaponItemToken.Typs.NOUN)
        WeaponItemToken.M_ONTOLOGY.add(t)
        t = Termin._new100("РЕВОЛЬВЕР", WeaponItemToken.Typs.NOUN)
        WeaponItemToken.M_ONTOLOGY.add(t)
        t = Termin._new100("ВИНТОВКА", WeaponItemToken.Typs.NOUN)
        WeaponItemToken.M_ONTOLOGY.add(t)
        t = Termin._new100("РУЖЬЕ", WeaponItemToken.Typs.NOUN)
        WeaponItemToken.M_ONTOLOGY.add(t)
        t = Termin._new102("АВТОМАТ", WeaponItemToken.Typs.NOUN, 1)
        WeaponItemToken.M_ONTOLOGY.add(t)
        t = Termin._new102("КАРАБИН", WeaponItemToken.Typs.NOUN, 1)
        WeaponItemToken.M_ONTOLOGY.add(t)
        t = Termin._new124("ПИСТОЛЕТ-ПУЛЕМЕТ", "ПИСТОЛЕТ-ПУЛЕМЕТ", WeaponItemToken.Typs.NOUN)
        WeaponItemToken.M_ONTOLOGY.add(t)
        t = Termin._new100("ПУЛЕМЕТ", WeaponItemToken.Typs.NOUN)
        WeaponItemToken.M_ONTOLOGY.add(t)
        t = Termin._new100("ГРАНАТОМЕТ", WeaponItemToken.Typs.NOUN)
        t.add_variant("СТРЕЛКОВО ГРАНАТОМЕТНЫЙ КОМПЛЕКС", False)
        WeaponItemToken.M_ONTOLOGY.add(t)
        t = Termin._new100("ОГНЕМЕТ", WeaponItemToken.Typs.NOUN)
        WeaponItemToken.M_ONTOLOGY.add(t)
        t = Termin._new100("МИНОМЕТ", WeaponItemToken.Typs.NOUN)
        WeaponItemToken.M_ONTOLOGY.add(t)
        t = Termin._new2777("ПЕРЕНОСНОЙ ЗЕНИТНО РАКЕТНЫЙ КОМПЛЕКС", "ПЗРК", WeaponItemToken.Typs.NOUN)
        WeaponItemToken.M_ONTOLOGY.add(t)
        t = Termin._new2777("ПРОТИВОТАНКОВЫЙ РАКЕТНЫЙ КОМПЛЕКС", "ПТРК", WeaponItemToken.Typs.NOUN)
        t.add_variant("ПЕРЕНОСНОЙ ПРОТИВОТАНКОВЫЙ РАКЕТНЫЙ КОМПЛЕКС", False)
        WeaponItemToken.M_ONTOLOGY.add(t)
        t = Termin._new100("АВИАЦИОННАЯ ПУШКА", WeaponItemToken.Typs.NOUN)
        t.add_variant("АВИАПУШКА", False)
        WeaponItemToken.M_ONTOLOGY.add(t)
        t = Termin._new100("НАРУЧНИКИ", WeaponItemToken.Typs.NOUN)
        WeaponItemToken.M_ONTOLOGY.add(t)
        t = Termin._new100("БРОНЕЖИЛЕТ", WeaponItemToken.Typs.NOUN)
        WeaponItemToken.M_ONTOLOGY.add(t)
        t = Termin._new100("ГРАНАТА", WeaponItemToken.Typs.NOUN)
        WeaponItemToken.M_ONTOLOGY.add(t)
        t = Termin._new100("ЛИМОНКА", WeaponItemToken.Typs.NOUN)
        WeaponItemToken.M_ONTOLOGY.add(t)
        t = Termin._new100("НОЖ", WeaponItemToken.Typs.NOUN)
        WeaponItemToken.M_ONTOLOGY.add(t)
        t = Termin._new100("ВЗРЫВАТЕЛЬ", WeaponItemToken.Typs.NOUN)
        WeaponItemToken.M_ONTOLOGY.add(t)
        for s in ["МАКАРОВ", "КАЛАШНИКОВ", "СИМОНОВ", "СТЕЧКИН", "ШМАЙСЕР", "МОСИН", "СЛОСТИН", "НАГАН", "МАКСИМ", "ДРАГУНОВ", "СЕРДЮКОВ", "ЯРЫГИН", "НИКОНОВ", "МАУЗЕР", "БРАУНИНГ", "КОЛЬТ", "ВИНЧЕСТЕР"]: 
            WeaponItemToken.M_ONTOLOGY.add(Termin._new100(s, WeaponItemToken.Typs.BRAND))
        for s in ["УЗИ"]: 
            WeaponItemToken.M_ONTOLOGY.add(Termin._new100(s, WeaponItemToken.Typs.NAME))
        t = Termin._new2788("ТУЛЬСКИЙ ТОКАРЕВА", "ТТ", "ТТ", WeaponItemToken.Typs.MODEL)
        li = list()
        li.append(Termin._new100("ПИСТОЛЕТ", WeaponItemToken.Typs.NOUN))
        li.append(Termin._new100("ТОКАРЕВ", WeaponItemToken.Typs.BRAND))
        t.tag2 = (li)
        WeaponItemToken.M_ONTOLOGY.add(t)
        t = Termin._new2788("ПИСТОЛЕТ МАКАРОВА", "ПМ", "ПМ", WeaponItemToken.Typs.MODEL)
        li = list()
        li.append(Termin._new100("ПИСТОЛЕТ", WeaponItemToken.Typs.NOUN))
        li.append(Termin._new100("МАКАРОВ", WeaponItemToken.Typs.BRAND))
        t.tag2 = (li)
        WeaponItemToken.M_ONTOLOGY.add(t)
        t = Termin._new2788("ПИСТОЛЕТ МАКАРОВА МОДЕРНИЗИРОВАННЫЙ", "ПММ", "ПММ", WeaponItemToken.Typs.MODEL)
        li = list()
        tt = Termin._new100("ПИСТОЛЕТ", WeaponItemToken.Typs.NOUN)
        li.append(tt)
        tt.add_variant("МОДЕРНИЗИРОВАННЫЙ ПИСТОЛЕТ", False)
        li.append(Termin._new100("МАКАРОВ", WeaponItemToken.Typs.BRAND))
        t.tag2 = (li)
        WeaponItemToken.M_ONTOLOGY.add(t)
        t = Termin._new2788("АВТОМАТ КАЛАШНИКОВА", "АК", "АК", WeaponItemToken.Typs.MODEL)
        li = list()
        li.append(Termin._new100("АВТОМАТ", WeaponItemToken.Typs.NOUN))
        li.append(Termin._new100("КАЛАШНИКОВ", WeaponItemToken.Typs.BRAND))
        t.tag2 = (li)
        WeaponItemToken.M_ONTOLOGY.add(t)
    
    @staticmethod
    def _new2754(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Typs', _arg4 : str, _arg5 : bool) -> 'WeaponItemToken':
        res = WeaponItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        res.is_internal = _arg5
        return res
    
    @staticmethod
    def _new2755(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Typs') -> 'WeaponItemToken':
        res = WeaponItemToken(_arg1, _arg2)
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new2756(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Typs', _arg4 : bool) -> 'WeaponItemToken':
        res = WeaponItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.is_doubt = _arg4
        return res
    
    @staticmethod
    def _new2760(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Typs', _arg4 : str) -> 'WeaponItemToken':
        res = WeaponItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        return res
    
    @staticmethod
    def _new2765(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Typs', _arg4 : 'Referent') -> 'WeaponItemToken':
        res = WeaponItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.ref = _arg4
        return res