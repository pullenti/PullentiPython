# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
import typing
import xml.etree
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.Token import Token
from pullenti.ner.core.IntOntologyItem import IntOntologyItem
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.MetaToken import MetaToken
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.Referent import Referent
from pullenti.morph.MorphWordForm import MorphWordForm
from pullenti.ner.address.internal.EpNerAddressInternalResourceHelper import EpNerAddressInternalResourceHelper
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.morph.MorphClass import MorphClass
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.Termin import Termin
from pullenti.ner.geo.internal.TerrTermin import TerrTermin
from pullenti.ner.core.IntOntologyCollection import IntOntologyCollection
from pullenti.ner.geo.GeoReferent import GeoReferent

class TerrItemToken(MetaToken):
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.onto_item = None;
        self.onto_item2 = None;
        self.termin_item = None;
        self.is_adjective = False
        self.is_district_name = False
        self.adjective_ref = None;
        self.rzd = None;
        self.rzd_dir = None;
        self.can_be_city = False
        self.can_be_surname = False
        self.is_adj_in_dictionary = False
        self.is_geo_in_dictionary = False
        self.is_doubt = False
    
    @property
    def is_city_region(self) -> bool:
        if (self.termin_item is None): 
            return False
        return ("ГОРОДС" in self.termin_item.canonic_text or "МІСЬК" in self.termin_item.canonic_text or "МУНИЦИПАЛ" in self.termin_item.canonic_text) or "МУНІЦИПАЛ" in self.termin_item.canonic_text
    
    def __str__(self) -> str:
        res = io.StringIO()
        if (self.onto_item is not None): 
            print("{0} ".format(self.onto_item.canonic_text), end="", file=res, flush=True)
        elif (self.termin_item is not None): 
            print("{0} ".format(self.termin_item.canonic_text), end="", file=res, flush=True)
        else: 
            print("{0} ".format(super().__str__()), end="", file=res, flush=True)
        if (self.adjective_ref is not None): 
            print(" (Adj: {0})".format(str(self.adjective_ref.referent)), end="", file=res, flush=True)
        return Utils.toStringStringIO(res).strip()
    
    @staticmethod
    def tryParseList(t : 'Token', int_ont : 'IntOntologyCollection', max_count : int) -> typing.List['TerrItemToken']:
        from pullenti.ner.geo.internal.CityItemToken import CityItemToken
        ci = TerrItemToken.tryParse(t, int_ont, False, False)
        if (ci is None): 
            return None
        li = list()
        li.append(ci)
        t = ci.end_token.next0_
        if (t is None): 
            return li
        if (ci.termin_item is not None and ci.termin_item.canonic_text == "АВТОНОМИЯ"): 
            if (t.morph.case_.is_genitive): 
                return None
        t = ci.end_token.next0_
        while t is not None: 
            ci = TerrItemToken.tryParse(t, int_ont, False, False)
            if (ci is None): 
                if (t.chars.is_capital_upper and len(li) == 1 and ((li[0].is_city_region or ((li[0].termin_item is not None and li[0].termin_item.is_specific_prefix))))): 
                    cit = CityItemToken.tryParse(t, int_ont, False, None)
                    if (cit is not None and cit.typ == CityItemToken.ItemType.PROPERNAME): 
                        ci = TerrItemToken(cit.begin_token, cit.end_token)
                if (t.isChar('(')): 
                    ci = TerrItemToken.tryParse(t.next0_, int_ont, False, False)
                    if (ci is not None and ci.end_token.next0_ is not None and ci.end_token.next0_.isChar(')')): 
                        ci0 = li[len(li) - 1]
                        if (ci0.onto_item is not None and ci.onto_item == ci0.onto_item): 
                            ci0.end_token = ci.end_token.next0_
                            t = ci0.end_token.next0_
                        else: 
                            li.append(ci)
                            ci.end_token = ci.end_token.next0_
                            t = ci.end_token.next0_
                        continue
                if (BracketHelper.canBeStartOfSequence(t, False, False)): 
                    lii = TerrItemToken.tryParseList(t.next0_, int_ont, max_count)
                    if (lii is not None and BracketHelper.canBeEndOfSequence(lii[len(lii) - 1].end_token.next0_, False, None, False)): 
                        li.extend(lii)
                        return li
                if (li[len(li) - 1].rzd is not None): 
                    ci = TerrItemToken.__tryParseRzdDir(t)
                if (ci is None): 
                    break
            if (ci.is_adjective and li[len(li) - 1].rzd is not None): 
                cii = TerrItemToken.__tryParseRzdDir(t)
                if (cii is not None): 
                    ci = cii
            if (t.is_table_control_char): 
                break
            if (t.is_newline_before): 
                if (len(li) > 0 and li[len(li) - 1].is_adjective and ci.termin_item is not None): 
                    pass
                elif (len(li) == 1 and li[0].termin_item is not None and ci.termin_item is None): 
                    pass
                else: 
                    break
            li.append(ci)
            t = ci.end_token.next0_
            if (max_count > 0 and len(li) >= max_count): 
                break
        for cc in li: 
            if (cc.onto_item is not None and not cc.is_adjective): 
                if (not cc.begin_token.chars.is_cyrillic_letter): 
                    continue
                alpha2 = None
                if (isinstance(cc.onto_item.referent, GeoReferent)): 
                    alpha2 = (cc.onto_item.referent).alpha2
                if (alpha2 == "TG"): 
                    if (isinstance(cc.begin_token, TextToken)): 
                        if (cc.begin_token.getSourceText() != "Того"): 
                            return None
                        if (len(li) == 1 and cc.begin_token.previous is not None and cc.begin_token.previous.isChar('.')): 
                            return None
                        npt = NounPhraseHelper.tryParse(cc.begin_token, NounPhraseParseAttr.PARSEPRONOUNS, 0)
                        if (npt is not None and npt.end_token != cc.begin_token): 
                            return None
                        if (cc.begin_token.next0_ is not None): 
                            if (cc.begin_token.next0_.morph.class0_.is_personal_pronoun or cc.begin_token.next0_.morph.class0_.is_pronoun): 
                                return None
                    if (len(li) < 2): 
                        return None
                if (alpha2 == "PE"): 
                    if (isinstance(cc.begin_token, TextToken)): 
                        if ((cc.begin_token).getSourceText() != "Перу"): 
                            return None
                        if (len(li) == 1 and cc.begin_token.previous is not None and cc.begin_token.previous.isChar('.')): 
                            return None
                    if (len(li) < 2): 
                        return None
                if (alpha2 == "DM"): 
                    if (cc.end_token.next0_ is not None): 
                        if (cc.end_token.next0_.chars.is_capital_upper or cc.end_token.next0_.chars.is_all_upper): 
                            return None
                    return None
                if (alpha2 == "JE"): 
                    if (cc.begin_token.previous is not None and cc.begin_token.previous.is_hiphen): 
                        return None
                return li
            elif (cc.onto_item is not None and cc.is_adjective): 
                alpha2 = None
                if (isinstance(cc.onto_item.referent, GeoReferent)): 
                    alpha2 = (cc.onto_item.referent).alpha2
                if (alpha2 == "SU"): 
                    if (cc.end_token.next0_ is None or not cc.end_token.next0_.isValue("СОЮЗ", None)): 
                        cc.onto_item = (None)
        i = 0
        first_pass2913 = True
        while True:
            if first_pass2913: first_pass2913 = False
            else: i += 1
            if (not (i < len(li))): break
            if (li[i].onto_item is not None and li[i].onto_item2 is not None): 
                nou = None
                if (i > 0 and li[i - 1].termin_item is not None): 
                    nou = (li[i - 1].termin_item)
                elif (((i + 1) < len(li)) and li[i + 1].termin_item is not None): 
                    nou = (li[i + 1].termin_item)
                if (nou is None or li[i].onto_item.referent is None or li[i].onto_item2.referent is None): 
                    continue
                if (li[i].onto_item.referent.findSlot(GeoReferent.ATTR_TYPE, nou.canonic_text.lower(), True) is None and li[i].onto_item2.referent.findSlot(GeoReferent.ATTR_TYPE, nou.canonic_text.lower(), True) is not None): 
                    li[i].onto_item = li[i].onto_item2
                    li[i].onto_item2 = (None)
                elif (li[i].onto_item.referent.findSlot(GeoReferent.ATTR_TYPE, "республика", True) is not None and nou.canonic_text != "РЕСПУБЛИКА"): 
                    li[i].onto_item = li[i].onto_item2
                    li[i].onto_item2 = (None)
        for cc in li: 
            if (cc.onto_item is not None or ((cc.termin_item is not None and not cc.is_adjective)) or cc.rzd is not None): 
                return li
        return None
    
    @staticmethod
    def __tryParseRzdDir(t : 'Token') -> 'TerrItemToken':
        napr = None
        tt0 = None
        tt1 = None
        val = None
        tt = t
        first_pass2914 = True
        while True:
            if first_pass2914: first_pass2914 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if (tt.isCharOf(",.")): 
                continue
            if (tt.is_newline_before): 
                break
            if (tt.isValue("НАПРАВЛЕНИЕ", None)): 
                napr = tt
                continue
            if (tt.isValue("НАПР", None)): 
                if (tt.next0_ is not None and tt.next0_.isChar('.')): 
                    tt = tt.next0_
                napr = tt
                continue
            npt = NounPhraseHelper.tryParse(tt, NounPhraseParseAttr.NO, 0)
            if (npt is not None and len(npt.adjectives) > 0 and npt.noun.isValue("КОЛЬЦО", None)): 
                tt0 = tt
                tt1 = npt.end_token
                val = npt.getNormalCaseText(None, True, MorphGender.UNDEFINED, False)
                break
            if ((isinstance(tt, TextToken)) and ((not tt.chars.is_all_lower or napr is not None)) and (((tt.morph.gender) & (MorphGender.NEUTER))) != (MorphGender.UNDEFINED)): 
                tt1 = tt
                tt0 = tt1
                continue
            if ((((isinstance(tt, TextToken)) and ((not tt.chars.is_all_lower or napr is not None)) and tt.next0_ is not None) and tt.next0_.is_hiphen and (isinstance(tt.next0_.next0_, TextToken))) and (((tt.next0_.next0_.morph.gender) & (MorphGender.NEUTER))) != (MorphGender.UNDEFINED)): 
                tt0 = tt
                tt = tt.next0_.next0_
                tt1 = tt
                continue
            break
        if (tt0 is not None): 
            ci = TerrItemToken._new1161(tt0, tt1, True)
            if (val is not None): 
                ci.rzd_dir = val
            else: 
                ci.rzd_dir = tt1.getNormalCaseText(MorphClass.ADJECTIVE, True, MorphGender.NEUTER, False)
                if (tt0 != tt1): 
                    ci.rzd_dir = "{0} {1}".format((tt0).term, ci.rzd_dir)
                ci.rzd_dir += " НАПРАВЛЕНИЕ"
            if (napr is not None and napr.end_char > ci.end_char): 
                ci.end_token = napr
            return ci
        return None
    
    @staticmethod
    def tryParse(t : 'Token', int_ont : 'IntOntologyCollection', can_be_low_capital : bool=False, noun_can_be_adjective : bool=False) -> 'TerrItemToken':
        from pullenti.ner.geo.internal.CityItemToken import CityItemToken
        if (t is None): 
            return None
        if (t.kit.is_recurce_overflow): 
            return None
        t.kit.recurse_level += 1
        res = TerrItemToken.__TryParse(t, int_ont, can_be_low_capital)
        t.kit.recurse_level -= 1
        if (res is None): 
            if (noun_can_be_adjective and t.morph.class0_.is_adjective): 
                tok = TerrItemToken._m_terr_noun_adjectives.tryParse(t, TerminParseAttr.NO)
                if (tok is not None): 
                    return TerrItemToken._new1162(tok.begin_token, tok.end_token, Utils.asObjectOrNull(tok.termin.tag, TerrTermin), False)
            if ((t.chars.is_all_upper and t.length_char == 2 and (isinstance(t, TextToken))) and int_ont is not None): 
                term = (t).term
                if (((term == "РБ" or term == "РК" or term == "TC") or term == "ТС" or term == "РТ") or term == "УР" or term == "РД"): 
                    for it in int_ont.items: 
                        if (isinstance(it.referent, GeoReferent)): 
                            alph2 = (it.referent).alpha2
                            if (((alph2 == "BY" and term == "РБ")) or ((alph2 == "KZ" and term == "РК"))): 
                                return TerrItemToken._new1163(t, t, it)
                            if (term == "РТ"): 
                                if (it.referent.findSlot(None, "ТАТАРСТАН", True) is not None): 
                                    return TerrItemToken._new1163(t, t, it)
                            if (term == "РД"): 
                                if (it.referent.findSlot(None, "ДАГЕСТАН", True) is not None): 
                                    return TerrItemToken._new1163(t, t, it)
                    ok = False
                    if ((t.whitespaces_before_count < 2) and (isinstance(t.previous, TextToken))): 
                        term2 = (t.previous).term
                        if ((t.previous.isValue("КОДЕКС", None) or t.previous.isValue("ЗАКОН", None) or term2 == "КОАП") or term2 == "ПДД" or term2 == "МЮ"): 
                            ok = True
                        elif ((t.previous.chars.is_all_upper and t.previous.length_char > 1 and (t.previous.length_char < 4)) and term2.endswith("К")): 
                            ok = True
                        elif (term == "РТ" or term == "УР" or term == "РД"): 
                            tt = t.previous
                            if (tt is not None and tt.is_comma): 
                                tt = tt.previous
                            if (tt is not None): 
                                if ((isinstance(tt.getReferent(), GeoReferent)) and (tt.getReferent()).alpha2 == "RU"): 
                                    ok = True
                                elif ((isinstance(tt, NumberToken)) and tt.length_char == 6 and (tt).typ == NumberSpellingType.DIGIT): 
                                    ok = True
                    elif (((t.whitespaces_before_count < 2) and (isinstance(t.previous, NumberToken)) and t.previous.length_char == 6) and (t.previous).typ == NumberSpellingType.DIGIT): 
                        ok = True
                    if (ok): 
                        if (term == "РК" and TerrItemToken.__m_kazahstan is not None): 
                            return TerrItemToken._new1163(t, t, TerrItemToken.__m_kazahstan)
                        if (term == "РТ" and TerrItemToken.__m_tatarstan is not None): 
                            return TerrItemToken._new1163(t, t, TerrItemToken.__m_tatarstan)
                        if (term == "РД" and TerrItemToken.__m_dagestan is not None): 
                            return TerrItemToken._new1163(t, t, TerrItemToken.__m_dagestan)
                        if (term == "УР" and TerrItemToken.__m_udmurtia is not None): 
                            return TerrItemToken._new1163(t, t, TerrItemToken.__m_udmurtia)
                        if (term == "РБ" and TerrItemToken.__m_belorussia is not None): 
                            return TerrItemToken._new1163(t, t, TerrItemToken.__m_belorussia)
                        if (((term == "ТС" or term == "TC")) and TerrItemToken.__m_tamog_sous is not None): 
                            return TerrItemToken._new1163(t, t, TerrItemToken.__m_tamog_sous)
            if (((isinstance(t, TextToken)) and ((t.isValue("Р", None) or t.isValue("P", None))) and t.next0_ is not None) and t.next0_.isChar('.') and not t.next0_.is_newline_after): 
                res = TerrItemToken.tryParse(t.next0_.next0_, int_ont, False, False)
                if (res is not None and res.onto_item is not None): 
                    str0_ = str(res.onto_item).upper()
                    if ("РЕСПУБЛИКА" in str0_): 
                        res.begin_token = t
                        res.is_doubt = False
                        return res
            if ((isinstance(t, TextToken)) and t.length_char > 2 and not t.chars.is_all_lower): 
                if (((t.morph.class0_.is_adjective or t.chars.is_all_upper or (t).term.endswith("ЖД"))) or ((t.next0_ is not None and t.next0_.is_hiphen))): 
                    rt0 = t.kit.processReferent("ORGANIZATION", t)
                    if (rt0 is not None): 
                        if ((Utils.ifNotNull(rt0.referent.getStringValue("TYPE"), "")).endswith("дорога")): 
                            return TerrItemToken._new1172(t, rt0.end_token, rt0, rt0.morph)
                rzd_dir_ = TerrItemToken.__tryParseRzdDir(t)
                if (rzd_dir_ is not None): 
                    tt = rzd_dir_.end_token.next0_
                    while tt is not None:
                        if (tt.isCharOf(",.")): 
                            tt = tt.next0_
                        else: 
                            break
                    chhh = TerrItemToken.tryParse(tt, int_ont, False, False)
                    if (chhh is not None and chhh.rzd is not None): 
                        return rzd_dir_
            return TerrItemToken.tryParseDistrictName(t, int_ont)
        if (res.is_adjective): 
            rt0 = t.kit.processReferent("ORGANIZATION", t)
            if (rt0 is not None): 
                if ((Utils.ifNotNull(rt0.referent.getStringValue("TYPE"), "")).endswith("дорога")): 
                    return TerrItemToken._new1172(t, rt0.end_token, rt0, rt0.morph)
            rzd_dir_ = TerrItemToken.__tryParseRzdDir(t)
            if (rzd_dir_ is not None): 
                tt = rzd_dir_.end_token.next0_
                while tt is not None:
                    if (tt.isCharOf(",.")): 
                        tt = tt.next0_
                    else: 
                        break
                rt0 = t.kit.processReferent("ORGANIZATION", tt)
                if (rt0 is not None): 
                    if ((Utils.ifNotNull(rt0.referent.getStringValue("TYPE"), "")).endswith("дорога")): 
                        return rzd_dir_
        if ((res.begin_token.length_char == 1 and res.begin_token.chars.is_all_upper and res.begin_token.next0_ is not None) and res.begin_token.next0_.isChar('.')): 
            return None
        if (res.termin_item is not None and res.termin_item.canonic_text == "ОКРУГ"): 
            if (t.previous is not None and ((t.previous.isValue("ГОРОДСКОЙ", None) or t.previous.isValue("МІСЬКИЙ", None)))): 
                return None
        if (res.onto_item is not None): 
            cit = CityItemToken.tryParse(res.begin_token, None, can_be_low_capital, None)
            if (cit is not None): 
                if (cit.typ == CityItemToken.ItemType.CITY and cit.onto_item is not None and cit.onto_item.misc_attr is not None): 
                    if (cit.end_token.isValue("CITY", None)): 
                        return None
                    if (cit.end_token == res.end_token): 
                        res.can_be_city = True
                        if (cit.end_token.next0_ is not None and cit.end_token.next0_.isValue("CITY", None)): 
                            return None
            cit = CityItemToken.tryParseBack(res.begin_token.previous)
            if (cit is not None and cit.typ == CityItemToken.ItemType.NOUN and ((res.is_adjective or (cit.whitespaces_after_count < 1)))): 
                res.can_be_city = True
        if (res.termin_item is not None): 
            res.is_doubt = res.termin_item.is_doubt
            if (not res.termin_item.is_region): 
                if (res.termin_item.is_moscow_region and res.begin_token == res.end_token): 
                    res.is_doubt = True
                elif (res.termin_item.acronym == "МО" and res.begin_token == res.end_token and res.length_char == 2): 
                    if (res.begin_token.previous is not None and res.begin_token.previous.isValue("ВЕТЕРАН", None)): 
                        return None
                    res.is_doubt = True
                    if (res.begin_token == res.end_token and res.length_char == 2): 
                        if (res.begin_token.previous is None or res.begin_token.previous.isCharOf(",") or res.begin_token.is_newline_before): 
                            if (res.end_token.next0_ is None or res.end_token.next0_.isCharOf(",") or res.is_newline_after): 
                                res.termin_item = (None)
                                res.onto_item = TerrItemToken.__m_mos_regru
                elif (res.termin_item.acronym == "ЛО" and res.begin_token == res.end_token and res.length_char == 2): 
                    res.is_doubt = True
                    if (res.begin_token.previous is None or res.begin_token.previous.is_comma_and or res.begin_token.is_newline_before): 
                        res.termin_item = (None)
                        res.onto_item = TerrItemToken.__m_len_regru
                elif (not res.morph.case_.is_nominative and not res.morph.case_.is_accusative): 
                    res.is_doubt = True
                elif (res.morph.number != MorphNumber.SINGULAR): 
                    if (res.termin_item.is_moscow_region and res.morph.number != MorphNumber.PLURAL): 
                        pass
                    else: 
                        res.is_doubt = True
            if (((res.termin_item is not None and res.termin_item.canonic_text == "АО")) or ((res.onto_item == TerrItemToken.__m_mos_regru and res.length_char == 2))): 
                tt = res.end_token.next0_
                rt = res.kit.processReferent("ORGANIZATION", res.begin_token)
                if (rt is None): 
                    rt = res.kit.processReferent("ORGANIZATION", res.begin_token.next0_)
                if (rt is not None): 
                    for s in rt.referent.slots: 
                        if (s.type_name == "TYPE"): 
                            ty = s.value
                            if (res.termin_item is not None and ty != res.termin_item.canonic_text): 
                                return None
        if (res is not None and res.begin_token == res.end_token and res.termin_item is None): 
            if (isinstance(t, TextToken)): 
                str0_ = (t).term
                if (str0_ == "ЧАДОВ" or str0_ == "ТОГОВ"): 
                    return None
            if ((((isinstance(t.next0_, TextToken)) and (t.whitespaces_after_count < 2) and not t.next0_.chars.is_all_lower) and t.chars == t.next0_.chars and not t.chars.is_latin_letter) and ((not t.morph.case_.is_genitive and not t.morph.case_.is_accusative))): 
                mc = t.next0_.getMorphClassInDictionary()
                if (mc.is_proper_surname or mc.is_proper_secname): 
                    res.is_doubt = True
            if ((isinstance(t.previous, TextToken)) and (t.whitespaces_before_count < 2) and not t.previous.chars.is_all_lower): 
                mc = t.previous.getMorphClassInDictionary()
                if (mc.is_proper_surname): 
                    res.is_doubt = True
            if (t.length_char <= 2 and res.onto_item is not None and not t.isValue("РФ", None)): 
                res.is_doubt = True
                tt = t.next0_
                if (tt is not None and ((tt.isCharOf(":") or tt.is_hiphen))): 
                    tt = tt.next0_
                if (tt is not None and tt.getReferent() is not None and tt.getReferent().type_name == "PHONE"): 
                    res.is_doubt = False
                elif (t.length_char == 2 and t.chars.is_all_upper and t.chars.is_latin_letter): 
                    res.is_doubt = False
        return res
    
    @staticmethod
    def __TryParse(t : 'Token', int_ont : 'IntOntologyCollection', can_be_low_capital : bool) -> 'TerrItemToken':
        from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
        from pullenti.ner.geo.internal.CityItemToken import CityItemToken
        if (not ((isinstance(t, TextToken)))): 
            return None
        li = None
        if (int_ont is not None): 
            li = int_ont.tryAttach(t, None, False)
        if (li is None and t.kit.ontology is not None): 
            li = t.kit.ontology.attachToken(GeoReferent.OBJ_TYPENAME, t)
        if (li is None or len(li) == 0): 
            li = TerrItemToken._m_terr_ontology.tryAttach(t, None, False)
        else: 
            li1 = TerrItemToken._m_terr_ontology.tryAttach(t, None, False)
            if (li1 is not None and len(li1) > 0): 
                if (li1[0].length_char > li[0].length_char): 
                    li = li1
        tt = Utils.asObjectOrNull(t, TextToken)
        if (li is not None): 
            for i in range(len(li) - 1, -1, -1):
                if (li[i].item is not None): 
                    g = Utils.asObjectOrNull(li[i].item.referent, GeoReferent)
                    if (g is None): 
                        continue
                    if (g.is_city and not g.is_region and not g.is_state): 
                        del li[i]
                    elif (g.is_state and t.length_char == 2 and li[i].length_char == 2): 
                        if (not t.is_whitespace_before and t.previous is not None and t.previous.isChar('.')): 
                            del li[i]
                        elif (t.previous is not None and t.previous.isValue("ДОМЕН", None)): 
                            del li[i]
            for nt in li: 
                if (nt.item is not None and not ((isinstance(nt.termin.tag, IntOntologyItem)))): 
                    if (can_be_low_capital or not MiscHelper.isAllCharactersLower(nt.begin_token, nt.end_token, False) or nt.begin_token != nt.end_token): 
                        res0 = TerrItemToken._new1174(nt.begin_token, nt.end_token, nt.item, nt.morph)
                        if (nt.end_token.morph.class0_.is_adjective and nt.begin_token == nt.end_token): 
                            if (nt.begin_token.getMorphClassInDictionary().is_proper_geo): 
                                pass
                            else: 
                                res0.is_adjective = True
                        if (nt.begin_token == nt.end_token and nt.chars.is_latin_letter): 
                            if ((nt.item.referent).is_state): 
                                pass
                            elif (nt.item.referent.findSlot(GeoReferent.ATTR_TYPE, "state", True) is not None): 
                                pass
                            else: 
                                res0.is_doubt = True
                        if ((len(li) == 2 and nt == li[0] and li[1].item is not None) and not ((isinstance(li[1].termin.tag, IntOntologyItem)))): 
                            res0.onto_item2 = li[1].item
                        return res0
            for nt in li: 
                if (nt.item is not None and (isinstance(nt.termin.tag, IntOntologyItem))): 
                    if (nt.end_token.next0_ is None or not nt.end_token.next0_.is_hiphen): 
                        res1 = TerrItemToken._new1175(nt.begin_token, nt.end_token, nt.item, True, nt.morph)
                        if ((len(li) == 2 and nt == li[0] and li[1].item is not None) and (isinstance(li[1].termin.tag, IntOntologyItem))): 
                            res1.onto_item2 = li[1].item
                        return res1
            for nt in li: 
                if (nt.termin is not None and nt.item is None): 
                    if (nt.end_token.next0_ is None or not nt.end_token.next0_.is_hiphen or not (nt.termin).is_adjective): 
                        res1 = TerrItemToken._new1176(nt.begin_token, nt.end_token, Utils.asObjectOrNull(nt.termin, TerrTermin), (nt.termin).is_adjective, nt.morph)
                        if (not res1.is_adjective): 
                            if (res1.termin_item.canonic_text == "РЕСПУБЛИКА" or res1.termin_item.canonic_text == "ШТАТ"): 
                                npt1 = NounPhraseHelper.tryParse(res1.begin_token.previous, NounPhraseParseAttr.NO, 0)
                                if (npt1 is not None and npt1.morph.number == MorphNumber.PLURAL): 
                                    res2 = TerrItemToken.tryParse(res1.end_token.next0_, int_ont, False, False)
                                    if ((res2 is not None and res2.onto_item is not None and res2.onto_item.referent is not None) and res2.onto_item.referent.findSlot(GeoReferent.ATTR_TYPE, "республика", True) is not None): 
                                        pass
                                    else: 
                                        return None
                            if (res1.termin_item.canonic_text == "ГОСУДАРСТВО"): 
                                if (t.previous is not None and t.previous.isValue("СОЮЗНЫЙ", None)): 
                                    return None
                        return res1
        if (tt is None): 
            return None
        if (not tt.chars.is_capital_upper and not tt.chars.is_all_upper): 
            return None
        if (((tt.length_char == 2 or tt.length_char == 3)) and tt.chars.is_all_upper): 
            if (tt.term in TerrItemToken._m_alpha2state): 
                ok = False
                tt2 = tt.next0_
                if (tt2 is not None and tt2.isChar(':')): 
                    tt2 = tt2.next0_
                if (isinstance(tt2, ReferentToken)): 
                    r = tt2.getReferent()
                    if (r is not None and r.type_name == "PHONE"): 
                        ok = True
                if (ok): 
                    return TerrItemToken._new1163(tt, tt, TerrItemToken._m_alpha2state[tt.term])
        if (tt.length_char < 3): 
            return None
        if (MiscHelper.isEngArticle(tt)): 
            return None
        if (tt.length_char < 5): 
            if (tt.next0_ is None or not tt.next0_.is_hiphen): 
                return None
        t0 = tt
        prefix = None
        if (t0.next0_ is not None and t0.next0_.is_hiphen and (isinstance(t0.next0_.next0_, TextToken))): 
            tt = (Utils.asObjectOrNull(t0.next0_.next0_, TextToken))
            if (not tt.chars.is_all_lower and ((t0.is_whitespace_after or t0.next0_.is_whitespace_after))): 
                tit = TerrItemToken.__TryParse(tt, int_ont, False)
                if (tit is not None): 
                    if (tit.onto_item is not None): 
                        return None
            if (tt.length_char > 1): 
                if (tt.chars.is_capital_upper): 
                    prefix = t0.term
                elif (not tt.is_whitespace_before and not t0.is_whitespace_after): 
                    prefix = t0.term
                if (((not tt.is_whitespace_after and tt.next0_ is not None and tt.next0_.is_hiphen) and not tt.next0_.is_whitespace_after and (isinstance(tt.next0_.next0_, TextToken))) and tt.next0_.next0_.chars == t0.chars): 
                    prefix = "{0}-{1}".format(prefix, tt.term)
                    tt = (Utils.asObjectOrNull(tt.next0_.next0_, TextToken))
            if (prefix is None): 
                tt = t0
        if (tt.morph.class0_.is_adverb): 
            return None
        cit = CityItemToken.tryParse(t0, None, False, None)
        if (cit is not None): 
            if (cit.onto_item is not None or cit.typ == CityItemToken.ItemType.NOUN or cit.typ == CityItemToken.ItemType.CITY): 
                if (not cit.doubtful and not tt.morph.class0_.is_adjective): 
                    return None
        npt = NounPhraseHelper.tryParse(t0, NounPhraseParseAttr.NO, 0)
        if (npt is not None): 
            if (((npt.noun.isValue("ФЕДЕРАЦИЯ", None) or npt.noun.isValue("ФЕДЕРАЦІЯ", None))) and len(npt.adjectives) == 1): 
                if (MiscHelper.isNotMoreThanOneError("РОССИЙСКАЯ", npt.adjectives[0]) or MiscHelper.isNotMoreThanOneError("РОСІЙСЬКА", npt.adjectives[0])): 
                    return TerrItemToken._new1174(npt.begin_token, npt.end_token, (TerrItemToken.__m_russiaua if t0.kit.base_language.is_ua else TerrItemToken.__m_russiaru), npt.morph)
        if (t0.morph.class0_.is_proper_name): 
            if (t0.is_whitespace_after or t0.next0_.is_whitespace_after): 
                return None
        if (npt is not None and npt.end_token == tt.next0_): 
            adj = False
            reg_after = False
            if (len(npt.adjectives) == 1 and not t0.chars.is_all_lower): 
                if (((((tt.next0_.isValue("РАЙОН", None) or tt.next0_.isValue("ОБЛАСТЬ", None) or tt.next0_.isValue("КРАЙ", None)) or tt.next0_.isValue("ВОЛОСТЬ", None) or tt.next0_.isValue("УЛУС", None)) or tt.next0_.isValue("ОКРУГ", None) or tt.next0_.isValue("АВТОНОМИЯ", "АВТОНОМІЯ")) or tt.next0_.isValue("РЕСПУБЛИКА", "РЕСПУБЛІКА") or tt.next0_.isValue("COUNTY", None)) or tt.next0_.isValue("STATE", None) or tt.next0_.isValue("REGION", None)): 
                    reg_after = True
                else: 
                    tok = TerrItemToken._m_terr_ontology.tryAttach(tt.next0_, None, False)
                    if (tok is not None): 
                        if ((((tok[0].termin.canonic_text == "РАЙОН" or tok[0].termin.canonic_text == "ОБЛАСТЬ" or tok[0].termin.canonic_text == "УЛУС") or tok[0].termin.canonic_text == "КРАЙ" or tok[0].termin.canonic_text == "ВОЛОСТЬ") or tok[0].termin.canonic_text == "ОКРУГ" or tok[0].termin.canonic_text == "АВТОНОМИЯ") or tok[0].termin.canonic_text == "АВТОНОМІЯ" or ((tok[0].chars.is_latin_letter and (isinstance(tok[0].termin, TerrTermin)) and (tok[0].termin).is_region))): 
                            reg_after = True
            if (reg_after): 
                adj = True
                for wff in tt.morph.items: 
                    wf = Utils.asObjectOrNull(wff, MorphWordForm)
                    if (wf is None): 
                        continue
                    if (wf.class0_.is_verb and wf.is_in_dictionary): 
                        adj = False
                        break
                    elif (wf.is_in_dictionary and not wf.class0_.is_adjective): 
                        pass
                if (not adj and prefix is not None): 
                    adj = True
                if (not adj): 
                    cit1 = CityItemToken.tryParse(tt.next0_.next0_, None, False, None)
                    if (cit1 is not None and cit1.typ != CityItemToken.ItemType.PROPERNAME): 
                        adj = True
                if (not adj): 
                    if (MiscLocationHelper.checkGeoObjectBefore(npt.begin_token)): 
                        adj = True
                te = tt.next0_.next0_
                if (te is not None and te.isCharOf(",")): 
                    te = te.next0_
                if (not adj and (isinstance(te, ReferentToken))): 
                    if (isinstance(te.getReferent(), GeoReferent)): 
                        adj = True
                if (not adj): 
                    te = t0.previous
                    if (te is not None and te.isCharOf(",")): 
                        te = te.previous
                    if (isinstance(te, ReferentToken)): 
                        if (isinstance(te.getReferent(), GeoReferent)): 
                            adj = True
                if (adj and npt.adjectives[0].begin_token != npt.adjectives[0].end_token): 
                    if (npt.adjectives[0].begin_token.chars != npt.adjectives[0].end_token.chars): 
                        return None
            if (not adj and not t0.chars.is_latin_letter): 
                return None
        res = TerrItemToken(t0, tt)
        res.is_adjective = tt.morph.class0_.is_adjective
        res.morph = tt.morph
        if (isinstance(t0, TextToken)): 
            for wf in t0.morph.items: 
                f = Utils.asObjectOrNull(wf, MorphWordForm)
                if (not f.is_in_dictionary): 
                    continue
                if (wf.class0_.is_proper_surname and f.is_in_dictionary): 
                    res.can_be_surname = True
                elif (wf.class0_.is_adjective and f.is_in_dictionary): 
                    res.is_adj_in_dictionary = True
                elif (wf.class0_.is_proper_geo): 
                    if (not t0.chars.is_all_lower): 
                        res.is_geo_in_dictionary = True
        if ((tt.whitespaces_after_count < 2) and (isinstance(tt.next0_, TextToken)) and tt.next0_.chars.is_capital_upper): 
            dir0_ = MiscLocationHelper.tryAttachNordWest(tt.next0_)
            if (dir0_ is not None): 
                res.end_token = dir0_.end_token
        return res
    
    @staticmethod
    def tryParseDistrictName(t : 'Token', int_ont : 'IntOntologyCollection') -> 'TerrItemToken':
        """ Это пыделение возможного имени для городского района типа Владыкино, Тёплый Стан)
        
        Args:
            t(Token): 
            int_ont(IntOntologyCollection): 
            proc: 
        
        """
        from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
        if (not ((isinstance(t, TextToken))) or not t.chars.is_capital_upper or not t.chars.is_cyrillic_letter): 
            return None
        if ((t.next0_ is not None and t.next0_.is_hiphen and (isinstance(t.next0_.next0_, TextToken))) and t.next0_.next0_.chars == t.chars): 
            tok = TerrItemToken._m_terr_ontology.tryAttach(t, None, False)
            if ((tok is not None and tok[0].item is not None and (isinstance(tok[0].item.referent, GeoReferent))) and (tok[0].item.referent).is_state): 
                return None
            tok = TerrItemToken._m_terr_ontology.tryAttach(t.next0_.next0_, None, False)
            if ((tok is not None and tok[0].item is not None and (isinstance(tok[0].item.referent, GeoReferent))) and (tok[0].item.referent).is_state): 
                return None
            return TerrItemToken(t, t.next0_.next0_)
        if ((isinstance(t.next0_, TextToken)) and t.next0_.chars == t.chars): 
            npt = NounPhraseHelper.tryParse(t, NounPhraseParseAttr.NO, 0)
            if (npt is not None and npt.end_token == t.next0_ and len(npt.adjectives) == 1): 
                if (not npt.end_token.morph.class0_.is_adjective or ((npt.end_token.morph.case_.is_nominative and (isinstance(npt.end_token, TextToken)) and LanguageHelper.endsWith((npt.end_token).term, "О")))): 
                    ty = TerrItemToken.__TryParse(t.next0_, int_ont, False)
                    if (ty is not None and ty.termin_item is not None): 
                        return None
                    return TerrItemToken(t, t.next0_)
        str0_ = (t).term
        res = TerrItemToken._new1179(t, t, True)
        if (not LanguageHelper.endsWith(str0_, "О")): 
            res.is_doubt = True
        dir0_ = MiscLocationHelper.tryAttachNordWest(t)
        if (dir0_ is not None): 
            res.end_token = dir0_.end_token
            res.is_doubt = False
            if (res.end_token.whitespaces_after_count < 2): 
                res2 = TerrItemToken.tryParseDistrictName(res.end_token.next0_, int_ont)
                if (res2 is not None and res2.termin_item is None): 
                    res.end_token = res2.end_token
        return res
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
        if (TerrItemToken._m_terr_ontology is not None): 
            return
        TerrItemToken._m_terr_ontology = IntOntologyCollection()
        TerrItemToken._m_terr_adjs = TerminCollection()
        TerrItemToken._m_mans_by_state = TerminCollection()
        TerrItemToken._m_unknown_regions = TerminCollection()
        TerrItemToken._m_terr_noun_adjectives = TerminCollection()
        TerrItemToken._m_capitals_by_state = TerminCollection()
        TerrItemToken._m_geo_abbrs = TerminCollection()
        t = TerrTermin("РЕСПУБЛИКА")
        t.addAbridge("РЕСП.")
        t.addAbridge("РЕСП-КА")
        t.addAbridge("РЕСПУБ.")
        t.addAbridge("РЕСПУБЛ.")
        t.addAbridge("Р-КА")
        t.addAbridge("РЕСП-КА")
        TerrItemToken._m_terr_ontology.add(t)
        TerrItemToken._m_terr_ontology.add(TerrTermin("РЕСПУБЛІКА", MorphLang.UA))
        t = TerrTermin._new1180("ГОСУДАРСТВО", True)
        t.addAbridge("ГОС-ВО")
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1181("ДЕРЖАВА", MorphLang.UA, True)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin("АВТОНОМНАЯ СОВЕТСКАЯ СОЦИАЛИСТИЧЕСКАЯ РЕСПУБЛИКА")
        t.acronym = "АССР"
        TerrItemToken._m_terr_ontology.add(t)
        for s in ["СОЮЗ", "СОДРУЖЕСТВО", "ФЕДЕРАЦИЯ", "КОНФЕДЕРАЦИЯ"]: 
            TerrItemToken._m_terr_ontology.add(TerrTermin._new1182(s, True, True))
        for s in ["СОЮЗ", "СПІВДРУЖНІСТЬ", "ФЕДЕРАЦІЯ", "КОНФЕДЕРАЦІЯ"]: 
            TerrItemToken._m_terr_ontology.add(TerrTermin._new1183(s, MorphLang.UA, True, True))
        for s in ["КОРОЛЕВСТВО", "КНЯЖЕСТВО", "ГЕРЦОГСТВО", "ИМПЕРИЯ", "ЦАРСТВО", "KINGDOM", "DUCHY", "EMPIRE"]: 
            TerrItemToken._m_terr_ontology.add(TerrTermin._new1180(s, True))
        for s in ["КОРОЛІВСТВО", "КНЯЗІВСТВО", "ГЕРЦОГСТВО", "ІМПЕРІЯ"]: 
            TerrItemToken._m_terr_ontology.add(TerrTermin._new1181(s, MorphLang.UA, True))
        for s in ["НЕЗАВИСИМЫЙ", "ОБЪЕДИНЕННЫЙ", "СОЕДИНЕННЫЙ", "НАРОДНЫЙ", "НАРОДНО", "ФЕДЕРАТИВНЫЙ", "ДЕМОКРАТИЧЕСКИЙ", "СОВЕТСКИЙ", "СОЦИАЛИСТИЧЕСКИЙ", "КООПЕРАТИВНЫЙ", "ИСЛАМСКИЙ", "АРАБСКИЙ", "МНОГОНАЦИОНАЛЬНЫЙ", "СУВЕРЕННЫЙ", "САМОПРОВОЗГЛАШЕННЫЙ", "НЕПРИЗНАННЫЙ"]: 
            TerrItemToken._m_terr_ontology.add(TerrTermin._new1186(s, True, True))
        for s in ["НЕЗАЛЕЖНИЙ", "ОБЄДНАНИЙ", "СПОЛУЧЕНИЙ", "НАРОДНИЙ", "ФЕДЕРАЛЬНИЙ", "ДЕМОКРАТИЧНИЙ", "РАДЯНСЬКИЙ", "СОЦІАЛІСТИЧНИЙ", "КООПЕРАТИВНИЙ", "ІСЛАМСЬКИЙ", "АРАБСЬКИЙ", "БАГАТОНАЦІОНАЛЬНИЙ", "СУВЕРЕННИЙ"]: 
            TerrItemToken._m_terr_ontology.add(TerrTermin._new1187(s, MorphLang.UA, True, True))
        t = TerrTermin._new1188("ОБЛАСТЬ", True)
        t.addAbridge("ОБЛ.")
        TerrItemToken._m_terr_noun_adjectives.add(Termin._new118("ОБЛАСТНОЙ", t))
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1188("REGION", True)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1191("ОБЛАСТЬ", MorphLang.UA, True)
        t.addAbridge("ОБЛ.")
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1192(None, True, "АО")
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1193(None, MorphLang.UA, True, "АО")
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1188("РАЙОН", True)
        t.addAbridge("Р-Н")
        t.addAbridge("Р-ОН")
        TerrItemToken._m_terr_noun_adjectives.add(Termin._new118("РАЙОННЫЙ", t))
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1191("РАЙОН", MorphLang.UA, True)
        t.addAbridge("Р-Н")
        t.addAbridge("Р-ОН")
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1188("УЛУС", True)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1198("ШТАТ", True, True)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1188("STATE", True)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1200("ШТАТ", MorphLang.UA, True, True)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1198("ПРОВИНЦИЯ", True, True)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1200("ПРОВІНЦІЯ", MorphLang.UA, True, True)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1188("PROVINCE", True)
        t.addVariant("PROVINCIAL", False)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1188("ПРЕФЕКТУРА", True)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1188("PREFECTURE", True)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1188("АВТОНОМИЯ", True)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1188("AUTONOMY", True)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1191("АВТОНОМІЯ", MorphLang.UA, True)
        TerrItemToken._m_terr_ontology.add(t)
        for s in ["РЕСПУБЛИКА", "КРАЙ", "ОКРУГ", "ФЕДЕРАЛЬНЫЙ ОКРУГ", "АВТОНОМНЫЙ ОКРУГ", "НАЦИОНАЛЬНЫЙ ОКРУГ", "ВОЛОСТЬ", "ФЕДЕРАЛЬНАЯ ЗЕМЛЯ", "МУНИЦИПАЛЬНЫЙ РАЙОН", "МУНИЦИПАЛЬНЫЙ ОКРУГ", "АДМИНИСТРАТИВНЫЙ ОКРУГ", "ГОРОДСКОЙ РАЙОН", "ВНУТРИГОРОДСКОЙ РАЙОН", "ВНУТРИГОРОДСКОЕ МУНИЦИПАЛЬНОЕ ОБРАЗОВАНИЕ", "REPUBLIC", "COUNTY", "BOROUGH", "PARISH", "MUNICIPALITY", "CENSUS AREA", "AUTONOMOUS REGION", "ADMINISTRATIVE REGION", "SPECIAL ADMINISTRATIVE REGION"]: 
            t = TerrTermin._new1209(s, True, " " in s)
            if (s == "КРАЙ"): 
                TerrItemToken._m_terr_noun_adjectives.add(Termin._new118("КРАЕВОЙ", t))
            elif (s == "ОКРУГ"): 
                TerrItemToken._m_terr_noun_adjectives.add(Termin._new118("ОКРУЖНОЙ", t))
            elif (s == "ФЕДЕРАЛЬНЫЙ ОКРУГ"): 
                t.acronym = "ФО"
                t.acronym_can_be_lower = False
            if (LanguageHelper.endsWith(s, "РАЙОН")): 
                t.addAbridge(s.replace("РАЙОН", "Р-Н"))
            TerrItemToken._m_terr_ontology.add(t)
        for s in ["РЕСПУБЛІКА", "КРАЙ", "ОКРУГ", "ФЕДЕРАЛЬНИЙ ОКРУГ", "АВТОНОМНЫЙ ОКРУГ", "НАЦІОНАЛЬНИЙ ОКРУГ", "ВОЛОСТЬ", "ФЕДЕРАЛЬНА ЗЕМЛЯ", "МУНІЦИПАЛЬНИЙ РАЙОН", "МУНІЦИПАЛЬНИЙ ОКРУГ", "АДМІНІСТРАТИВНИЙ ОКРУГ", "МІСЬКИЙ РАЙОН", "ВНУТРИГОРОДСКОЕ МУНІЦИПАЛЬНЕ УТВОРЕННЯ"]: 
            t = TerrTermin._new1212(s, MorphLang.UA, True, " " in s)
            if (LanguageHelper.endsWith(s, "РАЙОН")): 
                t.addAbridge(s.replace("РАЙОН", "Р-Н"))
            TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1188("СЕЛЬСКИЙ ОКРУГ", True)
        t.addAbridge("С.О.")
        t.addAbridge("C.O.")
        t.addAbridge("ПС С.О.")
        t.addAbridge("С/ОКРУГ")
        t.addAbridge("С/О")
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1191("СІЛЬСЬКИЙ ОКРУГ", MorphLang.UA, True)
        t.addAbridge("С.О.")
        t.addAbridge("C.O.")
        t.addAbridge("С/ОКРУГ")
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1215("СЕЛЬСКИЙ СОВЕТ", "СЕЛЬСКИЙ ОКРУГ", True)
        t.addVariant("СЕЛЬСОВЕТ", False)
        t.addAbridge("С.С.")
        t.addAbridge("С/С")
        t.addVariant("СЕЛЬСКАЯ АДМИНИСТРАЦИЯ", False)
        t.addAbridge("С.А.")
        t.addAbridge("С.АДМ.")
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1188("ПОСЕЛКОВЫЙ ОКРУГ", True)
        t.addAbridge("П.О.")
        t.addAbridge("П/О")
        t.addVariant("ПОСЕЛКОВАЯ АДМИНИСТРАЦИЯ", False)
        t.addAbridge("П.А.")
        t.addAbridge("П.АДМ.")
        t.addAbridge("П/А")
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1215("ПОСЕЛКОВЫЙ СОВЕТ", "ПОСЕЛКОВЫЙ ОКРУГ", True)
        t.addAbridge("П.С.")
        TerrItemToken._m_terr_ontology.add(t)
        TerrItemToken._m_terr_ontology.add(TerrTermin._new1218("АВТОНОМНЫЙ", True, True))
        TerrItemToken._m_terr_ontology.add(TerrTermin._new1219("АВТОНОМНИЙ", MorphLang.UA, True, True))
        TerrItemToken._m_terr_ontology.add(TerrTermin._new1220("МУНИЦИПАЛЬНОЕ СОБРАНИЕ", True, True, True))
        TerrItemToken._m_terr_ontology.add(TerrTermin._new1221("МУНІЦИПАЛЬНЕ ЗБОРИ", MorphLang.UA, True, True, True))
        t = TerrTermin._new1222("МУНИЦИПАЛЬНОЕ ОБРАЗОВАНИЕ", "МО")
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin("ТЕРРИТОРИЯ")
        t.addAbridge("ТЕР.")
        t.addAbridge("ТЕРРИТОР.")
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1223("ЦЕНТРАЛЬНЫЙ АДМИНИСТРАТИВНЫЙ ОКРУГ", True)
        t.addAbridge("ЦАО")
        t.addVariant("ЦЕНТРАЛЬНЫЙ АО", False)
        t.addVariant("ЦЕНТРАЛЬНЫЙ ОКРУГ", False)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1223("СЕВЕРНЫЙ АДМИНИСТРАТИВНЫЙ ОКРУГ", True)
        t.addAbridge("САО")
        t.addVariant("СЕВЕРНЫЙ АО", False)
        t.addVariant("СЕВЕРНЫЙ ОКРУГ", False)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1223("СЕВЕРО-ВОСТОЧНЫЙ АДМИНИСТРАТИВНЫЙ ОКРУГ", True)
        t.addAbridge("СВАО")
        t.addVariant("СЕВЕРО-ВОСТОЧНЫЙ АО", False)
        t.addVariant("СЕВЕРО-ВОСТОЧНЫЙ ОКРУГ", False)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1223("ВОСТОЧНЫЙ АДМИНИСТРАТИВНЫЙ ОКРУГ", True)
        t.addAbridge("ВАО")
        t.addVariant("ВОСТОЧНЫЙ АО", False)
        t.addVariant("ВОСТОЧНЫЙ ОКРУГ", False)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1223("ЮГО-ВОСТОЧНЫЙ АДМИНИСТРАТИВНЫЙ ОКРУГ", True)
        t.addAbridge("ЮВАО")
        t.addVariant("ЮГО-ВОСТОЧНЫЙ АО", False)
        t.addVariant("ЮГО-ВОСТОЧНЫЙ ОКРУГ", False)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1223("ЮЖНЫЙ АДМИНИСТРАТИВНЫЙ ОКРУГ", True)
        t.addAbridge("ЮАО")
        t.addVariant("ЮЖНЫЙ АО", False)
        t.addVariant("ЮЖНЫЙ ОКРУГ", False)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1223("ЗАПАДНЫЙ АДМИНИСТРАТИВНЫЙ ОКРУГ", True)
        t.addAbridge("ЗАО")
        t.addVariant("ЗАПАДНЫЙ АО", False)
        t.addVariant("ЗАПАДНЫЙ ОКРУГ", False)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1223("СЕВЕРО-ЗАПАДНЫЙ АДМИНИСТРАТИВНЫЙ ОКРУГ", True)
        t.addAbridge("СЗАО")
        t.addVariant("СЕВЕРО-ЗАПАДНЫЙ АО", False)
        t.addVariant("СЕВЕРО-ЗАПАДНЫЙ ОКРУГ", False)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1223("ЗЕЛЕНОГРАДСКИЙ АДМИНИСТРАТИВНЫЙ ОКРУГ", True)
        t.addAbridge("ЗЕЛАО")
        t.addVariant("ЗЕЛЕНОГРАДСКИЙ АО", False)
        t.addVariant("ЗЕЛЕНОГРАДСКИЙ ОКРУГ", False)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1223("ТРОИЦКИЙ АДМИНИСТРАТИВНЫЙ ОКРУГ", True)
        t.addAbridge("ТАО")
        t.addVariant("ТРОИЦКИЙ АО", False)
        t.addVariant("ТРОИЦКИЙ ОКРУГ", False)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1223("НОВОМОСКОВСКИЙ АДМИНИСТРАТИВНЫЙ ОКРУГ", True)
        t.addAbridge("НАО")
        t.addVariant("НОВОМОСКОВСКИЙ АО", False)
        t.addVariant("НОВОМОСКОВСКИЙ ОКРУГ", False)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1223("ТРОИЦКИЙ И НОВОМОСКОВСКИЙ АДМИНИСТРАТИВНЫЙ ОКРУГ", True)
        t.addAbridge("ТИНАО")
        t.addAbridge("НИТАО")
        t.addVariant("ТРОИЦКИЙ И НОВОМОСКОВСКИЙ АО", False)
        t.addVariant("ТРОИЦКИЙ И НОВОМОСКОВСКИЙ ОКРУГ", False)
        TerrItemToken._m_terr_ontology.add(t)
        TerrItemToken._m_alpha2state = dict()
        dat = EpNerAddressInternalResourceHelper.getBytes("t.dat")
        if (dat is None): 
            raise Utils.newException("Not found resource file t.dat in Analyzer.Location", None)
        dat = MiscLocationHelper._deflate(dat)
        with io.BytesIO(dat) as tmp: 
            tmp.seek(0, io.SEEK_SET)
            xml0_ = None # new XmlDocument
            xml0_ = xml.etree.ElementTree.parse(tmp)
            for x in xml0_.getroot(): 
                lang = MorphLang.RU
                a = Utils.getXmlAttrByName(x.attrib, "l")
                if (a is not None): 
                    if (a[1] == "en"): 
                        lang = MorphLang.EN
                    elif (a[1] == "ua"): 
                        lang = MorphLang.UA
                if (x.tag == "state"): 
                    TerrItemToken.__loadState(x, lang)
                elif (x.tag == "reg"): 
                    TerrItemToken.__loadRegion(x, lang)
                elif (x.tag == "unknown"): 
                    a = Utils.getXmlAttrByName(x.attrib, "name")
                    if (a is not None and a[1] is not None): 
                        TerrItemToken._m_unknown_regions.add(Termin._new898(a[1], lang))
    
    _m_terr_ontology = None
    
    _m_geo_abbrs = None
    
    __m_russiaru = None
    
    __m_russiaua = None
    
    __m_mos_regru = None
    
    __m_len_regru = None
    
    __m_belorussia = None
    
    __m_kazahstan = None
    
    __m_tamog_sous = None
    
    __m_tatarstan = None
    
    __m_udmurtia = None
    
    __m_dagestan = None
    
    _m_terr_adjs = None
    
    _m_mans_by_state = None
    
    _m_unknown_regions = None
    
    _m_terr_noun_adjectives = None
    
    _m_capitals_by_state = None
    
    _m_alpha2state = None
    
    _m_all_states = None
    
    @staticmethod
    def __loadState(xml0_ : xml.etree.ElementTree.Element, lang : 'MorphLang') -> None:
        from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
        state = GeoReferent()
        c = IntOntologyItem(state)
        acrs = None
        for x in xml0_: 
            if (x.tag == "n"): 
                te = Termin()
                te.initByNormalText(Utils.getXmlInnerText(x), None)
                c.termins.append(te)
                state._addName(Utils.getXmlInnerText(x))
            elif (x.tag == "acr"): 
                c.termins.append(Termin._new1236(Utils.getXmlInnerText(x), lang))
                state._addName(Utils.getXmlInnerText(x))
                if (acrs is None): 
                    acrs = list()
                acrs.append(Utils.getXmlInnerText(x))
            elif (x.tag == "a"): 
                te = Termin()
                te.initByNormalText(Utils.getXmlInnerText(x), lang)
                te.tag = (c)
                c.termins.append(te)
                TerrItemToken._m_terr_adjs.add(te)
            elif (x.tag == "a2"): 
                state.alpha2 = Utils.getXmlInnerText(x)
            elif (x.tag == "m"): 
                te = Termin()
                te.initByNormalText(Utils.getXmlInnerText(x), lang)
                te.tag = (state)
                te.gender = MorphGender.MASCULINE
                TerrItemToken._m_mans_by_state.add(te)
            elif (x.tag == "w"): 
                te = Termin()
                te.initByNormalText(Utils.getXmlInnerText(x), lang)
                te.tag = (state)
                te.gender = MorphGender.FEMINIE
                TerrItemToken._m_mans_by_state.add(te)
            elif (x.tag == "cap"): 
                te = Termin()
                te.initByNormalText(Utils.getXmlInnerText(x), lang)
                te.tag = (state)
                TerrItemToken._m_capitals_by_state.add(te)
        c.setShortestCanonicalText(True)
        if (c.canonic_text == "ГОЛЛАНДИЯ" or c.canonic_text.startswith("КОРОЛЕВСТВО НИДЕР")): 
            c.canonic_text = "НИДЕРЛАНДЫ"
        elif (c.canonic_text == "ГОЛЛАНДІЯ" or c.canonic_text.startswith("КОРОЛІВСТВО НІДЕР")): 
            c.canonic_text = "НІДЕРЛАНДИ"
        if (state.alpha2 == "RU"): 
            if (lang.is_ua): 
                TerrItemToken.__m_russiaua = c
            else: 
                TerrItemToken.__m_russiaru = c
        elif (state.alpha2 == "BY"): 
            if (not lang.is_ua): 
                TerrItemToken.__m_belorussia = c
        elif (state.alpha2 == "KZ"): 
            if (not lang.is_ua): 
                TerrItemToken.__m_kazahstan = c
        elif (c.canonic_text == "ТАМОЖЕННЫЙ СОЮЗ"): 
            if (not lang.is_ua): 
                TerrItemToken.__m_tamog_sous = c
        if (state.findSlot(GeoReferent.ATTR_TYPE, None, True) is None): 
            if (lang.is_ua): 
                state._addTypState(lang)
            else: 
                state._addTypState(MorphLang.RU)
                state._addTypState(MorphLang.EN)
        TerrItemToken._m_terr_ontology.addItem(c)
        if (lang.is_ru): 
            TerrItemToken._m_all_states.append(state)
        a2 = state.alpha2
        if (a2 is not None): 
            if (not a2 in TerrItemToken._m_alpha2state): 
                TerrItemToken._m_alpha2state[a2] = c
            wrapa31237 = RefOutArgWrapper(None)
            inoutres1238 = Utils.tryGetValue(MiscLocationHelper._m_alpha2_3, a2, wrapa31237)
            a3 = wrapa31237.value
            if (inoutres1238): 
                if (not a3 in TerrItemToken._m_alpha2state): 
                    TerrItemToken._m_alpha2state[a3] = c
        if (acrs is not None): 
            for a in acrs: 
                if (not a in TerrItemToken._m_alpha2state): 
                    TerrItemToken._m_alpha2state[a] = c
    
    @staticmethod
    def __loadRegion(xml0_ : xml.etree.ElementTree.Element, lang : 'MorphLang') -> None:
        reg = GeoReferent()
        r = IntOntologyItem(reg)
        aterm = None
        for x in xml0_: 
            if (x.tag == "n"): 
                v = Utils.getXmlInnerText(x)
                if (v.startswith("ЦЕНТРАЛ")): 
                    pass
                te = Termin()
                te.initByNormalText(v, lang)
                if (lang.is_ru and TerrItemToken.__m_mos_regru is None and v == "ПОДМОСКОВЬЕ"): 
                    TerrItemToken.__m_mos_regru = r
                    te.addAbridge("МОС.ОБЛ.")
                    te.addAbridge("МОСК.ОБЛ.")
                    te.addAbridge("МОСКОВ.ОБЛ.")
                    te.addAbridge("МОС.ОБЛАСТЬ")
                    te.addAbridge("МОСК.ОБЛАСТЬ")
                    te.addAbridge("МОСКОВ.ОБЛАСТЬ")
                elif (lang.is_ru and TerrItemToken.__m_len_regru is None and v == "ЛЕНОБЛАСТЬ"): 
                    te.acronym = "ЛО"
                    te.addAbridge("ЛЕН.ОБЛ.")
                    te.addAbridge("ЛЕН.ОБЛАСТЬ")
                    TerrItemToken.__m_len_regru = r
                r.termins.append(te)
                reg._addName(v)
            elif (x.tag == "t"): 
                reg._addTyp(Utils.getXmlInnerText(x))
            elif (x.tag == "a"): 
                te = Termin()
                te.initByNormalText(Utils.getXmlInnerText(x), lang)
                te.tag = (r)
                r.termins.append(te)
            elif (x.tag == "ab"): 
                if (aterm is None): 
                    aterm = Termin._new477(reg.getStringValue(GeoReferent.ATTR_NAME), lang, reg)
                aterm.addAbridge(Utils.getXmlInnerText(x))
        if (aterm is not None): 
            TerrItemToken._m_geo_abbrs.add(aterm)
        r.setShortestCanonicalText(True)
        if (r.canonic_text.startswith("КАРАЧАЕВО")): 
            r.canonic_text = "КАРАЧАЕВО - ЧЕРКЕССИЯ"
        if ("ТАТАРСТАН" in r.canonic_text): 
            TerrItemToken.__m_tatarstan = r
        elif ("УДМУРТ" in r.canonic_text): 
            TerrItemToken.__m_udmurtia = r
        elif ("ДАГЕСТАН" in r.canonic_text): 
            TerrItemToken.__m_dagestan = r
        if (reg.is_state and reg.is_region): 
            reg._addTypReg(lang)
        TerrItemToken._m_terr_ontology.addItem(r)
    
    @staticmethod
    def _new1161(_arg1 : 'Token', _arg2 : 'Token', _arg3 : bool) -> 'TerrItemToken':
        res = TerrItemToken(_arg1, _arg2)
        res.is_adjective = _arg3
        return res
    
    @staticmethod
    def _new1162(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'TerrTermin', _arg4 : bool) -> 'TerrItemToken':
        res = TerrItemToken(_arg1, _arg2)
        res.termin_item = _arg3
        res.is_doubt = _arg4
        return res
    
    @staticmethod
    def _new1163(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'IntOntologyItem') -> 'TerrItemToken':
        res = TerrItemToken(_arg1, _arg2)
        res.onto_item = _arg3
        return res
    
    @staticmethod
    def _new1172(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ReferentToken', _arg4 : 'MorphCollection') -> 'TerrItemToken':
        res = TerrItemToken(_arg1, _arg2)
        res.rzd = _arg3
        res.morph = _arg4
        return res
    
    @staticmethod
    def _new1174(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'IntOntologyItem', _arg4 : 'MorphCollection') -> 'TerrItemToken':
        res = TerrItemToken(_arg1, _arg2)
        res.onto_item = _arg3
        res.morph = _arg4
        return res
    
    @staticmethod
    def _new1175(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'IntOntologyItem', _arg4 : bool, _arg5 : 'MorphCollection') -> 'TerrItemToken':
        res = TerrItemToken(_arg1, _arg2)
        res.onto_item = _arg3
        res.is_adjective = _arg4
        res.morph = _arg5
        return res
    
    @staticmethod
    def _new1176(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'TerrTermin', _arg4 : bool, _arg5 : 'MorphCollection') -> 'TerrItemToken':
        res = TerrItemToken(_arg1, _arg2)
        res.termin_item = _arg3
        res.is_adjective = _arg4
        res.morph = _arg5
        return res
    
    @staticmethod
    def _new1179(_arg1 : 'Token', _arg2 : 'Token', _arg3 : bool) -> 'TerrItemToken':
        res = TerrItemToken(_arg1, _arg2)
        res.is_doubt = _arg3
        return res
    
    # static constructor for class TerrItemToken
    @staticmethod
    def _static_ctor():
        TerrItemToken._m_all_states = list()

TerrItemToken._static_ctor()