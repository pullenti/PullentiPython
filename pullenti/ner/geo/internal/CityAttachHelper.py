# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping (www.unisharping.ru) from Pullenti C#.NET project. The latest version of the code is available on the site www.pullenti.ru

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.address.internal.StreetDefineHelper import StreetDefineHelper
from pullenti.ner.Token import Token
from pullenti.ner.geo.internal.GeoOwnerHelper import GeoOwnerHelper
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.date.DateReferent import DateReferent
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.address.internal.StreetItemType import StreetItemType
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken
from pullenti.ner.TextToken import TextToken
from pullenti.ner.Referent import Referent
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
from pullenti.morph.MorphClass import MorphClass
from pullenti.ner.address.internal.StreetItemToken import StreetItemToken
from pullenti.ner.geo.internal.CityItemToken import CityItemToken
from pullenti.ner.core.ProperNameHelper import ProperNameHelper

class CityAttachHelper:
    
    @staticmethod
    def try_attach_city(li : typing.List['CityItemToken'], ad : 'AnalyzerDataWithOntology', always : bool=False) -> 'ReferentToken':
        if (li is None): 
            return None
        if (len(li) > 2 and li[0].typ == CityItemToken.ItemType.MISC and li[1].typ == CityItemToken.ItemType.NOUN): 
            li[1].doubtful = False
            del li[0]
        res = None
        if (res is None and len(li) > 1): 
            res = CityAttachHelper.__try4(li)
            if (res is not None and res.end_char <= li[1].end_char): 
                res = (None)
        if (res is None): 
            wrapoi1125 = RefOutArgWrapper(None)
            res = CityAttachHelper.__try1(li, wrapoi1125, ad)
            oi = wrapoi1125.value
        if (res is None): 
            wrapoi1126 = RefOutArgWrapper(None)
            res = CityAttachHelper.__try_noun_name(li, wrapoi1126, False)
            oi = wrapoi1126.value
        if (res is None): 
            wrapoi1127 = RefOutArgWrapper(None)
            res = CityAttachHelper.__try_name_exist(li, wrapoi1127, False)
            oi = wrapoi1127.value
        if (res is None): 
            res = CityAttachHelper.__try4(li)
        if (res is None and always): 
            wrapoi1128 = RefOutArgWrapper(None)
            res = CityAttachHelper.__try_noun_name(li, wrapoi1128, True)
            oi = wrapoi1128.value
        if (res is None and always): 
            if (AddressItemToken.try_attach_org(li[0].begin_token) is not None): 
                pass
            else: 
                wrapoi1129 = RefOutArgWrapper(None)
                res = CityAttachHelper.__try_name_exist(li, wrapoi1129, True)
                oi = wrapoi1129.value
        if (res is None): 
            return None
        if (res is not None and res.morph is not None): 
            pass
        if (res.begin_token.previous is not None): 
            if (res.begin_token.previous.is_value("ТЕРРИТОРИЯ", None)): 
                res.begin_token = res.begin_token.previous
                res.morph = res.begin_token.morph
            if ((BracketHelper.can_be_start_of_sequence(res.begin_token.previous, False, False) and BracketHelper.can_be_end_of_sequence(res.end_token.next0_, False, None, False) and res.begin_token.previous.previous is not None) and res.begin_token.previous.previous.is_value("ТЕРРИТОРИЯ", None)): 
                res.begin_token = res.begin_token.previous.previous
                res.morph = res.begin_token.morph
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
                if (li[0].begin_token.previous is not None and li[0].begin_token.previous.is_value("В", None)): 
                    pass
                else: 
                    ok = False
        if (len(li) == 1 and li[0].begin_token.morph.class0_.is_adjective): 
            sits = StreetItemToken.try_parse_list(li[0].begin_token, None, 3)
            if (sits is not None and len(sits) == 2 and sits[1].typ == StreetItemType.NOUN): 
                return None
        typ = None
        alttyp = None
        mc = li[0].morph
        if (i < len(li)): 
            if (li[i].typ == CityItemToken.ItemType.NOUN): 
                at = None
                if (not li[i].chars.is_all_lower and (li[i].whitespaces_after_count < 2)): 
                    sit = StreetItemToken.try_parse(li[i].end_token.next0_, None, False, None, False)
                    if (sit is not None and sit.typ == StreetItemType.NOUN): 
                        at = AddressItemToken.try_parse(li[i].begin_token, None, False, False, None)
                        if (at is not None): 
                            at2 = AddressItemToken.try_parse(li[i].end_token.next0_, None, False, False, None)
                            if (at2 is not None and at2.typ == AddressItemToken.ItemType.STREET): 
                                at = (None)
                if (at is None): 
                    typ = li[i].value
                    alttyp = li[i].alt_value
                    if (li[i].begin_token.is_value("СТ", None) and li[i].begin_token.chars.is_all_upper): 
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
                            if (tt0.is_value("МЭР", "МЕР") or tt0.is_value("ГЛАВА", None) or tt0.is_value("ГРАДОНАЧАЛЬНИК", None)): 
                                ok = True
                                i += 1
        if (not ok and oi.value is not None and (len(oi.value.canonic_text) < 4)): 
            return None
        if (not ok and li[0].begin_token.morph.class0_.is_proper_name): 
            return None
        if (not ok): 
            if (not MiscHelper.is_exists_in_dictionary(li[0].begin_token, li[0].end_token, (MorphClass.ADJECTIVE) | MorphClass.NOUN | MorphClass.PRONOUN)): 
                ok = (li[0].geo_object_before or li[i - 1].geo_object_after)
                if (ok and li[0].begin_token == li[0].end_token): 
                    mcc = li[0].begin_token.get_morph_class_in_dictionary()
                    if (mcc.is_proper_name or mcc.is_proper_surname): 
                        ok = False
                    elif (li[0].geo_object_before and (li[0].whitespaces_after_count < 2)): 
                        ad1 = AddressItemToken.try_parse(li[0].begin_token, None, False, False, None)
                        if (ad1 is not None and ad1.typ == AddressItemToken.ItemType.STREET): 
                            ad2 = AddressItemToken.try_parse(li[0].end_token.next0_, None, False, False, None)
                            if (ad2 is None or ad2.typ != AddressItemToken.ItemType.STREET): 
                                ok = False
                        elif (AddressItemToken.try_attach_org(li[0].begin_token) is not None): 
                            ok = False
            if (ok): 
                if (li[0].kit.process_referent("PERSON", li[0].begin_token) is not None): 
                    ok = False
        if (not ok): 
            ok = CityAttachHelper.check_year_after(li[0].end_token.next0_)
        if (not ok and ((not li[0].begin_token.morph.class0_.is_adjective or li[0].begin_token != li[0].end_token))): 
            ok = CityAttachHelper.check_city_after(li[0].end_token.next0_)
        if (not ok): 
            return None
        if (i < len(li)): 
            del li[i:i+len(li) - i]
        rt = None
        if (oi.value is None): 
            if (li[0].value is not None and li[0].higher_geo is not None): 
                cap = GeoReferent()
                cap._add_name(li[0].value)
                cap._add_typ_city(li[0].kit.base_language)
                cap.higher = li[0].higher_geo
                if (typ is not None): 
                    cap._add_typ(typ)
                if (alttyp is not None): 
                    cap._add_typ(alttyp)
                rt = ReferentToken(cap, li[0].begin_token, li[0].end_token)
            else: 
                if (li[0].value is None): 
                    return None
                if (typ is None): 
                    if ((len(li) == 1 and li[0].begin_token.previous is not None and li[0].begin_token.previous.is_hiphen) and (isinstance(li[0].begin_token.previous.previous, ReferentToken)) and (isinstance(li[0].begin_token.previous.previous.get_referent(), GeoReferent))): 
                        pass
                    else: 
                        return None
                else: 
                    if (not LanguageHelper.ends_with_ex(typ, "ПУНКТ", "ПОСЕЛЕНИЕ", "ПОСЕЛЕННЯ", "ПОСЕЛОК")): 
                        if (not LanguageHelper.ends_with(typ, "CITY")): 
                            if (typ == "СТАНЦИЯ" and ((MiscLocationHelper.check_geo_object_before(li[0].begin_token)))): 
                                pass
                            elif (len(li) > 1 and li[1].typ == CityItemToken.ItemType.NOUN and li[0].typ == CityItemToken.ItemType.CITY): 
                                pass
                            elif ((len(li) == 2 and li[1].typ == CityItemToken.ItemType.NOUN and li[0].typ == CityItemToken.ItemType.PROPERNAME) and ((li[0].geo_object_before or li[1].geo_object_after))): 
                                pass
                            else: 
                                return None
                    if (li[0].begin_token.morph.class0_.is_adjective): 
                        li[0].value = ProperNameHelper.get_name_ex(li[0].begin_token, li[0].end_token, MorphClass.ADJECTIVE, li[1].morph.case_, li[1].morph.gender, False, False)
        elif (isinstance(oi.value.referent, GeoReferent)): 
            city = Utils.asObjectOrNull(oi.value.referent.clone(), GeoReferent)
            city.occurrence.clear()
            rt = ReferentToken._new734(city, li[0].begin_token, li[len(li) - 1].end_token, mc)
        elif (typ is None): 
            typ = oi.value.typ
        if (rt is None): 
            city = GeoReferent()
            city._add_name((li[0].value if oi.value is None else oi.value.canonic_text))
            if (typ is not None): 
                city._add_typ(typ)
            else: 
                city._add_typ_city(li[0].kit.base_language)
            if (alttyp is not None): 
                city._add_typ(alttyp)
            rt = ReferentToken._new734(city, li[0].begin_token, li[len(li) - 1].end_token, mc)
        if ((isinstance(rt.referent, GeoReferent)) and len(li) == 1 and rt.referent.is_city): 
            if (rt.begin_token.previous is not None and rt.begin_token.previous.is_value("Г", None)): 
                rt.begin_token = rt.begin_token.previous
            elif ((rt.begin_token.previous is not None and rt.begin_token.previous.is_char('.') and rt.begin_token.previous.previous is not None) and rt.begin_token.previous.previous.is_value("Г", None)): 
                rt.begin_token = rt.begin_token.previous.previous
            elif (rt.end_token.next0_ is not None and (rt.whitespaces_after_count < 2) and rt.end_token.next0_.is_value("Г", None)): 
                rt.end_token = rt.end_token.next0_
                if (rt.end_token.next0_ is not None and rt.end_token.next0_.is_char('.')): 
                    rt.end_token = rt.end_token.next0_
        return rt
    
    @staticmethod
    def __try_noun_name(li : typing.List['CityItemToken'], oi : 'IntOntologyItem', always : bool) -> 'ReferentToken':
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
        if ((typ is not None and li[i1].typ == CityItemToken.ItemType.NOUN and ((i1 + 1) < len(li))) and li[0].whitespaces_after_count <= 1 and (((LanguageHelper.ends_with(typ, "ПОСЕЛОК") or LanguageHelper.ends_with(typ, "СЕЛИЩЕ") or typ == "ДЕРЕВНЯ") or typ == "СЕЛО"))): 
            if (li[i1].begin_token == li[i1].end_token): 
                ooo = AddressItemToken.try_attach_org(li[i1].begin_token)
                if (ooo is not None and ooo.ref_token is not None): 
                    return None
            typ2 = li[i1].value
            if (typ2 == "СТАНЦИЯ" and li[i1].begin_token.is_value("СТ", None) and ((i1 + 1) < len(li))): 
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
                    elif (StreetDefineHelper.check_street_after(li[1].end_token.next0_)): 
                        ok = True
                    elif (li[1].end_token.next0_ is not None and (isinstance(li[1].end_token.next0_.get_referent(), DateReferent))): 
                        ok = True
                    elif ((li[1].whitespaces_before_count < 2) and li[1].onto_item is not None): 
                        if (li[1].is_newline_after): 
                            ok = True
                        else: 
                            ok = True
                if (li[1].doubtful and li[1].end_token.next0_ is not None and li[1].end_token.chars == li[1].end_token.next0_.chars): 
                    ok = False
                if (li[0].begin_token.previous is not None and li[0].begin_token.previous.is_value("В", None)): 
                    ok = True
            if (not ok): 
                ok = CityAttachHelper.check_year_after(li[1].end_token.next0_)
            if (not ok): 
                ok = CityAttachHelper.check_city_after(li[1].end_token.next0_)
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
                        if (li[i1].end_token.next0_ is None or MiscLocationHelper.check_geo_object_after(li[i1].end_token.next0_, False) or AddressItemToken.check_house_after(li[i1].end_token.next0_, False, True)): 
                            pass
                        elif (li[0].begin_token.previous is None or MiscLocationHelper.check_geo_object_before(li[0].begin_token)): 
                            pass
                        else: 
                            ok = False
                    if (ok): 
                        rt0 = li[i1].kit.process_referent("PERSONPROPERTY", li[0].begin_token.previous)
                        if (rt0 is not None): 
                            rt1 = li[i1].kit.process_referent("PERSON", li[i1].begin_token)
                            if (rt1 is not None): 
                                ok = False
                npt = NounPhraseHelper.try_parse(li[i1].begin_token, NounPhraseParseAttr.NO, 0, None)
                if (npt is not None): 
                    if (npt.end_token.end_char > li[i1].end_char and len(npt.adjectives) > 0 and not npt.adjectives[0].end_token.next0_.is_comma): 
                        ok = False
                    elif (TerrItemToken._m_unknown_regions.try_parse(npt.end_token, TerminParseAttr.FULLWORDSONLY) is not None): 
                        ok1 = False
                        if (li[0].begin_token.previous is not None): 
                            ttt = li[0].begin_token.previous
                            if (ttt.is_comma and ttt.previous is not None): 
                                ttt = ttt.previous
                            geo_ = Utils.asObjectOrNull(ttt.get_referent(), GeoReferent)
                            if (geo_ is not None and not geo_.is_city): 
                                ok1 = True
                        if (npt.end_token.next0_ is not None): 
                            ttt = npt.end_token.next0_
                            if (ttt.is_comma and ttt.next0_ is not None): 
                                ttt = ttt.next0_
                            geo_ = Utils.asObjectOrNull(ttt.get_referent(), GeoReferent)
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
                ok = CityAttachHelper.check_year_after(li[i1].end_token.next0_)
            if (not ok): 
                ok = CityAttachHelper.check_street_after(li[i1].end_token.next0_)
            if (not ok and li[0].begin_token.previous is not None and li[0].begin_token.previous.is_value("В", None)): 
                ok = True
        else: 
            return None
        if (not ok and not always): 
            if (MiscLocationHelper.check_near_before(li[0].begin_token.previous) is None): 
                return None
        if (len(li) > (i1 + 1)): 
            del li[i1 + 1:i1 + 1+len(li) - i1 - 1]
        city = GeoReferent()
        if (oi.value is not None and oi.value.referent is not None): 
            city = (Utils.asObjectOrNull(oi.value.referent.clone(), GeoReferent))
            city.occurrence.clear()
        if (not li[0].morph.case_.is_undefined and li[0].morph.gender != MorphGender.UNDEFINED): 
            if (li[i1].end_token.morph.class0_.is_adjective and li[i1].begin_token == li[i1].end_token): 
                nam = ProperNameHelper.get_name_ex(li[i1].begin_token, li[i1].end_token, MorphClass.ADJECTIVE, li[0].morph.case_, li[0].morph.gender, False, False)
                if (nam is not None and nam != name): 
                    name = nam
        if (li[0].morph.case_.is_nominative): 
            if (alt_name is not None): 
                city._add_name(alt_name)
            alt_name = (None)
        city._add_name(name)
        if (prob_adj is not None): 
            city._add_name(prob_adj + " " + name)
        if (alt_name is not None): 
            city._add_name(alt_name)
            if (prob_adj is not None): 
                city._add_name(prob_adj + " " + alt_name)
        if (typ is not None): 
            city._add_typ(typ)
        elif (not city.is_city): 
            city._add_typ_city(li[0].kit.base_language)
        if (typ2 is not None): 
            city._add_typ(typ2.lower())
        if (li[0].higher_geo is not None and GeoOwnerHelper.can_be_higher(li[0].higher_geo, city)): 
            city.higher = li[0].higher_geo
        if (li[0].typ == CityItemToken.ItemType.MISC): 
            del li[0]
        res = ReferentToken._new734(city, li[0].begin_token, li[len(li) - 1].end_token, mc)
        if (res.end_token.next0_ is not None and res.end_token.next0_.is_hiphen and (isinstance(res.end_token.next0_.next0_, NumberToken))): 
            num = Utils.asObjectOrNull(res.end_token.next0_.next0_, NumberToken)
            if ((num.typ == NumberSpellingType.DIGIT and not num.morph.class0_.is_adjective and num.int_value is not None) and (num.int_value < 50)): 
                for s in city.slots: 
                    if (s.type_name == GeoReferent.ATTR_NAME): 
                        city.upload_slot(s, "{0}-{1}".format(s.value, num.value))
                res.end_token = num
        if (li[0].begin_token == li[0].end_token and li[0].begin_token.is_value("ГОРОДОК", None)): 
            if (AddressItemToken.check_house_after(res.end_token.next0_, True, False)): 
                return None
        return res
    
    @staticmethod
    def __try_name_exist(li : typing.List['CityItemToken'], oi : 'IntOntologyItem', always : bool) -> 'ReferentToken':
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
                if ((isinstance(tt.next0_, TextToken)) and tt.next0_.get_morph_class_in_dictionary().is_proper_secname): 
                    pass
                else: 
                    ok = True
            elif (tt.previous is not None and tt.previous.is_value("В", None) and tt.term == "РИМЕ"): 
                ok = True
        elif (oi.value is not None and oi.value.referent is not None and oi.value.owner.is_ext_ontology): 
            ok = True
        elif (nam.endswith("ГРАД") or nam.endswith("СК")): 
            ok = True
        elif (nam.endswith("TOWN") or nam.startswith("SAN")): 
            ok = True
        elif (li[0].chars.is_latin_letter and li[0].begin_token.previous is not None and ((li[0].begin_token.previous.is_value("IN", None) or li[0].begin_token.previous.is_value("FROM", None)))): 
            ok = True
        else: 
            tt2 = li[0].end_token.next0_
            first_pass3643 = True
            while True:
                if first_pass3643: first_pass3643 = False
                else: tt2 = tt2.next0_
                if (not (tt2 is not None)): break
                if (tt2.is_newline_before): 
                    break
                if ((tt2.is_char_of(",(") or tt2.morph.class0_.is_preposition or tt2.morph.class0_.is_conjunction) or tt2.morph.class0_.is_misc): 
                    continue
                if ((isinstance(tt2.get_referent(), GeoReferent)) and tt2.chars.is_cyrillic_letter == li[0].chars.is_cyrillic_letter): 
                    ok = True
                break
            if (not ok): 
                tt2 = li[0].begin_token.previous
                first_pass3644 = True
                while True:
                    if first_pass3644: first_pass3644 = False
                    else: tt2 = tt2.previous
                    if (not (tt2 is not None)): break
                    if (tt2.is_newline_after): 
                        break
                    if ((tt2.is_char_of(",)") or tt2.morph.class0_.is_preposition or tt2.morph.class0_.is_conjunction) or tt2.morph.class0_.is_misc): 
                        continue
                    if ((isinstance(tt2.get_referent(), GeoReferent)) and tt2.chars.is_cyrillic_letter == li[0].chars.is_cyrillic_letter): 
                        ok = True
                    if (ok): 
                        sits = StreetItemToken.try_parse_list(li[0].begin_token, None, 10)
                        if (sits is not None and len(sits) > 1): 
                            ss = StreetDefineHelper._try_parse_street(sits, False, False)
                            if (ss is not None): 
                                del sits[0]
                                if (StreetDefineHelper._try_parse_street(sits, False, False) is None): 
                                    ok = False
                    if (ok): 
                        if (len(li) > 1 and li[1].typ == CityItemToken.ItemType.PROPERNAME and (li[1].whitespaces_before_count < 3)): 
                            ok = False
                        else: 
                            mc = li[0].begin_token.get_morph_class_in_dictionary()
                            if (mc.is_proper_name or mc.is_proper_surname or mc.is_adjective): 
                                ok = False
                            else: 
                                npt = NounPhraseHelper.try_parse(li[0].begin_token, NounPhraseParseAttr.NO, 0, None)
                                if (npt is not None and npt.end_char > li[0].end_char): 
                                    ok = False
                    if (AddressItemToken.try_attach_org(li[0].begin_token) is not None): 
                        ok = False
                        break
                    break
        if (always): 
            if (li[0].whitespaces_before_count > 3 and li[0].doubtful and li[0].begin_token.get_morph_class_in_dictionary().is_proper_surname): 
                pp = li[0].kit.process_referent("PERSON", li[0].begin_token)
                if (pp is not None): 
                    always = False
        if (li[0].begin_token.chars.is_latin_letter and li[0].begin_token == li[0].end_token): 
            tt1 = li[0].end_token.next0_
            if (tt1 is not None and tt1.is_char(',')): 
                tt1 = tt1.next0_
            if (((isinstance(tt1, TextToken)) and tt1.chars.is_latin_letter and (tt1.length_char < 3)) and not tt1.chars.is_all_lower): 
                ok = False
        if (not ok and not always): 
            return None
        city = None
        if (oi.value is not None and (isinstance(oi.value.referent, GeoReferent)) and not oi.value.owner.is_ext_ontology): 
            city = (Utils.asObjectOrNull(oi.value.referent.clone(), GeoReferent))
            city.occurrence.clear()
        else: 
            city = GeoReferent()
            city._add_name(nam)
            if (oi.value is not None and (isinstance(oi.value.referent, GeoReferent))): 
                city._merge_slots2(Utils.asObjectOrNull(oi.value.referent, GeoReferent), li[0].kit.base_language)
            if (not city.is_city): 
                city._add_typ_city(li[0].kit.base_language)
        return ReferentToken._new734(city, li[0].begin_token, li[0].end_token, li[0].morph)
    
    @staticmethod
    def __try4(li : typing.List['CityItemToken']) -> 'ReferentToken':
        if ((len(li) > 0 and li[0].typ == CityItemToken.ItemType.NOUN and ((li[0].value != "ГОРОД" and li[0].value != "МІСТО" and li[0].value != "CITY"))) and ((not li[0].doubtful or li[0].geo_object_before))): 
            if (len(li) > 1 and li[1].org_ref is not None): 
                geo_ = GeoReferent()
                geo_._add_typ(li[0].value)
                geo_._add_org_referent(li[1].org_ref.referent)
                geo_.add_ext_referent(li[1].org_ref)
                return ReferentToken(geo_, li[0].begin_token, li[1].end_token)
            else: 
                aid = AddressItemToken.try_attach_org(li[0].end_token.next0_)
                if (aid is not None): 
                    geo_ = GeoReferent()
                    geo_._add_typ(li[0].value)
                    geo_._add_org_referent(aid.referent)
                    geo_.add_ext_referent(aid.ref_token)
                    return ReferentToken(geo_, li[0].begin_token, aid.end_token)
        return None
    
    @staticmethod
    def check_year_after(tt : 'Token') -> bool:
        if (tt is not None and ((tt.is_comma or tt.is_hiphen))): 
            tt = tt.next0_
        if (tt is not None and tt.is_newline_after): 
            if ((isinstance(tt, NumberToken)) and tt.int_value is not None): 
                year = tt.int_value
                if (year > 1990 and (year < 2100)): 
                    return True
            elif (tt.get_referent() is not None and tt.get_referent().type_name == "DATE"): 
                return True
        return False
    
    @staticmethod
    def check_street_after(tt : 'Token') -> bool:
        if (tt is not None and ((tt.is_comma_and or tt.is_hiphen or tt.morph.class0_.is_preposition))): 
            tt = tt.next0_
        if (tt is None): 
            return False
        ait = AddressItemToken.try_parse(tt, None, False, False, None)
        if (ait is not None and ait.typ == AddressItemToken.ItemType.STREET): 
            return True
        return False
    
    @staticmethod
    def check_city_after(tt : 'Token') -> bool:
        while tt is not None and (((tt.is_comma_and or tt.is_hiphen or tt.morph.class0_.is_preposition) or tt.is_char('.'))):
            tt = tt.next0_
        if (tt is None): 
            return False
        cits = CityItemToken.try_parse_list(tt, None, 5)
        if (cits is None or len(cits) == 0): 
            if (tt.length_char == 1 and tt.chars.is_all_lower and ((tt.is_value("Д", None) or tt.is_value("П", None)))): 
                tt1 = tt.next0_
                if (tt1 is not None and tt1.is_char('.')): 
                    tt1 = tt1.next0_
                ci = CityItemToken.try_parse(tt1, None, False, None)
                if (ci is not None and ((ci.typ == CityItemToken.ItemType.PROPERNAME or ci.typ == CityItemToken.ItemType.CITY))): 
                    return True
            return False
        if (CityAttachHelper.try_attach_city(cits, None, False) is not None): 
            return True
        if (cits[0].typ == CityItemToken.ItemType.NOUN): 
            if (tt.previous is not None and tt.previous.is_comma): 
                return True
        return False