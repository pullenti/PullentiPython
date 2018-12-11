# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import io
import typing
import math
import xml.etree
from enum import IntEnum
from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.NumberExType import NumberExType
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.Referent import Referent
from pullenti.ner.MetaToken import MetaToken
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.MorphCollection import MorphCollection
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.address.internal.EpNerAddressInternalResourceHelper import EpNerAddressInternalResourceHelper
from pullenti.ner.core.IntOntologyItem import IntOntologyItem
from pullenti.ner.date.DateReferent import DateReferent
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.address.internal.StreetItemType import StreetItemType
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.core.IntOntologyCollection import IntOntologyCollection
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.morph.MorphWordForm import MorphWordForm
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.NumberExToken import NumberExToken
from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
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
    
    def mergeWithNext(self, ne : 'CityItemToken') -> bool:
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
    def tryParseList(t : 'Token', loc : 'IntOntologyCollection', max_count : int) -> typing.List['CityItemToken']:
        ci = CityItemToken.tryParse(t, loc, False, None)
        if (ci is None): 
            if (t is None): 
                return None
            if (((isinstance(t, TextToken)) and t.isValue("МУНИЦИПАЛЬНЫЙ", None) and t.next0_ is not None) and t.next0_.isValue("ОБРАЗОВАНИЕ", None)): 
                t1 = t.next0_.next0_
                br = False
                if (BracketHelper.canBeStartOfSequence(t1, False, False)): 
                    br = True
                    t1 = t1.next0_
                lii = CityItemToken.tryParseList(t1, loc, max_count)
                if (lii is not None and lii[0].typ == CityItemToken.ItemType.NOUN): 
                    lii[0].begin_token = t
                    lii[0].doubtful = False
                    if (br and BracketHelper.canBeEndOfSequence(lii[len(lii) - 1].end_token.next0_, False, None, False)): 
                        lii[len(lii) - 1].end_token = lii[len(lii) - 1].end_token.next0_
                    return lii
            return None
        if (ci.chars.is_latin_letter and ci.typ == CityItemToken.ItemType.NOUN and not t.chars.is_all_lower): 
            return None
        li = list()
        li.append(ci)
        t = ci.end_token.next0_
        first_pass2905 = True
        while True:
            if first_pass2905: first_pass2905 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_newline_before): 
                if (len(li) == 1 and li[0].typ == CityItemToken.ItemType.NOUN): 
                    pass
                else: 
                    break
            ci0 = CityItemToken.tryParse(t, loc, False, ci)
            if (ci0 is None): 
                if (t.is_newline_before): 
                    break
                if (ci.typ == CityItemToken.ItemType.NOUN and BracketHelper.canBeStartOfSequence(t, False, False)): 
                    br = BracketHelper.tryParse(t, BracketParseAttr.NO, 100)
                    if ((br is not None and (br.length_char < 50) and t.next0_.chars.is_cyrillic_letter) and not t.next0_.chars.is_all_lower): 
                        ci0 = CityItemToken._new1121(br.begin_token, br.end_token, CityItemToken.ItemType.PROPERNAME)
                        tt = br.end_token.previous
                        num = None
                        if (isinstance(tt, NumberToken)): 
                            num = str((tt).value)
                            tt = tt.previous
                            if (tt is not None and tt.is_hiphen): 
                                tt = tt.previous
                        ci0.value = MiscHelper.getTextValue(br.begin_token.next0_, tt, GetTextAttr.NO)
                        if (tt != br.begin_token.next0_): 
                            ci0.alt_value = MiscHelper.getTextValue(br.begin_token.next0_, tt, GetTextAttr.NO)
                        if (Utils.isNullOrEmpty(ci0.value)): 
                            ci0 = (None)
                        elif (num is not None): 
                            ci0.value = "{0}-{1}".format(ci0.value, num)
                            if (ci0.alt_value is not None): 
                                ci0.alt_value = "{0}-{1}".format(ci0.alt_value, num)
                if ((ci0 is None and ((ci.typ == CityItemToken.ItemType.PROPERNAME or ci.typ == CityItemToken.ItemType.CITY)) and t.is_comma) and li[0] == ci): 
                    npt = NounPhraseHelper.tryParse(t.next0_, NounPhraseParseAttr.NO, 0)
                    if (npt is not None): 
                        tt = t.next0_
                        while tt is not None and tt.end_char <= npt.end_char: 
                            ci00 = CityItemToken.tryParse(tt, loc, False, ci)
                            if (ci00 is not None and ci00.typ == CityItemToken.ItemType.NOUN): 
                                ci01 = CityItemToken.tryParse(ci00.end_token.next0_, loc, False, ci)
                                if (ci01 is None): 
                                    ci0 = ci00
                                    ci0.alt_value = MiscHelper.getTextValue(t.next0_, ci00.end_token, (GetTextAttr.IGNOREARTICLES if t.kit.base_language.is_en else GetTextAttr.FIRSTNOUNGROUPTONOMINATIVESINGLE)).lower()
                                    break
                            if (not tt.chars.is_all_lower): 
                                break
                            tt = tt.next0_
                if (ci0 is None): 
                    break
            if ((ci0.typ == CityItemToken.ItemType.NOUN and ci0.value is not None and LanguageHelper.endsWith(ci0.value, "УСАДЬБА")) and ci.typ == CityItemToken.ItemType.NOUN): 
                ci.doubtful = False
                ci.end_token = ci0.end_token
                t = ci.end_token
                continue
            if (ci0.typ == CityItemToken.ItemType.NOUN and ci.typ == CityItemToken.ItemType.MISC and ci.value == "АДМИНИСТРАЦИЯ"): 
                ci0.doubtful = False
            if (ci.mergeWithNext(ci0)): 
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
            if (li[0].mergeWithNext(li[1])): 
                del li[1]
        if (len(li) > 2 and li[0].is_newline_after): 
            del li[1:1+len(li) - 1]
        if (not li[0].geo_object_before): 
            li[0].geo_object_before = MiscLocationHelper.checkGeoObjectBefore(li[0].begin_token)
        if (not li[len(li) - 1].geo_object_after): 
            li[len(li) - 1].geo_object_after = MiscLocationHelper.checkGeoObjectAfter(li[len(li) - 1].end_token)
        return li
    
    @staticmethod
    def __checkDoubtful(tt : 'TextToken') -> bool:
        if (tt is None): 
            return True
        if (tt.chars.is_all_lower): 
            return True
        if (tt.length_char < 3): 
            return True
        if (((tt.term == "СОЧИ" or tt.isValue("КИЕВ", None) or tt.isValue("ПСКОВ", None)) or tt.isValue("БОСТОН", None) or tt.isValue("РИГА", None)) or tt.isValue("АСТАНА", None) or tt.isValue("АЛМАТЫ", None)): 
            return False
        if ((isinstance(tt.next0_, TextToken)) and (tt.whitespaces_after_count < 2) and not tt.next0_.chars.is_all_lower): 
            if (tt.chars == tt.next0_.chars and not tt.chars.is_latin_letter and ((not tt.morph.case_.is_genitive and not tt.morph.case_.is_accusative))): 
                mc = tt.next0_.getMorphClassInDictionary()
                if (mc.is_proper_surname or mc.is_proper_secname): 
                    return True
        if ((isinstance(tt.previous, TextToken)) and (tt.whitespaces_before_count < 2) and not tt.previous.chars.is_all_lower): 
            mc = tt.previous.getMorphClassInDictionary()
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
                if (LanguageHelper.endsWithEx(val, "ОВ", "ЕВ", "ИН", None)): 
                    if (val != "БЕРЛИН"): 
                        if (tt.previous is not None and tt.previous.isValue("В", None)): 
                            pass
                        else: 
                            return True
        if (not ok): 
            return False
        t0 = tt.previous
        if (t0 is not None and ((t0.isChar(',') or t0.morph.class0_.is_conjunction))): 
            t0 = t0.previous
        if (t0 is not None and (isinstance(t0.getReferent(), GeoReferent))): 
            return False
        t1 = tt.next0_
        if (t1 is not None and ((t1.isChar(',') or t1.morph.class0_.is_conjunction))): 
            t1 = t1.next0_
        if (CityItemToken.M_RECURSIVE == 0): 
            CityItemToken.M_RECURSIVE += 1
            cit = CityItemToken.__TryParse(t1, None, False, None)
            CityItemToken.M_RECURSIVE -= 1
            if (cit is None): 
                return True
            if (cit.typ == CityItemToken.ItemType.NOUN or cit.typ == CityItemToken.ItemType.CITY): 
                return False
        return True
    
    M_RECURSIVE = 0
    
    @staticmethod
    def tryParse(t : 'Token', loc : 'IntOntologyCollection', can_be_low_char : bool=False, prev : 'CityItemToken'=None) -> 'CityItemToken':
        if (t is None): 
            return None
        if (t.kit.is_recurce_overflow): 
            return None
        t.kit.recurse_level += 1
        res = CityItemToken.__tryParseInt(t, loc, can_be_low_char, prev)
        t.kit.recurse_level -= 1
        if (res is not None and res.typ == CityItemToken.ItemType.NOUN and (res.whitespaces_after_count < 2)): 
            nn = NounPhraseHelper.tryParse(res.end_token.next0_, NounPhraseParseAttr.NO, 0)
            if (nn is not None and ((nn.end_token.isValue("ЗНАЧЕНИЕ", "ЗНАЧЕННЯ") or nn.end_token.isValue("ТИП", None) or nn.end_token.isValue("ХОЗЯЙСТВО", "ХАЗЯЙСТВО")))): 
                res.end_token = nn.end_token
        if ((res is not None and res.typ == CityItemToken.ItemType.PROPERNAME and res.value is not None) and res.begin_token == res.end_token and len(res.value) > 4): 
            if (res.value.endswith("ГРАД") or res.value.endswith("ГОРОД")): 
                res.alt_value = (None)
                res.typ = CityItemToken.ItemType.CITY
            elif (((res.value.endswith("СК") or res.value.endswith("ИНО") or res.value.endswith("ПОЛЬ")) or res.value.endswith("ВЛЬ") or res.value.endswith("АС")) or res.value.endswith("ЕС")): 
                sits = StreetItemToken.tryParseList(res.end_token.next0_, None, 3)
                if (sits is not None): 
                    if (len(sits) == 1 and sits[0].typ == StreetItemType.NOUN): 
                        return res
                    if (len(sits) == 2 and sits[0].typ == StreetItemType.NUMBER and sits[1].typ == StreetItemType.NOUN): 
                        return res
                mc = res.end_token.getMorphClassInDictionary()
                if (mc.is_proper_geo or mc.is_undefined): 
                    res.alt_value = (None)
                    res.typ = CityItemToken.ItemType.CITY
            elif (res.value.endswith("АНЬ") or res.value.endswith("TOWN") or res.value.startswith("SAN")): 
                res.typ = CityItemToken.ItemType.CITY
            elif (isinstance(res.end_token, TextToken)): 
                lem = (res.end_token).lemma
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
    def __tryParseInt(t : 'Token', loc : 'IntOntologyCollection', can_be_low_char : bool, prev : 'CityItemToken') -> 'CityItemToken':
        if (t is None): 
            return None
        res = CityItemToken.__TryParse(t, loc, can_be_low_char, prev)
        if ((prev is None and t.chars.is_cyrillic_letter and t.chars.is_all_upper) and t.length_char == 2): 
            if (t.isValue("ТА", None)): 
                res = CityItemToken.__TryParse(t.next0_, loc, can_be_low_char, prev)
                if (res is not None): 
                    if (res.typ == CityItemToken.ItemType.NOUN): 
                        res.begin_token = t
                        res.doubtful = False
                    else: 
                        res = (None)
        if ((prev is not None and prev.typ == CityItemToken.ItemType.NOUN and CityItemToken.M_RECURSIVE == 0) and ((prev.value != "ГОРОД" and prev.value != "МІСТО"))): 
            if (res is None or ((res.typ != CityItemToken.ItemType.NOUN and res.typ != CityItemToken.ItemType.MISC and res.typ != CityItemToken.ItemType.CITY))): 
                CityItemToken.M_RECURSIVE += 1
                det = AddressItemToken.tryAttachOrg(t)
                CityItemToken.M_RECURSIVE -= 1
                if (det is not None): 
                    cou = 0
                    ttt = det.begin_token
                    while ttt is not None and ttt.end_char <= det.end_char: 
                        if (ttt.chars.is_letter): 
                            cou += 1
                        ttt = ttt.next0_
                    if (cou < 6): 
                        re = CityItemToken._new1121(det.begin_token, det.end_token, CityItemToken.ItemType.PROPERNAME)
                        if (det.referent.type_name == "ORGANIZATION"): 
                            re.org_ref = det.ref_token
                        else: 
                            re.value = MiscHelper.getTextValueOfMetaToken(det, GetTextAttr.NO)
                            re.alt_value = MiscHelper.getTextValueOfMetaToken(det, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)
                        return re
        if (res is not None and res.typ == CityItemToken.ItemType.NOUN and (res.whitespaces_after_count < 3)): 
            npt = NounPhraseHelper.tryParse(res.end_token.next0_, NounPhraseParseAttr.NO, 0)
            if (npt is not None): 
                if (npt.end_token.isValue("ПОДЧИНЕНИЕ", "ПІДПОРЯДКУВАННЯ")): 
                    res.end_token = npt.end_token
        if ((res is not None and t.chars.is_all_upper and res.typ == CityItemToken.ItemType.PROPERNAME) and CityItemToken.M_RECURSIVE == 0): 
            tt = t.previous
            if (tt is not None and tt.is_comma): 
                tt = tt.previous
            geo_prev = None
            if (tt is not None and (isinstance(tt.getReferent(), GeoReferent))): 
                geo_prev = (Utils.asObjectOrNull(tt.getReferent(), GeoReferent))
            if (geo_prev is not None and ((geo_prev.is_region or geo_prev.is_city))): 
                CityItemToken.M_RECURSIVE += 1
                det = AddressItemToken.tryAttachOrg(t)
                CityItemToken.M_RECURSIVE -= 1
                if (det is not None): 
                    res = (None)
        if (res is not None and res.typ == CityItemToken.ItemType.PROPERNAME): 
            if ((t.isValue("ДУМА", "РАДА") or t.isValue("ГЛАВА", "ГОЛОВА") or t.isValue("АДМИНИСТРАЦИЯ", "АДМІНІСТРАЦІЯ")) or t.isValue("МЭР", "МЕР") or t.isValue("ПРЕДСЕДАТЕЛЬ", "ГОЛОВА")): 
                return None
        if (res is None): 
            if (BracketHelper.canBeStartOfSequence(t, True, False)): 
                br = BracketHelper.tryParse(t, BracketParseAttr.NO, 100)
                if (br is not None): 
                    res = CityItemToken.__TryParse(t.next0_, loc, False, None)
                    if (res is not None and ((res.typ == CityItemToken.ItemType.PROPERNAME or res.typ == CityItemToken.ItemType.CITY))): 
                        res.begin_token = t
                        res.typ = CityItemToken.ItemType.PROPERNAME
                        res.end_token = br.end_token
                        if (res.end_token.next0_ != br.end_token): 
                            res.value = MiscHelper.getTextValue(t, br.end_token, GetTextAttr.NO)
                            res.alt_value = (None)
                        return res
            if (isinstance(t, TextToken)): 
                txt = (t).term
                if (txt == "ИМ" or txt == "ИМЕНИ"): 
                    t1 = t.next0_
                    if (t1 is not None and t1.isChar('.')): 
                        t1 = t1.next0_
                    res = CityItemToken.__TryParse(t1, loc, can_be_low_char, None)
                    if (res is not None and ((((res.typ == CityItemToken.ItemType.CITY and res.doubtful)) or res.typ == CityItemToken.ItemType.PROPERNAME))): 
                        res.begin_token = t
                        res.morph = MorphCollection()
                        return res
                if (prev is not None and prev.typ == CityItemToken.ItemType.NOUN and ((not prev.doubtful or MiscLocationHelper.checkGeoObjectBefore(prev.begin_token)))): 
                    if (t.chars.is_cyrillic_letter and t.length_char == 1 and t.chars.is_all_upper): 
                        if ((t.next0_ is not None and not t.is_whitespace_after and ((t.next0_.is_hiphen or t.next0_.isChar('.')))) and (t.next0_.whitespaces_after_count < 2)): 
                            res1 = CityItemToken.__TryParse(t.next0_.next0_, loc, False, None)
                            if (res1 is not None and ((res1.typ == CityItemToken.ItemType.PROPERNAME or res1.typ == CityItemToken.ItemType.CITY))): 
                                adjs = MiscLocationHelper.getStdAdjFullStr(txt, res1.morph.gender, res1.morph.number, True)
                                if (adjs is None and prev is not None and prev.typ == CityItemToken.ItemType.NOUN): 
                                    adjs = MiscLocationHelper.getStdAdjFullStr(txt, prev.morph.gender, MorphNumber.UNDEFINED, True)
                                if (adjs is None): 
                                    adjs = MiscLocationHelper.getStdAdjFullStr(txt, res1.morph.gender, res1.morph.number, False)
                                if (adjs is not None): 
                                    if (res1.value is None): 
                                        res1.value = res1.getSourceText().upper()
                                    if (res1.alt_value is not None): 
                                        res1.alt_value = "{0} {1}".format(adjs[0], res1.alt_value)
                                    elif (len(adjs) > 1): 
                                        res1.alt_value = "{0} {1}".format(adjs[1], res1.value)
                                    res1.value = "{0} {1}".format(adjs[0], res1.value)
                                    res1.begin_token = t
                                    res1.typ = CityItemToken.ItemType.PROPERNAME
                                    return res1
            tt = (t.previous if prev is None else prev.begin_token.previous)
            while tt is not None and tt.isCharOf(",."):
                tt = tt.previous
            geo_prev = None
            if (tt is not None and (isinstance(tt.getReferent(), GeoReferent))): 
                geo_prev = (Utils.asObjectOrNull(tt.getReferent(), GeoReferent))
            tt0 = t
            ooo = False
            if (geo_prev is not None or MiscLocationHelper.checkNearBefore(t.previous) is not None): 
                ooo = True
            elif (MiscLocationHelper.checkGeoObjectBefore(t)): 
                ooo = True
            else: 
                tt = t.next0_
                if (tt is not None and tt.isChar('.')): 
                    tt = tt.next0_
                if ((isinstance(tt, TextToken)) and not tt.chars.is_all_lower): 
                    if (MiscLocationHelper.checkGeoObjectAfter(tt.next0_)): 
                        ooo = True
            if (ooo): 
                tt = t
                ttt = tt
                first_pass2906 = True
                while True:
                    if first_pass2906: first_pass2906 = False
                    else: ttt = ttt.next0_
                    if (not (ttt is not None)): break
                    if (ttt.isCharOf(",.")): 
                        tt = ttt.next0_
                        continue
                    if (ttt.is_newline_before): 
                        break
                    det = AddressItemToken.tryAttachDetail(ttt)
                    if (det is not None): 
                        ttt = det.end_token
                        tt = det.end_token.next0_
                        continue
                    det = AddressItemToken.tryAttachOrg(ttt)
                    if (det is not None): 
                        ttt = det.end_token
                        tt = det.end_token.next0_
                        tt0 = tt
                        continue
                    ait = AddressItemToken.tryParse(ttt, None, False, True, None)
                    if (ait is not None and ait.typ == AddressItemToken.ItemType.PLOT): 
                        ttt = ait.end_token
                        tt = ait.end_token.next0_
                        tt0 = tt
                        continue
                    break
                if (isinstance(tt, TextToken)): 
                    if (tt0.is_comma and tt0.next0_ is not None): 
                        tt0 = tt0.next0_
                    txt = (tt).term
                    if (tt.chars.is_all_lower and (((txt == "Д" or txt == "С" or txt == "C") or txt == "П" or txt == "Х"))): 
                        tt1 = tt
                        if (tt1.next0_ is not None and tt1.next0_.isChar('.')): 
                            tt1 = tt1.next0_
                        tt2 = tt1.next0_
                        if ((tt2 is not None and tt2.length_char == 1 and tt2.chars.is_cyrillic_letter) and tt2.chars.is_all_upper): 
                            if (tt2.next0_ is not None and ((tt2.next0_.isChar('.') or tt2.next0_.is_hiphen)) and not tt2.is_whitespace_after): 
                                tt2 = tt2.next0_.next0_
                        ok = False
                        if (txt == "Д" and (isinstance(tt2, NumberToken)) and not tt2.is_newline_before): 
                            ok = False
                        elif (((txt == "С" or txt == "C")) and (isinstance(tt2, TextToken)) and ((tt2.isValue("О", None) or tt2.isValue("O", None)))): 
                            ok = False
                        elif (tt2 is not None and tt2.chars.is_capital_upper and (tt2.whitespaces_before_count < 2)): 
                            ok = True
                        elif (prev is not None and prev.typ == CityItemToken.ItemType.PROPERNAME and (tt.whitespaces_before_count < 2)): 
                            if (MiscLocationHelper.checkGeoObjectBefore(prev.begin_token.previous)): 
                                ok = True
                            if (txt == "П" and tt.next0_ is not None and ((tt.next0_.is_hiphen or tt.next0_.isCharOf("\\/")))): 
                                sit = StreetItemToken.tryParse(tt, None, False, None, False)
                                if (sit is not None and sit.typ == StreetItemType.NOUN): 
                                    ok = False
                        if (ok): 
                            res = CityItemToken._new1123(tt0, tt1, CityItemToken.ItemType.NOUN, True)
                            res.value = ("ДЕРЕВНЯ" if txt == "Д" else (("ПОСЕЛОК" if txt == "П" else (("ХУТОР" if txt == "Х" else "СЕЛО")))))
                            if (txt == "П"): 
                                res.alt_value = "ПОСЕЛЕНИЕ"
                            elif (txt == "С" or txt == "C"): 
                                res.alt_value = "СЕЛЕНИЕ"
                                if (tt0 == tt1): 
                                    npt = NounPhraseHelper.tryParse(tt1.next0_, NounPhraseParseAttr.PARSEPRONOUNS, 0)
                                    if (npt is not None and npt.morph.case_.is_instrumental): 
                                        return None
                            res.doubtful = True
                            return res
                    if ((txt == "СП" or txt == "РП" or txt == "ГП") or txt == "ДП"): 
                        if (tt.next0_ is not None and tt.next0_.isChar('.')): 
                            tt = tt.next0_
                        if (tt.next0_ is not None and tt.next0_.chars.is_capital_upper): 
                            return CityItemToken._new1124(tt0, tt, CityItemToken.ItemType.NOUN, True, ("РАБОЧИЙ ПОСЕЛОК" if txt == "РП" else (("ГОРОДСКОЕ ПОСЕЛЕНИЕ" if txt == "ГП" else (("ДАЧНЫЙ ПОСЕЛОК" if txt == "ДП" else "СЕЛЬСКОЕ ПОСЕЛЕНИЕ"))))))
                    res = CityItemToken.__TryParse(tt, loc, can_be_low_char, None)
                    if (res is not None and res.typ == CityItemToken.ItemType.NOUN): 
                        res.geo_object_before = True
                        res.begin_token = tt0
                        return res
                    if (tt.chars.is_all_upper and tt.length_char > 2 and tt.chars.is_cyrillic_letter): 
                        return CityItemToken._new1125(tt, tt, CityItemToken.ItemType.PROPERNAME, (tt).term)
            if ((isinstance(t, NumberToken)) and t.next0_ is not None): 
                net = NumberExToken.tryParseNumberWithPostfix(t)
                if (net is not None and net.ex_typ == NumberExType.KILOMETER): 
                    return CityItemToken._new1125(t, net.end_token, CityItemToken.ItemType.PROPERNAME, "{0}КМ".format(math.floor(net.real_value)))
            rt = Utils.asObjectOrNull(t, ReferentToken)
            if ((rt is not None and (isinstance(rt.referent, GeoReferent)) and rt.begin_token == rt.end_token) and (rt.referent).is_state): 
                if (t.previous is None): 
                    return None
                if (t.previous.morph.number == MorphNumber.SINGULAR and t.morph.case_.is_nominative and not t.morph.case_.is_genitive): 
                    return CityItemToken._new1125(t, t, CityItemToken.ItemType.PROPERNAME, rt.getSourceText().upper())
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
            if (res.alt_value is None and res.begin_token.isValue("ПОСЕЛЕНИЕ", None)): 
                res.value = "ПОСЕЛЕНИЕ"
                res.alt_value = "ПОСЕЛОК"
            if (LanguageHelper.endsWith(res.value, "УСАДЬБА") and res.alt_value is None): 
                res.alt_value = "НАСЕЛЕННЫЙ ПУНКТ"
            if (res.value == "СТАНЦИЯ" or res.value == "СТАНЦІЯ"): 
                res.doubtful = True
            if (res.end_token.isValue("СТОЛИЦА", None) or res.end_token.isValue("СТОЛИЦЯ", None)): 
                res.doubtful = True
                if (res.end_token.next0_ is not None): 
                    geo_ = Utils.asObjectOrNull(res.end_token.next0_.getReferent(), GeoReferent)
                    if (geo_ is not None and ((geo_.is_region or geo_.is_state))): 
                        res.higher_geo = geo_
                        res.end_token = res.end_token.next0_
                        res.doubtful = False
                        res.value = "ГОРОД"
                        for it in TerrItemToken._m_capitals_by_state.termins: 
                            ge = Utils.asObjectOrNull(it.tag, GeoReferent)
                            if (ge is None or not ge.canBeEquals(geo_, Referent.EqualType.WITHINONETEXT)): 
                                continue
                            tok = TerrItemToken._m_capitals_by_state.tryParse(res.end_token.next0_, TerminParseAttr.NO)
                            if (tok is not None and tok.termin == it): 
                                break
                            res.typ = CityItemToken.ItemType.CITY
                            res.value = it.canonic_text
                            return res
            if ((res.begin_token.length_char == 1 and res.begin_token.chars.is_all_upper and res.begin_token.next0_ is not None) and res.begin_token.next0_.isChar('.')): 
                return None
        if (res.typ == CityItemToken.ItemType.PROPERNAME or res.typ == CityItemToken.ItemType.CITY): 
            val = Utils.ifNotNull(res.value, ((None if res.onto_item is None else res.onto_item.canonic_text)))
            t1 = res.end_token
            if (((not t1.is_whitespace_after and t1.next0_ is not None and t1.next0_.is_hiphen) and not t1.next0_.is_whitespace_after and (isinstance(t1.next0_.next0_, NumberToken))) and ((t1.next0_.next0_).value < (30))): 
                res.end_token = t1.next0_.next0_
                res.value = "{0}-{1}".format(val, (t1.next0_.next0_).value)
                if (res.alt_value is not None): 
                    res.alt_value = "{0}-{1}".format(res.alt_value, (t1.next0_.next0_).value)
                res.typ = CityItemToken.ItemType.PROPERNAME
            elif (t1.whitespaces_after_count == 1 and (isinstance(t1.next0_, NumberToken)) and t1.next0_.morph.class0_.is_adjective): 
                ok = False
                if (t1.next0_.next0_ is None or t1.next0_.is_newline_after): 
                    ok = True
                elif (not t1.next0_.is_whitespace_after and t1.next0_.next0_ is not None and t1.next0_.next0_.isCharOf(",")): 
                    ok = True
                if (ok): 
                    res.end_token = t1.next0_
                    res.value = "{0}-{1}".format(val, (t1.next0_).value)
                    res.typ = CityItemToken.ItemType.PROPERNAME
        if (res.typ == CityItemToken.ItemType.CITY and res.begin_token == res.end_token): 
            if (res.begin_token.getMorphClassInDictionary().is_adjective and res.end_token.next0_ is not None): 
                ok = False
                t1 = None
                npt = NounPhraseHelper.tryParse(res.begin_token, NounPhraseParseAttr.NO, 0)
                if (npt is not None and npt.end_token == res.end_token.next0_): 
                    t1 = npt.end_token
                    if (res.end_token.next0_.chars == res.begin_token.chars): 
                        ok = True
                    elif (res.end_token.next0_.chars.is_all_lower): 
                        ttt = res.end_token.next0_.next0_
                        if (ttt is None or ttt.isCharOf(",.")): 
                            ok = True
                elif (res.end_token.next0_.chars == res.begin_token.chars and res.begin_token.chars.is_capital_upper): 
                    ttt = res.end_token.next0_.next0_
                    if (ttt is None or ttt.isCharOf(",.")): 
                        ok = True
                    t1 = res.end_token.next0_
                    npt = (None)
                if (ok and t1 is not None): 
                    res.typ = CityItemToken.ItemType.PROPERNAME
                    res.onto_item = (None)
                    res.end_token = t1
                    if (npt is not None): 
                        res.value = npt.getNormalCaseText(None, False, MorphGender.UNDEFINED, False)
                        res.morph = npt.morph
                    else: 
                        res.value = MiscHelper.getTextValue(res.begin_token, res.end_token, GetTextAttr.NO)
            if ((res.end_token.next0_ is not None and res.end_token.next0_.is_hiphen and not res.end_token.next0_.is_whitespace_after) and not res.end_token.next0_.is_whitespace_before): 
                res1 = CityItemToken.__TryParse(res.end_token.next0_.next0_, loc, False, None)
                if ((res1 is not None and res1.typ == CityItemToken.ItemType.PROPERNAME and res1.begin_token == res1.end_token) and res1.begin_token.chars == res.begin_token.chars): 
                    if (res1.onto_item is None and res.onto_item is None): 
                        res.typ = CityItemToken.ItemType.PROPERNAME
                        res.value = "{0}-{1}".format((res.value if res.onto_item is None else res.onto_item.canonic_text), res1.value)
                        if (res.alt_value is not None): 
                            res.alt_value = "{0}-{1}".format(res.alt_value, res1.value)
                        res.onto_item = (None)
                        res.end_token = res1.end_token
                        res.doubtful = False
                elif ((isinstance(res.end_token.next0_.next0_, NumberToken)) and ((res.end_token.next0_.next0_).value < (30))): 
                    res.typ = CityItemToken.ItemType.PROPERNAME
                    res.value = "{0}-{1}".format((res.value if res.onto_item is None else res.onto_item.canonic_text), (res.end_token.next0_.next0_).value)
                    if (res.alt_value is not None): 
                        res.alt_value = "{0}-{1}".format(res.alt_value, (res.end_token.next0_.next0_).value)
                    res.onto_item = (None)
                    res.end_token = res.end_token.next0_.next0_
            elif (res.begin_token.getMorphClassInDictionary().is_proper_name): 
                if (res.begin_token.isValue("КИЇВ", None) or res.begin_token.isValue("АСТАНА", None) or res.begin_token.isValue("АЛМАТЫ", None)): 
                    pass
                else: 
                    res.doubtful = True
                    tt = res.begin_token.previous
                    if (tt is not None and tt.previous is not None): 
                        if (tt.isChar(',') or tt.morph.class0_.is_conjunction): 
                            geo_ = Utils.asObjectOrNull(tt.previous.getReferent(), GeoReferent)
                            if (geo_ is not None and geo_.is_city): 
                                res.doubtful = False
                    if (tt is not None and tt.isValue("В", None) and tt.chars.is_all_lower): 
                        npt1 = NounPhraseHelper.tryParse(res.begin_token, NounPhraseParseAttr.NO, 0)
                        if (npt1 is None or npt1.end_char <= res.end_char): 
                            res.doubtful = False
            if ((res.begin_token == res.end_token and res.typ == CityItemToken.ItemType.CITY and res.onto_item is not None) and res.onto_item.canonic_text == "САНКТ - ПЕТЕРБУРГ"): 
                tt = res.begin_token.previous
                first_pass2907 = True
                while True:
                    if first_pass2907: first_pass2907 = False
                    else: tt = tt.previous
                    if (not (tt is not None)): break
                    if (tt.is_hiphen or tt.isChar('.')): 
                        continue
                    if (tt.isValue("С", None) or tt.isValue("C", None) or tt.isValue("САНКТ", None)): 
                        res.begin_token = tt
                    break
        if ((res.begin_token == res.end_token and res.typ == CityItemToken.ItemType.PROPERNAME and res.whitespaces_after_count == 1) and (isinstance(res.end_token.next0_, TextToken)) and res.end_token.chars == res.end_token.next0_.chars): 
            ok = False
            t1 = res.end_token
            if (t1.next0_.next0_ is None or t1.next0_.is_newline_after): 
                ok = True
            elif (not t1.next0_.is_whitespace_after and t1.next0_.next0_ is not None and t1.next0_.next0_.isCharOf(",.")): 
                ok = True
            if (ok): 
                pp = CityItemToken.__TryParse(t1.next0_, loc, False, None)
                if (pp is not None and pp.typ == CityItemToken.ItemType.NOUN): 
                    ok = False
                if (ok): 
                    te = TerrItemToken.tryParse(t1.next0_, None, False, False)
                    if (te is not None and te.termin_item is not None): 
                        ok = False
            if (ok): 
                res.end_token = t1.next0_
                res.value = MiscHelper.getTextValue(res.begin_token, res.end_token, GetTextAttr.NO)
                res.alt_value = (None)
                res.typ = CityItemToken.ItemType.PROPERNAME
        return res
    
    @staticmethod
    def __TryParse(t : 'Token', loc : 'IntOntologyCollection', can_be_low_char : bool=False, prev : 'CityItemToken'=None) -> 'CityItemToken':
        if (not ((isinstance(t, TextToken)))): 
            if ((isinstance(t, ReferentToken)) and (isinstance(t.getReferent(), DateReferent))): 
                aii = StreetItemToken._tryParseSpec(t, None)
                if (aii is not None): 
                    if (len(aii) > 1 and aii[0].typ == StreetItemType.NUMBER and aii[1].typ == StreetItemType.STDNAME): 
                        res2 = CityItemToken._new1121(t, aii[1].end_token, CityItemToken.ItemType.PROPERNAME)
                        res2.value = "{0} {1}".format((aii[0].value if aii[0].number is None else str(aii[0].number.value)), aii[1].value)
                        return res2
            return None
        li = list()
        li0 = None
        is_in_loc_onto = False
        if (loc is not None): 
            li0 = loc.tryAttach(t, None, False)
            if ((li0) is not None): 
                li.extend(li0)
                is_in_loc_onto = True
        if (t.kit.ontology is not None and len(li) == 0): 
            li0 = t.kit.ontology.attachToken(GeoReferent.OBJ_TYPENAME, t)
            if ((li0) is not None): 
                li.extend(li0)
                is_in_loc_onto = True
        if (len(li) == 0): 
            li0 = CityItemToken.M_ONTOLOGY.tryAttach(t, None, False)
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
                        if (can_be_low_char or not MiscHelper.isAllCharactersLower(nt.begin_token, nt.end_token, False)): 
                            ci = CityItemToken._new1129(nt.begin_token, nt.end_token, CityItemToken.ItemType.CITY, nt.item, nt.morph)
                            if (nt.begin_token == nt.end_token and not is_in_loc_onto): 
                                ci.doubtful = CityItemToken.__checkDoubtful(Utils.asObjectOrNull(nt.begin_token, TextToken))
                            tt1 = nt.end_token.next0_
                            if ((((tt1 is not None and tt1.is_hiphen and not tt1.is_whitespace_before) and not tt1.is_whitespace_after and prev is not None) and prev.typ == CityItemToken.ItemType.NOUN and (isinstance(tt1.next0_, TextToken))) and tt1.previous.chars == tt1.next0_.chars): 
                                li = (None)
                                break
                            return ci
                if (li is not None): 
                    for nt in li: 
                        if (nt.item is not None): 
                            if (can_be_low_char or not MiscHelper.isAllCharactersLower(nt.begin_token, nt.end_token, False)): 
                                ci = CityItemToken._new1129(nt.begin_token, nt.end_token, CityItemToken.ItemType.CITY, nt.item, nt.morph)
                                if (nt.begin_token == nt.end_token and (isinstance(nt.begin_token, TextToken))): 
                                    ci.doubtful = CityItemToken.__checkDoubtful(Utils.asObjectOrNull(nt.begin_token, TextToken))
                                    str0_ = (nt.begin_token).term
                                    if (str0_ != nt.item.canonic_text): 
                                        if (LanguageHelper.endsWithEx(str0_, "О", "А", None, None)): 
                                            ci.alt_value = str0_
                                return ci
            if (li is not None): 
                for nt in li: 
                    if (nt.item is None): 
                        ty = (CityItemToken.ItemType.NOUN if nt.termin.tag is None else Utils.valToEnum(nt.termin.tag, CityItemToken.ItemType))
                        ci = CityItemToken._new1131(nt.begin_token, nt.end_token, ty, nt.morph)
                        ci.value = nt.termin.canonic_text
                        if (ty == CityItemToken.ItemType.MISC and ci.value == "ЖИТЕЛЬ" and t.previous is not None): 
                            if (t.previous.isValue("МЕСТНЫЙ", "МІСЦЕВИЙ")): 
                                return None
                            if (t.previous.morph.class0_.is_pronoun): 
                                return None
                        if (ty == CityItemToken.ItemType.NOUN and not t.chars.is_all_lower): 
                            if (t.morph.class0_.is_proper_surname): 
                                ci.doubtful = True
                        if (nt.begin_token.kit.base_language.is_ua): 
                            if (nt.begin_token.isValue("М", None)): 
                                if (not nt.begin_token.chars.is_all_lower): 
                                    return None
                                ci.doubtful = True
                            elif (nt.begin_token.isValue("МІС", None)): 
                                if ((t).term != "МІС"): 
                                    return None
                                ci.doubtful = True
                        if (nt.begin_token.kit.base_language.is_ru): 
                            if (nt.begin_token.isValue("Г", None)): 
                                if (not nt.begin_token.chars.is_all_lower): 
                                    return None
                                if ((nt.end_token == nt.begin_token and nt.end_token.next0_ is not None and not nt.end_token.is_whitespace_after) and ((nt.end_token.next0_.isCharOf("\\/") or nt.end_token.next0_.is_hiphen))): 
                                    return None
                                if (not t.is_whitespace_before and t.previous is not None): 
                                    if (t.previous.isCharOf("\\/") or t.previous.is_hiphen): 
                                        return None
                                ci.doubtful = True
                            elif (nt.begin_token.isValue("ГОР", None)): 
                                if ((t).term != "ГОР"): 
                                    if (t.chars.is_capital_upper): 
                                        ci = (None)
                                        break
                                    return None
                                ci.doubtful = True
                            elif (nt.begin_token.isValue("ПОС", None)): 
                                if ((t).term != "ПОС"): 
                                    return None
                                ci.doubtful = True
                        npt1 = NounPhraseHelper.tryParse(t.previous, NounPhraseParseAttr.NO, 0)
                        if (npt1 is not None and len(npt1.adjectives) > 0): 
                            s = npt1.adjectives[0].getNormalCaseText(None, False, MorphGender.UNDEFINED, False)
                            if ((s == "РОДНОЙ" or s == "ЛЮБИМЫЙ" or s == "РІДНИЙ") or s == "КОХАНИЙ"): 
                                return None
                        return ci
        if (not ((isinstance(t, TextToken)))): 
            return None
        if ((t).term == "СПБ" and not t.chars.is_all_lower and CityItemToken.M_ST_PETERBURG is not None): 
            return CityItemToken._new1132(t, t, CityItemToken.ItemType.CITY, CityItemToken.M_ST_PETERBURG, CityItemToken.M_ST_PETERBURG.canonic_text)
        if (t.chars.is_all_lower): 
            return None
        stds = CityItemToken.M_STD_ADJECTIVES.tryAttach(t, None, False)
        if (stds is not None): 
            cit = CityItemToken.__TryParse(stds[0].end_token.next0_, loc, False, None)
            if (cit is not None and ((((cit.typ == CityItemToken.ItemType.PROPERNAME and cit.value is not None)) or cit.typ == CityItemToken.ItemType.CITY))): 
                adj = stds[0].termin.canonic_text
                cit.value = "{0} {1}".format(adj, Utils.ifNotNull(cit.value, (cit.onto_item.canonic_text if cit is not None and cit.onto_item is not None else None)))
                if (cit.alt_value is not None): 
                    cit.alt_value = "{0} {1}".format(adj, cit.alt_value)
                cit.begin_token = t
                npt0 = NounPhraseHelper.tryParse(t, NounPhraseParseAttr.NO, 0)
                if (npt0 is not None and npt0.end_token == cit.end_token): 
                    cit.morph = npt0.morph
                    cit.value = npt0.getNormalCaseText(None, False, MorphGender.UNDEFINED, False)
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
            if (not ((isinstance(tt, TextToken)))): 
                break
            if (not tt.chars.is_letter or ((tt.chars.is_cyrillic_letter != t.chars.is_cyrillic_letter and not tt.isValue("НА", None)))): 
                break
            if (tt != t): 
                si = StreetItemToken.tryParse(tt, None, False, None, False)
                if (si is not None and si.typ == StreetItemType.NOUN): 
                    if (si.end_token.next0_ is None or si.end_token.next0_.isCharOf(",.")): 
                        pass
                    else: 
                        break
                if (tt.length_char < 2): 
                    break
                if ((tt.length_char < 3) and not tt.isValue("НА", None)): 
                    if (tt.is_whitespace_before): 
                        break
            if (name.tell() > 0): 
                print('-', end="", file=name)
                if (altname is not None): 
                    print('-', end="", file=altname)
            if ((isinstance(tt, TextToken)) and ((is_prep or ((k > 0 and not tt.getMorphClassInDictionary().is_proper_geo))))): 
                print((tt).term, end="", file=name)
                if (altname is not None): 
                    print((tt).term, end="", file=altname)
            else: 
                ss = CityItemToken.__getNormalGeo(tt)
                if (ss != (tt).term): 
                    if (altname is None): 
                        altname = io.StringIO()
                    print(Utils.toStringStringIO(name), end="", file=altname)
                    print((tt).term, end="", file=altname)
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
            reee = CityItemToken._new1133(t, t1, CityItemToken.ItemType.PROPERNAME, Utils.toStringStringIO(name), doubt)
            if (altname is not None): 
                reee.alt_value = Utils.toStringStringIO(altname)
            return reee
        if (t is None): 
            return None
        npt = (None if t.chars.is_latin_letter else NounPhraseHelper.tryParse(t, NounPhraseParseAttr.NO, 0))
        if ((npt is not None and npt.end_token != t and len(npt.adjectives) > 0) and not npt.adjectives[0].end_token.next0_.is_comma): 
            cit = CityItemToken.__TryParse(t.next0_, loc, False, None)
            if (cit is not None and cit.typ == CityItemToken.ItemType.NOUN and ((LanguageHelper.endsWithEx(cit.value, "ПУНКТ", "ПОСЕЛЕНИЕ", "ПОСЕЛЕННЯ", "ПОСЕЛОК") or t.next0_.isValue("ГОРОДОК", None)))): 
                return CityItemToken._new1134(t, t, CityItemToken.ItemType.CITY, t.getNormalCaseText(None, False, MorphGender.UNDEFINED, False), npt.morph)
            else: 
                if (npt.end_token.chars != t.chars): 
                    if (npt.end_token.chars.is_all_lower and ((npt.end_token.next0_ is None or npt.end_token.next0_.is_comma))): 
                        pass
                    else: 
                        return None
                if (len(npt.adjectives) != 1): 
                    return None
                npt1 = NounPhraseHelper.tryParse(npt.end_token, NounPhraseParseAttr.NO, 0)
                if (npt1 is None or len(npt1.adjectives) == 0): 
                    si = StreetItemToken.tryParse(npt.end_token, None, False, None, False)
                    if (si is None or si.typ != StreetItemType.NOUN): 
                        t1 = npt.end_token
                        doubt = CityItemToken.__checkDoubtful(Utils.asObjectOrNull(t1, TextToken))
                        return CityItemToken._new1135(t, t1, CityItemToken.ItemType.PROPERNAME, npt.getNormalCaseText(None, False, MorphGender.UNDEFINED, False), doubt, npt.morph)
        if (t.next0_ is not None and t.next0_.chars == t.chars and not t.is_newline_after): 
            ok = False
            if (t.next0_.next0_ is None or t.next0_.next0_.chars != t.chars): 
                ok = True
            elif (isinstance(t.next0_.next0_.getReferent(), GeoReferent)): 
                ok = True
            elif (CityItemToken.M_RECURSIVE == 0): 
                CityItemToken.M_RECURSIVE += 1
                tis = TerrItemToken.tryParseList(t.next0_.next0_, loc, 2)
                CityItemToken.M_RECURSIVE -= 1
                if (tis is not None and len(tis) > 1): 
                    if (tis[0].is_adjective and tis[1].termin_item is not None): 
                        ok = True
            if (ok and (isinstance(t.next0_, TextToken))): 
                doubt = CityItemToken.__checkDoubtful(Utils.asObjectOrNull(t.next0_, TextToken))
                stat = t.kit.statistics.getBigrammInfo(t, t.next0_)
                ok1 = False
                if ((stat is not None and stat.pair_count >= 2 and stat.pair_count == stat.second_count) and not stat.second_has_other_first): 
                    if (stat.pair_count > 2): 
                        doubt = False
                    ok1 = True
                elif (CityItemToken.M_STD_ADJECTIVES.tryAttach(t, None, False) is not None and (isinstance(t.next0_, TextToken))): 
                    ok1 = True
                elif (((t.next0_.next0_ is None or t.next0_.next0_.is_comma)) and t.morph.class0_.is_noun and ((t.next0_.morph.class0_.is_adjective or t.next0_.morph.class0_.is_noun))): 
                    ok1 = True
                if (ok1): 
                    tne = CityItemToken.__tryParseInt(t.next0_, loc, False, None)
                    if (tne is not None and tne.typ == CityItemToken.ItemType.NOUN): 
                        pass
                    else: 
                        print(" {0}".format((t.next0_).term), end="", file=name, flush=True)
                        if (altname is not None): 
                            print(" {0}".format((t.next0_).term), end="", file=altname, flush=True)
                        t1 = t.next0_
                        return CityItemToken._new1136(t, t1, CityItemToken.ItemType.PROPERNAME, Utils.toStringStringIO(name), (None if altname is None else Utils.toStringStringIO(altname)), doubt, t.next0_.morph)
        if (t.length_char < 2): 
            return None
        t1 = t
        doubt = CityItemToken.__checkDoubtful(Utils.asObjectOrNull(t, TextToken))
        if (((t.next0_ is not None and prev is not None and prev.typ == CityItemToken.ItemType.NOUN) and t.next0_.chars.is_cyrillic_letter and t.next0_.chars.is_all_lower) and t.whitespaces_after_count == 1): 
            tt = t.next0_
            ok = False
            if (tt.next0_ is None or tt.next0_.isCharOf(",;")): 
                ok = True
            if (ok and AddressItemToken.tryParse(tt.next0_, None, False, False, None) is None): 
                t1 = tt
                print(" {0}".format(t1.getSourceText().upper()), end="", file=name, flush=True)
        if (MiscHelper.isEngArticle(t)): 
            return None
        res = CityItemToken._new1136(t, t1, CityItemToken.ItemType.PROPERNAME, Utils.toStringStringIO(name), (None if altname is None else Utils.toStringStringIO(altname)), doubt, t.morph)
        if (t1 == t and (isinstance(t1, TextToken)) and (t1).term0 is not None): 
            res.alt_value = (t1).term0
        sog = False
        glas = False
        for ch in res.value: 
            if (LanguageHelper.isCyrillicVowel(ch) or LanguageHelper.isLatinVowel(ch)): 
                glas = True
            else: 
                sog = True
        if (not glas or not sog): 
            return None
        if (t == t1 and (isinstance(t, TextToken))): 
            if ((t).term != res.value): 
                res.alt_value = (t).term
        return res
    
    @staticmethod
    def tryParseBack(t : 'Token') -> 'CityItemToken':
        while t is not None and ((t.isCharOf("(,") or t.is_and)):
            t = t.previous
        if (not ((isinstance(t, TextToken)))): 
            return None
        cou = 0
        tt = t
        first_pass2908 = True
        while True:
            if first_pass2908: first_pass2908 = False
            else: tt = tt.previous
            if (not (tt is not None)): break
            if (not ((isinstance(tt, TextToken)))): 
                return None
            if (not tt.chars.is_letter): 
                continue
            res = CityItemToken.tryParse(tt, None, True, None)
            if (res is not None and res.end_token == t): 
                return res
            cou += 1
            if ((cou) > 2): 
                break
        return None
    
    @staticmethod
    def __getNormalGeo(t : 'Token') -> str:
        tt = Utils.asObjectOrNull(t, TextToken)
        if (tt is None): 
            return None
        if (tt.term[len(tt.term) - 1] == 'О'): 
            return tt.term
        if (tt.term[len(tt.term) - 1] == 'Ы'): 
            return tt.term
        for wf in tt.morph.items: 
            if (wf.class0_.is_proper_geo and (wf).is_in_dictionary): 
                return (wf).normal_case
        geo_eq_term = False
        for wf in tt.morph.items: 
            if (wf.class0_.is_proper_geo): 
                ggg = (wf).normal_case
                if (ggg == tt.term): 
                    geo_eq_term = True
                elif (not wf.case_.is_nominative): 
                    return ggg
        if (geo_eq_term): 
            return tt.term
        if (tt.morph.items_count > 0): 
            return (tt.morph.getIndexerItem(0)).normal_case
        else: 
            return tt.term
    
    @staticmethod
    def initialize() -> None:
        if (CityItemToken.M_ONTOLOGY is not None): 
            return
        CityItemToken.M_ONTOLOGY = IntOntologyCollection()
        CityItemToken.M_CITY_ADJECTIVES = TerminCollection()
        t = Termin("ГОРОД")
        t.addAbridge("ГОР.")
        t.addAbridge("Г.")
        t.tag = CityItemToken.ItemType.NOUN
        t.addVariant("ГОРОДОК", False)
        t.addVariant("ШАХТЕРСКИЙ ГОРОДОК", False)
        t.addVariant("ПРИМОРСКИЙ ГОРОДОК", False)
        t.addVariant("МАЛЕНЬКИЙ ГОРОДОК", False)
        t.addVariant("НЕБОЛЬШОЙ ГОРОДОК", False)
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("CITY")
        t.tag = CityItemToken.ItemType.NOUN
        t.addVariant("TOWN", False)
        t.addVariant("CAPITAL", False)
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("МІСТО", MorphLang.UA)
        t.addAbridge("МІС.")
        t.addAbridge("М.")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin._new1104("ГОРОД-ГЕРОЙ", "ГОРОД")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin._new1139("МІСТО-ГЕРОЙ", MorphLang.UA, "МІСТО")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin._new1104("ГОРОД-КУРОРТ", "ГОРОД")
        t.addAbridge("Г.К.")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin._new1139("МІСТО-КУРОРТ", MorphLang.UA, "МІСТО")
        t.addAbridge("М.К.")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("СЕЛО")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("ДЕРЕВНЯ")
        t.addAbridge("ДЕР.")
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
        t.addAbridge("ПОС.")
        t.tag = CityItemToken.ItemType.NOUN
        t.addVariant("ПОСЕЛЕНИЕ", False)
        t.addVariant("ЖИЛОЙ ПОСЕЛОК", False)
        t.addVariant("КОТТЕДЖНЫЙ ПОСЕЛОК", False)
        t.addVariant("ВАХТОВЫЙ ПОСЕЛОК", False)
        t.addVariant("ШАХТЕРСКИЙ ПОСЕЛОК", False)
        t.addVariant("ДАЧНЫЙ ПОСЕЛОК", False)
        t.addVariant("КУРОРТНЫЙ ПОСЕЛОК", False)
        t.addVariant("ПОСЕЛОК СОВХОЗА", False)
        t.addVariant("ПОСЕЛОК КОЛХОЗА", False)
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("СЕЛИЩЕ", MorphLang.UA)
        t.addAbridge("СЕЛ.")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("ПОСЕЛОК ГОРОДСКОГО ТИПА")
        t.acronym_smart = "ПГТ"
        t.acronym = t.acronym_smart
        t.addAbridge("ПГТ.")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("СЕЛИЩЕ МІСЬКОГО ТИПУ", MorphLang.UA)
        t.acronym_smart = "СМТ"
        t.acronym = t.acronym_smart
        t.addAbridge("СМТ.")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("РАБОЧИЙ ПОСЕЛОК")
        t.addAbridge("Р.П.")
        t.tag = CityItemToken.ItemType.NOUN
        t.addAbridge("РАБ.П.")
        t.addAbridge("Р.ПОС.")
        t.addAbridge("РАБ.ПОС.")
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("РОБОЧЕ СЕЛИЩЕ", MorphLang.UA)
        t.addAbridge("Р.С.")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("ДАЧНЫЙ ПОСЕЛОК")
        t.addAbridge("Д.П.")
        t.tag = CityItemToken.ItemType.NOUN
        t.addAbridge("ДАЧ.П.")
        t.addAbridge("Д.ПОС.")
        t.addAbridge("ДАЧ.ПОС.")
        t.addVariant("ЖИЛИЩНО ДАЧНЫЙ ПОСЕЛОК", False)
        t.addVariant("ДАЧНОЕ ПОСЕЛЕНИЕ", False)
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("ДАЧНЕ СЕЛИЩЕ", MorphLang.UA)
        t.addAbridge("Д.С.")
        t.tag = CityItemToken.ItemType.NOUN
        t.addAbridge("ДАЧ.С.")
        t.addAbridge("Д.СЕЛ.")
        t.addAbridge("ДАЧ.СЕЛ.")
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("ГОРОДСКОЕ ПОСЕЛЕНИЕ")
        t.addAbridge("Г.П.")
        t.tag = CityItemToken.ItemType.NOUN
        t.addAbridge("Г.ПОС.")
        t.addAbridge("ГОР.П.")
        t.addAbridge("ГОР.ПОС.")
        t.addVariant("ГОРОДСКОЙ ОКРУГ", False)
        t.addAbridge("ГОР. ОКРУГ")
        t.addAbridge("Г.О.")
        t.addAbridge("Г.О.Г.")
        t.addAbridge("ГОРОДСКОЙ ОКРУГ Г.")
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin._new142("ПОСЕЛКОВОЕ ПОСЕЛЕНИЕ", "ПОСЕЛОК", CityItemToken.ItemType.NOUN)
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("МІСЬКЕ ПОСЕЛЕННЯ", MorphLang.UA)
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("СЕЛЬСКОЕ ПОСЕЛЕНИЕ")
        t.tag = CityItemToken.ItemType.NOUN
        t.addAbridge("С.ПОС.")
        t.addAbridge("С.П.")
        t.addVariant("СЕЛЬСОВЕТ", False)
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("СІЛЬСЬКЕ ПОСЕЛЕННЯ", MorphLang.UA)
        t.addAbridge("С.ПОС.")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("СТАНИЦА")
        t.tag = CityItemToken.ItemType.NOUN
        t.addAbridge("СТ-ЦА")
        t.addAbridge("СТАН-ЦА")
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("СТАНИЦЯ", MorphLang.UA)
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin._new1104("СТОЛИЦА", "ГОРОД")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin._new1139("СТОЛИЦЯ", MorphLang.UA, "МІСТО")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("СТАНЦИЯ")
        t.addAbridge("СТАНЦ.")
        t.addAbridge("СТ.")
        t.addAbridge("СТАН.")
        t.tag = CityItemToken.ItemType.NOUN
        t.addVariant("ПЛАТФОРМА", False)
        t.addAbridge("ПЛАТФ.")
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
        t.addAbridge("Н.П.")
        t.addAbridge("Б.Н.П.")
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin("НАСЕЛЕНИЙ ПУНКТ", MorphLang.UA)
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin._new1104("РАЙОННЫЙ ЦЕНТР", "НАСЕЛЕННЫЙ ПУНКТ")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin._new1139("РАЙОННИЙ ЦЕНТР", MorphLang.UA, "НАСЕЛЕНИЙ ПУНКТ")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin._new1104("ГОРОДСКОЙ ОКРУГ", "НАСЕЛЕННЫЙ ПУНКТ")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin._new1139("МІСЬКИЙ ОКРУГ", MorphLang.UA, "НАСЕЛЕНИЙ ПУНКТ")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin._new1104("ОБЛАСТНОЙ ЦЕНТР", "НАСЕЛЕННЫЙ ПУНКТ")
        t.tag = CityItemToken.ItemType.NOUN
        CityItemToken.M_ONTOLOGY.add(t)
        t = Termin._new1139("ОБЛАСНИЙ ЦЕНТР", MorphLang.UA, "НАСЕЛЕНИЙ ПУНКТ")
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
        t.addVariant("ЦЕНТРАЛЬНАЯ УСАДЬБА", False)
        t.addAbridge("ЦЕНТР.УС.")
        t.addAbridge("ЦЕНТР.УСАДЬБА")
        t.addAbridge("Ц/У")
        t.addAbridge("УС-БА")
        t.addAbridge("ЦЕНТР.УС-БА")
        CityItemToken.M_ONTOLOGY.add(t)
        for s in ["ЖИТЕЛЬ", "МЭР"]: 
            CityItemToken.M_ONTOLOGY.add(Termin._new118(s, CityItemToken.ItemType.MISC))
        for s in ["ЖИТЕЛЬ", "МЕР"]: 
            CityItemToken.M_ONTOLOGY.add(Termin._new477(s, MorphLang.UA, CityItemToken.ItemType.MISC))
        t = Termin._new118("АДМИНИСТРАЦИЯ", CityItemToken.ItemType.MISC)
        t.addAbridge("АДМ.")
        CityItemToken.M_ONTOLOGY.add(t)
        CityItemToken.M_STD_ADJECTIVES = IntOntologyCollection()
        t = Termin("ВЕЛИКИЙ")
        t.addAbridge("ВЕЛ.")
        t.addAbridge("ВЕЛИК.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("БОЛЬШОЙ")
        t.addAbridge("БОЛ.")
        t.addAbridge("БОЛЬШ.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("МАЛЫЙ")
        t.addAbridge("МАЛ.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("ВЕРХНИЙ")
        t.addAbridge("ВЕР.")
        t.addAbridge("ВЕРХ.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("НИЖНИЙ")
        t.addAbridge("НИЖ.")
        t.addAbridge("НИЖН.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("СРЕДНИЙ")
        t.addAbridge("СРЕД.")
        t.addAbridge("СРЕДН.")
        t.addAbridge("СР.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("СТАРЫЙ")
        t.addAbridge("СТ.")
        t.addAbridge("СТАР.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("НОВЫЙ")
        t.addAbridge("НОВ.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("ВЕЛИКИЙ", MorphLang.UA)
        t.addAbridge("ВЕЛ.")
        t.addAbridge("ВЕЛИК.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("МАЛИЙ", MorphLang.UA)
        t.addAbridge("МАЛ.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("ВЕРХНІЙ", MorphLang.UA)
        t.addAbridge("ВЕР.")
        t.addAbridge("ВЕРХ.")
        t.addAbridge("ВЕРХН.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("НИЖНІЙ", MorphLang.UA)
        t.addAbridge("НИЖ.")
        t.addAbridge("НИЖН.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("СЕРЕДНІЙ", MorphLang.UA)
        t.addAbridge("СЕР.")
        t.addAbridge("СЕРЕД.")
        t.addAbridge("СЕРЕДН.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("СТАРИЙ", MorphLang.UA)
        t.addAbridge("СТ.")
        t.addAbridge("СТАР.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        t = Termin("НОВИЙ", MorphLang.UA)
        t.addAbridge("НОВ.")
        CityItemToken.M_STD_ADJECTIVES.add(t)
        CityItemToken.M_STD_ADJECTIVES.add(Termin("SAN"))
        CityItemToken.M_STD_ADJECTIVES.add(Termin("LOS"))
        dat = EpNerAddressInternalResourceHelper.getBytes("c.dat")
        if (dat is None): 
            raise Utils.newException("Not found resource file c.dat in Analyzer.Location", None)
        with io.BytesIO(MiscLocationHelper._deflate(dat)) as tmp: 
            tmp.seek(0, io.SEEK_SET)
            xml0_ = None # new XmlDocument
            xml0_ = xml.etree.ElementTree.parse(tmp)
            for x in xml0_.getroot(): 
                if (x.tag == "bigcity"): 
                    CityItemToken.__loadBigCity(x)
                elif (x.tag == "city"): 
                    CityItemToken.__loadCity(x)
    
    @staticmethod
    def __loadCity(xml0_ : xml.etree.ElementTree.Element) -> None:
        ci = IntOntologyItem(None)
        onto = CityItemToken.M_ONTOLOGY
        lang = MorphLang.RU
        if (Utils.getXmlAttrByName(xml0_.attrib, "l") is not None and Utils.getXmlAttrByName(xml0_.attrib, "l")[1] == "ua"): 
            lang = MorphLang.UA
        for x in xml0_: 
            if (x.tag == "n"): 
                v = Utils.getXmlInnerText(x)
                t = Termin()
                t.initByNormalText(v, lang)
                ci.termins.append(t)
                t.addStdAbridges()
                if (v.startswith("SAINT ")): 
                    t.addAbridge("ST. " + v[6:])
                elif (v.startswith("SAITNE ")): 
                    t.addAbridge("STE. " + v[7:])
        onto.addItem(ci)
    
    @staticmethod
    def __loadBigCity(xml0_ : xml.etree.ElementTree.Element) -> None:
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
                t.initByNormalText(v, lang)
                ci.termins.append(t)
                if (v == "САНКТ-ПЕТЕРБУРГ"): 
                    if (CityItemToken.M_ST_PETERBURG is None): 
                        CityItemToken.M_ST_PETERBURG = ci
                    t.acronym = "СПБ"
                    t.addAbridge("С.ПЕТЕРБУРГ")
                    t.addAbridge("СП-Б")
                    ci.termins.append(Termin("ПЕТЕРБУРГ", lang))
                elif (v.startswith("SAINT ")): 
                    t.addAbridge("ST. " + v[6:])
                elif (v.startswith("SAITNE ")): 
                    t.addAbridge("STE. " + v[7:])
            elif (x.tag == "a"): 
                adj = Utils.getXmlInnerText(x)
        onto.addItem(ci)
        if (not Utils.isNullOrEmpty(adj)): 
            at = Termin()
            at.initByNormalText(adj, lang)
            at.tag = (ci)
            city_adj.add(at)
            spb = adj == "САНКТ-ПЕТЕРБУРГСКИЙ" or adj == "САНКТ-ПЕТЕРБУРЗЬКИЙ"
            if (spb): 
                city_adj.add(Termin._new477(adj[6:], lang, ci))
    
    M_ONTOLOGY = None
    
    M_ST_PETERBURG = None
    
    M_CITY_ADJECTIVES = None
    
    M_STD_ADJECTIVES = None
    
    @staticmethod
    def _new1121(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType') -> 'CityItemToken':
        res = CityItemToken(_arg1, _arg2)
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new1123(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : bool) -> 'CityItemToken':
        res = CityItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.geo_object_before = _arg4
        return res
    
    @staticmethod
    def _new1124(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : bool, _arg5 : str) -> 'CityItemToken':
        res = CityItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.geo_object_before = _arg4
        res.value = _arg5
        return res
    
    @staticmethod
    def _new1125(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : str) -> 'CityItemToken':
        res = CityItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        return res
    
    @staticmethod
    def _new1129(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : 'IntOntologyItem', _arg5 : 'MorphCollection') -> 'CityItemToken':
        res = CityItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.onto_item = _arg4
        res.morph = _arg5
        return res
    
    @staticmethod
    def _new1131(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : 'MorphCollection') -> 'CityItemToken':
        res = CityItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.morph = _arg4
        return res
    
    @staticmethod
    def _new1132(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : 'IntOntologyItem', _arg5 : str) -> 'CityItemToken':
        res = CityItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.onto_item = _arg4
        res.value = _arg5
        return res
    
    @staticmethod
    def _new1133(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : str, _arg5 : bool) -> 'CityItemToken':
        res = CityItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        res.doubtful = _arg5
        return res
    
    @staticmethod
    def _new1134(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : str, _arg5 : 'MorphCollection') -> 'CityItemToken':
        res = CityItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        res.morph = _arg5
        return res
    
    @staticmethod
    def _new1135(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : str, _arg5 : bool, _arg6 : 'MorphCollection') -> 'CityItemToken':
        res = CityItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        res.doubtful = _arg5
        res.morph = _arg6
        return res
    
    @staticmethod
    def _new1136(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : str, _arg5 : str, _arg6 : bool, _arg7 : 'MorphCollection') -> 'CityItemToken':
        res = CityItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        res.alt_value = _arg5
        res.doubtful = _arg6
        res.morph = _arg7
        return res