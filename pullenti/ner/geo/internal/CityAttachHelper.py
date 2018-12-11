# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project (www.pullenti.ru).
# See www.pullenti.ru/downloadpage.aspx.

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.address.internal.StreetDefineHelper import StreetDefineHelper
from pullenti.ner.Token import Token
from pullenti.ner.date.DateReferent import DateReferent
from pullenti.ner.geo.internal.GeoOwnerHelper import GeoOwnerHelper
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.address.internal.StreetItemType import StreetItemType
from pullenti.ner.TextToken import TextToken
from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken
from pullenti.ner.Referent import Referent
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.morph.MorphClass import MorphClass
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.geo.internal.CityItemToken import CityItemToken
from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.address.internal.StreetItemToken import StreetItemToken
from pullenti.ner.core.ProperNameHelper import ProperNameHelper

class CityAttachHelper:
    
    @staticmethod
    def tryAttachCity(li : typing.List['CityItemToken'], ad : 'AnalyzerDataWithOntology', always : bool=False) -> 'ReferentToken':
        if (li is None): 
            return None
        if (len(li) > 2 and li[0].typ == CityItemToken.ItemType.MISC and li[1].typ == CityItemToken.ItemType.NOUN): 
            li[1].doubtful = False
            del li[0]
        wrapoi1116 = RefOutArgWrapper(None)
        res = CityAttachHelper.__try1(li, wrapoi1116, ad)
        oi = wrapoi1116.value
        if (res is None): 
            wrapoi1112 = RefOutArgWrapper(None)
            res = CityAttachHelper.__tryNounName(li, wrapoi1112, False)
            oi = wrapoi1112.value
        if (res is None): 
            wrapoi1113 = RefOutArgWrapper(None)
            res = CityAttachHelper.__tryNameExist(li, wrapoi1113, False)
            oi = wrapoi1113.value
        if (res is None): 
            res = CityAttachHelper.__try4(li)
        if (res is None and always): 
            wrapoi1114 = RefOutArgWrapper(None)
            res = CityAttachHelper.__tryNounName(li, wrapoi1114, True)
            oi = wrapoi1114.value
        if (res is None and always): 
            if (AddressItemToken.tryAttachOrg(li[0].begin_token) is not None): 
                pass
            else: 
                wrapoi1115 = RefOutArgWrapper(None)
                res = CityAttachHelper.__tryNameExist(li, wrapoi1115, True)
                oi = wrapoi1115.value
        if (res is None): 
            return None
        if (res is not None and res.morph is not None): 
            pass
        if (res.begin_token.previous is not None): 
            if (res.begin_token.previous.isValue("ТЕРРИТОРИЯ", None)): 
                res.begin_token = res.begin_token.previous
            if ((BracketHelper.canBeStartOfSequence(res.begin_token.previous, False, False) and BracketHelper.canBeEndOfSequence(res.end_token.next0_, False, None, False) and res.begin_token.previous.previous is not None) and res.begin_token.previous.previous.isValue("ТЕРРИТОРИЯ", None)): 
                res.begin_token = res.begin_token.previous.previous
                res.end_token = res.end_token.next0_
        return res
    
    @staticmethod
    def __try1(li : typing.List['CityItemToken'], oi : 'IntOntologyItem', ad : 'AnalyzerDataWithOntology') -> 'ReferentToken':
        oi.value = (None)
        if (li is None or (len(li) < 1)): 
            return None
        elif (li[0].typ != CityItemToken.ItemType.CITY): 
            if (len(li) != 2 or li[0].typ != CityItemToken.ItemType.PROPERNAME or li[1].typ != CityItemToken.ItemType.NOUN): 
                return None
        i = 1
        oi.value = li[0].onto_item
        ok = not li[0].doubtful
        if ((ok and li[0].onto_item is not None and li[0].onto_item.misc_attr is None) and ad is not None): 
            if (li[0].onto_item.owner != ad.local_ontology and not li[0].onto_item.owner.is_ext_ontology): 
                if (li[0].begin_token.previous is not None and li[0].begin_token.previous.isValue("В", None)): 
                    pass
                else: 
                    ok = False
        if (len(li) == 1 and li[0].begin_token.morph.class0_.is_adjective): 
            sits = StreetItemToken.tryParseList(li[0].begin_token, None, 3)
            if (sits is not None and len(sits) == 2 and sits[1].typ == StreetItemType.NOUN): 
                return None
        typ = None
        alttyp = None
        mc = li[0].morph
        if (i < len(li)): 
            if (li[i].typ == CityItemToken.ItemType.NOUN): 
                at = None
                if (not li[i].chars.is_all_lower and (li[i].whitespaces_after_count < 2)): 
                    sit = StreetItemToken.tryParse(li[i].end_token.next0_, None, False, None, False)
                    if (sit is not None and sit.typ == StreetItemType.NOUN): 
                        at = AddressItemToken.tryParse(li[i].begin_token, None, False, False, None)
                        if (at is not None): 
                            at2 = AddressItemToken.tryParse(li[i].end_token.next0_, None, False, False, None)
                            if (at2 is not None and at2.typ == AddressItemToken.ItemType.STREET): 
                                at = (None)
                if (at is None): 
                    typ = li[i].value
                    alttyp = li[i].alt_value
                    if (li[i].begin_token.isValue("СТ", None) and li[i].begin_token.chars.is_all_upper): 
                        return None
                    if ((i + 1) == len(li)): 
                        ok = True
                        if (not li[i].morph.case_.is_undefined): 
                            mc = li[i].morph
                        i += 1
                    elif (ok): 
                        i += 1
                    else: 
                        tt0 = li[0].begin_token.previous
                        if ((isinstance(tt0, TextToken)) and (tt0.whitespaces_after_count < 3)): 
                            if (tt0.isValue("МЭР", "МЕР") or tt0.isValue("ГЛАВА", None) or tt0.isValue("ГРАДОНАЧАЛЬНИК", None)): 
                                ok = True
                                i += 1
        if (not ok and oi.value is not None and (len(oi.value.canonic_text) < 4)): 
            return None
        if (not ok and li[0].begin_token.morph.class0_.is_proper_name): 
            return None
        if (not ok): 
            if (not MiscHelper.isExistsInDictionary(li[0].begin_token, li[0].end_token, (MorphClass.ADJECTIVE) | MorphClass.NOUN | MorphClass.PRONOUN)): 
                ok = (li[0].geo_object_before or li[i - 1].geo_object_after)
                if (ok and li[0].begin_token == li[0].end_token): 
                    mcc = li[0].begin_token.getMorphClassInDictionary()
                    if (mcc.is_proper_name or mcc.is_proper_surname): 
                        ok = False
                    elif (li[0].geo_object_before and (li[0].whitespaces_after_count < 2)): 
                        ad1 = AddressItemToken.tryParse(li[0].begin_token, None, False, False, None)
                        if (ad1 is not None and ad1.typ == AddressItemToken.ItemType.STREET): 
                            ad2 = AddressItemToken.tryParse(li[0].end_token.next0_, None, False, False, None)
                            if (ad2 is None or ad2.typ != AddressItemToken.ItemType.STREET): 
                                ok = False
                        elif (AddressItemToken.tryAttachOrg(li[0].begin_token) is not None): 
                            ok = False
            if (ok): 
                if (li[0].kit.processReferent("PERSON", li[0].begin_token) is not None): 
                    ok = False
        if (not ok): 
            ok = CityAttachHelper.checkYearAfter(li[0].end_token.next0_)
        if (not ok and ((not li[0].begin_token.morph.class0_.is_adjective or li[0].begin_token != li[0].end_token))): 
            ok = CityAttachHelper.checkCityAfter(li[0].end_token.next0_)
        if (not ok): 
            return None
        if (i < len(li)): 
            del li[i:i+len(li) - i]
        rt = None
        if (oi.value is None): 
            if (li[0].value is not None and li[0].higher_geo is not None): 
                cap = GeoReferent()
                cap._addName(li[0].value)
                cap._addTypCity(li[0].kit.base_language)
                cap.higher = li[0].higher_geo
                if (typ is not None): 
                    cap._addTyp(typ)
                if (alttyp is not None): 
                    cap._addTyp(alttyp)
                rt = ReferentToken(cap, li[0].begin_token, li[0].end_token)
            else: 
                if (li[0].value is None): 
                    return None
                if (typ is None): 
                    if ((len(li) == 1 and li[0].begin_token.previous is not None and li[0].begin_token.previous.is_hiphen) and (isinstance(li[0].begin_token.previous.previous, ReferentToken)) and (isinstance(li[0].begin_token.previous.previous.getReferent(), GeoReferent))): 
                        pass
                    else: 
                        return None
                else: 
                    if (not LanguageHelper.endsWithEx(typ, "ПУНКТ", "ПОСЕЛЕНИЕ", "ПОСЕЛЕННЯ", "ПОСЕЛОК")): 
                        if (not LanguageHelper.endsWith(typ, "CITY")): 
                            if (typ == "СТАНЦИЯ" and ((MiscLocationHelper.checkGeoObjectBefore(li[0].begin_token)))): 
                                pass
                            elif (len(li) > 1 and li[1].typ == CityItemToken.ItemType.NOUN and li[0].typ == CityItemToken.ItemType.CITY): 
                                pass
                            else: 
                                return None
                    if (li[0].begin_token.morph.class0_.is_adjective): 
                        li[0].value = ProperNameHelper.getNameEx(li[0].begin_token, li[0].end_token, MorphClass.ADJECTIVE, li[1].morph.case_, li[1].morph.gender, False, False)
        elif (isinstance(oi.value.referent, GeoReferent)): 
            rt = ReferentToken._new746(Utils.asObjectOrNull(oi.value.referent, GeoReferent), li[0].begin_token, li[len(li) - 1].end_token, mc)
        elif (typ is None): 
            typ = oi.value.typ
        if (rt is None): 
            city = GeoReferent()
            city._addName((li[0].value if oi.value is None else oi.value.canonic_text))
            if (typ is not None): 
                city._addTyp(typ)
            else: 
                city._addTypCity(li[0].kit.base_language)
            if (alttyp is not None): 
                city._addTyp(alttyp)
            rt = ReferentToken._new746(city, li[0].begin_token, li[len(li) - 1].end_token, mc)
        if ((isinstance(rt.referent, GeoReferent)) and len(li) == 1 and (rt.referent).is_city): 
            if (rt.begin_token.previous is not None and rt.begin_token.previous.isValue("Г", None)): 
                rt.begin_token = rt.begin_token.previous
            elif ((rt.begin_token.previous is not None and rt.begin_token.previous.isChar('.') and rt.begin_token.previous.previous is not None) and rt.begin_token.previous.previous.isValue("Г", None)): 
                rt.begin_token = rt.begin_token.previous.previous
            elif (rt.end_token.next0_ is not None and (rt.whitespaces_after_count < 2) and rt.end_token.next0_.isValue("Г", None)): 
                rt.end_token = rt.end_token.next0_
                if (rt.end_token.next0_ is not None and rt.end_token.next0_.isChar('.')): 
                    rt.end_token = rt.end_token.next0_
        return rt
    
    @staticmethod
    def __tryNounName(li : typing.List['CityItemToken'], oi : 'IntOntologyItem', always : bool) -> 'ReferentToken':
        oi.value = (None)
        if (li is None or (len(li) < 2) or ((li[0].typ != CityItemToken.ItemType.NOUN and li[0].typ != CityItemToken.ItemType.MISC))): 
            return None
        ok = not li[0].doubtful
        if (ok and li[0].typ == CityItemToken.ItemType.MISC): 
            ok = False
        typ = (None if li[0].typ == CityItemToken.ItemType.MISC else li[0].value)
        typ2 = (None if li[0].typ == CityItemToken.ItemType.MISC else li[0].alt_value)
        prob_adj = None
        i1 = 1
        org0_ = None
        if ((typ is not None and li[i1].typ == CityItemToken.ItemType.NOUN and ((i1 + 1) < len(li))) and li[0].whitespaces_after_count <= 1 and (((LanguageHelper.endsWith(typ, "ПОСЕЛОК") or LanguageHelper.endsWith(typ, "СЕЛИЩЕ") or typ == "ДЕРЕВНЯ") or typ == "СЕЛО"))): 
            if (li[i1].begin_token == li[i1].end_token): 
                ooo = AddressItemToken.tryAttachOrg(li[i1].begin_token)
                if (ooo is not None and ooo.ref_token is not None): 
                    return None
            typ2 = li[i1].value
            if (typ2 == "СТАНЦИЯ" and li[i1].begin_token.isValue("СТ", None) and ((i1 + 1) < len(li))): 
                m = li[i1 + 1].morph
                if (m.number == MorphNumber.PLURAL): 
                    prob_adj = "СТАРЫЕ"
                elif (m.gender == MorphGender.FEMINIE): 
                    prob_adj = "СТАРАЯ"
                elif (m.gender == MorphGender.MASCULINE): 
                    prob_adj = "СТАРЫЙ"
                else: 
                    prob_adj = "СТАРОЕ"
            i1 += 1
        name = Utils.ifNotNull(li[i1].value, ((None if li[i1].onto_item is None else li[i1].onto_item.canonic_text)))
        alt_name = li[i1].alt_value
        if (name is None): 
            return None
        mc = li[0].morph
        if (i1 == 1 and li[i1].typ == CityItemToken.ItemType.CITY and ((li[0].value == "ГОРОД" or li[0].value == "МІСТО" or li[0].typ == CityItemToken.ItemType.MISC))): 
            if (typ is None and ((i1 + 1) < len(li)) and li[i1 + 1].typ == CityItemToken.ItemType.NOUN): 
                return None
            oi.value = li[i1].onto_item
            if (oi.value is not None): 
                name = oi.value.canonic_text
            if (len(name) > 2 or oi.value.misc_attr is not None): 
                if (not li[1].doubtful or ((oi.value is not None and oi.value.misc_attr is not None))): 
                    ok = True
                elif (not ok and not li[1].is_newline_before): 
                    if (li[0].geo_object_before or li[1].geo_object_after): 
                        ok = True
                    elif (StreetDefineHelper.checkStreetAfter(li[1].end_token.next0_)): 
                        ok = True
                    elif (li[1].end_token.next0_ is not None and (isinstance(li[1].end_token.next0_.getReferent(), DateReferent))): 
                        ok = True
                    elif ((li[1].whitespaces_before_count < 2) and li[1].onto_item is not None): 
                        if (li[1].is_newline_after): 
                            ok = True
                if (li[1].doubtful and li[1].end_token.next0_ is not None and li[1].end_token.chars == li[1].end_token.next0_.chars): 
                    ok = False
                if (li[0].begin_token.previous is not None and li[0].begin_token.previous.isValue("В", None)): 
                    ok = True
            if (not ok): 
                ok = CityAttachHelper.checkYearAfter(li[1].end_token.next0_)
            if (not ok): 
                ok = CityAttachHelper.checkCityAfter(li[1].end_token.next0_)
        elif ((li[i1].typ == CityItemToken.ItemType.PROPERNAME or li[i1].typ == CityItemToken.ItemType.CITY)): 
            if (((li[0].value == "АДМИНИСТРАЦИЯ" or li[0].value == "АДМІНІСТРАЦІЯ")) and i1 == 1): 
                return None
            if (li[i1].is_newline_before): 
                if (len(li) != 2): 
                    return None
            if (not li[0].doubtful): 
                ok = True
                if (len(name) < 2): 
                    ok = False
                elif ((len(name) < 3) and li[0].morph.number != MorphNumber.SINGULAR): 
                    ok = False
                if (li[i1].doubtful and not li[i1].geo_object_after and not li[0].geo_object_before): 
                    if (li[i1].morph.case_.is_genitive): 
                        if (((li[0].begin_token.previous is None or MiscLocationHelper.checkGeoObjectBefore(li[0].begin_token))) and ((li[i1].end_token.next0_ is None or MiscLocationHelper.checkGeoObjectAfter(li[i1].end_token.next0_) or AddressItemToken.checkHouseAfter(li[i1].end_token.next0_, False, True)))): 
                            pass
                        else: 
                            ok = False
                    else: 
                        rt0 = li[i1].kit.processReferent("PERSONPROPERTY", li[0].begin_token.previous)
                        if (rt0 is not None): 
                            rt1 = li[i1].kit.processReferent("PERSON", li[i1].begin_token)
                            if (rt1 is not None): 
                                ok = False
                npt = NounPhraseHelper.tryParse(li[i1].begin_token, NounPhraseParseAttr.NO, 0)
                if (npt is not None): 
                    if (npt.end_token.end_char > li[i1].end_char and len(npt.adjectives) > 0 and not npt.adjectives[0].end_token.next0_.is_comma): 
                        ok = False
                    elif (TerrItemToken._m_unknown_regions.tryParse(npt.end_token, TerminParseAttr.FULLWORDSONLY) is not None): 
                        ok1 = False
                        if (li[0].begin_token.previous is not None): 
                            ttt = li[0].begin_token.previous
                            if (ttt.is_comma and ttt.previous is not None): 
                                ttt = ttt.previous
                            geo_ = Utils.asObjectOrNull(ttt.getReferent(), GeoReferent)
                            if (geo_ is not None and not geo_.is_city): 
                                ok1 = True
                        if (npt.end_token.next0_ is not None): 
                            ttt = npt.end_token.next0_
                            if (ttt.is_comma and ttt.next0_ is not None): 
                                ttt = ttt.next0_
                            geo_ = Utils.asObjectOrNull(ttt.getReferent(), GeoReferent)
                            if (geo_ is not None and not geo_.is_city): 
                                ok1 = True
                        if (not ok1): 
                            return None
                if (li[0].value == "ПОРТ"): 
                    if (li[i1].chars.is_all_upper or li[i1].chars.is_latin_letter): 
                        return None
            elif (li[0].geo_object_before): 
                ok = True
            elif (li[i1].geo_object_after and not li[i1].is_newline_after): 
                ok = True
            else: 
                ok = CityAttachHelper.checkYearAfter(li[i1].end_token.next0_)
            if (not ok): 
                ok = CityAttachHelper.checkStreetAfter(li[i1].end_token.next0_)
            if (not ok and li[0].begin_token.previous is not None and li[0].begin_token.previous.isValue("В", None)): 
                ok = True
        else: 
            return None
        if (not ok and not always): 
            if (MiscLocationHelper.checkNearBefore(li[0].begin_token.previous) is None): 
                return None
        if (len(li) > (i1 + 1)): 
            del li[i1 + 1:i1 + 1+len(li) - i1 - 1]
        city = GeoReferent()
        if (oi.value is not None and oi.value.referent is not None): 
            city = (Utils.asObjectOrNull(oi.value.referent.clone(), GeoReferent))
            city.occurrence.clear()
        if (not li[0].morph.case_.is_undefined and li[0].morph.gender != MorphGender.UNDEFINED): 
            if (li[i1].end_token.morph.class0_.is_adjective and li[i1].begin_token == li[i1].end_token): 
                nam = ProperNameHelper.getNameEx(li[i1].begin_token, li[i1].end_token, MorphClass.ADJECTIVE, li[0].morph.case_, li[0].morph.gender, False, False)
                if (nam is not None and nam != name): 
                    name = nam
        if (li[0].morph.case_.is_nominative): 
            if (alt_name is not None): 
                city._addName(alt_name)
            alt_name = (None)
        city._addName(name)
        if (prob_adj is not None): 
            city._addName(prob_adj + " " + name)
        if (alt_name is not None): 
            city._addName(alt_name)
            if (prob_adj is not None): 
                city._addName(prob_adj + " " + alt_name)
        if (typ is not None): 
            city._addTyp(typ)
        elif (not city.is_city): 
            city._addTypCity(li[0].kit.base_language)
        if (typ2 is not None): 
            city._addTyp(typ2.lower())
        if (li[0].higher_geo is not None and GeoOwnerHelper.canBeHigher(li[0].higher_geo, city)): 
            city.higher = li[0].higher_geo
        if (li[0].typ == CityItemToken.ItemType.MISC): 
            del li[0]
        res = ReferentToken._new746(city, li[0].begin_token, li[len(li) - 1].end_token, mc)
        if (res.end_token.next0_ is not None and res.end_token.next0_.is_hiphen and (isinstance(res.end_token.next0_.next0_, NumberToken))): 
            num = Utils.asObjectOrNull(res.end_token.next0_.next0_, NumberToken)
            if (num.typ == NumberSpellingType.DIGIT and not num.morph.class0_.is_adjective and (num.value < (50))): 
                for s in city.slots: 
                    if (s.type_name == GeoReferent.ATTR_NAME): 
                        city.uploadSlot(s, "{0}-{1}".format(s.value, num.value))
                res.end_token = num
        if (li[0].begin_token == li[0].end_token and li[0].begin_token.isValue("ГОРОДОК", None)): 
            if (AddressItemToken.checkHouseAfter(res.end_token.next0_, True, False)): 
                return None
        return res
    
    @staticmethod
    def __tryNameExist(li : typing.List['CityItemToken'], oi : 'IntOntologyItem', always : bool) -> 'ReferentToken':
        """ Это проверяем некоторые частные случаи
        
        Args:
            li(typing.List[CityItemToken]): 
            oi(IntOntologyItem): 
        
        """
        oi.value = (None)
        if (li is None or li[0].typ != CityItemToken.ItemType.CITY): 
            return None
        oi.value = li[0].onto_item
        tt = Utils.asObjectOrNull(li[0].begin_token, TextToken)
        if (tt is None): 
            return None
        ok = False
        nam = (li[0].value if oi.value is None else oi.value.canonic_text)
        if (nam is None): 
            return None
        if (nam == "РИМ"): 
            if (tt.term == "РИМ"): 
                if ((isinstance(tt.next0_, TextToken)) and tt.next0_.getMorphClassInDictionary().is_proper_secname): 
                    pass
                else: 
                    ok = True
            elif (tt.previous is not None and tt.previous.isValue("В", None) and tt.term == "РИМЕ"): 
                ok = True
        elif (oi.value is not None and oi.value.referent is not None and oi.value.owner.is_ext_ontology): 
            ok = True
        elif (nam.endswith("ГРАД") or nam.endswith("СК")): 
            ok = True
        elif (nam.endswith("TOWN") or nam.startswith("SAN")): 
            ok = True
        elif (li[0].chars.is_latin_letter and li[0].begin_token.previous is not None and ((li[0].begin_token.previous.isValue("IN", None) or li[0].begin_token.previous.isValue("FROM", None)))): 
            ok = True
        else: 
            tt2 = li[0].end_token.next0_
            first_pass2903 = True
            while True:
                if first_pass2903: first_pass2903 = False
                else: tt2 = tt2.next0_
                if (not (tt2 is not None)): break
                if (tt2.is_newline_before): 
                    break
                if ((tt2.isCharOf(",(") or tt2.morph.class0_.is_preposition or tt2.morph.class0_.is_conjunction) or tt2.morph.class0_.is_misc): 
                    continue
                if ((isinstance(tt2.getReferent(), GeoReferent)) and tt2.chars.is_cyrillic_letter == li[0].chars.is_cyrillic_letter): 
                    ok = True
                break
            if (not ok): 
                tt2 = li[0].begin_token.previous
                first_pass2904 = True
                while True:
                    if first_pass2904: first_pass2904 = False
                    else: tt2 = tt2.previous
                    if (not (tt2 is not None)): break
                    if (tt2.is_newline_after): 
                        break
                    if ((tt2.isCharOf(",)") or tt2.morph.class0_.is_preposition or tt2.morph.class0_.is_conjunction) or tt2.morph.class0_.is_misc): 
                        continue
                    if ((isinstance(tt2.getReferent(), GeoReferent)) and tt2.chars.is_cyrillic_letter == li[0].chars.is_cyrillic_letter): 
                        ok = True
                    if (ok): 
                        sits = StreetItemToken.tryParseList(li[0].begin_token, None, 10)
                        if (sits is not None and len(sits) > 1): 
                            ss = StreetDefineHelper._tryParseStreet(sits, False, False)
                            if (ss is not None): 
                                del sits[0]
                                if (StreetDefineHelper._tryParseStreet(sits, False, False) is None): 
                                    ok = False
                    if (ok): 
                        if (len(li) > 1 and li[1].typ == CityItemToken.ItemType.PROPERNAME and (li[1].whitespaces_before_count < 3)): 
                            ok = False
                        else: 
                            mc = li[0].begin_token.getMorphClassInDictionary()
                            if (mc.is_proper_name or mc.is_proper_surname or mc.is_adjective): 
                                ok = False
                            else: 
                                npt = NounPhraseHelper.tryParse(li[0].begin_token, NounPhraseParseAttr.NO, 0)
                                if (npt is not None and npt.end_char > li[0].end_char): 
                                    ok = False
                    if (AddressItemToken.tryAttachOrg(li[0].begin_token) is not None): 
                        ok = False
                        break
                    break
        if (always): 
            if (li[0].whitespaces_before_count > 3 and li[0].doubtful and li[0].begin_token.getMorphClassInDictionary().is_proper_surname): 
                pp = li[0].kit.processReferent("PERSON", li[0].begin_token)
                if (pp is not None): 
                    always = False
        if (li[0].begin_token.chars.is_latin_letter and li[0].begin_token == li[0].end_token): 
            tt1 = li[0].end_token.next0_
            if (tt1 is not None and tt1.isChar(',')): 
                tt1 = tt1.next0_
            if (((isinstance(tt1, TextToken)) and tt1.chars.is_latin_letter and (tt1.length_char < 3)) and not tt1.chars.is_all_lower): 
                ok = False
        if (not ok and not always): 
            return None
        city = None
        if (oi.value is not None and (isinstance(oi.value.referent, GeoReferent)) and not oi.value.owner.is_ext_ontology): 
            city = (Utils.asObjectOrNull(oi.value.referent, GeoReferent))
        else: 
            city = GeoReferent()
            city._addName(nam)
            if (oi.value is not None and (isinstance(oi.value.referent, GeoReferent))): 
                city._mergeSlots2(Utils.asObjectOrNull(oi.value.referent, GeoReferent), li[0].kit.base_language)
            if (not city.is_city): 
                city._addTypCity(li[0].kit.base_language)
        return ReferentToken._new746(city, li[0].begin_token, li[0].end_token, li[0].morph)
    
    @staticmethod
    def __try4(li : typing.List['CityItemToken']) -> 'ReferentToken':
        if ((len(li) > 0 and li[0].typ == CityItemToken.ItemType.NOUN and ((li[0].value != "ГОРОД" and li[0].value != "МІСТО" and li[0].value != "CITY"))) and ((not li[0].doubtful or li[0].geo_object_before))): 
            if (len(li) > 1 and li[1].org_ref is not None): 
                geo_ = GeoReferent()
                geo_._addTyp(li[0].value)
                geo_._addOrgReferent(li[1].org_ref.referent)
                geo_.addExtReferent(li[1].org_ref)
                return ReferentToken(geo_, li[0].begin_token, li[1].end_token)
            else: 
                aid = AddressItemToken.tryAttachOrg(li[0].end_token.next0_)
                if (aid is not None): 
                    geo_ = GeoReferent()
                    geo_._addTyp(li[0].value)
                    geo_._addOrgReferent(aid.referent)
                    geo_.addExtReferent(aid.ref_token)
                    return ReferentToken(geo_, li[0].begin_token, aid.end_token)
        return None
    
    @staticmethod
    def checkYearAfter(tt : 'Token') -> bool:
        if (tt is not None and ((tt.is_comma or tt.is_hiphen))): 
            tt = tt.next0_
        if (tt is not None and tt.is_newline_after): 
            if (isinstance(tt, NumberToken)): 
                year = (tt).value
                if (year > (1990) and (year < (2100))): 
                    return True
            elif (tt.getReferent() is not None and tt.getReferent().type_name == "DATE"): 
                return True
        return False
    
    @staticmethod
    def checkStreetAfter(tt : 'Token') -> bool:
        if (tt is not None and ((tt.is_comma_and or tt.is_hiphen or tt.morph.class0_.is_preposition))): 
            tt = tt.next0_
        if (tt is None): 
            return False
        ait = AddressItemToken.tryParse(tt, None, False, False, None)
        if (ait is not None and ait.typ == AddressItemToken.ItemType.STREET): 
            return True
        return False
    
    @staticmethod
    def checkCityAfter(tt : 'Token') -> bool:
        while tt is not None and (((tt.is_comma_and or tt.is_hiphen or tt.morph.class0_.is_preposition) or tt.isChar('.'))):
            tt = tt.next0_
        if (tt is None): 
            return False
        cits = CityItemToken.tryParseList(tt, None, 5)
        if (cits is None or len(cits) == 0): 
            if (tt.length_char == 1 and tt.chars.is_all_lower and ((tt.isValue("Д", None) or tt.isValue("П", None)))): 
                tt1 = tt.next0_
                if (tt1 is not None and tt1.isChar('.')): 
                    tt1 = tt1.next0_
                ci = CityItemToken.tryParse(tt1, None, False, None)
                if (ci is not None and ((ci.typ == CityItemToken.ItemType.PROPERNAME or ci.typ == CityItemToken.ItemType.CITY))): 
                    return True
            return False
        if (CityAttachHelper.tryAttachCity(cits, None, False) is not None): 
            return True
        if (cits[0].typ == CityItemToken.ItemType.NOUN): 
            if (tt.previous is not None and tt.previous.is_comma): 
                return True
        return False