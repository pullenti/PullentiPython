# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import io
import typing
import math
import xml.etree
from enum import IntEnum
from pullenti.unisharp.Utils import Utils

from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.morph.MorphWordForm import MorphWordForm
from pullenti.ner.core.ReferentsEqualType import ReferentsEqualType
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.core.NumberExType import NumberExType
from pullenti.ner.TextToken import TextToken
from pullenti.ner.address.internal.PullentiNerAddressInternalResourceHelper import PullentiNerAddressInternalResourceHelper
from pullenti.ner.MorphCollection import MorphCollection
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.core.IntOntologyItem import IntOntologyItem
from pullenti.ner.date.DateReferent import DateReferent
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.Referent import Referent
from pullenti.ner.core.IntOntologyCollection import IntOntologyCollection
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.address.internal.StreetItemType import StreetItemType
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken
from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
from pullenti.ner.address.internal.StreetItemToken import StreetItemToken

class CityItemToken(MetaToken):
    
    class ItemType(IntEnum):
        PROPERNAME = 0
        CITY = 1
        NOUN = 2
        MISC = 3
        
        @classmethod
        def has_value(cls, value):
            return any(value == item.value for item in cls)
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.typ = CityItemToken.ItemType.PROPERNAME
        self.value = None;
        self.alt_value = None;
        self.onto_item = None;
        self.doubtful = False
        self.geo_object_before = False
        self.geo_object_after = False
        self.higher_geo = None;
        self.org_ref = None;
    
    def __str__(self) -> str:
        res = io.StringIO()
        print("{0}".format(Utils.enumToString(self.typ)), end="", file=res, flush=True)
        if (self.value is not None): 
            print(" {0}".format(self.value), end="", file=res, flush=True)
        if (self.onto_item is not None): 
            print(" {0}".format(str(self.onto_item)), end="", file=res, flush=True)
        if (self.doubtful): 
            print(" (?)", end="", file=res)
        if (self.org_ref is not None): 
            print(" (Org: {0})".format(self.org_ref.referent), end="", file=res, flush=True)
        if (self.geo_object_before): 
            print(" GeoBefore", end="", file=res)
        if (self.geo_object_after): 
            print(" GeoAfter", end="", file=res)
        return Utils.toStringStringIO(res)
    
    def merge_with_next(self, ne : 'CityItemToken') -> bool:
        if (self.typ != CityItemToken.ItemType.NOUN or ne.typ != CityItemToken.ItemType.NOUN): 
            return False
        ok = False
        if (self.value == "ГОРОДСКОЕ ПОСЕЛЕНИЕ" and ne.value == "ГОРОД"): 
            ok = True
        if (not ok): 
            return False
        self.end_token = ne.end_token
        self.doubtful = False
        return True
    
    @staticmethod
    def try_parse_list(t : 'Token', loc : 'IntOntologyCollection', max_count : int) -> typing.List['CityItemToken']:
        from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
        ci = CityItemToken.try_parse(t, loc, False, None)
        if (ci is None): 
            if (t is None): 
                return None
            if (((isinstance(t, TextToken)) and t.is_value("МУНИЦИПАЛЬНЫЙ", None) and t.next0_ is not None) and t.next0_.is_value("ОБРАЗОВАНИЕ", None)): 
                t1 = t.next0_.next0_
                br = False
                if (BracketHelper.can_be_start_of_sequence(t1, False, False)): 
                    br = True
                    t1 = t1.next0_
                lii = CityItemToken.try_parse_list(t1, loc, max_count)
                if (lii is not None and lii[0].typ == CityItemToken.ItemType.NOUN): 
                    lii[0].begin_token = t
                    lii[0].doubtful = False
                    if (br and BracketHelper.can_be_end_of_sequence(lii[len(lii) - 1].end_token.next0_, False, None, False)): 
                        lii[len(lii) - 1].end_token = lii[len(lii) - 1].end_token.next0_
                    return lii
            return None
        if (ci.chars.is_latin_letter and ci.typ == CityItemToken.ItemType.NOUN and not t.chars.is_all_lower): 
            return None
        li = list()
        li.append(ci)
        t = ci.end_token.next0_
        first_pass3645 = True
        while True:
            if first_pass3645: first_pass3645 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_newline_before): 
                if (len(li) == 1 and li[0].typ == CityItemToken.ItemType.NOUN): 
                    pass
                else: 
                    break
            ci0 = CityItemToken.try_parse(t, loc, False, ci)
            if (ci0 is None): 
                if (t.is_newline_before): 
                    break
                if (ci.typ == CityItemToken.ItemType.NOUN and BracketHelper.can_be_start_of_sequence(t, True, False)): 
                    br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                    if ((br is not None and (br.length_char < 50) and t.next0_.chars.is_cyrillic_letter) and not t.next0_.chars.is_all_lower): 
                        ci0 = CityItemToken._new1134(br.begin_token, br.end_token, CityItemToken.ItemType.PROPERNAME)
                        tt = br.end_token.previous
                        num = None
                        if (isinstance(tt, NumberToken)): 
                            num = str(tt.value)
                            tt = tt.previous
                            if (tt is not None and tt.is_hiphen): 
                                tt = tt.previous
                        ci0.value = MiscHelper.get_text_value(br.begin_token.next0_, tt, GetTextAttr.NO)
                        if (tt != br.begin_token.next0_): 
                            ci0.alt_value = MiscHelper.get_text_value(br.begin_token.next0_, tt, GetTextAttr.NO)
                        if (Utils.isNullOrEmpty(ci0.value)): 
                            ci0 = (None)
                        elif (num is not None): 
                            ci0.value = "{0}-{1}".format(ci0.value, num)
                            if (ci0.alt_value is not None): 
                                ci0.alt_value = "{0}-{1}".format(ci0.alt_value, num)
                if ((ci0 is None and ((ci.typ == CityItemToken.ItemType.PROPERNAME or ci.typ == CityItemToken.ItemType.CITY)) and t.is_comma) and li[0] == ci): 
                    npt = NounPhraseHelper.try_parse(t.next0_, NounPhraseParseAttr.NO, 0, None)
                    if (npt is not None): 
                        tt = t.next0_
                        while tt is not None and tt.end_char <= npt.end_char: 
                            ci00 = CityItemToken.try_parse(tt, loc, False, ci)
                            if (ci00 is not None and ci00.typ == CityItemToken.ItemType.NOUN): 
                                ci01 = CityItemToken.try_parse(ci00.end_token.next0_, loc, False, ci)
                                if (ci01 is None): 
                                    ci0 = ci00
                                    ci0.alt_value = MiscHelper.get_text_value(t.next0_, ci00.end_token, (GetTextAttr.IGNOREARTICLES if t.kit.base_language.is_en else GetTextAttr.FIRSTNOUNGROUPTONOMINATIVESINGLE)).lower()
                                    break
                            if (not tt.chars.is_all_lower): 
                                break
                            tt = tt.next0_
                if (ci0 is None): 
                    break
            if ((ci0.typ == CityItemToken.ItemType.NOUN and ci0.value is not None and LanguageHelper.ends_with(ci0.value, "УСАДЬБА")) and ci.typ == CityItemToken.ItemType.NOUN): 
                ci.doubtful = False
                ci.end_token = ci0.end_token
                t = ci.end_token
                continue
            if (ci0.typ == CityItemToken.ItemType.NOUN and ci.typ == CityItemToken.ItemType.MISC and ci.value == "АДМИНИСТРАЦИЯ"): 
                ci0.doubtful = False
            if (ci.merge_with_next(ci0)): 
                t = ci.end_token
                continue
            ci = ci0
            li.append(ci)
            t = ci.end_token
            if (max_count > 0 and len(li) >= max_count): 
                break
        if (len(li) > 1 and li[0].value == "СОВЕТ"): 
            return None
        if (len(li) > 2 and li[0].typ == CityItemToken.ItemType.NOUN and li[1].typ == CityItemToken.ItemType.NOUN): 
            if (li[0].merge_with_next(li[1])): 
                del li[1]
        if (len(li) > 2 and li[0].is_newline_after): 
            del li[1:1+len(li) - 1]
        if (not li[0].geo_object_before): 
            li[0].geo_object_before = MiscLocationHelper.check_geo_object_before(li[0].begin_token)
        if (not li[len(li) - 1].geo_object_after): 
            li[len(li) - 1].geo_object_after = MiscLocationHelper.check_geo_object_after(li[len(li) - 1].end_token, True)
        if ((len(li) == 2 and li[0].typ == CityItemToken.ItemType.NOUN and li[1].typ == CityItemToken.ItemType.NOUN) and ((li[0].geo_object_before or li[1].geo_object_after))): 
            if (li[0].chars.is_capital_upper and li[1].chars.is_all_lower): 
                li[0].typ = CityItemToken.ItemType.PROPERNAME
            elif (li[1].chars.is_capital_upper and li[0].chars.is_all_lower): 
                li[1].typ = CityItemToken.ItemType.PROPERNAME
        return li
    
    @staticmethod
    def __check_doubtful(tt : 'TextToken') -> bool:
        if (tt is None): 
            return True
        if (tt.chars.is_all_lower): 
            return True
        if (tt.length_char < 3): 
            return True
        if (((tt.term == "СОЧИ" or tt.is_value("КИЕВ", None) or tt.is_value("ПСКОВ", None)) or tt.is_value("БОСТОН", None) or tt.is_value("РИГА", None)) or tt.is_value("АСТАНА", None) or tt.is_value("АЛМАТЫ", None)): 
            return False
        if (tt.term.endswith("ВО")): 
            return False
        if ((isinstance(tt.next0_, TextToken)) and (tt.whitespaces_after_count < 2) and not tt.next0_.chars.is_all_lower): 
            if (tt.chars == tt.next0_.chars and not tt.chars.is_latin_letter and ((not tt.morph.case_.is_genitive and not tt.morph.case_.is_accusative))): 
                mc = tt.next0_.get_morph_class_in_dictionary()
                if (mc.is_proper_surname or mc.is_proper_secname): 
                    return True
        if ((isinstance(tt.previous, TextToken)) and (tt.whitespaces_before_count < 2) and not tt.previous.chars.is_all_lower): 
            mc = tt.previous.get_morph_class_in_dictionary()
            if (mc.is_proper_surname): 
                return True
        ok = False
        for wff in tt.morph.items: 
            wf = Utils.asObjectOrNull(wff, MorphWordForm)
            if (wf.is_in_dictionary): 
                if (not wf.class0_.is_proper): 
                    ok = True
                if (wf.class0_.is_proper_surname or wf.class0_.is_proper_name or wf.class0_.is_proper_secname): 
                    if (wf.normal_case != "ЛОНДОН" and wf.normal_case != "ЛОНДОНЕ"): 
                        ok = True
            elif (wf.class0_.is_proper_surname): 
                val = Utils.ifNotNull(wf.normal_full, Utils.ifNotNull(wf.normal_case, ""))
                if (LanguageHelper.ends_with_ex(val, "ОВ", "ЕВ", "ИН", None)): 
                    if (val != "БЕРЛИН"): 
                        if (tt.previous is not None and tt.previous.is_value("В", None)): 
                            pass
                        else: 
                            return True
        if (not ok): 
            return False
        t0 = tt.previous
        if (t0 is not None and ((t0.is_char(',') or t0.morph.class0_.is_conjunction))): 
            t0 = t0.previous
        if (t0 is not None and (isinstance(t0.get_referent(), GeoReferent))): 
            return False
        t1 = tt.next0_
        if (t1 is not None and ((t1.is_char(',') or t1.morph.class0_.is_conjunction))): 
            t1 = t1.next0_
        if (CityItemToken.M_RECURSIVE == 0): 
            CityItemToken.M_RECURSIVE += 1
            cit = CityItemToken.__try_parse(t1, None, False, None)
            CityItemToken.M_RECURSIVE -= 1
            if (cit is None): 
                return True
            if (cit.typ == CityItemToken.ItemType.NOUN or cit.typ == CityItemToken.ItemType.CITY): 
                return False
        return True
    
    M_RECURSIVE = 0
    
    @staticmethod
    def try_parse(t : 'Token', loc : 'IntOntologyCollection', can_be_low_char : bool=False, prev : 'CityItemToken'=None) -> 'CityItemToken':
        if (t is None): 
            return None
        if (t.kit.is_recurce_overflow): 
            return None
        t.kit.recurse_level += 1
        res = CityItemToken.__try_parse_int(t, loc, can_be_low_char, prev)
        t.kit.recurse_level -= 1
        if (res is not None and res.typ == CityItemToken.ItemType.NOUN and (res.whitespaces_after_count < 2)): 
            nn = NounPhraseHelper.try_parse(res.end_token.next0_, NounPhraseParseAttr.NO, 0, None)
            if (nn is not None and ((nn.end_token.is_value("ЗНАЧЕНИЕ", "ЗНАЧЕННЯ") or nn.end_token.is_value("ТИП", None) or nn.end_token.is_value("ХОЗЯЙСТВО", "ХАЗЯЙСТВО")))): 
                res.end_token = nn.end_token
        if ((res is not None and res.typ == CityItemToken.ItemType.PROPERNAME and res.value is not None) and res.begin_token == res.end_token and len(res.value) > 4): 
            if (res.value.endswith("ГРАД") or res.value.endswith("ГОРОД")): 
                res.alt_value = (None)
                res.typ = CityItemToken.ItemType.CITY
            elif (((res.value.endswith("СК") or res.value.endswith("ИНО") or res.value.endswith("ПОЛЬ")) or res.value.endswith("ВЛЬ") or res.value.endswith("АС")) or res.value.endswith("ЕС")): 
                sits = StreetItemToken.try_parse_list(res.end_token.next0_, None, 3)
                if (sits is not None): 
                    if (len(sits) == 1 and sits[0].typ == StreetItemType.NOUN): 
                        return res
                    if (len(sits) == 2 and sits[0].typ == StreetItemType.NUMBER and sits[1].typ == StreetItemType.NOUN): 
                        return res
                mc = res.end_token.get_morph_class_in_dictionary()
                if (mc.is_proper_geo or mc.is_undefined): 
                    res.alt_value = (None)
                    res.typ = CityItemToken.ItemType.CITY
            elif (res.value.endswith("АНЬ") or res.value.endswith("TOWN") or res.value.startswith("SAN")): 
                res.typ = CityItemToken.ItemType.CITY
            elif (isinstance(res.end_token, TextToken)): 
                lem = res.end_token.lemma
                if ((lem.endswith("ГРАД") or lem.endswith("ГОРОД") or lem.endswith("СК")) or lem.endswith("АНЬ") or lem.endswith("ПОЛЬ")): 
                    res.alt_value = res.value
                    res.value = lem
                    ii = res.alt_value.find('-')
                    if (ii >= 0): 
                        res.value = (res.alt_value[0:0+ii + 1] + lem)
                    if (not lem.endswith("АНЬ")): 
                        res.alt_value = (None)
        return res
    
    @staticmethod
    def __try_parse_int(t : 'Token', loc : 'IntOntologyCollection', can_be_low_char : bool, prev : 'CityItemToken') -> 'CityItemToken':
        from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
        if (t is None): 
            return None
        res = CityItemToken.__try_parse(t, loc, can_be_low_char, prev)
        if ((prev is None and t.chars.is_cyrillic_letter and t.chars.is_all_upper) and t.length_char == 2): 
            if (t.is_value("ТА", None)): 
                res = CityItemToken.__try_parse(t.next0_, loc, can_be_low_char, prev)
                if (res is not None): 
                    if (res.typ == CityItemToken.ItemType.NOUN): 
                        res.begin_token = t
                        res.doubtful = False
                    else: 
                        res = (None)
        if ((prev is not None and prev.typ == CityItemToken.ItemType.NOUN and CityItemToken.M_RECURSIVE == 0) and ((prev.value != "ГОРОД" and prev.value != "МІСТО"))): 
            if (res is None or ((res.typ != CityItemToken.ItemType.NOUN and res.typ != CityItemToken.ItemType.MISC and res.typ != CityItemToken.ItemType.CITY))): 
                CityItemToken.M_RECURSIVE += 1
                det = AddressItemToken.try_attach_org(t)
                CityItemToken.M_RECURSIVE -= 1
                if (det is not None): 
                    cou = 0
                    ttt = det.begin_token
                    while ttt is not None and ttt.end_char <= det.end_char: 
                        if (ttt.chars.is_letter): 
                            cou += 1
                        ttt = ttt.next0_
                    if (cou < 6): 
                        re = CityItemToken._new1134(det.begin_token, det.end_token, CityItemToken.ItemType.PROPERNAME)
                        if (det.referent.type_name == "ORGANIZATION"): 
                            re.org_ref = det.ref_token
                        else: 
                            re.value = MiscHelper.get_text_value_of_meta_token(det, GetTextAttr.NO)
                            re.alt_value = MiscHelper.get_text_value_of_meta_token(det, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)
                        return re
        if (res is not None and res.typ == CityItemToken.ItemType.NOUN and (res.whitespaces_after_count < 3)): 
            npt = NounPhraseHelper.try_parse(res.end_token.next0_, NounPhraseParseAttr.NO, 0, None)
            if (npt is not None): 
                if (npt.end_token.is_value("ПОДЧИНЕНИЕ", "ПІДПОРЯДКУВАННЯ")): 
                    res.end_token = npt.end_token
        if ((res is not None and t.chars.is_all_upper and res.typ == CityItemToken.ItemType.PROPERNAME) and CityItemToken.M_RECURSIVE == 0): 
            tt = t.previous
            if (tt is not None and tt.is_comma): 
                tt = tt.previous
            geo_prev = None
            if (tt is not None and (isinstance(tt.get_referent(), GeoReferent))): 
                geo_prev = (Utils.asObjectOrNull(tt.get_referent(), GeoReferent))
            if (geo_prev is not None and ((geo_prev.is_region or geo_prev.is_city))): 
                CityItemToken.M_RECURSIVE += 1
                det = AddressItemToken.try_attach_org(t)
                CityItemToken.M_RECURSIVE -= 1
                if (det is not None): 
                    res = (None)
        if (res is not None and res.typ == CityItemToken.ItemType.PROPERNAME): 
            if ((t.is_value("ДУМА", "РАДА") or t.is_value("ГЛАВА", "ГОЛОВА") or t.is_value("АДМИНИСТРАЦИЯ", "АДМІНІСТРАЦІЯ")) or t.is_value("МЭР", "МЕР") or t.is_value("ПРЕДСЕДАТЕЛЬ", "ГОЛОВА")): 
                return None
        geo_after = None
        if (res is None): 
            if (BracketHelper.can_be_start_of_sequence(t, True, False)): 
                br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                if (br is not None): 
                    res = CityItemToken.__try_parse(t.next0_, loc, False, None)
                    if (res is not None and ((res.typ == CityItemToken.ItemType.PROPERNAME or res.typ == CityItemToken.ItemType.CITY))): 
                        res.begin_token = t
                        res.typ = CityItemToken.ItemType.PROPERNAME
                        res.end_token = br.end_token
                        if (res.end_token.next0_ != br.end_token): 
                            res.value = MiscHelper.get_text_value(t, br.end_token, GetTextAttr.NO)
                            res.alt_value = (None)
                        return res
            if (isinstance(t, TextToken)): 
                txt = t.term
                if (txt == "ИМ" or txt == "ИМЕНИ"): 
                    t1 = t.next0_
                    if (t1 is not None and t1.is_char('.')): 
                        t1 = t1.next0_
                    res = CityItemToken.__try_parse(t1, loc, can_be_low_char, None)
                    if (res is not None and ((((res.typ == CityItemToken.ItemType.CITY and res.doubtful)) or res.typ == CityItemToken.ItemType.PROPERNAME))): 
                        res.begin_token = t
                        res.morph = MorphCollection()
                        return res
                if (prev is not None and prev.typ == CityItemToken.ItemType.NOUN and ((not prev.doubtful or MiscLocationHelper.check_geo_object_before(prev.begin_token)))): 
                    if (t.chars.is_cyrillic_letter and t.length_char == 1 and t.chars.is_all_upper): 
                        if ((t.next0_ is not None and not t.is_whitespace_after and ((t.next0_.is_hiphen or t.next0_.is_char('.')))) and (t.next0_.whitespaces_after_count < 2)): 
                            res1 = CityItemToken.__try_parse(t.next0_.next0_, loc, False, None)
                            if (res1 is not None and ((res1.typ == CityItemToken.ItemType.PROPERNAME or res1.typ == CityItemToken.ItemType.CITY))): 
                                adjs = MiscLocationHelper.get_std_adj_full_str(txt, res1.morph.gender, res1.morph.number, True)
                                if (adjs is None and prev is not None and prev.typ == CityItemToken.ItemType.NOUN): 
                                    adjs = MiscLocationHelper.get_std_adj_full_str(txt, prev.morph.gender, MorphNumber.UNDEFINED, True)
                                if (adjs is None): 
                                    adjs = MiscLocationHelper.get_std_adj_full_str(txt, res1.morph.gender, res1.morph.number, False)
                                if (adjs is not None): 
                                    if (res1.value is None): 
                                        res1.value = res1.get_source_text().upper()
                                    if (res1.alt_value is not None): 
                                        res1.alt_value = "{0} {1}".format(adjs[0], res1.alt_value)
                                    elif (len(adjs) > 1): 
                                        res1.alt_value = "{0} {1}".format(adjs[1], res1.value)
                                    res1.value = "{0} {1}".format(adjs[0], res1.value)
                                    res1.begin_token = t
                                    res1.typ = CityItemToken.ItemType.PROPERNAME
                                    return res1
            tt = (t.previous if prev is None else prev.begin_token.previous)
            while tt is not None and tt.is_char_of(",."):
                tt = tt.previous
            geo_prev = None
            if (tt is not None and (isinstance(tt.get_referent(), GeoReferent))): 
                geo_prev = (Utils.asObjectOrNull(tt.get_referent(), GeoReferent))
            tt0 = t
            ooo = False
            has_geo_after = False
            if (geo_prev is not None or MiscLocationHelper.check_near_before(t.previous) is not None): 
                ooo = True
            elif (MiscLocationHelper.check_geo_object_before(t)): 
                ooo = True
            elif (t.chars.is_letter): 
                tt = t.next0_
                if (tt is not None and tt.is_char('.')): 
                    tt = tt.next0_
                if ((isinstance(tt, TextToken)) and not tt.chars.is_all_lower): 
                    if (MiscLocationHelper.check_geo_object_after(tt, True)): 
                        has_geo_after = True
                        ooo = has_geo_after
                    elif (AddressItemToken.check_street_after(tt.next0_)): 
                        ooo = True
                    else: 
                        if (loc is not None): 
                            pass
                        cit2 = CityItemToken.__try_parse(tt, loc, False, None)
                        if (cit2 is not None and cit2.begin_token != cit2.end_token and ((cit2.typ == CityItemToken.ItemType.PROPERNAME or cit2.typ == CityItemToken.ItemType.CITY))): 
                            if (AddressItemToken.check_street_after(cit2.end_token.next0_)): 
                                ooo = True
                        if (cit2 is not None and cit2.typ == CityItemToken.ItemType.CITY and tt.previous.is_char('.')): 
                            if (cit2.is_whitespace_after or ((cit2.end_token.next0_ is not None and cit2.end_token.next0_.length_char == 1))): 
                                ooo = True
                                if (cit2.onto_item is not None): 
                                    geo_after = (Utils.asObjectOrNull(cit2.onto_item.referent, GeoReferent))
            if (ooo): 
                tt = t
                ttt = tt
                first_pass3646 = True
                while True:
                    if first_pass3646: first_pass3646 = False
                    else: ttt = ttt.next0_
                    if (not (ttt is not None)): break
                    if (ttt.is_char_of(",.")): 
                        tt = ttt.next0_
                        continue
                    if (ttt.is_newline_before): 
                        break
                    det = AddressItemToken.try_attach_detail(ttt)
                    if (det is not None): 
                        ttt = det.end_token
                        tt = det.end_token.next0_
                        continue
                    det = AddressItemToken.try_attach_org(ttt)
                    if (det is not None): 
                        ttt = det.end_token
                        tt = det.end_token.next0_
                        tt0 = tt
                        continue
                    ait = AddressItemToken.try_parse(ttt, None, False, True, None)
                    if (ait is not None and ait.typ == AddressItemToken.ItemType.PLOT): 
                        ttt = ait.end_token
                        tt = ait.end_token.next0_
                        tt0 = tt
                        continue
                    break
                if (isinstance(tt, TextToken)): 
                    if (tt0.is_comma and tt0.next0_ is not None): 
                        tt0 = tt0.next0_
                    txt = tt.term
                    if ((((txt == "Д" or txt == "С" or txt == "C") or txt == "П" or txt == "Х")) and ((tt.chars.is_all_lower or ((tt.next0_ is not None and tt.next0_.is_char('.')))))): 
                        tt1 = tt
                        if (tt1.next0_ is not None and tt1.next0_.is_char('.')): 
                            tt1 = tt1.next0_
                        tt2 = tt1.next0_
                        if ((tt2 is not None and tt2.length_char == 1 and tt2.chars.is_cyrillic_letter) and tt2.chars.is_all_upper): 
                            if (tt2.next0_ is not None and ((tt2.next0_.is_char('.') or tt2.next0_.is_hiphen)) and not tt2.is_whitespace_after): 
                                tt2 = tt2.next0_.next0_
                        ok = False
                        if (txt == "Д" and (isinstance(tt2, NumberToken)) and not tt2.is_newline_before): 
                            ok = False
                        elif (((txt == "С" or txt == "C")) and (isinstance(tt2, TextToken)) and ((tt2.is_value("О", None) or tt2.is_value("O", None)))): 
                            ok = False
                        elif (tt2 is not None and tt2.chars.is_capital_upper and (tt2.whitespaces_before_count < 2)): 
                            ok = tt.chars.is_all_lower
                        elif (tt2 is not None and tt2.chars.is_all_upper and (tt2.whitespaces_before_count < 2)): 
                            ok = True
                            if (tt.chars.is_all_upper): 
                                rtt = tt.kit.process_referent("PERSON", tt)
                                if (rtt is not None): 
                                    ok = False
                                    ttt2 = rtt.end_token.next0_
                                    if (ttt2 is not None and ttt2.is_comma): 
                                        ttt2 = ttt2.next0_
                                    if (AddressItemToken.check_house_after(ttt2, False, False) or AddressItemToken.check_street_after(ttt2)): 
                                        ok = True
                                elif (tt.previous is not None and tt.previous.is_char('.')): 
                                    ok = False
                            elif (tt1 == tt): 
                                ok = False
                            if (not ok and tt1.next0_ is not None): 
                                ttt2 = tt1.next0_.next0_
                                if (ttt2 is not None and ttt2.is_comma): 
                                    ttt2 = ttt2.next0_
                                if (AddressItemToken.check_house_after(ttt2, False, False) or AddressItemToken.check_street_after(ttt2)): 
                                    ok = True
                        elif (prev is not None and prev.typ == CityItemToken.ItemType.PROPERNAME and (tt.whitespaces_before_count < 2)): 
                            if (MiscLocationHelper.check_geo_object_before(prev.begin_token.previous)): 
                                ok = True
                            if (txt == "П" and tt.next0_ is not None and ((tt.next0_.is_hiphen or tt.next0_.is_char_of("\\/")))): 
                                sit = StreetItemToken.try_parse(tt, None, False, None, False)
                                if (sit is not None and sit.typ == StreetItemType.NOUN): 
                                    ok = False
                        elif (prev is None): 
                            if (MiscLocationHelper.check_geo_object_before(tt.previous)): 
                                ok = True
                            elif (geo_after is not None or has_geo_after): 
                                ok = True
                        if (tt.previous is not None and tt.previous.is_hiphen and not tt.is_whitespace_before): 
                            if (tt.next0_ is not None and tt.next0_.is_char('.')): 
                                pass
                            else: 
                                ok = False
                        if (ok): 
                            res = CityItemToken._new1136(tt0, tt1, CityItemToken.ItemType.NOUN, True)
                            res.value = ("ДЕРЕВНЯ" if txt == "Д" else (("ПОСЕЛОК" if txt == "П" else (("ХУТОР" if txt == "Х" else "СЕЛО")))))
                            if (txt == "П"): 
                                res.alt_value = "ПОСЕЛЕНИЕ"
                            elif (txt == "С" or txt == "C"): 
                                res.alt_value = "СЕЛЕНИЕ"
                                if (tt0 == tt1): 
                                    npt = NounPhraseHelper.try_parse(tt1.next0_, NounPhraseParseAttr.PARSEPRONOUNS, 0, None)
                                    if (npt is not None and npt.morph.case_.is_instrumental): 
                                        return None
                            res.doubtful = True
                            return res
                    if ((txt == "СП" or txt == "РП" or txt == "ГП") or txt == "ДП"): 
                        if (tt.next0_ is not None and tt.next0_.is_char('.')): 
                            tt = tt.next0_
                        if (tt.next0_ is not None and tt.next0_.chars.is_capital_upper): 
                            return CityItemToken._new1137(tt0, tt, CityItemToken.ItemType.NOUN, True, ("РАБОЧИЙ ПОСЕЛОК" if txt == "РП" else (("ГОРОДСКОЕ ПОСЕЛЕНИЕ" if txt == "ГП" else (("ДАЧНЫЙ ПОСЕЛОК" if txt == "ДП" else "СЕЛЬСКОЕ ПОСЕЛЕНИЕ"))))))
                    res = CityItemToken.__try_parse(tt, loc, can_be_low_char, None)
                    if (res is not None and res.typ == CityItemToken.ItemType.NOUN): 
                        res.geo_object_before = True
                        res.begin_token = tt0
                        return res
                    if (tt.chars.is_all_upper and tt.length_char > 2 and tt.chars.is_cyrillic_letter): 
                        return CityItemToken._new1138(tt, tt, CityItemToken.ItemType.PROPERNAME, tt.term)
            if ((isinstance(t, NumberToken)) and t.next0_ is not None): 
                net = NumberHelper.try_parse_number_with_postfix(t)
                if (net is not None and net.ex_typ == NumberExType.KILOMETER): 
                    return CityItemToken._new1138(t, net.end_token, CityItemToken.ItemType.PROPERNAME, "{0}КМ".format(math.floor(net.real_value)))
            rt = Utils.asObjectOrNull(t, ReferentToken)
            if ((rt is not None and (isinstance(rt.referent, GeoReferent)) and rt.begin_token == rt.end_token) and rt.referent.is_state): 
                if (t.previous is None): 
                    return None
                if (t.previous.morph.number == MorphNumber.SINGULAR and t.morph.case_.is_nominative and not t.morph.case_.is_genitive): 
                    return CityItemToken._new1138(t, t, CityItemToken.ItemType.PROPERNAME, rt.get_source_text().upper())
            return None
        if (res.typ == CityItemToken.ItemType.NOUN): 
            if (res.value == "СЕЛО" and (isinstance(t, TextToken))): 
                if (t.previous is None): 
                    pass
                elif (t.previous.morph.class0_.is_preposition): 
                    pass
                else: 
                    res.doubtful = True
                res.morph.gender = MorphGender.NEUTER
            if (res.alt_value is None and res.begin_token.is_value("ПОСЕЛЕНИЕ", None)): 
                res.value = "ПОСЕЛЕНИЕ"
                res.alt_value = "ПОСЕЛОК"
            if (LanguageHelper.ends_with(res.value, "УСАДЬБА") and res.alt_value is None): 
                res.alt_value = "НАСЕЛЕННЫЙ ПУНКТ"
            if (res.value == "СТАНЦИЯ" or res.value == "СТАНЦІЯ"): 
                res.doubtful = True
            if (res.end_token.is_value("СТОЛИЦА", None) or res.end_token.is_value("СТОЛИЦЯ", None)): 
                res.doubtful = True
                if (res.end_token.next0_ is not None): 
                    geo_ = Utils.asObjectOrNull(res.end_token.next0_.get_referent(), GeoReferent)
                    if (geo_ is not None and ((geo_.is_region or geo_.is_state))): 
                        res.higher_geo = geo_
                        res.end_token = res.end_token.next0_
                        res.doubtful = False
                        res.value = "ГОРОД"
                        for it in TerrItemToken._m_capitals_by_state.termins: 
                            ge = Utils.asObjectOrNull(it.tag, GeoReferent)
                            if (ge is None or not ge.can_be_equals(geo_, ReferentsEqualType.WITHINONETEXT)): 
                                continue
                            tok = TerrItemToken._m_capitals_by_state.try_parse(res.end_token.next0_, TerminParseAttr.NO)
                            if (tok is not None and tok.termin == it): 
                                break
                            res.typ = CityItemToken.ItemType.CITY
                            res.value = it.canonic_text
                            return res
            if ((res.begin_token.length_char == 1 and res.begin_token.chars.is_all_upper and res.begin_token.next0_ is not None) and res.begin_token.next0_.is_char('.')): 
                ne = CityItemToken.__try_parse_int(res.begin_token.next0_.next0_, loc, False, None)
                if (ne is not None and ne.typ == CityItemToken.ItemType.CITY): 
                    pass
                elif (ne is not None and ne.typ == CityItemToken.ItemType.PROPERNAME and ((ne.value.endswith("К") or ne.value.endswith("О")))): 
                    pass
                else: 
                    return None
        if (res.typ == CityItemToken.ItemType.PROPERNAME or res.typ == CityItemToken.ItemType.CITY): 
            val = Utils.ifNotNull(res.value, ((None if res.onto_item is None else res.onto_item.canonic_text)))
            t1 = res.end_token
            if (((not t1.is_whitespace_after and t1.next0_ is not None and t1.next0_.is_hiphen) and not t1.next0_.is_whitespace_after and (isinstance(t1.next0_.next0_, NumberToken))) and t1.next0_.next0_.int_value is not None and (t1.next0_.next0_.int_value < 30)): 
                res.end_token = t1.next0_.next0_
                res.value = "{0}-{1}".format(val, t1.next0_.next0_.value)
                if (res.alt_value is not None): 
                    res.alt_value = "{0}-{1}".format(res.alt_value, t1.next0_.next0_.value)
                res.typ = CityItemToken.ItemType.PROPERNAME
            elif (t1.whitespaces_after_count == 1 and (isinstance(t1.next0_, NumberToken)) and t1.next0_.morph.class0_.is_adjective): 
                ok = False
                if (t1.next0_.next0_ is None or t1.next0_.is_newline_after): 
                    ok = True
                elif (not t1.next0_.is_whitespace_after and t1.next0_.next0_ is not None and t1.next0_.next0_.is_char_of(",")): 
                    ok = True
                if (ok): 
                    res.end_token = t1.next0_
                    res.value = "{0}-{1}".format(val, t1.next0_.value)
                    res.typ = CityItemToken.ItemType.PROPERNAME
        if (res.typ == CityItemToken.ItemType.CITY and res.begin_token == res.end_token): 
            if (res.begin_token.get_morph_class_in_dictionary().is_adjective and (isinstance(res.end_token.next0_, TextToken))): 
                ok = False
                t1 = None
                npt = NounPhraseHelper.try_parse(res.begin_token, NounPhraseParseAttr.NO, 0, None)
                if (npt is not None and npt.end_token == res.end_token.next0_): 
                    t1 = npt.end_token
                    if (res.end_token.next0_.chars == res.begin_token.chars): 
                        ok = True
                        if (res.begin_token.chars.is_all_upper): 
                            cii = CityItemToken.__try_parse_int(res.end_token.next0_, loc, False, None)
                            if (cii is not None and cii.typ == CityItemToken.ItemType.NOUN): 
                                ok = False
                    elif (res.end_token.next0_.chars.is_all_lower): 
                        ttt = res.end_token.next0_.next0_
                        if (ttt is None or ttt.is_char_of(",.")): 
                            ok = True
                elif (res.end_token.next0_.chars == res.begin_token.chars and res.begin_token.chars.is_capital_upper): 
                    ttt = res.end_token.next0_.next0_
                    if (ttt is None or ttt.is_char_of(",.")): 
                        ok = True
                    t1 = res.end_token.next0_
                    npt = (None)
                if (ok and t1 is not None): 
                    res.typ = CityItemToken.ItemType.PROPERNAME
                    res.onto_item = (None)
                    res.end_token = t1
                    if (npt is not None): 
                        res.value = npt.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
                        res.morph = npt.morph
                    else: 
                        res.value = MiscHelper.get_text_value(res.begin_token, res.end_token, GetTextAttr.NO)
            if ((res.end_token.next0_ is not None and res.end_token.next0_.is_hiphen and not res.end_token.next0_.is_whitespace_after) and not res.end_token.next0_.is_whitespace_before): 
                res1 = CityItemToken.__try_parse(res.end_token.next0_.next0_, loc, False, None)
                if ((res1 is not None and res1.typ == CityItemToken.ItemType.PROPERNAME and res1.begin_token == res1.end_token) and res1.begin_token.chars == res.begin_token.chars): 
                    if (res1.onto_item is None and res.onto_item is None): 
                        res.typ = CityItemToken.ItemType.PROPERNAME
                        res.value = "{0}-{1}".format((res.value if res.onto_item is None else res.onto_item.canonic_text), res1.value)
                        if (res.alt_value is not None): 
                            res.alt_value = "{0}-{1}".format(res.alt_value, res1.value)
                        res.onto_item = (None)
                        res.end_token = res1.end_token
                        res.doubtful = False
                elif ((isinstance(res.end_token.next0_.next0_, NumberToken)) and res.end_token.next0_.next0_.int_value is not None and (res.end_token.next0_.next0_.int_value < 30)): 
                    res.typ = CityItemToken.ItemType.PROPERNAME
                    res.value = "{0}-{1}".format((res.value if res.onto_item is None else res.onto_item.canonic_text), res.end_token.next0_.next0_.value)
                    if (res.alt_value is not None): 
                        res.alt_value = "{0}-{1}".format(res.alt_value, res.end_token.next0_.next0_.value)
                    res.onto_item = (None)
                    res.end_token = res.end_token.next0_.next0_
            elif (res.begin_token.get_morph_class_in_dictionary().is_proper_name): 
                if (res.begin_token.is_value("КИЇВ", None) or res.begin_token.is_value("АСТАНА", None) or res.begin_token.is_value("АЛМАТЫ", None)): 
                    pass
                elif ((isinstance(res.end_token, TextToken)) and res.end_token.term.endswith("ВО")): 
                    pass
                else: 
                    res.doubtful = True
                    tt = res.begin_token.previous
                    if (tt is not None and tt.previous is not None): 
                        if (tt.is_char(',') or tt.morph.class0_.is_conjunction): 
                            geo_ = Utils.asObjectOrNull(tt.previous.get_referent(), GeoReferent)
                            if (geo_ is not None and geo_.is_city): 
                                res.doubtful = False
                    if (tt is not None and tt.is_value("В", None) and tt.chars.is_all_lower): 
                        npt1 = NounPhraseHelper.try_parse(res.begin_token, NounPhraseParseAttr.NO, 0, None)
                        if (npt1 is None or npt1.end_char <= res.end_char): 
                            res.doubtful = False
            if ((res.begin_token == res.end_token and res.typ == CityItemToken.ItemType.CITY and res.onto_item is not None) and res.onto_item.canonic_text == "САНКТ - ПЕТЕРБУРГ"): 
                tt = res.begin_token.previous
                first_pass3647 = True
                while True:
                    if first_pass3647: first_pass3647 = False
                    else: tt = tt.previous
                    if (not (tt is not None)): break
                    if (tt.is_hiphen or tt.is_char('.')): 
                        continue
                    if (tt.is_value("С", None) or tt.is_value("C", None) or tt.is_value("САНКТ", None)): 
                        res.begin_token = tt
                    break
        if ((res.begin_token == res.end_token and res.typ == CityItemToken.ItemType.PROPERNAME and res.whitespaces_after_count == 1) and (isinstance(res.end_token.next0_, TextToken)) and res.end_token.chars == res.end_token.next0_.chars): 
            ok = False
            t1 = res.end_token
            if (t1.next0_.next0_ is None or t1.next0_.is_newline_after): 
                ok = True
            elif (not t1.next0_.is_whitespace_after and t1.next0_.next0_ is not None and t1.next0_.next0_.is_char_of(",.")): 
                ok = True
            if (ok): 
                pp = CityItemToken.__try_parse(t1.next0_, loc, False, None)
                if (pp is not None and pp.typ == CityItemToken.ItemType.NOUN): 
                    ok = False
                if (ok): 
                    te = TerrItemToken.try_parse(t1.next0_, None, False, False, None)
                    if (te is not None and te.termin_item is not None): 
                        ok = False
            if (ok): 
                res.end_token = t1.next0_
                res.value = MiscHelper.get_text_value(res.begin_token, res.end_token, GetTextAttr.NO)
                res.alt_value = (None)
                res.typ = CityItemToken.ItemType.PROPERNAME
        return res
    
    @staticmethod
    def __try_parse(t : 'Token', loc : 'IntOntologyCollection', can_be_low_char : bool=False, prev : 'CityItemToken'=None) -> 'CityItemToken':
        if (not (isinstance(t, TextToken))): 
            if ((isinstance(t, ReferentToken)) and (isinstance(t.get_referent(), DateReferent))): 
                aii = StreetItemToken._try_parse_spec(t, None)
                if (aii is not None): 
                    if (len(aii) > 1 and aii[0].typ == StreetItemType.NUMBER and aii[1].typ == StreetItemType.STDNAME): 
                        res2 = CityItemToken._new1134(t, aii[1].end_token, CityItemToken.ItemType.PROPERNAME)
                        res2.value = "{0} {1}".format((aii[0].value if aii[0].number is None else str(aii[0].number.int_value)), aii[1].value)
                        return res2
            return None
        li = list()
        li0 = None
        is_in_loc_onto = False
        if (loc is not None): 
            li0 = loc.try_attach(t, None, False)
            if ((li0) is not None): 
                li.extend(li0)
                is_in_loc_onto = True
        if (t.kit.ontology is not None and len(li) == 0): 
            li0 = t.kit.ontology.attach_token(GeoReferent.OBJ_TYPENAME, t)
            if ((li0) is not None): 
                li.extend(li0)
                is_in_loc_onto = True
        if (len(li) == 0): 
            li0 = CityItemToken.M_ONTOLOGY.try_attach(t, None, False)
            if (li0 is not None): 
                li.extend(li0)
        if (len(li) > 0): 
            if (isinstance(t, TextToken)): 
                for i in range(len(li) - 1, -1, -1):
                    if (li[i].item is not None): 
                        g = Utils.asObjectOrNull(li[i].item.referent, GeoReferent)
                        if (g is not None): 
                            if (not g.is_city): 
                                del li[i]
                                continue
                tt = Utils.asObjectOrNull(t, TextToken)
                for nt in li: 
                    if (nt.item is not None and nt.item.canonic_text == tt.term): 
                        if (can_be_low_char or not MiscHelper.is_all_characters_lower(nt.begin_token, nt.end_token, False)): 
                            ci = CityItemToken._new1142(nt.begin_token, nt.end_token, CityItemToken.ItemType.CITY, nt.item, nt.morph)
                            if (nt.begin_token == nt.end_token and not is_in_loc_onto): 
                                ci.doubtful = CityItemToken.__check_doubtful(Utils.asObjectOrNull(nt.begin_token, TextToken))
                            tt1 = nt.end_token.next0_
                            if ((((tt1 is not None and tt1.is_hiphen and not tt1.is_whitespace_before) and not tt1.is_whitespace_after and prev is not None) and prev.typ == CityItemToken.ItemType.NOUN and (isinstance(tt1.next0_, TextToken))) and tt1.previous.chars == tt1.next0_.chars): 
                                li = (None)
                                break
                            return ci
                if (li is not None): 
                    for nt in li: 
                        if (nt.item is not None): 
                            if (can_be_low_char or not MiscHelper.is_all_characters_lower(nt.begin_token, nt.end_token, False)): 
                                ci = CityItemToken._new1142(nt.begin_token, nt.end_token, CityItemToken.ItemType.CITY, nt.item, nt.morph)
                                if (nt.begin_token == nt.end_token and (isinstance(nt.begin_token, TextToken))): 
                                    ci.doubtful = CityItemToken.__check_doubtful(Utils.asObjectOrNull(nt.begin_token, TextToken))
                                    str0_ = nt.begin_token.term
                                    if (str0_ != nt.item.canonic_text): 
                                        if (LanguageHelper.ends_with_ex(str0_, "О", "А", None, None)): 
                                            ci.alt_value = str0_
                                return ci
            if (li is not None): 
                for nt in li: 
                    if (nt.item is None): 
                        ty = (CityItemToken.ItemType.NOUN if nt.termin.tag is None else Utils.valToEnum(nt.termin.tag, CityItemToken.ItemType))
                        ci = CityItemToken._new1144(nt.begin_token, nt.end_token, ty, nt.morph)
                        ci.value = nt.termin.canonic_text
                        if (ty == CityItemToken.ItemType.MISC and ci.value == "ЖИТЕЛЬ" and t.previous is not None): 
                            if (t.previous.is_value("МЕСТНЫЙ", "МІСЦЕВИЙ")): 
                                return None
                            if (t.previous.morph.class0_.is_pronoun): 
                                return None
                        if (ty == CityItemToken.ItemType.NOUN and not t.chars.is_all_lower): 
                            if (t.morph.class0_.is_proper_surname): 
                                ci.doubtful = True
                        if (nt.begin_token.kit.base_language.is_ua): 
                            if (nt.begin_token.is_value("М", None) or nt.begin_token.is_value("Г", None)): 
                                if (not nt.begin_token.chars.is_all_lower): 
                                    return None
                                ci.doubtful = True
                            elif (nt.begin_token.is_value("МІС", None)): 
                                if (t.term != "МІС"): 
                                    return None
                                ci.doubtful = True
                        if (nt.begin_token.kit.base_language.is_ru): 
                            if (nt.begin_token.is_value("Г", None)): 
                                if (nt.begin_token.previous is not None and nt.begin_token.previous.morph.class0_.is_preposition): 
                                    pass
                                else: 
                                    if (not nt.begin_token.chars.is_all_lower): 
                                        return None
                                    if ((nt.end_token == nt.begin_token and nt.end_token.next0_ is not None and not nt.end_token.is_whitespace_after) and ((nt.end_token.next0_.is_char_of("\\/") or nt.end_token.next0_.is_hiphen))): 
                                        return None
                                    if (not t.is_whitespace_before and t.previous is not None): 
                                        if (t.previous.is_char_of("\\/") or t.previous.is_hiphen): 
                                            return None
                                ci.doubtful = True
                            elif (nt.begin_token.is_value("ГОР", None)): 
                                if (t.term != "ГОР"): 
                                    if (t.chars.is_capital_upper): 
                                        ci = (None)
                                        break
                                    return None
                                ci.doubtful = True
                            elif (nt.begin_token.is_value("ПОС", None)): 
                                if (t.term != "ПОС"): 
                                    return None
                                ci.doubtful = True
                        npt1 = NounPhraseHelper.try_parse(t.previous, NounPhraseParseAttr.NO, 0, None)
                        if (npt1 is not None and len(npt1.adjectives) > 0): 
                            s = npt1.adjectives[0].get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
                            if ((s == "РОДНОЙ" or s == "ЛЮБИМЫЙ" or s == "РІДНИЙ") or s == "КОХАНИЙ"): 
                                return None
                        return ci
        if (not (isinstance(t, TextToken))): 
            return None
        if (t.term == "СПБ" and not t.chars.is_all_lower and CityItemToken.M_ST_PETERBURG is not None): 
            return CityItemToken._new1145(t, t, CityItemToken.ItemType.CITY, CityItemToken.M_ST_PETERBURG, CityItemToken.M_ST_PETERBURG.canonic_text)
        if (t.chars.is_all_lower): 
            return None
        stds = CityItemToken.M_STD_ADJECTIVES.try_attach(t, None, False)
        if (stds is not None): 
            cit = CityItemToken.__try_parse(stds[0].end_token.next0_, loc, False, None)
            if (cit is not None and ((((cit.typ == CityItemToken.ItemType.PROPERNAME and cit.value is not None)) or cit.typ == CityItemToken.ItemType.CITY))): 
                adj = stds[0].termin.canonic_text
                cit.value = "{0} {1}".format(adj, Utils.ifNotNull(cit.value, (cit.onto_item.canonic_text if cit is not None and cit.onto_item is not None else None)))
                if (cit.alt_value is not None): 
                    cit.alt_value = "{0} {1}".format(adj, cit.alt_value)
                cit.begin_token = t
                npt0 = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0, None)
                if (npt0 is not None and npt0.end_token == cit.end_token): 
                    cit.morph = npt0.morph
                    cit.value = npt0.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
                cit.typ = CityItemToken.ItemType.PROPERNAME
                cit.doubtful = False
                return cit
        t1 = t
        doubt = False
        name = io.StringIO()
        altname = None
        k = 0
        is_prep = False
        tt = t
        while tt is not None: 
            if (not (isinstance(tt, TextToken))): 
                break
            if (not tt.chars.is_letter or ((tt.chars.is_cyrillic_letter != t.chars.is_cyrillic_letter and not tt.is_value("НА", None)))): 
                break
            if (tt != t): 
                si = StreetItemToken.try_parse(tt, None, False, None, False)
                if (si is not None and si.typ == StreetItemType.NOUN): 
                    if (si.end_token.next0_ is None or si.end_token.next0_.is_char_of(",.")): 
                        pass
                    else: 
                        break
                if (tt.length_char < 2): 
                    break
                if ((tt.length_char < 3) and not tt.is_value("НА", None)): 
                    if (tt.is_whitespace_before): 
                        break
            if (name.tell() > 0): 
                print('-', end="", file=name)
                if (altname is not None): 
                    print('-', end="", file=altname)
            if ((isinstance(tt, TextToken)) and ((is_prep or ((k > 0 and not tt.get_morph_class_in_dictionary().is_proper_geo))))): 
                print(tt.term, end="", file=name)
                if (altname is not None): 
                    print(tt.term, end="", file=altname)
            else: 
                ss = CityItemToken.__get_normal_geo(tt)
                if (ss != tt.term): 
                    if (altname is None): 
                        altname = io.StringIO()
                    print(Utils.toStringStringIO(name), end="", file=altname)
                    print(tt.term, end="", file=altname)
                print(ss, end="", file=name)
            t1 = tt
            is_prep = tt.morph.class0_.is_preposition
            if (tt.next0_ is None or tt.next0_.next0_ is None): 
                break
            if (not tt.next0_.is_hiphen): 
                break
            if (tt.is_whitespace_after or tt.next0_.is_whitespace_after): 
                if (tt.whitespaces_after_count > 1 or tt.next0_.whitespaces_after_count > 1): 
                    break
                if (tt.next0_.next0_.chars != tt.chars): 
                    break
                ttt = tt.next0_.next0_.next0_
                if (ttt is not None and not ttt.is_newline_after): 
                    if (ttt.chars.is_letter): 
                        break
            tt = tt.next0_
            k += 1
            tt = tt.next0_
        if (k > 0): 
            if (k > 2): 
                return None
            reee = CityItemToken._new1146(t, t1, CityItemToken.ItemType.PROPERNAME, Utils.toStringStringIO(name), doubt)
            if (altname is not None): 
                reee.alt_value = Utils.toStringStringIO(altname)
            return reee
        if (t is None): 
            return None
        npt = (None if t.chars.is_latin_letter else NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0, None))
        if ((npt is not None and npt.end_token != t and len(npt.adjectives) > 0) and not npt.adjectives[0].end_token.next0_.is_comma): 
            cit = CityItemToken.__try_parse(t.next0_, loc, False, None)
            if (cit is not None and cit.typ == CityItemToken.ItemType.NOUN and ((LanguageHelper.ends_with_ex(cit.value, "ПУНКТ", "ПОСЕЛЕНИЕ", "ПОСЕЛЕННЯ", "ПОСЕЛОК") or t.next0_.is_value("ГОРОДОК", None)))): 
                return CityItemToken._new1147(t, t, CityItemToken.ItemType.CITY, t.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False), npt.morph)
            else: 
                if (npt.end_token.chars != t.chars): 
                    if (npt.end_token.chars.is_all_lower and ((npt.end_token.next0_ is None or npt.end_token.next0_.is_comma))): 
                        pass
                    else: 
                        return None
                if (len(npt.adjectives) != 1): 
                    return None
                npt1 = NounPhraseHelper.try_parse(npt.end_token, NounPhraseParseAttr.NO, 0, None)
                if (npt1 is None or len(npt1.adjectives) == 0): 
                    si = StreetItemToken.try_parse(npt.end_token, None, False, None, False)
                    if (si is None or si.typ != StreetItemType.NOUN): 
                        t1 = npt.end_token
                        doubt = CityItemToken.__check_doubtful(Utils.asObjectOrNull(t1, TextToken))
                        return CityItemToken._new1148(t, t1, CityItemToken.ItemType.PROPERNAME, npt.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False), doubt, npt.morph)
        if (t.next0_ is not None and t.next0_.chars == t.chars and not t.is_newline_after): 
            ok = False
            if (t.next0_.next0_ is None or t.next0_.next0_.chars != t.chars): 
                ok = True
            elif (isinstance(t.next0_.next0_.get_referent(), GeoReferent)): 
                ok = True
            elif (CityItemToken.M_RECURSIVE == 0): 
                CityItemToken.M_RECURSIVE += 1
                tis = TerrItemToken.try_parse_list(t.next0_.next0_, loc, 2)
                CityItemToken.M_RECURSIVE -= 1
                if (tis is not None and len(tis) > 1): 
                    if (tis[0].is_adjective and tis[1].termin_item is not None): 
                        ok = True
            if (ok and (isinstance(t.next0_, TextToken))): 
                doubt = CityItemToken.__check_doubtful(Utils.asObjectOrNull(t.next0_, TextToken))
                stat = t.kit.statistics.get_bigramm_info(t, t.next0_)
                ok1 = False
                if ((stat is not None and stat.pair_count >= 2 and stat.pair_count == stat.second_count) and not stat.second_has_other_first): 
                    if (stat.pair_count > 2): 
                        doubt = False
                    ok1 = True
                elif (CityItemToken.M_STD_ADJECTIVES.try_attach(t, None, False) is not None and (isinstance(t.next0_, TextToken))): 
                    ok1 = True
                elif (((t.next0_.next0_ is None or t.next0_.next0_.is_comma)) and t.morph.class0_.is_noun and ((t.next0_.morph.class0_.is_adjective or t.next0_.morph.class0_.is_noun))): 
                    ok1 = True
                if (ok1): 
                    tne = CityItemToken.__try_parse_int(t.next0_, loc, False, None)
                    if (tne is not None and tne.typ == CityItemToken.ItemType.NOUN): 
                        pass
                    else: 
                        print(" {0}".format(t.next0_.term), end="", file=name, flush=True)
                        if (altname is not None): 
                            print(" {0}".format(t.next0_.term), end="", file=altname, flush=True)
                        t1 = t.next0_
                        return CityItemToken._new1149(t, t1, CityItemToken.ItemType.PROPERNAME, Utils.toStringStringIO(name), (None if altname is None else Utils.toStringStringIO(altname)), doubt, t.next0_.morph)
        if (t.length_char < 2): 
            return None
        t1 = t
        doubt = CityItemToken.__check_doubtful(Utils.asObjectOrNull(t, TextToken))
        if (((t.next0_ is not None and prev is not None and prev.typ == CityItemToken.ItemType.NOUN) and t.next0_.chars.is_cyrillic_letter and t.next0_.chars.is_all_lower) and t.whitespaces_after_count == 1): 
            tt = t.next0_
            ok = False
            if (tt.next0_ is None or tt.next0_.is_char_of(",;")): 
                ok = True
            if (ok and AddressItemToken.try_parse(tt.next0_, None, False, False, None) is None): 
                t1 = tt
                print(" {0}".format(t1.get_source_text().upper()), end="", file=name, flush=True)
        if (MiscHelper.is_eng_article(t)): 
            return None
        res = CityItemToken._new1149(t, t1, CityItemToken.ItemType.PROPERNAME, Utils.toStringStringIO(name), (None if altname is None else Utils.toStringStringIO(altname)), doubt, t.morph)
        if (t1 == t and (isinstance(t1, TextToken)) and t1.term0 is not None): 
            res.alt_value = t1.term0
        sog = False
        glas = False
        for ch in res.value: 
            if (LanguageHelper.is_cyrillic_vowel(ch) or LanguageHelper.is_latin_vowel(ch)): 
                glas = True
            else: 
                sog = True
        if (not glas or not sog): 
            return None
        if (t == t1 and (isinstance(t, TextToken))): 
            if (t.term != res.value): 
                res.alt_value = t.term
        return res
    
    @staticmethod
    def try_parse_back(t : 'Token') -> 'CityItemToken':
        while t is not None and ((t.is_char_of("(,") or t.is_and)):
            t = t.previous
        if (not (isinstance(t, TextToken))): 
            return None
        cou = 0
        tt = t
        first_pass3648 = True
        while True:
            if first_pass3648: first_pass3648 = False
            else: tt = tt.previous
            if (not (tt is not None)): break
            if (not (isinstance(tt, TextToken))): 
                return None
            if (not tt.chars.is_letter): 
                continue
            res = CityItemToken.try_parse(tt, None, True, None)
            if (res is not None and res.end_token == t): 
                return res
            cou += 1
            if (cou > 2): 
                break
        return None
    
    @staticmethod
    def __get_normal_geo(t : 'Token') -> str:
        tt = Utils.asObjectOrNull(t, TextToken)
        if (tt is None): 
            return None
        if (tt.term[len(tt.term) - 1] == 'О'): 
            return tt.term
        if (tt.term[len(tt.term) - 1] == 'Ы'): 
            return tt.term
        for wf in tt.morph.items: 
            if (wf.class0_.is_proper_geo and wf.is_in_dictionary): 
                return wf.normal_case
        geo_eq_term = False
        for wf in tt.morph.items: 
            if (wf.class0_.is_proper_geo): 
                ggg = wf.normal_case
                if (ggg == tt.term): 
                    geo_eq_term = True
                elif (not wf.case_.is_nominative): 
                    return ggg
        if (geo_eq_term): 
            return tt.term
        if (tt.morph.items_count > 0): 
            return tt.morph.get_indexer_item(0).normal_case
        else: 
            return tt.term
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
        if (CityItemToken.M_ONTOLOGY is not None): 
            return
        CityItemToken.M_ONTOLOGY = IntOntologyCollection()
        CityItemToken.M_CITY_ADJECTIVES = TerminCollection()
        t = Termin("ГОРОД")
        t.add_abridge("ГОР.")
        t.add_abridge("Г.")
        t.tag = CityItemToken.ItemType.NOUN
        t.add_variant("ГОРОДОК", False)
        t.add_variant("ШАХТЕРСКИЙ ГОРОДОК", False)
        t.add_variant("ПРИМОРСКИЙ ГОРОДОК", False)
        t.add_variant("МАЛЕНЬКИЙ ГОРОДОК", False)
        t.add_variant("НЕБОЛЬШОЙ ГОРОДОК", False)
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("CITY")
        t.tag = CityItemToken.ItemType.NOUN
        t.add_variant("TOWN", False)
        t.add_variant("CAPITAL", False)
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("МІСТО", MorphLang.UA)
        t.add_abridge("МІС.")
        t.add_abridge("М.")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin._new1116("ГОРОД-ГЕРОЙ", "ГОРОД")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin._new1152("МІСТО-ГЕРОЙ", MorphLang.UA, "МІСТО")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin._new1116("ГОРОД-КУРОРТ", "ГОРОД")
        t.add_abridge("Г.К.")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin._new1152("МІСТО-КУРОРТ", MorphLang.UA, "МІСТО")
        t.add_abridge("М.К.")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("СЕЛО")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("ДЕРЕВНЯ")
        t.add_abridge("ДЕР.")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("СЕЛЕНИЕ")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("СЕЛО", MorphLang.UA)
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("ПОРТ")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("ПОРТ", MorphLang.UA)
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("ПОСЕЛОК")
        t.add_abridge("ПОС.")
        t.tag = CityItemToken.ItemType.NOUN
        t.add_variant("ПОСЕЛЕНИЕ", False)
        t.add_variant("ЖИЛОЙ ПОСЕЛОК", False)
        t.add_variant("КОТТЕДЖНЫЙ ПОСЕЛОК", False)
        t.add_variant("ВАХТОВЫЙ ПОСЕЛОК", False)
        t.add_variant("ШАХТЕРСКИЙ ПОСЕЛОК", False)
        t.add_variant("ДАЧНЫЙ ПОСЕЛОК", False)
        t.add_variant("КУРОРТНЫЙ ПОСЕЛОК", False)
        t.add_variant("ПОСЕЛОК СОВХОЗА", False)
        t.add_variant("ПОСЕЛОК КОЛХОЗА", False)
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("СЕЛИЩЕ", MorphLang.UA)
        t.add_abridge("СЕЛ.")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("ПОСЕЛОК ГОРОДСКОГО ТИПА")
        t.acronym_smart = "ПГТ"
        t.acronym = t.acronym_smart
        t.add_abridge("ПГТ.")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("СЕЛИЩЕ МІСЬКОГО ТИПУ", MorphLang.UA)
        t.acronym_smart = "СМТ"
        t.acronym = t.acronym_smart
        t.add_abridge("СМТ.")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("РАБОЧИЙ ПОСЕЛОК")
        t.add_abridge("Р.П.")
        t.tag = CityItemToken.ItemType.NOUN
        t.add_abridge("РАБ.П.")
        t.add_abridge("Р.ПОС.")
        t.add_abridge("РАБ.ПОС.")
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("РОБОЧЕ СЕЛИЩЕ", MorphLang.UA)
        t.add_abridge("Р.С.")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("ДАЧНЫЙ ПОСЕЛОК")
        t.add_abridge("Д.П.")
        t.tag = CityItemToken.ItemType.NOUN
        t.add_abridge("ДАЧ.П.")
        t.add_abridge("Д.ПОС.")
        t.add_abridge("ДАЧ.ПОС.")
        t.add_variant("ЖИЛИЩНО ДАЧНЫЙ ПОСЕЛОК", False)
        t.add_variant("ДАЧНОЕ ПОСЕЛЕНИЕ", False)
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("ДАЧНЕ СЕЛИЩЕ", MorphLang.UA)
        t.add_abridge("Д.С.")
        t.tag = CityItemToken.ItemType.NOUN
        t.add_abridge("ДАЧ.С.")
        t.add_abridge("Д.СЕЛ.")
        t.add_abridge("ДАЧ.СЕЛ.")
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("ГОРОДСКОЕ ПОСЕЛЕНИЕ")
        t.add_abridge("Г.П.")
        t.tag = CityItemToken.ItemType.NOUN
        t.add_abridge("Г.ПОС.")
        t.add_abridge("ГОР.П.")
        t.add_abridge("ГОР.ПОС.")
        t.add_variant("ГОРОДСКОЙ ОКРУГ", False)
        t.add_abridge("ГОР. ОКРУГ")
        t.add_abridge("Г.О.")
        t.add_abridge("Г.О.Г.")
        t.add_abridge("ГОРОДСКОЙ ОКРУГ Г.")
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin._new124("ПОСЕЛКОВОЕ ПОСЕЛЕНИЕ", "ПОСЕЛОК", CityItemToken.ItemType.NOUN)
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("МІСЬКЕ ПОСЕЛЕННЯ", MorphLang.UA)
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("СЕЛЬСКОЕ ПОСЕЛЕНИЕ")
        t.tag = CityItemToken.ItemType.NOUN
        t.add_abridge("С.ПОС.")
        t.add_abridge("С.П.")
        t.add_variant("СЕЛЬСОВЕТ", False)
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("СІЛЬСЬКЕ ПОСЕЛЕННЯ", MorphLang.UA)
        t.add_abridge("С.ПОС.")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("СТАНИЦА")
        t.tag = CityItemToken.ItemType.NOUN
        t.add_abridge("СТ-ЦА")
        t.add_abridge("СТАН-ЦА")
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("СТАНИЦЯ", MorphLang.UA)
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin._new1116("СТОЛИЦА", "ГОРОД")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin._new1152("СТОЛИЦЯ", MorphLang.UA, "МІСТО")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("СТАНЦИЯ")
        t.add_abridge("СТАНЦ.")
        t.add_abridge("СТ.")
        t.add_abridge("СТАН.")
        t.tag = CityItemToken.ItemType.NOUN
        t.add_variant("ПЛАТФОРМА", False)
        t.add_abridge("ПЛАТФ.")
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("СТАНЦІЯ", MorphLang.UA)
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("ЖЕЛЕЗНОДОРОЖНАЯ СТАНЦИЯ")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("ЗАЛІЗНИЧНА СТАНЦІЯ", MorphLang.UA)
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("НАСЕЛЕННЫЙ ПУНКТ")
        t.tag = CityItemToken.ItemType.NOUN
        t.add_abridge("Н.П.")
        t.add_abridge("Б.Н.П.")
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("НАСЕЛЕНИЙ ПУНКТ", MorphLang.UA)
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin._new1116("РАЙОННЫЙ ЦЕНТР", "НАСЕЛЕННЫЙ ПУНКТ")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin._new1152("РАЙОННИЙ ЦЕНТР", MorphLang.UA, "НАСЕЛЕНИЙ ПУНКТ")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin._new1116("ГОРОДСКОЙ ОКРУГ", "НАСЕЛЕННЫЙ ПУНКТ")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin._new1152("МІСЬКИЙ ОКРУГ", MorphLang.UA, "НАСЕЛЕНИЙ ПУНКТ")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin._new1116("ОБЛАСТНОЙ ЦЕНТР", "НАСЕЛЕННЫЙ ПУНКТ")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin._new1152("ОБЛАСНИЙ ЦЕНТР", MorphLang.UA, "НАСЕЛЕНИЙ ПУНКТ")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("ХУТОР")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("АУЛ")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("ААЛ")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("АРБАН")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("ВЫСЕЛКИ")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("МЕСТЕЧКО")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("УРОЧИЩЕ")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("УСАДЬБА")
        t.tag = CityItemToken.ItemType.NOUN
        t.add_variant("ЦЕНТРАЛЬНАЯ УСАДЬБА", False)
        t.add_abridge("ЦЕНТР.УС.")
        t.add_abridge("ЦЕНТР.УСАДЬБА")
        t.add_abridge("Ц/У")
        t.add_abridge("УС-БА")
        t.add_abridge("ЦЕНТР.УС-БА")
        CityItemToken.M_ONTOLOGY.add(t)
        for s in ["ЖИТЕЛЬ", "МЭР"]: 
            CityItemToken.M_ONTOLOGY.add(Termin._new100(s, CityItemToken.ItemType.MISC))
        for s in ["ЖИТЕЛЬ", "МЕР"]: 
            CityItemToken.M_ONTOLOGY.add(Termin._new388(s, MorphLang.UA, CityItemToken.ItemType.MISC))
        t = Termin._new100("АДМИНИСТРАЦИЯ", CityItemToken.ItemType.MISC)
        t.add_abridge("АДМ.")
        CityItemToken.M_ONTOLOGY.add(t)
        CityItemToken.M_STD_ADJECTIVES = IntOntologyCollection()
        t = Termin("ВЕЛИКИЙ")
        t.add_abridge("ВЕЛ.")
        t.add_abridge("ВЕЛИК.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("БОЛЬШОЙ")
        t.add_abridge("БОЛ.")
        t.add_abridge("БОЛЬШ.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("МАЛЫЙ")
        t.add_abridge("МАЛ.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("ВЕРХНИЙ")
        t.add_abridge("ВЕР.")
        t.add_abridge("ВЕРХ.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("НИЖНИЙ")
        t.add_abridge("НИЖ.")
        t.add_abridge("НИЖН.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("СРЕДНИЙ")
        t.add_abridge("СРЕД.")
        t.add_abridge("СРЕДН.")
        t.add_abridge("СР.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("СТАРЫЙ")
        t.add_abridge("СТ.")
        t.add_abridge("СТАР.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("НОВЫЙ")
        t.add_abridge("НОВ.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("ВЕЛИКИЙ", MorphLang.UA)
        t.add_abridge("ВЕЛ.")
        t.add_abridge("ВЕЛИК.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("МАЛИЙ", MorphLang.UA)
        t.add_abridge("МАЛ.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("ВЕРХНІЙ", MorphLang.UA)
        t.add_abridge("ВЕР.")
        t.add_abridge("ВЕРХ.")
        t.add_abridge("ВЕРХН.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("НИЖНІЙ", MorphLang.UA)
        t.add_abridge("НИЖ.")
        t.add_abridge("НИЖН.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("СЕРЕДНІЙ", MorphLang.UA)
        t.add_abridge("СЕР.")
        t.add_abridge("СЕРЕД.")
        t.add_abridge("СЕРЕДН.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("СТАРИЙ", MorphLang.UA)
        t.add_abridge("СТ.")
        t.add_abridge("СТАР.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("НОВИЙ", MorphLang.UA)
        t.add_abridge("НОВ.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        CityItemToken.M_STD_ADJECTIVES.add(Termin("SAN"))
        CityItemToken.M_STD_ADJECTIVES.add(Termin("LOS"))
        dat = PullentiNerAddressInternalResourceHelper.get_bytes("c.dat")
        if (dat is None): 
            raise Utils.newException("Not found resource file c.dat in Analyzer.Location", None)
        with io.BytesIO(MiscLocationHelper._deflate(dat)) as tmp: 
            tmp.seek(0, io.SEEK_SET)
            xml0_ = None # new XmlDocument
            xml0_ = xml.etree.ElementTree.parse(tmp)
            for x in xml0_.getroot(): 
                if (x.tag == "bigcity"): 
                    CityItemToken.__load_big_city(x)
                elif (x.tag == "city"): 
                    CityItemToken.__load_city(x)
    
    @staticmethod
    def __load_city(xml0_ : xml.etree.ElementTree.Element) -> None:
        ci = IntOntologyItem(None)
        onto = CityItemToken.M_ONTOLOGY
        lang = MorphLang.RU
        if (Utils.getXmlAttrByName(xml0_.attrib, "l") is not None and Utils.getXmlAttrByName(xml0_.attrib, "l")[1] == "ua"): 
            lang = MorphLang.UA
        for x in xml0_: 
            if (x.tag == "n"): 
                v = Utils.getXmlInnerText(x)
                t = Termin()
                t.init_by_normal_text(v, lang)
                ci.termins.append(t)
                t.add_std_abridges()
                if (v.startswith("SAINT ")): 
                    t.add_abridge("ST. " + v[6:])
                elif (v.startswith("SAITNE ")): 
                    t.add_abridge("STE. " + v[7:])
        onto.add_item(ci)
    
    @staticmethod
    def __load_big_city(xml0_ : xml.etree.ElementTree.Element) -> None:
        ci = IntOntologyItem(None)
        ci.misc_attr = (ci)
        adj = None
        onto = CityItemToken.M_ONTOLOGY
        city_adj = CityItemToken.M_CITY_ADJECTIVES
        lang = MorphLang.RU
        if (Utils.getXmlAttrByName(xml0_.attrib, "l") is not None): 
            la = Utils.getXmlAttrByName(xml0_.attrib, "l")[1]
            if (la == "ua"): 
                lang = MorphLang.UA
            elif (la == "en"): 
                lang = MorphLang.EN
        for x in xml0_: 
            if (x.tag == "n"): 
                v = Utils.getXmlInnerText(x)
                if (Utils.isNullOrEmpty(v)): 
                    continue
                t = Termin()
                t.init_by_normal_text(v, lang)
                ci.termins.append(t)
                if (v == "САНКТ-ПЕТЕРБУРГ"): 
                    if (CityItemToken.M_ST_PETERBURG is None): 
                        CityItemToken.M_ST_PETERBURG = ci
                    t.acronym = "СПБ"
                    t.add_abridge("С.ПЕТЕРБУРГ")
                    t.add_abridge("СП-Б")
                    ci.termins.append(Termin("ПЕТЕРБУРГ", lang))
                elif (v.startswith("SAINT ")): 
                    t.add_abridge("ST. " + v[6:])
                elif (v.startswith("SAITNE ")): 
                    t.add_abridge("STE. " + v[7:])
            elif (x.tag == "a"): 
                adj = Utils.getXmlInnerText(x)
        onto.add_item(ci)
        if (not Utils.isNullOrEmpty(adj)): 
            at = Termin()
            at.init_by_normal_text(adj, lang)
            at.tag = (ci)
            city_adj.add(at)
            spb = adj == "САНКТ-ПЕТЕРБУРГСКИЙ" or adj == "САНКТ-ПЕТЕРБУРЗЬКИЙ"
            if (spb): 
                city_adj.add(Termin._new388(adj[6:], lang, ci))
    
    M_ONTOLOGY = None
    
    M_ST_PETERBURG = None
    
    M_CITY_ADJECTIVES = None
    
    M_STD_ADJECTIVES = None
    
    @staticmethod
    def _new1134(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType') -> 'CityItemToken':
        res = CityItemToken(_arg1, _arg2)
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new1136(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : bool) -> 'CityItemToken':
        res = CityItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.geo_object_before = _arg4
        return res
    
    @staticmethod
    def _new1137(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : bool, _arg5 : str) -> 'CityItemToken':
        res = CityItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.geo_object_before = _arg4
        res.value = _arg5
        return res
    
    @staticmethod
    def _new1138(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : str) -> 'CityItemToken':
        res = CityItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        return res
    
    @staticmethod
    def _new1142(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : 'IntOntologyItem', _arg5 : 'MorphCollection') -> 'CityItemToken':
        res = CityItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.onto_item = _arg4
        res.morph = _arg5
        return res
    
    @staticmethod
    def _new1144(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : 'MorphCollection') -> 'CityItemToken':
        res = CityItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.morph = _arg4
        return res
    
    @staticmethod
    def _new1145(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : 'IntOntologyItem', _arg5 : str) -> 'CityItemToken':
        res = CityItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.onto_item = _arg4
        res.value = _arg5
        return res
    
    @staticmethod
    def _new1146(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : str, _arg5 : bool) -> 'CityItemToken':
        res = CityItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        res.doubtful = _arg5
        return res
    
    @staticmethod
    def _new1147(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : str, _arg5 : 'MorphCollection') -> 'CityItemToken':
        res = CityItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        res.morph = _arg5
        return res
    
    @staticmethod
    def _new1148(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : str, _arg5 : bool, _arg6 : 'MorphCollection') -> 'CityItemToken':
        res = CityItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        res.doubtful = _arg5
        res.morph = _arg6
        return res
    
    @staticmethod
    def _new1149(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : str, _arg5 : str, _arg6 : bool, _arg7 : 'MorphCollection') -> 'CityItemToken':
        res = CityItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        res.alt_value = _arg5
        res.doubtful = _arg6
        res.morph = _arg7
        return res